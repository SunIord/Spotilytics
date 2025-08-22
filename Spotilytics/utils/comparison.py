import streamlit as st
import pandas as pd
from .helpers import format_number
from .charts import plot_top_tracks_comparison, plot_album_stats_comparison, plot_radar_chart

def render_artist_comparison(artist1, artist2, artist1_tracks, artist2_tracks, artist1_albums_stats, artist2_albums_stats, artist1_metrics, artist2_metrics):
    st.write("## Artist Comparison")
    
    # Create two columns for the artists
    col1, col2 = st.columns(2)
    
    with col1:
        render_artist_card(artist1, "Artist 1")
    
    with col2:
        render_artist_card(artist2, "Artist 2")
    
    # Add some metrics comparison
    st.divider()
    st.subheader("Metrics Comparison")
    
    comp_col1, comp_col2, comp_col3 = st.columns(3)
    
    with comp_col1:
        st.metric("Followers", 
                 f"{format_number(artist1['followers']['total'])}", 
                 f"{format_number(artist2['followers']['total'] - artist1['followers']['total'])}",
                 delta_color="inverse")
    
    with comp_col2:
        st.metric("Popularity", 
                 f"{artist1['popularity']}/100", 
                 f"{artist2['popularity'] - artist1['popularity']}")
    
    with comp_col3:
        genres1 = len(artist1['genres']) if artist1['genres'] else 0
        genres2 = len(artist2['genres']) if artist2['genres'] else 0
        st.metric("Genres Count", 
                 genres1, 
                 genres2 - genres1,
                 delta_color="inverse")
    
    # Add comparative charts
    st.divider()
    st.subheader("Comparative Analysis")
    
    # Top Tracks Comparison
    plot_top_tracks_comparison(artist1_tracks, artist2_tracks, artist1['name'], artist2['name'])
    
    # Album Comparison
    plot_album_stats_comparison(artist1_albums_stats, artist2_albums_stats, artist1['name'], artist2['name'])
    
    # Radar Chart for general metrics
    plot_radar_chart(artist1_metrics, artist2_metrics, artist1['name'], artist2['name'])

def render_artist_card(artist, title):
    st.subheader(title)
    
    from .helpers import render_square_image
    render_square_image(artist['images'][0]['url'] if artist['images'] else None, size=200)
    
    st.write(f"**Name:** {artist['name']}")
    st.write(f"**Followers:** {format_number(artist['followers']['total'])}")
    st.write(f"**Popularity:** {artist['popularity']}/100")
    
    if artist['genres']:
        st.write(f"**Genres:** {', '.join(artist['genres'])}")
    else:
        st.write("**Genres:** No genres available")