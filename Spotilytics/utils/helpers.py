import streamlit as st

def truncate_text(text, max_length):
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def format_number(number): 
    return f"{number:,}".replace(",", ".")

def render_square_image(image_url, size=200):
    if image_url:
        html = f"""
        <div style="width: {size}px; height: {size}px; 
                    overflow: hidden; border-radius: 5px; 
                    margin-bottom: 1rem;">
            <img src="{image_url}" 
                 style="width: 100%; height: 100%; 
                        object-fit: cover;">
        </div>
        """
    else:
        html = f"""
        <div style="width: {size}px; height: {size}px; 
                    display: flex; justify-content: center; align-items: center; 
                    background-color: #1DB954; color: white; border-radius: 5px; 
                    margin-bottom: 1rem;">
            No Image
        </div>
        """
    st.markdown(html, unsafe_allow_html=True)