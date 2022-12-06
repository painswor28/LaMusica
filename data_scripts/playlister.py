#!/usr/bin/env python3

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from data_retrieval_algorithms import *

# spotipy credentials
cid = "c027b7e9ce4b4ea4b02da734b37b105d"
secret = "9680a6425d1b46808755165447252bc3"

client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=10, retries=10)

# cleans user playlist to be compatible with post_playlist in data_retrieval_algorithms.py
def clean_user_playlist(uri, name, num_followers, tracks):
    return {
        "uri": uri,
        "name": name, 
        "num_followers": num_followers,
        "tracks": tracks
    }
# given a spotify username, returns a list of all public playlist uri's on the user's account
def get_user_playlists(username):
    try:
        user_playlists = sp.user_playlists(username)
    except spotipy.SpotifyException:
        return []
    return [p['uri'] for p in user_playlists['items']]

# given a playlist uri, returns the name and cover image of the playlist
def show_playlist_contents(playlist_uri):
    playlist_metadata = sp.playlist(playlist_uri)
    uri = playlist_metadata['uri']
    name = playlist_metadata['name']
    num_followers = playlist_metadata['followers']['total']
    if playlist_metadata['images']:
        image = playlist_metadata['images'][0]['url']
    else:
        image = ""
    return playlist_metadata, uri, name, num_followers, image

# given a list of playlist_uris, returns a list of json objects
def playlist_info_json(playlist_uris):
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

# given a spotify username, returns a list of high-level playlist metadata
def playlist_list_view(username):
    playlist_uris = get_user_playlists(username=username)
    playlist_info = playlist_info_json(playlist_uris=playlist_uris)
    return playlist_info

# function to load the data of a single playlist uri to the database
def load_single_playlist(playlist_uri):
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

# from a list of playlist uri's, loads all metadata for every uri to the db 
def load_playlist_metadata(playlist_uris):
    for p in playlist_uris:
        load_single_playlist(p)
        
# loads every public playlist associated with a given account to the database
def load_user_playlists(username):
    playlist_uris = get_user_playlists(username)
    load_playlist_metadata(playlist_uris)

def main():
    load_user_playlists('meuusnaogk14lqxydvhufdqz7')
    #print(playlist_list_view('p.ainsworth2gkhkjhkjh'))

if __name__ == '__main__':
    main()