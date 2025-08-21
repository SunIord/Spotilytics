import streamlit as st
import pandas as pd
from .helpers import truncate_text, format_number

def render_artist_selection(artists):
    if artists:
        st.write("**Matching artists:**")
        for i, artist in enumerate(artists):
            artist_name = truncate_text(artist['name'], 20)
            genres_text = truncate_text(', '.join(artist['genres'][:2]) if artist['genres'] else 'No genres', 25)

            if st.button(
                f"{artist_name} ({genres_text})", 
                key=f"artist_{i}",
                use_container_width=True
            ):
                return artist
    return None

def create_tracks_dataframe(tracks):
    data = []
    for track in tracks:
        data.append({
            "Track": track["name"],
            "Album": track["album"]["name"],
            "Released Date": track["album"]["release_date"],
            "Popularity": track["popularity"] 
        })

    df_tracks = pd.DataFrame(data)
    df_tracks.index = df_tracks.index + 1
    return df_tracks

def create_discography_dataframe(tracks):
    data = []
    for track in tracks:
        # Para discografia completa, usamos album_info
        data.append({
            "Track": track["name"],
            "Album": track['album_info']['name'],
            "Released Date": track['album_info']['release_date']
            # Não incluímos Popularity pois não está disponível
        })

    df_tracks = pd.DataFrame(data)
    df_tracks.index = df_tracks.index + 1
    return df_tracks

def create_display_dataframe(df_tracks):
    return df_tracks[["Track", "Album", "Released Date"]]

def render_artist_profile(artist, tracks):
    col1, col2 = st.columns([1, 3])
    with col1:
        if artist['images']:
            st.image(artist['images'][0]['url'], width=250)
        else:
            st.image("https://via.placeholder.com/250x250/1DB954/FFFFFF?text=No+Image", width=250)
    
    with col2:
        st.write(f"## {artist['name']}")
        st.write(f"**Followers:** {format_number(artist['followers']['total'])}")
        st.write(f"**Popularity:** {artist['popularity']}")
        if artist['genres']:
            st.write(f"**Genres:** {', '.join(artist['genres'])}")
        else:
            st.write("**Genres:** No genres available")

    # Render top tracks
    st.divider()
    st.subheader("Top Tracks")
 
    df_tracks_complete = create_tracks_dataframe(tracks)
    df_display = create_display_dataframe(df_tracks_complete)
    
    st.dataframe(df_display)
    
    return df_tracks_complete

def render_welcome_message():
    st.write("## Welcome to Spotilytics!")
    st.write("Discover insights about your favorite artists")
    st.write("")
    st.write("### How to use:")
    st.write("1. Enter an artist name in the sidebar search box")
    st.write("2. View detailed information about the artist")
    st.write("3. Explore their top tracks and popularity stats")

def render_artist_not_found():
    st.write("Artist not found.")