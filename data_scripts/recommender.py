#!/usr/bin/env python3
import sys
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

def recommender(track_uri, limit=25):
    # 
    recommended_tracks =  sp.recommendations(seed_tracks=track_uri, limit=limit)['tracks']
    uris = [track['uri'] for track in recommended_tracks]
    loaddata(uris)
    print("entering recursion")
    for uri in uris:
        print(f"recommender({uri})")
        recommender([uri])

recommender(["spotify:track:0EdOXJSlR6cpMLHmVlTz4p"], limit=50)