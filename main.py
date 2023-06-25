import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

os.environ["SPOTIPY_CLIENT_ID"] = "YOUR_ID" 
os.environ["SPOTIPY_CLIENT_SECRET"] = "YOUR_SECRET"
os.environ["SPOTIPY_REDIRECT_URI"] = "YOUR_REDIRECT_URI"

username = "YOUR_USERNAME" # your spotify username
playlist_name = "Top 10 Songs (script)"

def create_spotify_playlist(username, playlist_name):
    scope = "playlist-modify-public" # Change to playlist-modify-private for the playlist to be private

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username=username))
    playlists = sp.current_user_playlists()
    playlist_exists = False

    # Check if the playlist already exists
    for playlist in playlists["items"]:
        if playlist["name"] == playlist_name:
            playlist_id = playlist["id"]
            playlist_exists = True
            break

    # If the playlist doesn't exist, create a new one
    if not playlist_exists:
        playlist = sp.user_playlist_create(user=username, name=playlist_name)
        playlist_id = playlist["id"]

    return playlist_id

def add_tracks_to_playlist(username, playlist_id, track_uris):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public", username=username))
    sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=track_uris)

def get_top_tracks(username, limit=10, time_range="short_term"):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-top-read", username=username))
    top_tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    track_uris = [track["uri"] for track in top_tracks["items"]]
    return track_uris


# Grab the top tracks
track_uris = get_top_tracks(username)

# Create or retrieve the playlist ID
playlist_id = create_spotify_playlist(username, playlist_name)

# Add the tracks to the playlist 
add_tracks_to_playlist(username, playlist_id, track_uris)

print("Your top 10 songs this week have been added to your playlist.")