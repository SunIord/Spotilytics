import streamlit as st # used to create the web interface
import pandas as pd # used for data manipulation
import plotly.express as px # used to create interactive charts
import spotipy # used to interact with the Spotify API
from spotipy.oauth2 import SpotifyClientCredentials
import os # used to access environment variables
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
        st.dataframe(df_tracks)

    else:
        st.write("Artist not found.")