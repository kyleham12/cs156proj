import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from flask import Flask, jsonify, request, render_template, redirect, session, url_for, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
CORS(app)

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

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    recommended_music_artists = []
    for i in distances[1:11]:
        artist = music.iloc[i[0]].artist
        #print(artist)
        #print(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
        recommended_music_artists.append(music.iloc[i[0]].artist)
    return recommended_music_names,recommended_music_posters,recommended_music_artists

# Function to update feedback based on like/dislike
def update_feedback(song_name, liked):
    index = music.index[music['song'] == song_name].tolist()[0]
    if liked:
        music.loc[index, 'feedback'] += 1
    else:
        music.loc[index, 'feedback'] -= 1



music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

music_list = music['song'].values



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
    song_list = music_list.tolist()
    return jsonify({'songList': song_list})

@app.route("/getRecList", methods=['POST'])
def getRecList():
    data = request.get_json()
    selected_movie = data.get('selected_song')
    recommended_music_names,recommended_music_posters,recommended_music_artists = recommend(selected_movie)
    recList = [];
    for i in range(0,10):
        temp = []
        temp.append(recommended_music_names[i])
        temp.append(recommended_music_artists[i])
        temp.append(recommended_music_posters[i])
        recList.append(temp)
        #print(recList)
    return jsonify({'recList': recList})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
