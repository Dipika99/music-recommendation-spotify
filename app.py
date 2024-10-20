import streamlit as st
import os
import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return ""
    
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse = True, key = lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

st.header('Music Recommender System')
music = pickle.load(open('pkl/train','rb'))
similarity = pickle.load(open('pkl/similarity','rb'))

music_list = music['song'].values
selected_song = st.selectbox(
    "Select a song",
    music_list
)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_song)

    cols_n = len(recommended_music_names)
    cols = st.columns(cols_n)
    default_image_url = os.path.join("images/album", "default.png")

    for i in range(cols_n):
        with cols[i]:
            image_url = recommended_music_posters[i] if recommended_music_posters[i] else default_image_url
            st.image(image_url)
            st.markdown(
                f"<span style='background-color:yellow'>{recommended_music_names[i]}</span>",
                unsafe_allow_html=True
            )

