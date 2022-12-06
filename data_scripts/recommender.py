#!/usr/bin/env python3
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from data_retrieval_algorithms import *
from random import randint

# spotipy credentials
cid = "325f1fd79d3442cda063aaa9b573df59"
secret = "b4535dab66824c92bd88884122b8b75f"

client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=10, retries=10)

# returns a list of 'limit' recommended tracks based on a track_uri 
def recommender(track_uri, limit=25):
    # get recommended tracks
    recommended_tracks =  sp.recommendations(seed_tracks=track_uri, limit=limit)['tracks']
    recommended_uris = [track['uri'] for track in recommended_tracks]
    #loaddata(recommended_uris)
    return recommended_uris

def data_ingestor(track_uri, limit=25):
    recommended_uris = recommender(track_uri=track_uri)
    loaddata(recommended_uris)
    new_seed = recommended_uris[randint(0, 24)]
    data_ingestor(new_seed)

data_ingestor(["spotify:track:3s7MCdXyWmwjdcWh7GWXas"], limit=50)