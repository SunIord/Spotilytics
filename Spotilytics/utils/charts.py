import plotly.express as px
import streamlit as st
import pandas as pd

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