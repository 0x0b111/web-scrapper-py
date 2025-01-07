import spotipy;
from spotipy.oauth2 import SpotifyOAuth;
import os;
from dotenv import load_dotenv;
load_dotenv()


class SpotifyClient:

    def __init__(self):
        self.SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID");
        self.SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET");
        self.SPOTIFY_CLIENT_URI = os.getenv("SPOTIFY_CLIENT_URI");
        self.USERNAME = os.getenv('USERNAME');

        self.sp = spotipy.Spotify(
        auth_manager = SpotifyOAuth(
                client_id=self.SPOTIFY_CLIENT_ID,
                client_secret=self.SPOTIFY_CLIENT_SECRET,
                redirect_uri=self.SPOTIFY_CLIENT_URI,
                username= self.USERNAME,
                scope="playlist-modify-private",
                show_dialog=True,
                cache_path="token.txt"
            )
    )

    def search_songs(self, song_names, date):
        song_uris = []
        year = date.year
        for song in song_names:
            result = self.sp.search(q=f"track:{song} year:{year}", type="track")
            print(result)
            try:
                uri = result["tracks"]["items"][0]["uri"]
                song_uris.append(uri)
            except IndexError:
                print(f"{song} doesn't exist in Spotify. Skipped.")
        return song_uris
    
    def add_playlists(self, user_id, playlist_name, song_uri, public=False):
        
        try:
            playlist = self.sp.user_playlist_create(
                user=user_id, name=playlist_name, public=public
            )
            print(f"Playlist created: {playlist['name']} (ID: {playlist['id']})")
            return playlist
        
        except Exception as e:
            print(f"An error occurred while creating the playlist: {e}")
            return None
        
    def add_songs_to_playlist(self, playlist_id, song_uris):
        try:
            if song_uris:
                self.sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
                print(f"Added {len(song_uris)} songs to the playlist (ID: {playlist_id}).")
                return True
            else:
                print("No songs to add to the playlist.")
                return False
        except Exception as e:
            print(f"An error occurred while adding songs to the playlist: {e}")
            return False
    

# client = SpotifyClient();

# user_id = client.sp.current_user()["id"]