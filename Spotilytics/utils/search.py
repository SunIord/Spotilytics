import streamlit as st

@st.cache_data(ttl=3600, show_spinner=False)
def search_artists(_sp_client, query): 
    """Search for artists using the Spotify API"""
    results = _sp_client.search(q='artist:' + query, type='artist', limit=10)
    return results['artists']['items']

@st.cache_data(ttl=3600, show_spinner=False)
def get_artist_top_tracks(_sp_client, artist_id):
    return _sp_client.artist_top_tracks(artist_id)['tracks']

def update_search(sp_client, session_state, search_term):
    if search_term:
        # Clear selected artist when doing a new search
        session_state.selected_artist = None
        
        # Only search if the term has changed
        if search_term != session_state.last_search:
            results = search_artists(sp_client, search_term)
            session_state.artist_results = results
            session_state.last_search = search_term
    else:
        session_state.artist_results = []
        session_state.selected_artist = None
        session_state.last_search = ""