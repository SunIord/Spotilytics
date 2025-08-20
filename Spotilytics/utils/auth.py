import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def init_spotify_client():
    load_dotenv()
    client_id = os.getenv("spotipyId")
    client_secret = os.getenv("spotipySecret")
    
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    ))