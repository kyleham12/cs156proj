import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


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
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    recommended_music_artists = []
    for i in distances[1:6]:
        # fetch the movie poster
        artist = music.iloc[i[0]].artist
        #print(artist)
        #print(music.iloc[i[0]].song)
        #recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
        recommended_music_artists.append(music.iloc[i[0]].artist)
    return recommended_music_names,recommended_music_posters,recommended_music_artists



st.header('Music Recommender System')
music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

music_list = music['song'].values
selected_movie = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)


recommended_music_names,recommended_music_posters,recommended_music_artists = recommend(selected_movie)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown("<strong>Song Name</strong>", unsafe_allow_html=True)
    st.text(recommended_music_names[0])
    st.text(recommended_music_names[1])
    st.text(recommended_music_names[2])
with col2:
    st.markdown("<strong>Artist(s)</strong>", unsafe_allow_html=True)
    st.text(recommended_music_artists[0])
    st.text(recommended_music_artists[1])
    st.text(recommended_music_artists[2])
with col4:
    st.markdown(":+1: (Like)", unsafe_allow_html=True)
    song1_like = st.checkbox(label="rec1Good", key="rec1Good", value=False, label_visibility="collapsed")
    song2_like = st.checkbox(label="rec2Good", key="rec2Good", value=False, label_visibility="collapsed")
    song3_like = st.checkbox(label="rec3Good", key="rec3Good", value=False, label_visibility="collapsed")
with col5:
    st.markdown(":-1: (Dislike)", unsafe_allow_html=True)
    song1_dislike = st.checkbox(label="rec1Dislike", key="rec1Dislike", value=False, label_visibility="collapsed")
    song2_dislike = st.checkbox(label="rec2Dislike", key="rec2Dislike", value=False, label_visibility="collapsed")
    song3_dislike = st.checkbox(label="rec3Dislike", key="rec3Dislike", value=False, label_visibility="collapsed")

