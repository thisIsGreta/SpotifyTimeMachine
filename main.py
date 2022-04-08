import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup
client_ID = os.environ['client_ID']
client_secret = os.environ['client_secret']
redirect_uri = "https://example.com/callback"
my_scope = "playlist-modify-private"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_ID,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=my_scope,
        cache_path="token.txt")
)
user_id = sp.current_user()["id"]

time = input("Which year would you like to go back to? Type the date in this format YYYY-MM-DD: ")
billbord_link = f"https://www.billboard.com/charts/hot-100/{time}/"
response = requests.get(billbord_link)
chart = response.text
soup = BeautifulSoup(chart, "html.parser")

songs_in_chart = soup.find_all("h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
singers_in_chart = soup.find_all("span", class_="a-no-trucate")
ranks_in_chart = soup.find_all("span", class_="u-letter-spacing-0080@tablet")

songs = [song.getText().split("\n\n\t\n\t\n\t\t\n\t\t\t\t\t")[1].split("\t\t\n\t\n")[0] for song in songs_in_chart]
singers = [singer.getText().split("\n\t\n\t")[1].split("\n")[0] for singer in singers_in_chart]
ranks = [rank.getText().split("\n\t\n\t")[1].split("\n")[0] for rank in ranks_in_chart]
# print(songs)
# print(singers)
# print(ranks)
track_uris = []
# for song in songs:
for num in range(len(songs)-1):
    searchQuery = songs[num] + ' ' + time.split("-")[0]
    searchResults = sp.search(q=searchQuery)
    try:
        track_uri = searchResults['tracks']['items'][0]['uri']
    except IndexError:
        continue
    else:
        track_uris.append(track_uri)
# print(track_uris)

playlist_name = f'{time} Billboard 100'
playlist = sp.user_playlist_create(user_id, playlist_name, description='Creates a playlist for user', public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)
