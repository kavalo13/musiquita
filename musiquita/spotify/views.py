from django.shortcuts import render
from decouple import config
from django.http import HttpResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta
def results(request):
    scope ="user-follow-read user-library-read user-library-modify "
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config("client_ID"), client_secret=config("client_SECRET"), redirect_uri=config("redirect_URL"), scope=scope))
    results = sp.current_user_followed_artists()
    artists = results['artists']['items']
    new_songs = []

    for artist in artists:
        artist_id = artist["id"]
        artist_albums = sp.artist_albums(artist_id)
        albums = artist_albums['items']
        for album in albums:
            album_name = album["name"]
            album_release_date = album["release_date"]
            album_id = album["id"]
            date_limit = datetime.now() - timedelta(7)
            album_release_date_time = try_parsing_date(album_release_date)
            if album_release_date_time >= date_limit:
                album_tracks = sp.album_tracks(album_id)
                album_songs = album_tracks["items"]
                for album_song in album_songs:
                    album_song_id = album_song['id']
                    sp.current_user_saved_tracks_add([album_song_id])
                    song_name = album_song.get("name")
                    album_cover_url = album['images'][0]['url'] if album['images'] else None
                    new_songs.append({"name": song_name, "album_cover_url": album_cover_url})

    return render(request, "results.html", {"song_names": new_songs})
# This function calls HttpResponse and simply returns 'Musiquita Homepage'
# def homepage(request):
#     return HttpResponse('Musiquita Homepage')

# This function calls render and returns the 'homepage.html' file
def homepage(request):
    return render(request, 'homepage.html')


def try_parsing_date(text):
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%Y'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')
