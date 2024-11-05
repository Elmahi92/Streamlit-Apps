import streamlit as st
import spotipy
import pandas as pd
import plotly.express as px
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify authentication
#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id='c7832f4cfebb4553b27447fe32b29c1d', client_secret='d61c1c95e44446bdab707511f8d306ae')
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

playlist_link = "https://open.spotify.com/playlist/2QECvpSDU035PFS5uJ8x3l?si=5730077d7aca4db3"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]


# Function to extract playlist_id from the playlist_link
def extract_playlist_id(playlist_link):
    playlist_id = playlist_link.split('/')[-1].split('?')[0]
    return playlist_id

# Function to get playlist tracks (more than 100 songs)
def get_playlist_tracks_more_than_100_songs(username, playlist_link):
    playlist_id = extract_playlist_id(playlist_link)
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    playlist_data = []

    for i, item in enumerate(tracks):
        try:
            track = item['track']
            features = sp.audio_features(track['id'])[0]
            artist_list = ', '.join([artist['name'] for artist in track['artists']])
            
            track_info = {
                'Title': track['name'],
                'Artists': artist_list,
                'Release Date': track['album']['release_date'],
                'Popularity': track['popularity'],
                'Danceability': features['danceability'],
                'Energy': features['energy'],
                'Key': features['key'],
                'Loudness': features['loudness'],
                'Mode': features['mode'],
                'Acousticness': features['acousticness'],
                'Instrumentalness': features['instrumentalness'],
                'Liveness': features['liveness'],
                'Valence': features['valence'],
                'Tempo': features['tempo'],
                'Duration (ms)': features['duration_ms'],
                'Time Signature': features['time_signature']
            }
            playlist_data.append(track_info)
        except:
            continue
    
    df = pd.DataFrame(playlist_data)
    return df

# Streamlit app
st.title("Spotify Playlist Metadata Analyzer")

# User inputs
username = st.sidebar.text_input("Enter Spotify Username")
playlist_link = st.sidebar.text_input("Enter Spotify Playlist Link")

# Tabs for navigation
tabs = st.tabs(["About", "Home"])

# About tab
with tabs[0]:
    st.markdown("""
    ### About this App
    This app lets you analyze Spotify playlists and albums. Simply enter your Spotify username and a playlist or album link to begin.

    ### Spotify Track Features Explained:
    - **Popularity**: Ranges from 0 to 100, showing how well-known a track is. Higher scores indicate more popularity.
    - **Danceability**: Rates a track's suitability for dancing, from 0.0 to 1.0. Higher values mean the track is more danceable.
    - **Energy**: Measures intensity and activity on a scale from 0.0 to 1.0. Higher scores reflect more energetic tracks.
    - **Key**: Identifies the musical key of the track (e.g., 0 = C, 1 = C♯/D♭). Helpful for harmonizing songs.
    - **Loudness**: The average loudness of a track in decibels (dB). Tracks closer to 0dB are louder.
    - **Mode**: Indicates if the track is in a major (1) or minor (0) key. Major is usually happy, while minor is more somber.
    - **Acousticness**: Predicts the likelihood of a track being acoustic, ranging from 0.0 to 1.0. Higher values indicate more acoustic elements.
    - **Instrumentalness**: Estimates whether a track is instrumental, with higher values indicating fewer vocals.
    - **Liveness**: Detects live performance elements, with higher scores suggesting live recordings.
    - **Valence**: Measures the positivity of a track, from 0.0 (sad/angry) to 1.0 (happy/cheerful).
    - **Tempo**: The speed of the track in beats per minute (BPM). Higher BPM indicates a faster track.
    """)


# Home tab
with tabs[1]:
    st.header("Home")
    if st.sidebar.button("Get Playlist Data"):
        if username and playlist_link:
            with st.spinner("Fetching data..."):
                try:
                    df = get_playlist_tracks_more_than_100_songs(username, playlist_link)
                    st.success("Data retrieved successfully!")
                    
                    st.write("### Playlist Data")
                    st.dataframe(df)
                    
                    # Visualizations
                    st.write("### Visualizations")
                    
                    fig1 = px.histogram(df, x='Danceability', nbins=20, title="Danceability Distribution")
                    st.plotly_chart(fig1)
                    
                    fig2 = px.scatter(df, x='Energy', y='Valence', color='Popularity', 
                                    title="Energy vs Valence with Popularity",
                                    hover_data = {'Title':True})
                    st.plotly_chart(fig2)
                    
                    fig3 = px.box(df, x='Time Signature', y='Tempo', title="Tempo Distribution by Time Signature")
                    st.plotly_chart(fig3)
                     
                    # Preprocess data for line chart
                    df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
                    df = df.dropna(subset=['Release Date'])  # Drop rows with invalid dates
                    release_date_counts = df['Release Date'].dt.to_period('Y').value_counts().sort_index()
                    release_date_counts_df = release_date_counts.reset_index()
                    release_date_counts_df.columns = ['Release Date', 'Count']
                    release_date_counts_df['Release Date'] = release_date_counts_df['Release Date'].astype(str)  # Convert Period to string
                    
                    # Line chart for release date and count of songs
                    fig4 = px.line(release_date_counts_df, x='Release Date', y='Count', title="Count of Songs by Release Date")
                    st.plotly_chart(fig4)
     
                except Exception as e:
                    st.error(f"Error fetching data: {str(e)}")
        else:
            st.warning("Please enter both username and playlist link.")
