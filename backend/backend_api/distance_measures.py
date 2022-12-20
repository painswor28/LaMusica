import numpy as np
from .models import *


def cam_encode(code_1, code_2):
  camelot_key_encoding = {'1A':{'1A': 0 ,  '1B':0.5,'12A':0.5,'2A':0.5},
                        '1B':{'1B': 0 ,  '1A':0.5,'12B':0.5,'2B':0.5},

                        '2A':{'2A': 0 ,  '2B':0.5,'1A':0.5,'3A':0.5},
                        '2B':{'2B': 0 ,  '2A':0.5,'1B':0.5,'3B':0.5},

                        '3A':{'3A': 0 ,  '3B':0.5,'2A':0.5,'4A':0.5},
                        '3B':{'3B': 0 ,  '3A':0.5,'2B':0.5,'4B':0.5},

                        '4A':{'4A': 0 ,  '4B':0.5,'3A':0.5,'5A':0.5},
                        '4B':{'4B': 0 ,  '4A':0.5,'3B':0.5,'5B':0.5},

                        '5A':{'5A': 0 ,  '5B':0.5,'4A':0.5,'6A':0.5},
                        '5B':{'5B': 0 ,  '5A':0.5,'4B':0.5,'6B':0.5},

                        '6A':{'6A': 0 ,  '6B':0.5,'5A':0.5,'7A':0.5},
                        '6B':{'6B': 0 ,  '6A':0.5,'5B':0.5,'7B':0.5},

                        '7A':{'7A': 0 ,  '7B':0.5,'6A':0.5,'8A':0.5},
                        '7B':{'7B': 0 ,  '7A':0.5,'6B':0.5,'8B':0.5},

                        '8A':{'8A': 0 ,  '8B':0.5,'7A':0.5,'9A':0.5},
                        '8B':{'8B': 0 ,  '8A':0.5,'7B':0.5,'9B':0.5},

                        '9A':{'9A': 0 ,  '9B':0.5,'8A':0.5,'10A':0.5},
                        '9B':{'9B': 0 ,  '9A':0.5,'8B':0.5,'10B':0.5},

                        '10A':{'10A': 0 ,  '10B':0.5,'9A':0.5,'11A':0.5},
                        '10B':{'10B': 0 ,  '10A':0.5,'9B':0.5,'11B':0.5},

                        '11A':{'11A': 0 ,  '11B':0.5,'10A':0.5,'12A':0.5},
                        '11B':{'11B': 0 ,  '11A':0.5,'10B':0.5,'12B':0.5},

                        '12A':{'12A': 0 ,  '12B':0.5,'11A':0.5,'1A':0.5},
                        '12B':{'12B': 0 ,  '12A':0.5,'11B':0.5,'1B':0.5}
  }

  return camelot_key_encoding[code_1].get(   code_2  , 1 )



def cam_dance(track_URI_1, track_URI_2):
  track_1 = Track.objects.get(uri = track_URI_1)

  track_2 = Track.objects.get(uri = track_URI_2)

  


  point1 = np.array((track_1.danceability, cam_encode(track_1.camelot_key , track_2.camelot_key )))
  point2 = np.array((track_2.danceability, 0))

  #print(point1, point2)

  return np.linalg.norm(point1 - point2)
  
  #( (track_1['tempo'] - track_2['tempo'])**2  + camelot_key_encoding[track_1['camelot_key']].get(   track_2['camelot_key']  , 10 )**2)**0.5  



def cam_dance_energy(track_URI_1, track_URI_2):
  track_1 = Track.objects.get(uri = track_URI_1)
  track_2 = Track.objects.get(uri = track_URI_2)
  


  point1 = np.array((track_1.danceability,track_1.energy, cam_encode(track_1.camelot_key, track_2.camelot_key) ))
  point2 = np.array((track_2.danceability,track_2.energy, 0))

  #print(point1, point2)

  return np.linalg.norm(point1 - point2)



def cam_dance_energy_valence(track_URI_1, track_URI_2):
  track_1 = Track.objects.get(uri = track_URI_1)

  track_2 = Track.objects.get(uri= track_URI_2)
  


  point1 = np.array((track_1.energy,track_1.danceability,track_1.valence, cam_encode(track_1.camelot_key , track_2.camelot_key )  ))
  point2 = np.array((track_2.energy,track_2.danceability,track_2.valence, 0))


  #print(point1, point2)
  return np.linalg.norm(point1 - point2)


def cam_dance_energy_val_accoustic(track_URI_1, track_URI_2):
  track_1 = Track.objects.get(uri = track_URI_1)
  track_2 = Track.objects.get(uri = track_URI_2)
  


  point1 = np.array((track_1.valence,track_1.energy,track_1.danceability,track_1.acousticness, cam_encode(track_1.camelot_key , track_2.camelot_key )))
  point2 = np.array((track_2.valence,track_2.energy,track_2.danceability,track_2.acousticness, 0))


  #print(point1, point2)
  return np.linalg.norm(point1 - point2)


def all_dist(track_URI_1, track_URI_2):
  track_1 = Track.objects.get(uri = track_URI_1)
  track_2 = Track.objects.get(uri = track_URI_2)


  



  point1 = np.array(  (   track_1.danceability, track_1.energy  , track_1.loudness   , track_1.speechiness   ,  track_1.acousticness   , track_1.instrumentalness   , track_1.liveness   , track_1.valence    ,  track_1.tempo   ,  track_1.popularity  ,track_1.explicit ,  cam_encode(track_1.camelot_key , track_2.camelot_key )  ) )
  point2 = np.array(    (   track_2.danceability, track_2.energy  , track_2.loudness   , track_2.speechiness   ,  track_2.acousticness   , track_2.instrumentalness   , track_2.liveness   , track_2.valence    ,  track_2.tempo   ,  track_2.popularity  ,track_2.explicit ,0  ) )


  #print(point1, point2)
  return np.linalg.norm(point1 - point2)

