#!/usr/bin/env python3
import ijson
import json
import requests
import spotipy
from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials
from pathlib import Path
import time
from requests.exceptions import ReadTimeout
import sys
import os

PORT = "5003"
TRACK_URL = "http://db8.cse.nd.edu:" + PORT + "/backend/tracks/"
ALBUM_URL = "http://db8.cse.nd.edu:" + PORT + "/backend/albums/"
PLAYLIST_URL = "http://db8.cse.nd.edu:" + PORT + "/backend/playlists/"
GENRE_URL = "http://db8.cse.nd.edu:" + PORT + "/backend/genres/"
ARTIST_URL = "http://db8.cse.nd.edu:" + PORT + "/backend/artists/"

# cid and secret both belong to me (Ryan)
# cid = "325f1fd79d3442cda063aaa9b573df59"
# cid = "9b5b3d715b164701b899f00d20d450cc"
# cid = "c027b7e9ce4b4ea4b02da734b37b105d"
# cid = "d5f293dffeac43e0ae9bfdb15939dbfd"
# cid = "c862e96acb4147479ac62ab94fcfd098"
# cid = "4c3864ec85b34e14b96201ae20966487"
# cid = "f15b1363498441f2a6f546240d75ecdf"
# cid = "e1006b40bc954149b3ece3763c92e613"
# cid = "625edf0f24974b49b597e4c134e45097"
# cid = "efb2e53223e4416584ab18f0201046ef"
# cid = "9cf740d3f8054d238af52e171ca4db0e"
# secret = "b4535dab66824c92bd88884122b8b75f"
# secret = "2d4b4d17ac3244cb97010af0a93c4cef"
# secret = "9680a6425d1b46808755165447252bc3"
# secret = "fe9d4ffb4ef346afb9157f79d934e5cb"
# secret = "e282fb8aee794151ac934632afb007ad"
# secret = "fab18e1f503542ddaf6bfd112e32a21a"
# secret = "79fb163aa0164d83a92ec08729adca3a"
# secret = "b9681cad8c1a4f16a232ac5612f89364"
# secret = "aab891666ca04af49120c97854af2426"
# secret = "095fe18ce4a04541834eafa8b139bf2d"
# secret = "d8c0675ee67244949a1df6a829b5a097"

if len(sys.argv) > 1:
    partition = sys.argv[1]
else:
    partition = 'partition1'
    
if len(sys.argv) > 2:
    cid = sys.argv[2]
else:
    cid = "325f1fd79d3442cda063aaa9b573df59"

if len(sys.argv) > 3:
    secret = sys.argv[3]
else:
    secret = "b4535dab66824c92bd88884122b8b75f"

client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=10, retries=10)

# print(sp.track('spotify:track:6RSNKGdv3nDTHqgw4bdzyF'))
# function to retrieve song features metadata from a list of uris
def get_track_features(uris):
    # track_features is a dict of all audio features metadata for each track
    print('getting features')
    try: 
        result = sp.audio_features(uris)
    except ReadTimeout:
        result = sp.audio_features(['spotify:track:6RSNKGdv3nDTHqgw4bdzyF'])
    return result


def get_track_desc(uris):
    print('getting tracks')
    try: 
        result = sp.tracks(uris)
    except ReadTimeout:
        result = sp.tracks(['spotify:track:6RSNKGdv3nDTHqgw4bdzyF'])
    print('return track desc')
    return result

# return mapping of songs with their respective artists
def artists_from_desc(desc):
    song_to_artists = [{} for _ in range(len(desc))]
    for i, song in enumerate(desc):
        try:
            if song:
                songUri = song['uri']
            else:
                continue
            for artist in song['artists']:
                artistUri = artist['uri']
                if song_to_artists[i].get(songUri):
                    song_to_artists[i][songUri].append(artistUri)
                else:
                    song_to_artists[i][songUri] = [artistUri]
        except TypeError:
            continue

    return song_to_artists
# function to call Spotify's artists API in batches of 50    
def batch_call_artists(song_to_artists):
    artist_batch = []
    artist_desc_list = []
    # retrieve list of artist uris
    for d in song_to_artists:
        for vs in d.values():
            for v in vs:
                if v not in artist_batch:
                    artist_batch.append(v)
    # batch call artists in groups of 50
    artist_batch = list(divide_chunks(artist_batch, 50))
    for chunk in artist_batch:
        try:
            artists = sp.artists(chunk)
        except ReadTimeout:
            artists = {"artists": [None]}
        for artist in artists['artists']:
            artist_desc_list.append(artist)
    return artist_desc_list

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]
# function to clean track features metadata
def clean_track(uri, features, desc, artists, album):
    track = {
        "uri": uri,
        "name": desc["name"],
        "danceability": features["danceability"],
        "energy": features["energy"],
        "loudness": features["loudness"],
        "speechiness": features["speechiness"],
        "acousticness": features["acousticness"],
        "instrumentalness": features["instrumentalness"],
        "liveness": features["liveness"],
        "valence": features["valence"],
        "tempo": features["tempo"],
        "duration_ms": features["duration_ms"],
        "time_signature": features["time_signature"],
        "camelot_key": get_camelot((features["key"], features["mode"])),
        "popularity": desc["popularity"],
        "explicit": desc["explicit"],
        "preview_url": desc["preview_url"],
        "spotify_url": desc["external_urls"]["spotify"],
        "album": album["uri"],
        "artists": artists,
    }

    return track


def get_camelot(key_mode):

    camelot_mapping = {
        (0, 1): "8B",
        (1, 1): "3B",
        (2, 1): "10B",
        (3, 1): "5B",
        (4, 1): "12B",
        (5, 1): "7B",
        (6, 1): "2B",
        (7, 1): "9B",
        (8, 1): "4B",
        (9, 1): "11B",
        (10, 1): "6B",
        (11, 1): "1B",
        (0, 0): "5A",
        (1, 0): "12A",
        (2, 0): "7A",
        (3, 0): "2A",
        (4, 0): "9A",
        (5, 0): "4A",
        (6, 0): "11A",
        (7, 0): "6A",
        (8, 0): "1A",
        (9, 0): "8A",
        (10, 0): "3A",
        (11, 0): "10A",
    }

    return camelot_mapping[key_mode]


def clean_artist(artist, genres):
    return {
        "uri": artist["uri"],
        "name": artist["name"],
        "link": artist["external_urls"]["spotify"],
        "image": artist["images"][0]["url"] if len(artist["images"]) > 0 else None,
        "popularity": artist["popularity"],
        "genres": genres,
    }


def clean_album(album, artists):
    if len(album["release_date"]) < 10:
        album["release_date"] = album["release_date"][:4] + "-01-01"

    return {
        "uri": album["uri"],
        "name": album["name"],
        "link": album["external_urls"]["spotify"],
        "cover_image": album["images"][0]["url"] if len(album["images"]) > 0 else None,
        "release_date": album["release_date"],
        "artists": artists,
    }

def get_playlist_tracks(playlist):
    tracks = []
    for track in playlist["tracks"]:
        tracks.append(track["track_uri"])
    return tracks

def clean_playlist(playlist, tracks):
    return {
        #"pid": playlist["pid"],
        "name": playlist["name"],
        "num_followers": playlist["num_followers"],
        "tracks": tracks,
    }

def get_genre(artist):
    res = []

    for g in artist["genres"]:
        res.append(g)

    return res

def get_artists_uri(desc):
    res = []
    for artist in desc["artists"]:
        res.append(artist["uri"])

    return res

def get_album(desc):
    return desc["album"]


def post_track(j):
    r = requests.post(TRACK_URL, json=j)
    print(r.text)


def post_playlist(j):
    print('posting playlist')
    r = requests.post(PLAYLIST_URL, json=j)
    print(r.text)


def post_album(j):
    r = requests.post(ALBUM_URL, json=j)
    #print(r.text)


def post_genre(j):
    try:
        r = requests.post(GENRE_URL, json=j)
    except requests.exceptions.RequestException:
        return
    #print(r.text)


def post_artist(j):
    r = requests.post(ARTIST_URL, json=j)
    print(r.text)

def loaddata(uris):
    desc = get_track_desc(uris)["tracks"]
    features = get_track_features(uris)
    #TODO: get and post all genre and artist info in one loop
    song_to_artists = artists_from_desc(desc)
    list_of_artists = batch_call_artists(song_to_artists)
    print('retrieving artists and genres')
    for artist in list_of_artists:
        genres = get_genre(artist)
        for genre in genres:
            genre = {"name": genre}
            post_genre(genre)
        artist = clean_artist(artist, genres)
        post_artist(artist)
    # loop to just post album and track
    print('retrieving artists and tracks')
    for i in range(len(uris)):
        if not desc[i]:
            continue
        if desc[i] and features[i]:
            artists = get_artists_uri(desc[i])
            albums = get_album(desc[i])
            track = clean_track(uris[i], features[i], desc[i], artists, albums)
            album = clean_album(albums, artists)
            post_album(album)
            post_track(track)
        else:
            continue

def insert_single_track(uri):
    loaddata([uri])

def main():
    # assign directory to iterate over
    tracks = []
    DIRECTORY = "./data/f/partitions.nosync/" + partition + "/" + sys.argv[4]
    print(DIRECTORY)
    FILES_IN_DIRECTORY = Path(DIRECTORY).glob("*")
    playlist_tracks = []
    # for file in FILES_IN_DIRECTORY:
    #     with open(str(file), "rb") as f:
    #         print("Opening File")
    #         for playlist in ijson.items(f, "playlists.item"):
    #             tracks.clear()
    #             print("-----" + playlist["name"] + "-----")
    #             tracks = get_playlist_tracks(playlist)
    #             cp = clean_playlist(playlist, tracks)
    #             post_playlist(cp)

    playlistCount = 0
    fileCount = 1
    cntr = 0
    batchList = []
    for file in FILES_IN_DIRECTORY:
        fStr = str(file)
        print(f'---Reading file {fileCount}: "{str(file)}"---')
        if not fStr.split('/')[-1].startswith('mpd'):
            continue
        with open(fStr, "rb") as f:
            print("File open")
            for playlist in ijson.items(f, "playlists.item"):
                print("Playlist:", str(playlistCount) + ":", playlist["name"])
                playlistCount += 1
                for track in playlist["tracks"]:
                    artist_uri = track["artist_uri"]
                    track_uri = track["track_uri"]

                    cntr += 1
                    print("Track", cntr, ": ", track_uri)  # this is just a test
                    # we can batch call up to 50 tracks at a time
                    if len(batchList) >= 49:
                        #time.sleep(10)
                        print(batchList)
                        loaddata(batchList)
                        batchList.clear()
                    else:
                        batchList.append(track_uri)
                playlist_tracks = get_playlist_tracks(playlist)
                cp = clean_playlist(playlist, playlist_tracks)
                post_playlist(cp)

        print(f'---Closing file {fileCount}: "{str(file)}"---')
        if not os.path.exists(DIRECTORY + '/toPost'):
            os.makedirs(DIRECTORY + '/toPost')
            os.replace(DIRECTORY + '/' + str(file).split('/')[-1], DIRECTORY + '/toPost/' + str(file).split('/')[-1])
        else:
            os.replace(DIRECTORY + '/' + str(file).split('/')[-1], DIRECTORY + '/toPost/' + str(file).split('/')[-1])
        fileCount += 1

if __name__ == '__main__':
    main()