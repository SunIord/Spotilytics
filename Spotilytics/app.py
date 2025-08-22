import streamlit as st
from utils.auth import init_spotify_client
from utils.search import update_search, get_artist_top_tracks, get_complete_discography
from utils.ui import render_artist_profile, render_welcome_message, render_artist_not_found, create_tracks_dataframe, create_discography_dataframe, render_artist_basic_info
from utils.charts import plot_top_tracks, plot_release_timeline, plot_album_track_stats
from utils.comparison import render_artist_comparison 

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
if 'compare_mode' not in st.session_state:
    st.session_state.compare_mode = False
if 'artist_to_compare' not in st.session_state:
    st.session_state.artist_to_compare = None

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
    
    # Show artists if we have results
    if st.session_state.artist_results:
        # Different behavior based on mode
        if st.session_state.compare_mode:
            st.write("**Select an artist to compare:**")
        else:
            st.write("**Matching artists:**")
        
        for i, artist in enumerate(st.session_state.artist_results):
            artist_name = artist['name'][:20] + "..." if len(artist['name']) > 20 else artist['name']
            genres_text = ', '.join(artist['genres'][:2]) if artist['genres'] else 'No genres'
            genres_text = genres_text[:25] + "..." if len(genres_text) > 25 else genres_text

            if st.button(
                f"{artist_name} ({genres_text})", 
                key=f"artist_{i}",
                use_container_width=True
            ):
                if st.session_state.compare_mode:
                    # In compare mode, set as second artist and show comparison
                    st.session_state.selected_artist = artist
                    st.rerun()
                else:
                    # Normal mode, just select the artist
                    st.session_state.selected_artist = artist
                    st.rerun()

# Display content based on current mode
if st.session_state.compare_mode:
    # Comparison mode
    if st.session_state.artist_to_compare and st.session_state.selected_artist:
        # Both artists selected, show comparison
        artist1 = st.session_state.artist_to_compare
        artist2 = st.session_state.selected_artist
        
        # Get top tracks for both artists
        artist1_top_tracks = get_artist_top_tracks(sp, artist1['id'])
        artist2_top_tracks = get_artist_top_tracks(sp, artist2['id'])
        
        # Create DataFrames for top tracks
        artist1_tracks_df = create_tracks_dataframe(artist1_top_tracks)
        artist2_tracks_df = create_tracks_dataframe(artist2_top_tracks)
        
        # Calculate album statistics for each artist
        artist1_albums_stats = artist1_tracks_df.groupby('Album').agg({'Track': 'count', 'Popularity': 'mean'}).reset_index()
        artist2_albums_stats = artist2_tracks_df.groupby('Album').agg({'Track': 'count', 'Popularity': 'mean'}).reset_index()
        
        # Prepare metrics for radar chart
        max_followers = max(artist1['followers']['total'], artist2['followers']['total'])
        artist1_metrics = {
            'Popularity': artist1['popularity'],
            'Followers': (artist1['followers']['total'] / max_followers) * 100,
            'Genres': len(artist1['genres']) * 10 if artist1['genres'] else 0
        }
        artist2_metrics = {
            'Popularity': artist2['popularity'],
            'Followers': (artist2['followers']['total'] / max_followers) * 100,
            'Genres': len(artist2['genres']) * 10 if artist2['genres'] else 0
        }
        
        # Render comparison
        render_artist_comparison(
            artist1, 
            artist2, 
            artist1_tracks_df, 
            artist2_tracks_df, 
            artist1_albums_stats, 
            artist2_albums_stats,
            artist1_metrics,
            artist2_metrics
        )
        
        if st.button("← Back to single artist view"):
            st.session_state.compare_mode = False
            st.session_state.selected_artist = st.session_state.artist_to_compare
            st.session_state.artist_to_compare = None
            st.rerun()
    else:
        # Waiting for second artist selection
        if st.session_state.artist_to_compare:
            st.info("Please select a second artist to compare from the sidebar.")
            render_artist_basic_info(st.session_state.artist_to_compare)
            
            if st.button("Cancel comparison"):
                st.session_state.compare_mode = False
                st.session_state.artist_to_compare = None
                st.rerun()
        else:
            st.warning("Comparison mode activated but no artist selected. Please search for an artist.")
            
elif st.session_state.selected_artist:
    # Normal single artist view
    artist = st.session_state.selected_artist
    top_tracks = get_artist_top_tracks(sp, artist['id'])
    complete_discography = get_complete_discography(sp, artist['id'])
    
    # Render artist profile and get dataframes
    df_tracks_complete = render_artist_profile(artist, top_tracks)
    df_discography = create_discography_dataframe(complete_discography)
    
    # Display charts and analytics
    st.divider()
    st.subheader("Track Analytics")
    
    plot_top_tracks(df_tracks_complete)
    plot_album_track_stats(df_tracks_complete)
    plot_release_timeline(df_discography)

    # Add buttons to go back to search results or to compare
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to search results"):
            st.session_state.selected_artist = None
            st.rerun()
    with col2:
        if st.button("🔀 Compare with another artist"):
            st.session_state.artist_to_compare = artist
            st.session_state.compare_mode = True
            st.session_state.selected_artist = None
            st.rerun()

elif st.session_state.search_term and not st.session_state.selected_artist and not st.session_state.artist_results:
    render_artist_not_found()

else:
    render_welcome_message()