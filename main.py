from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

year = input("Which year do you want to travel to? Type in this format YYYY-MM-DD: ")
url_b = f"https://www.billboard.com/charts/hot-100/{year}/"
scope = "playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="*****",
        client_secret="****",
        show_dialog=True,
        cache_path="token.txt"))

#user_id = sp.current_user()["id"]


res = requests.get(url=url_b)
soup = BeautifulSoup(res.text, "html.parser")

song_array = soup.find_all("h3", id="title-of-a-story")
arr = []

for song in song_array:
    res = song.getText().replace("\n", "").replace("\t", "").replace("’"," " )

    if len(res) < 30 and res.find('Songwriter(s):') == -1 and res.find('Producer(s):') == -1 and res.find(
            'Imprint/Promotion Label:') == -1:
        arr.append(res)

arr_uri = []

for song_ in arr:
    song_res = sp.search(q=f"track:{song_} year:{year}", type="track")
    try:
        s = song_res["tracks"]["items"][0]["uri"]
        arr_uri.append(s)
    except IndexError:
        print("Song not found.")

playlist = sp.user_playlist_create(user="****", name=f"{year.split('-')[0]} Billboard 100", public=False)

len(arr_uri)
sp.playlist_add_items(playlist_id=playlist["id"], items=arr_uri)