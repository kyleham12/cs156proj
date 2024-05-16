import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from flask import Flask, jsonify, request, render_template, redirect, session, url_for, send_from_directory
from flask_cors import CORS
from scipy.sparse import hstack, csr_matrix
import numpy as np
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
CORS(app)

num_of_features = 19298

CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        #print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song, svc):
    idx = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[idx])),reverse=True,key=lambda x:x[1])
    recs = []
    song_probs = []
    
    for m_id in distances[1:21]:
        artist = music.iloc[m_id[0]]['artist']
        song = music.iloc[m_id[0]]['song']
        text = music.iloc[m_id[0]]['text']
        
        combo = f"{artist} {song} {text}"
        X = tfidvector.fit_transform([combo])

        num_columns_to_add = num_of_features - X.shape[1]

        zeros_matrix = csr_matrix((X.shape[0], num_columns_to_add), dtype=np.float64)

        X = hstack([X, zeros_matrix])
    
        probability = svc.predict_proba(X)[0][1]
        song_probs.append(probability)
    
    sorted_indices = sorted(range(len(song_probs)), key=lambda i: song_probs[i], reverse=True)
    sorted_songs = [distances[i+1][0] for i in sorted_indices]
    
    recs = [music.iloc[i]['song'] for i in sorted_songs]
    recommended_music_names = []
    recommended_music_posters = []
    recommended_music_artists = []
    for i in distances[1:11]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
        recommended_music_artists.append(music.iloc[i[0]].artist)
    name_index_map = {name: index for index, name in enumerate(recs)}
    sorted_recs = sorted(recommended_music_names, key=lambda x: name_index_map.get(x, len(recs)))
    sorted_artists = []
    sorted_posters = []
    for song in sorted_recs:
        artist = music.loc[music['song'] == song, 'artist'].iloc[0]
        sorted_artists.append(artist)
        sorted_posters.append(get_song_album_cover_url(song, artist))
    return sorted_recs,sorted_posters,sorted_artists

def update_model(return_info):
    for row in return_info:
        song_name = row[0]
        feedback_value = row[2]
        music.loc[music['song'] == song_name, 'feedback'] = feedback_value

    music['combined_text'] = music['artist'] + ' ' + music['song'] + ' ' + music['text']
    tfid_X = tfidvector.fit_transform(music['combined_text'])

    y = music['feedback']

    X_train, X_test, y_train, y_test = train_test_split(tfid_X, y, test_size=0.2, random_state=42)

    svc = SVC(probability=True)
    svc.fit(X_train, y_train)

    return svc

music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
svc = pickle.load(open('svc.pkl','rb'))

tfidvector = TfidfVectorizer(analyzer='word',stop_words='english')


@app.route("/")
def base():
    return send_from_directory('client/build', 'index.html')

@app.route("/<path:path>")
def assets(path):
    try:
        response = send_from_directory('client/build', path)
        return response
    except:
        return send_from_directory('client/build', 'index.html')
    
@app.route("/getSongsList")
def getSongsList():
    song_list = music['song'].values.tolist()
    artist_list = music['artist'].values.tolist()
    image_list = []
    return jsonify({'songList': song_list, 'artist_list': artist_list, 'image_list': image_list})

@app.route("/getRecList", methods=['POST'])
def getRecList():
    data = request.get_json()
    selected_movie = data.get('selected_song')
    sorted_recs,sorted_posters,sorted_artists  = recommend(selected_movie, svc)
    recList = []
    for i in range(0,10):
        temp = []
        temp.append(sorted_recs[i])
        temp.append(sorted_artists[i])
        temp.append(sorted_posters[i])
        recList.append(temp)
    return jsonify({'recList': recList})

@app.route("/getOpinion", methods=['POST'])
def getOpinion():
    data = request.get_json()
    selected_movie = data.get('selected_song')
    return_info = data.get('returnInfo')
    print(selected_movie)
    print(return_info)
    svc = update_model(return_info)
    return jsonify({'msg': "Opinion saved successfully"})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)