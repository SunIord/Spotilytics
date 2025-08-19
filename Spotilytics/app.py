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

# Sidebar for search
with st.sidebar:
    st.header("Artist Search")
    artistName = st.text_input("Type the name of an artist:", key="sidebar_search", placeholder="🔍 Search artist...")

    st.divider()
    #st.write("")

# Search for the artist and display their information
if artistName:
    results = sp.search(q='artist:' + artistName, type='artist')
    if results['artists']['items']:
        artist = results['artists']['items'][0]

        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(artist['images'][0]['url'], width=250)
        with col2:
            st.write(f"## {artist['name']}")
            st.write(f"**Followers:** {artist['followers']['total']}")
            st.write(f"**Popularity:** {artist['popularity']}")
            # Display genres if available
            if artist['genres']:
                st.write(f"**Genres:** {', '.join(artist['genres'])}")
            else:
                st.write("**Genres:** No genres available")

        # Fetch top tracks for the artist
        st.divider()
        st.subheader("Top Tracks")

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

else: # If no artist is searched, show a welcome message
    st.write("## Welcome to Spotilytics!")
    st.write("Discover insights about your favorite artists")
    st.write("")
    st.write("### How to use:")
    st.write("1. Enter an artist name in the sidebar search box")
    st.write("2. View detailed information about the artist")
    st.write("3. Explore their top tracks and popularity stats")