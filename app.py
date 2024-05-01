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
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
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

if st.button('Show Recommendation'):
    recommended_music_names,recommended_music_posters,recommended_music_artists = recommend(selected_movie)

    col1, col2, col3, col4 = st.columns(4)
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
    with col3:
        st.markdown("<strong>Best Rec.</strong>", unsafe_allow_html=True)
        song1_best = st.checkbox(label="rec1Best", key="rec1Best", value=False, label_visibility="collapsed")
        song2_best = st.checkbox(label="rec2Best", key="rec2Best", value=False, label_visibility="collapsed")
        song3_best = st.checkbox(label="rec3Best", key="rec3Best", value=False, label_visibility="collapsed")
    with col4:
        st.markdown("<strong>Worse Rec.</strong>", unsafe_allow_html=True)
        song1_worse = st.checkbox(label="rec1Worse", key="rec1Worse", value=False, label_visibility="collapsed")
        song2_worse = st.checkbox(label="rec2Worse", key="rec2Worse", value=False, label_visibility="collapsed")
        song3_worse = st.checkbox(label="rec3Worse", key="rec3Worse", value=False, label_visibility="collapsed")

