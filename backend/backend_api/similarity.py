#!/usr/bin/env python3

from .priority_tracks import *
from .distance_measures import *





 
def make_similarity(self, track_URI, symm=True):
    print( self, type(track_URI) )

    
    track_URI_obj =Priority.objects.get(track_ptr_id=track_URI)
    self_obj =Priority.objects.get(track_ptr_id=self)
    #track_URI_obj = Priority.objects.get(track_ptr_id=  track_URI)

    similarity, created = Similar.objects.get_or_create(
        from_uri=self_obj,
        to_uri=track_URI_obj,
        cam_tempo=cam_tempo(self, track_URI), 
        cam_tempo_dance=cam_tempo_dance(self, track_URI), 
        cam_tempo_dance_energy=cam_tempo_dance_energy(self, track_URI), 
        cam_tempo_dance_energy_loud=cam_tempo_dance_energy_loud(self, track_URI), 
        all_dist=all_dist(self, track_URI) 
        )
    if symm:
        # avoid recursion by passing `symm=False`
        make_similarity(track_URI,self, symm=False)
    return similarity




def remove_similarity(self, track_URI, symm=True):
    Similar.objects.filter(
        from_uri=self,
        to_uri=track_URI).delete()
    if symm:
        # avoid recursion by passing `symm=False`
        remove_similarity(track_URI,self, False)


def refresh_similarity():
  priority_track_list = Priority.objects.all().values('track_ptr_id')
  priority_track_list = [x['track_ptr_id'] for x in priority_track_list]
  
  Similar.objects.all().delete()

  while priority_track_list:
    curr_track = priority_track_list.pop()

    for track in priority_track_list:
      make_similarity( curr_track, track)















