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
from random import randint

# Backend endpoints
PORT = "5003"
TRACK_URL = "http://db8.cse.nd.edu:" + PORT + "/backend/tracks/"
ALBUM_URL = "http://db8.cse.nd.edu:" + PORT + "/backend/albums/"
PLAYLIST_URL = "http://db8.cse.nd.edu:" + PORT + "/backend/playlists/"
GENRE_URL = "http://db8.cse.nd.edu:" + PORT + "/backend/genres/"
ARTIST_URL = "http://db8.cse.nd.edu:" + PORT + "/backend/artists/"

# Spotify API credentials — index 0 is the cid, index 1 is the secret
credentials = [
    ["325f1fd79d3442cda063aaa9b573df59", "b4535dab66824c92bd88884122b8b75f"],
    ["9b5b3d715b164701b899f00d20d450cc", "2d4b4d17ac3244cb97010af0a93c4cef"],
    ["c027b7e9ce4b4ea4b02da734b37b105d", "9680a6425d1b46808755165447252bc3"],
    ["d5f293dffeac43e0ae9bfdb15939dbfd", "fe9d4ffb4ef346afb9157f79d934e5cb"],
    ["c862e96acb4147479ac62ab94fcfd098", "e282fb8aee794151ac934632afb007ad"],
    ["4c3864ec85b34e14b96201ae20966487", "fab18e1f503542ddaf6bfd112e32a21a"],
    ["f15b1363498441f2a6f546240d75ecdf", "79fb163aa0164d83a92ec08729adca3a"],
    ["e1006b40bc954149b3ece3763c92e613", "b9681cad8c1a4f16a232ac5612f89364"],
    ["625edf0f24974b49b597e4c134e45097", "aab891666ca04af49120c97854af2426"],
    ["efb2e53223e4416584ab18f0201046ef", "095fe18ce4a04541834eafa8b139bf2d"],
    ["9cf740d3f8054d238af52e171ca4db0e", "d8c0675ee67244949a1df6a829b5a097"],
    ["4b15e4a0258746478d7f684a31ecd20d", "a69ac9366c574730b087645cd88b8293"],
    ["97c0ac9ce6ec4d848c07ffa6b88661de", "9aa89341b71f4df597e4c6d72430eedc"],
    ["6b58516948b44f4a9bb0a7dd6db41bba", "4a1bcd6c81cb4d76b7e897163a7f16f1"],
    ["526d6889bfea46b2bde60edbd56711b2", "0293adb3dd9a4b9287393ed72601db1e"],
    ["4c77048c5cc04a5c949ee1459c2f8430", "d5cc7c94d6924799add37db93fa11cea"],
    ["5702c99baf6e45d88b882a0e4c8eddda", "211dee4cb3bd4674a68d6a4fcd8a6631"],
    ["6b26acfd7215441180b2a89b94446ed4", "f39f7a169bb14a67865c57e61db54aa0"],
    ["14c34c85083147f9b2ec1ac5556a1056", "b1eca574bd92498da4d528859f6e8e04"],
    ["2538e50e89f64aed8f7fd16b8d5bba7e", "43045f4dd6d344c3b88f6c986425053f"],
    ["1e76715416b94384998ef1758f6b8b9c", "351517c28db7451d8c0f071af42f43c7"],
    ["e8bd885516a6419e991f34813d84c540", "82a59a1014c74dc387dd5f93f6683a07"],
    ["aa04f7729e6543c89c8c97644036f1b4", "5b5d1aacff314b2b8d6bb0eaa88cca53"],
    ["8747ba4e1c6647e8b7c9c3939cc4445e", "a19d2df9c18746f3baa416e03948a519"]
]

def initialize_spotipy():
    ''' 
    function that returns the spotipy API client - just pulls a cid/secret pairing at random from credentials 
    (enough entropy with our usage that rate limits shouldn't be a problem)
    '''
    randNum = randint(0, len(credentials) - 1)
    cid = credentials[randNum][0]
    secret = credentials[randNum][1]
    client_credentials_manager = SpotifyClientCredentials(
        client_id=cid, client_secret=secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=10, retries=10)

    return sp

sp = initialize_spotipy()

def get_track_features(uris):
    ''' function to retrieve song features metadata from a list of uris '''
    # track_features is a dict of all audio features metadata for each track
    print('getting features')
    try: 
        result = sp.audio_features(uris)
    except ReadTimeout as t:
        print(t.msg)
        result = sp.audio_features(['spotify:track:6RSNKGdv3nDTHqgw4bdzyF'])
    return result

def get_track_desc(uris):
    ''' returns track description given list of uris '''
    print('getting tracks')
    try: 
        result = sp.tracks(uris)
    except ReadTimeout as t:
        print(t.msg)
        result = sp.tracks(['spotify:track:6RSNKGdv3nDTHqgw4bdzyF'])
    print('return track desc')
    return result

def artists_from_desc(desc):
    ''' return mapping of songs with their respective artists '''
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

def batch_call_artists(song_to_artists):
    ''' function to call Spotify's artists API in batches of 50 '''
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
    ''' divide list into sublists of size n '''
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def clean_track(uri, features, desc, artists, album):
    ''' function to clean track features metadata '''
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
    ''' given tuple of key and mode, returns appropriate camelot kepy mapping '''
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
    ''' returns properly formatted json for artist '''
    return {
        "uri": artist["uri"],
        "name": artist["name"],
        "link": artist["external_urls"]["spotify"],
        "image": artist["images"][0]["url"] if len(artist["images"]) > 0 else None,
        "popularity": artist["popularity"],
        "genres": genres,
    }


def clean_album(album, artists):
    ''' cleans album into properly formatted json '''
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
    ''' returns list of all track uris in playlist '''
    tracks = []
    for track in playlist["tracks"]:
        tracks.append(track["track_uri"])
    return tracks

def clean_playlist(playlist, tracks):
    ''' cleans playlist into proper json '''
    return {
        "pid": playlist["pid"],
        "name": playlist["name"],
        "num_followers": playlist["num_followers"],
        "tracks": tracks,
    }

def get_genre(artist):
    ''' returns a list of genres for given artist '''
    res = []

    for g in artist["genres"]:
        res.append(g)

    return res

def get_artists_uri(desc):
    ''' from track description, returns a list of artist uris '''
    res = []
    for artist in desc["artists"]:
        res.append(artist["uri"])

    return res

def get_album(desc):
    ''' post an album to the backend '''
    return desc["album"]

# Posting functions

def post_track(j):
    ''' post a track to the backend '''
    r = requests.post(TRACK_URL, json=j)
    print(r.text)


def post_playlist(j):
    '''post a playlist to the backend '''
    print('posting playlist')
    r = requests.post(PLAYLIST_URL, json=j)
    print(r.text)


def post_album(j):
    ''' post an album to the backend '''
    r = requests.post(ALBUM_URL, json=j)
    #print(r.text)


def post_genre(j):
    ''' post a genre to the backend '''
    try:
        r = requests.post(GENRE_URL, json=j)
    except requests.exceptions.RequestException:
        return
    #print(r.text)


def post_artist(j):
    ''' post an artist to the backend '''
    r = requests.post(ARTIST_URL, json=j)
    print(r.text)

# Loading data

def loaddata(uris):
    ''' primary data loading algorithm - posts up to 50 uris to the database at a time '''
    desc = get_track_desc(uris)["tracks"]
    features = get_track_features(uris)
    # get and post all genre and artist info in one loop
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
    ''' loads a single track to the database given a uri '''
    loaddata([uri])

# Searching songs

def track_search(queryString, limit=10):
    ''' loads data from a spotify search and returns limit number of track uri's that result from the search '''
    queryResult = sp.search(queryString, limit=limit)
    songUris = [item['uri'] for item in queryResult['tracks']['items']]
    loaddata(songUris)
    return songUris

# Playlist Functions

def clean_user_playlist(uri, name, num_followers, tracks):
    ''' cleans user playlist to be compatible with post_playlist in data_retrieval_algorithms.py '''
    return {
        "uri": uri,
        "name": name, 
        "num_followers": num_followers,
        "tracks": tracks
    }

def get_user_playlists(username):
    ''' given a spotify username, returns a list of all public playlist uri's on the user's account '''
    try:
        user_playlists = sp.user_playlists(username)
    except spotipy.SpotifyException:
        return []
    return [p['uri'] for p in user_playlists['items']]

def show_playlist_contents(playlist_uri):
    ''' given a playlist uri, returns the name and cover image of the playlist '''
    playlist_metadata = sp.playlist(playlist_uri)
    uri = playlist_metadata['uri']
    name = playlist_metadata['name']
    num_followers = playlist_metadata['followers']['total']
    if playlist_metadata['images']:
        image = playlist_metadata['images'][0]['url']
    else:
        image = ""
    return playlist_metadata, uri, name, num_followers, image

def playlist_info_json(playlist_uris):
    ''' given a list of playlist_uris, returns a list of json objects '''
    playlist_info = []
    for p in playlist_uris:
        _, uri, name, num_followers, image = show_playlist_contents(p)
        playlist_info.append(
            {
                "uri": uri,
                "name": name,
                "num_followers": num_followers,
                "image": image
            }
        )
    return playlist_info

def playlist_list_view(username):
    ''' given a spotify username, returns a list of high-level playlist metadata '''
    playlist_uris = get_user_playlists(username=username)
    playlist_info = playlist_info_json(playlist_uris=playlist_uris)
    return playlist_info

def load_single_playlist(playlist_uri):
    ''' function to load the data of a single playlist uri to the database ''' 
    playlist_metadata, _, name, num_followers, _ = show_playlist_contents(playlist_uri=playlist_uri)
    track_uris = [] 
    for track_metadata in playlist_metadata['tracks']['items']:
        if track_metadata['track']:
            uri = track_metadata['track']['uri']
            # take out any songs that are stored locally
            if uri.split(':')[1] == 'local':
                continue
            track_uris.append(uri)
    # break the tracks down into batches of size 50
    batched_tracks = list(divide_chunks(track_uris, 50))
    # load batch of tracks into the database
    for batch in batched_tracks:
        loaddata(batch)
    # post the playlist
    cp = clean_user_playlist(uri=playlist_uri, name=name, num_followers=num_followers, tracks=track_uris)
    post_playlist(cp)

def load_playlist_metadata(playlist_uris):
    ''' from a list of playlist uri's, loads all metadata for every uri to the db  '''
    for p in playlist_uris:
        load_single_playlist(p)
        
def load_user_playlists(username):
    ''' loads every public playlist associated with a given account to the database '''
    playlist_uris = get_user_playlists(username)
    load_playlist_metadata(playlist_uris)

def search_playlists(query, limit=20):
    ''' retrieve list of playlist uris based on search query '''
    # get list of playlist uris
    return [p['uri'] for p in sp.search(query, type='playlist')['playlists']['items']]

def recommender(track_uri, limit=10):
    ''' returns a list of 'limit' recommended tracks based on a track_uri '''
    # get recommended tracks
    recommended_tracks =  sp.recommendations(seed_tracks=[track_uri], limit=limit)['tracks']
    recommended_uris = [track['uri'] for track in recommended_tracks]
    loaddata(recommended_uris)
    return recommended_uris
