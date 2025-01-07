import requests;
from bs4 import BeautifulSoup;
from datetime import datetime;
from spotify_auth import SpotifyClient

# class initialize:
client = SpotifyClient();

url = "https://www.billboard.com/charts/hot-100/2000-08-12";
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
response = requests.get(url, headers= header);
if response.status_code != 200:
    print("failed to fetch")


web = BeautifulSoup(response.text, 'html.parser');
song_titles = web.select("li ul li h3");
song_title_list = [element.getText().strip() for element in song_titles];

if not song_title_list:
    print("No songs found on Billboard. Exiting.")
    exit()

print(f"Found {len(song_title_list)} songs from Billboard Hot 100.")

if client and hasattr(client, 'sp') and client.sp is not None:
    print("SpotifyClient was initialized successfully.")
else:
    print("SpotifyClient initialization failed earlier.")


user_input = input("Enter a date in yyyy-mm-dd format: ")
try:
    date = datetime.strptime(user_input, "%Y-%m-%d")
    print(f"Valid date entered: {date.date()}")
    
except ValueError:
    print("Invalid format");

print("Searching for songs on Spotify...")
song_uris = client.search_songs(song_title_list, date)

if not song_uris:
    print("No songs found on Spotify. Exiting.")
    exit()

print(f"Found {len(song_uris)} songs on Spotify.")


user_id = client.sp.current_user()['id']
playlist_name = f"Billboard Hot 100 - {date}"
playlist = client.add_playlists(user_id=user_id, playlist_name=playlist_name, song_uri=song_uris, public=False)

if playlist is None:
    print("Failed to create playlist. Exiting.")
    exit()


success = client.add_playlists(playlist_id=playlist["id"], song_uris=song_uris)
if success:
    print(f"Playlist '{playlist_name}' created and updated successfully!")
else:
    print("Failed to add songs to the playlist.")