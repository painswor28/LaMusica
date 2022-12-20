#!/usr/bin/env python3

from .models import *
from .similarity_creator import *

#print(Track.objects.get(uri="spotify:track:003TeKLxu9qrcWLF0JXgf9") )

def add_priority_track(track_URI, priority = 100):
  '''This whole function is tested  except similarity''' 

  
  if priority == -1:
    priority = Priority.objects.all().order_by('-queue').values( 'queue')[0]['queue'] +1
    #print(priority)
    

  tracks = Priority.objects.all().values('uri')
  try :
    this_track = Tracks.objects.get(uri = track_URI)
    p = Priority(track_ptr=track_URI, queue=priority)
    p.__dict__.update(this_track.__dict__)
    p.save()
    
  except:
    print(track_URI)
  else:
    for track in tracks:
      make_similarity(track_URI, track['uri'])

def add_priority_playlist(playlist_URI):
  ''' This whole function except for if we want to delete is tested '''

  playlist_tracks = Playlist.objects.filter(uri=playlist_URI)[0].tracks.all().values('uri')
  #print(playlist_tracks)
  playlist_tracks = playlist_tracks.values() 

  #print(playlist_tracks)
  priority_tracks = Priority.objects.all().values('uri')
  priority_tracks = priority_tracks.values() 
  
  
  for track in playlist_tracks:
    if track in priority_tracks:
      del playlist_tracks[track]
      #Priority.objects.filter(uri=track).delete()
      
  '''
  if we_want_to_delete == True:
    PRIORITY.objects.order_by('priority')[:len(playlist_tracks)-cnt].delete()
  '''
  cnt=1
  for track in playlist_tracks:
    add_priority_track(track['uri'], priority = -1)
    

def refresh_priority(N = 10000):
  #Similar.objects.all().delete()
  #:wPriority.objects.all().delete() #everything but deletes are tested

  tracks = Priority.objects.all().values('uri')
  for priority, track in  enumerate(Track.objects.all().order_by('-popularity')[:N]) :
    

    try :



      p = Priority(track_ptr_id=track.uri, queue=priority)
      p.__dict__.update(track.__dict__)
      p.save()
    
    except:
      print(type(track), '  ',track.uri,'  ', track.__dict__)
    else:
      for track_i in tracks:
        make_similarity(track.uri, track_i['uri'])

