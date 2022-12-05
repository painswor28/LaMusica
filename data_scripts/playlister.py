#!/usr/bin/env python3

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from data_retrieval_algorithms import *

# spotipy credentials
cid = "325f1fd79d3442cda063aaa9b573df59"
secret = "b4535dab66824c92bd88884122b8b75f"

client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=10, retries=10)

# cleans user playlist to be compatible with post_playlist in data_retrieval_algorithms.py
def clean_user_playlist(name, num_followers, tracks):
    return {
        "name": name, 
        "num_followers": num_followers,
        "tracks": tracks
    }
# given a spotify username, returns a list of all public playlist uri's on the user's account
def get_user_playlists(username):
    user_playlists = sp.user_playlists(username)
    return [p['uri'] for p in user_playlists['items']]

# from a list of playlist uri's, returns all metadata related to that playlist and 
def load_playlist_metadata(playlist_uris):
    for p in playlist_uris:
        playlist_metadata = sp.playlist(p)
        name = sp.playlist(p)['name']
        num_followers = playlist_metadata['followers']['total']
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
        cp = clean_user_playlist(name=name, num_followers=num_followers, tracks=track_uris)
        post_playlist(cp)
        

def post_user_playlists(username):
    pass

l = get_user_playlists('p.ainsworth2')
load_playlist_metadata(l)