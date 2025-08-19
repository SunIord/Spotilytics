import streamlit as st
import pandas as pd 
import plotly.express as px 
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import os 
from dotenv import load_dotenv  

# Authentication with the Spotify API using environment variables
load_dotenv()

client_id = os.getenv("spotipyId")
client_secret = os.getenv("spotipySecret")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

# Page configuration
st.set_page_config(page_title="Spotilytics", page_icon="🎶", layout="wide")
st.title("Spotilytics")

# Search for the artist and display their information
artistName = st.text_input("Type the name of an artist:")

if artistName:
    results = sp.search(q='artist:' + artistName, type='artist')
    if results['artists']['items']:
        artist = results['artists']['items'][0]
        st.image(artist['images'][0]['url'], width=200)
        st.write(f"**Name:** {artist['name']}")
        st.write(f"**Followers:** {artist['followers']['total']}")
        st.write(f"**Popularity:** {artist['popularity']}")
        st.write(f"**Genres:** {', '.join(artist['genres'])}")

        # Fetch top tracks for the artist
        top_tracks = sp.artist_top_tracks(artist['id'])['tracks']
        data = []
        for track in top_tracks:
            data.append({
                "Track": track["name"],
                "Album": track["album"]["name"],
                "Released Date": track["album"]["release_date"],
                "Popularity": track["popularity"]
            })

        df_tracks = pd.DataFrame(data)
        df_tracks.index = df_tracks.index + 1
        st.dataframe(df_tracks)

    else:
        st.write("Artist not found.")

else:
    st.write("## Welcome to Spotilytics!")
    st.write("Discover insights about your favorite artists")
    st.write("")
    st.write("### How to use:")
    st.write("1. Enter an artist name in the search box")
    st.write("2. View detailed information about the artist")
    st.write("3. Explore their top tracks and popularity stats")
    st.write("")