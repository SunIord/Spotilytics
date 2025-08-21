import streamlit as st

@st.cache_data(ttl=3600, show_spinner=False)
def search_artists(_sp_client, query): 
    results = _sp_client.search(q='artist:' + query, type='artist', limit=10)
    return results['artists']['items']

@st.cache_data(ttl=3600, show_spinner=False)
def get_artist_top_tracks(_sp_client, artist_id):
    return _sp_client.artist_top_tracks(artist_id)['tracks']

@st.cache_data(ttl=86400, show_spinner=False)  # Cache de 24 horas para discografia
def get_artist_albums(_sp_client, artist_id):
    """Busca TODOS os álbuns do artista"""
    albums = _sp_client.artist_albums(
        artist_id, 
        album_type='album,single,compilation',
        limit=50  # Máximo permitido pela API
    )
    return albums['items']

@st.cache_data(ttl=86400, show_spinner=False)  # Cache de 24 horas
def get_album_tracks(_sp_client, album_id):
    """Busca TODAS as faixas de um álbum"""
    tracks = _sp_client.album_tracks(album_id)
    return tracks['items']

@st.cache_data(ttl=86400, show_spinner="Fetching complete discography...")
def get_complete_discography(_sp_client, artist_id):
    """Busca a discografia COMPLETA do artista"""
    all_tracks = []
    albums = get_artist_albums(_sp_client, artist_id)
    
    for album in albums:
        tracks = get_album_tracks(_sp_client, album['id'])
        for track in tracks:
            # Adicionar informações do álbum em cada faixa
            track['album_info'] = {
                'name': album['name'],
                'release_date': album['release_date'],
                'id': album['id'],
                'images': album['images']
            }
            all_tracks.append(track)
    
    return all_tracks

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