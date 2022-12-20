#!/usr/bin/env python3
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .data_retrieval_algorithms import *
from random import randint
from operator import itemgetter
from .models import *
from .priority_tracks import *
from django.db import connection
from .distance_measures import*

# returns a list of 'limit' recommended tracks based on a track_uri 
def recommender(track_uri, limit=10):
    # get recommended tracks
    print(track_uri)
    recommended_tracks =  sp.recommendations(seed_tracks=[track_uri], limit=limit)['tracks']
    recommended_uris = [track['uri'] for track in recommended_tracks]
    loaddata(recommended_uris)
    return recommended_uris

def search_popular(track_uri, output_playlist = None, SIMILARITY_MEASURE = 'cam_dance', N=10):
 
  we_want_to_delete = False 

  if output_playlist:
   add_priority_playlist(output_playlist) 

  if not Priority.objects.filter(track_ptr_id=track_uri).exists(): #could do create or get, 
    if we_want_to_delete == True:
      PRIORITY.objects.order_by('priority')[0].delete()
    add_priority_track(track_uri)

  with connection.cursor() as cursor:
    playlist_output = ''
    if output_playlist:

      func={'cam_dance':cam_dance,'cam_dance_energy':cam_dance_energy, 'cam_dance_energy_valence'
: cam_dance_energy_valence , 'cam_dance_energy_val_acoustic':cam_dance_energy_val_accoustic, 'all_dist':all_dist}

      output_playlist = Playlist.objects.filter(uri=output_playlist)[0].tracks.values('uri')
      op = output_playlist.values()
      inter =[]
      for i in range(len(op) ):
        #print(op)
        inter.append((op[i]['uri'] , func[SIMILARITY_MEASURE](track_uri, op[i]['uri']  )) )

    
        res = [ y[0] for y in sorted(inter, key = lambda x: x[1] ) ]





      playlist_output = 'WHERE EXISTS (SELECT * from backend_api_playlist_tracks WHERE playlist_id = "{output_playlist}" AND track_id = S.uri )'

  # repilcate this 
    cursor.execute(f'SELECT S.uri FROM (SELECT P.track_ptr_id as uri, similar.id as id, {SIMILARITY_MEASURE} FROM backend_api_similar similar, backend_api_priority P WHERE similar.to_uri_id = P.track_ptr_id AND similar.from_uri_id ="{track_uri}") S {playlist_output} ORDER BY S.{SIMILARITY_MEASURE} LIMIT {N};')
    similar_URIs = cursor.fetchall()
    
  if not output_playlist:
    res =  [x[0] for x in similar_URIs]

  return res[:10]


def most_playlists_shared(track_URI,key = '', N=25):
  if key != '':
    key = f'T.camelot_key={key} AND '
  with connection.cursor() as cursor:
    cursor.execute( f' SELECT T.uri, count(UPL.playlist_id) AS cnt FROM backend_api_track T, (SELECT playlist_id FROM backend_api_playlist_tracks WHERE track_id = "{track_URI}" )UPL , backend_api_playlist_tracks PT WHERE {key}T.uri != "{track_URI}" AND T.uri = PT.track_id AND UPL.playlist_id = PT.playlist_id GROUP BY T.uri ORDER BY cnt DESC LIMIT {N}' )
    shared_URIs = cursor.fetchall()

  return [x[0] for x in shared_URIs]




def song_playlist_similarity(playlist_tracks, track_URI, SIMILARITY_MEASURE= 'cam_dance'):
  sum=0
  with connection.cursor() as cursor:
    for track in playlist_tracks:
      
      cursor.execute( f'SELECT S.{SIMILARITY_MEASURE} FROM SIMILAR S WHERE uri_1={track} AND uri_2={track_URI} OR uri_1={track_URI} AND uri_2={track} LIMIT 1'           )

    sum = sum([ x[0] for x in cursor.fetchall() ])

    # might have to do some work on that object to make it an actual number rather than an object
    #also might have to adjust to work with a target playlist.

  return sum





def next_songs(playlist_URI, N=25, SIMILARITY_MEASURE='cam_dance'):
  ''' not sure I tested this  this is for multiple input songs'''
  priority_tracks = PRIORITY.objects.all().values('uri')
  priority_tracks = priority_tracks.values()

  playlist_tracks = PLAYLIST.objects.all().filter(uri=uri).tracks.values('uri')
  playlist_tracks = playlist_tracks.values()


  sim={}

  for track in priority_tracks:
    sim[track] = song_playlist_similarity(playlist_tracks, track, SIMILARITY_MEASURE)


  return list(dict(sorted(sim.items(), key=itemgetter(1))  ).keys() )[:25]
