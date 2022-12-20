

from django.db import models
from .distance_measures import * 





def make_similarity(self, track_URI, symm=True):

    try:
        Test=Priority.objects.get(track_ptr_id=self),
    except:
     
        print(self, '   ' , track_URI)

    if self.startswith('spotify:track:') and track_URI.startswith('spotify:track:') and self != track_URI:
        similarity, created = Similar.objects.get_or_create(
            from_uri=Priority.objects.get(track_ptr_id=self),
            to_uri=Priority.objects.get(track_ptr_id=track_URI),
        




        
            cam_dance = cam_dance(self, track_URI), 
            cam_dance_energy= cam_dance_energy(self, track_URI), 
            cam_dance_energy_valence= cam_dance_energy_valence(self, track_URI), 
            cam_dance_energy_valence_acoustic= cam_dance_energy_val_accoustic(self, track_URI), 
            all_dist= all_dist(self, track_URI) )
        
        if symm:
        # avoid recursion by passing `symm=False`
            make_similarity(track_URI,self, False)
        return similarity




def remove_similarity(self, track_URI, symm=True):
    Similar.objects.filter(
        from_uri=self,
        to_uri=person).delete()
    if symm:
        # avoid recursion by passing `symm=False`
        remove_similarity(track_URI, self, False)






