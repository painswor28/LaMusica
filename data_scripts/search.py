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

query = sys.argv[1]


def search(queryString):
    queryResult = sp.search(queryString, limit=20)
    songUris = [item['uri'] for item in queryResult['tracks']['items']]
    loaddata(songUris)
    

def main():
    search(query)

if __name__ == '__main__':
    main()
