import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_artists = []
    for i in distances[1:6]:
        recommended_music_names.append(music.iloc[i[0]].song)
        recommended_music_artists.append(music.iloc[i[0]].artist)
    return recommended_music_names,recommended_music_artists

# Function to update feedback based on like/dislike
def update_feedback(song_name, liked):
    index = music.index[music['song'] == song_name].tolist()[0]
    if liked:
        music.loc[index, 'feedback'] += 1
    else:
        music.loc[index, 'feedback'] -= 1



st.header('Music Recommender System')
music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

music_list = [''] + music['song'].values.tolist()
selected_movie = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)


if selected_movie != "":
    recommended_music_names,recommended_music_artists = recommend(selected_movie)
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
        st.markdown(":+1: (Like)", unsafe_allow_html=True)
        song1_like = st.checkbox(label="rec1Good", key="rec1Good", value=False, label_visibility="collapsed")
        song2_like = st.checkbox(label="rec2Good", key="rec2Good", value=False, label_visibility="collapsed")
        song3_like = st.checkbox(label="rec3Good", key="rec3Good", value=False, label_visibility="collapsed")
    with col4:
        st.markdown(":-1: (Dislike)", unsafe_allow_html=True)
        song1_dislike = st.checkbox(label="rec1Dislike", key="rec1Dislike", value=False, label_visibility="collapsed")
        song2_dislike = st.checkbox(label="rec2Dislike", key="rec2Dislike", value=False, label_visibility="collapsed")
        song3_dislike = st.checkbox(label="rec3Dislike", key="rec3Dislike", value=False, label_visibility="collapsed")

    # Update feedback based on user selections
    if song1_like:
        update_feedback(recommended_music_names[0], True)
    if song2_like:
        update_feedback(recommended_music_names[1], True)
    if song3_like:
        update_feedback(recommended_music_names[2], True)
    if song1_dislike:
        update_feedback(recommended_music_names[0], False)
    if song2_dislike:
        update_feedback(recommended_music_names[1], False)
    if song3_dislike:
        update_feedback(recommended_music_names[2], False)


