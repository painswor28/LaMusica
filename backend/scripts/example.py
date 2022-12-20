from backend_api.models import *

def run():
    queryset = Track.objects.all()

    print(queryset)

