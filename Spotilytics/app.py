import streamlit as st
from utils.auth import init_spotify_client
from utils.search import update_search, get_artist_top_tracks
from utils.ui import render_artist_selection, render_artist_profile, render_welcome_message, render_artist_not_found

# Authentication with the Spotify API using environment variables
sp = init_spotify_client()

# Page configuration
st.set_page_config(page_title="Spotilytics", page_icon="🎶", layout="wide")
st.title("Spotilytics")

# Initialize session state variables
if 'artist_results' not in st.session_state:
    st.session_state.artist_results = []
if 'selected_artist' not in st.session_state:
    st.session_state.selected_artist = None 
if 'search_term' not in st.session_state:
    st.session_state.search_term = ""
if 'last_search' not in st.session_state:
    st.session_state.last_search = ""

# Sidebar for search
with st.sidebar:
    st.header("Artist Search")
    
    # Search for the artist
    search_term = st.text_input(
        "Type the name of an artist:", 
        value=st.session_state.search_term,
        key="sidebar_search",
        placeholder="🔍 Search artist..."
    )
    st.divider()
    
    # Update search when input changes
    if search_term != st.session_state.search_term:
        st.session_state.search_term = search_term
        update_search(sp, st.session_state, search_term)
    
    # Show artists if we have results and no artist is selected
    if st.session_state.artist_results and st.session_state.selected_artist is None:
        selected_artist = render_artist_selection(st.session_state.artist_results)
        if selected_artist:
            st.session_state.selected_artist = selected_artist
            st.rerun()

# Display selected artist information
if st.session_state.selected_artist:
    artist = st.session_state.selected_artist
    top_tracks = get_artist_top_tracks(sp, artist['id'])
    
    render_artist_profile(artist, top_tracks)

    # Add a button to go back to search results
    if st.button("← Back to search results"):
        st.session_state.selected_artist = None
        st.rerun()

elif st.session_state.search_term and not st.session_state.selected_artist and not st.session_state.artist_results:
    render_artist_not_found()

else:
    render_welcome_message()