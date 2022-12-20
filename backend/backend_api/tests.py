#!/usr/bin/env python3
from django.test import TestCase

# Create your tests here.

#from .priority_tracks import * 

#from distance_measures import *

from .models import *

def example_test():
    queryset = Track.objects.all()
    print(queryset)

example_test()

class PriorityTestCase(TestCase):
    def setUp(self):
        Priority.objects.create(name="spotify:track:0039tOs9Khnihi4dLWnwR9", queue=1)
        Animal.objects.create(name="spotify:track:001wUOgo8t9VElHl45bxzr", queue="2")

'''
def test_priority_track_add(uri, priority=1):
    add_priority_track(uri, priority)

#settings.configure()

test_priority_track_add("spotify:track:003TeKLxu9qrcWLF0JXgf9")
'''
