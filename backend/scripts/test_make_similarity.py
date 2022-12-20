
from backend_api.models import *
from backend_api.similarity import *



def run():

    a  = Priority.objects.all()[0]
    b = Priority.objects.all()[1]


    make_similarity("spotify:track:00hVU6kDP67JHurfwG2dtq","spotify:track:00t7QTffOR3SA3L1BvSQVq")



    '''
    spotify:track:00hVU6kDP67JHurfwG2dtq
    spotify:track:01Aj44KIjCrPmZeXq4UOky
    spotify:track:00meczE1jpLTX0BBzIGrAR
    spotify:track:00t7QTffOR3SA3L1BvSQVq
    spotify:track:010ALbbh5KlQ4fKWgSdhRd    '''
