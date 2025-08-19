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

# Initialize session state variables
if 'artist_results' not in st.session_state:
    st.session_state.artist_results = []
if 'selected_artist' not in st.session_state:
    st.session_state.selected_artist = None  # Changed from [] to None
if 'search_term' not in st.session_state:
    st.session_state.search_term = ""
if 'last_search' not in st.session_state:
    st.session_state.last_search = ""

# Cache functions
@st.cache_data(ttl=3600, show_spinner=False)
def searchArtistsCached(query):
    results = sp.search(q='artist:' + query, type='artist', limit=10)
    return results['artists']['items']

@st.cache_data(ttl=3600, show_spinner=False)
def getTracksCached(artist_id):
    return sp.artist_top_tracks(artist_id)['tracks']

# Sidebar for search
def updateSearch():
    if st.session_state.sidebar_search:
        # Clear selected artist when doing a new search
        st.session_state.selected_artist = None
        
        # Only search if the term has changed
        if st.session_state.sidebar_search != st.session_state.last_search:
            results = searchArtistsCached(st.session_state.sidebar_search)
            st.session_state.artist_results = results
            st.session_state.last_search = st.session_state.sidebar_search
    else:
        st.session_state.artist_results = []
        st.session_state.selected_artist = None
        st.session_state.last_search = ""

with st.sidebar:
    st.header("Artist Search")
    
    # Search for the artist
    search_term = st.text_input(
        "Type the name of an artist:", 
        value=st.session_state.search_term,
        key="sidebar_search",
        placeholder="🔍 Search artist...",
        on_change=updateSearch 
    )
    st.divider()
    
    # Display artist options if we have results
    def truncateText(text, max_length):
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text

    # Show artists if we have results and no artist is selected
    if st.session_state.artist_results and st.session_state.selected_artist is None:
        st.write("**Matching artists:**")
        for i, artist in enumerate(st.session_state.artist_results):
            artist_name = truncateText(artist['name'], 20)
            genres_text = truncateText(', '.join(artist['genres'][:2]) if artist['genres'] else 'No genres', 25)

            # Create a button for each artist
            if st.button(
                f"{truncateText(artist['name'], 20)} ({truncateText(', '.join(artist['genres'][:2]) if artist['genres'] else 'No genres', 25)})", 
                key=f"artist_{i}",
                use_container_width=True
            ):
                st.session_state.selected_artist = artist
                st.rerun()

# Display selected artist information
def formatNumber(number): 
    return f"{number:,}".replace(",", ".")

if st.session_state.selected_artist:
    artist = st.session_state.selected_artist

    col1, col2 = st.columns([1, 3])
    with col1:
        if artist['images']:
            st.image(artist['images'][0]['url'], width=250)
        else:
            st.image("https://via.placeholder.com/250x250/1DB954/FFFFFF?text=No+Image", width=250)
    
    with col2:
        st.write(f"## {artist['name']}")
        st.write(f"**Followers:** {formatNumber(artist['followers']['total'])}")
        st.write(f"**Popularity:** {artist['popularity']}")
        if artist['genres']:
            st.write(f"**Genres:** {', '.join(artist['genres'])}")
        else:
            st.write("**Genres:** No genres available")

    # Fetch top tracks for the artist
    st.divider()
    st.subheader("Top Tracks")

    topTracks = getTracksCached(artist['id'])
    data = []
    for track in topTracks:
        data.append({
            "Track": track["name"],
            "Album": track["album"]["name"],
            "Released Date": track["album"]["release_date"],
            "Popularity": track["popularity"]
        })

    dfTracks = pd.DataFrame(data)
    dfTracks.index = dfTracks.index + 1
    st.dataframe(dfTracks)

    # Add a button to go back to search results
    if st.button("← Back to search results"):
        st.session_state.selected_artist = None
        st.rerun()

elif st.session_state.search_term and not st.session_state.selected_artist and not st.session_state.artist_results:
    st.write("Artist not found.")

else: # Show a welcome message
    st.write("## Welcome to Spotilytics!")
    st.write("Discover insights about your favorite artists")
    st.write("")
    st.write("### How to use:")
    st.write("1. Enter an artist name in the sidebar search box")
    st.write("2. View detailed information about the artist")
    st.write("3. Explore their top tracks and popularity stats")