import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def plot_top_tracks(df: pd.DataFrame):
    if df.empty:
        st.warning("No track data available to display.")
        return
    
    df_sorted = df.sort_values("Popularity", ascending=True)
    
    fig = px.bar(
        df_sorted,
        x="Popularity",
        y="Track",
        orientation='h',
        title="Popularity Tracks Ranking",
        labels={"Popularity": "Popularity Score", "Track": ""},
        text="Popularity",
        color="Popularity",
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    # Update text and hover information
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Popularity: %{x}<extra></extra>'
    )
    
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=500 if len(df_sorted) > 10 else 300,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_release_timeline(df: pd.DataFrame):
    if df.empty or "Released Date" not in df.columns:
        st.warning("No release date data available to display.")
        return
    
    # Create a copy for plotting
    plot_df = df.copy()
    
    # Data conversion and cleaning
    try:
        plot_df["Released Date"] = pd.to_datetime(plot_df["Released Date"], errors="coerce")
        plot_df = plot_df.dropna(subset=["Released Date"])
        
        if plot_df.empty:
            st.warning("No valid release dates found.")
            return
            
        # Yearly aggregation
        plot_df["Year"] = plot_df["Released Date"].dt.year
        yearly_data = plot_df.groupby("Year").agg({
            "Track": "count"
        }).reset_index()
        

        fig = px.bar(
            yearly_data,
            x="Year",
            y="Track",
            title="Career Timeline",
            labels={"Track": "Number of Tracks", "Year": "Year"},
            color="Track",
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Number of Tracks",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating timeline chart: {str(e)}")

def plot_album_track_stats(df: pd.DataFrame):
    if df.empty:
        st.warning("No track data available to display.")
        return
        
    if "Album" not in df.columns:
        st.warning("Album data not available.")
        return
        
    # Album aggregation
    album_stats = df.groupby("Album").agg({
        "Track": "count",
        "Popularity": "mean"
    }).reset_index()
    
    # Bubble chart
    fig = px.scatter(
        album_stats,
        x="Popularity",
        y="Track",
        size="Track",
        color="Popularity",
        hover_name="Album",
        title="Album Overview",
        labels={
            "Track": "Number of Tracks",
            "Popularity": "Average Popularity"
        },
        size_max=60,
        color_continuous_scale=px.colors.sequential.Plasma
    )
    
    fig.update_traces(
        hovertemplate='<b>%{hovertext}</b><br>Tracks: %{y}<br>Avg Popularity: %{x}<extra></extra>'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# COMPARISON FUNCTIONS
# =============================================================================

COMPARISON_COLORS = {
    'artist1': "#b41f1f",  
    'artist2': "#0e9fff",  
    'artist3': '#2ca02c',
    'artist4': "#fbff00"
}

def plot_top_tracks_comparison(artist1_tracks, artist2_tracks, artist1_name, artist2_name):
    top_artist1 = artist1_tracks.nlargest(5, 'Popularity')
    top_artist2 = artist2_tracks.nlargest(5, 'Popularity')
    
    top_artist1['Artist'] = artist1_name
    top_artist2['Artist'] = artist2_name
    
    combined = pd.concat([top_artist1, top_artist2])
    
    fig = px.bar(combined, 
                 x='Popularity', 
                 y='Track', 
                 color='Artist',
                 color_discrete_map={
                     artist1_name: COMPARISON_COLORS['artist1'],
                     artist2_name: COMPARISON_COLORS['artist2']
                 },
                 barmode='group',
                 title=f"Top Tracks Comparison: {artist1_name} vs {artist2_name}",
                 labels={'Popularity': 'Popularity Score', 'Track': ''})
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def plot_album_stats_comparison(artist1_albums, artist2_albums, artist1_name, artist2_name):
    artist1_albums['Artist'] = artist1_name
    artist2_albums['Artist'] = artist2_name
    
    combined = pd.concat([artist1_albums, artist2_albums])

    fig = px.scatter(combined,
                     x='Popularity',
                     y='Track',
                     size='Track',
                     color='Artist',
                     color_discrete_map={
                         artist1_name: COMPARISON_COLORS['artist1'],
                         artist2_name: COMPARISON_COLORS['artist2']
                     },
                     hover_name='Album',
                     title=f"Album Comparison: {artist1_name} vs {artist2_name}",
                     labels={'Track': 'Number of Tracks', 'Popularity': 'Average Popularity'})
    
    st.plotly_chart(fig, use_container_width=True)

def plot_radar_chart(artist1_metrics, artist2_metrics, artist1_name, artist2_name):
    categories = list(artist1_metrics.keys())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[artist1_metrics[cat] for cat in categories],
        theta=categories,
        fill='toself',
        name=artist1_name,
        line_color=COMPARISON_COLORS['artist1'],
        fillcolor='rgba(31, 119, 180, 0.5)', # Blue with 50% transparency
        opacity=0.7
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[artist2_metrics[cat] for cat in categories],
        theta=categories,
        fill='toself',
        name=artist2_name,
        line_color=COMPARISON_COLORS['artist2'],
        fillcolor='rgba(255, 127, 14, 0.5)',  # Orange with 50% transparency
        opacity=0.7
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title=f"Metrics Comparison: {artist1_name} vs {artist2_name}"
    )
    
    st.plotly_chart(fig, use_container_width=True)