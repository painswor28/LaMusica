from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import *
from .serializers import *

class SongListApiView(APIView):

    def get(self, request):

        songs = Songs.objects.all()
        serializer = songSerializer(songs, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        data = {
            "id": request.data.get("id"),
            "artist": request.data.get("artist"),
            "songKey": request.data.get("songKey"),
            "tempo": request.data.get("tempo"),
        }

        serializer = songSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SongDetailApiView(APIView):
    def get_object(self, song_id):
        """
        Helper method to get the object with given song_id
        """
        try:
            return Songs.objects.get(id=song_id)
        except Songs.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, id):
        """
        Retrieves the Song with given song_id
        """
        song_instance = self.get_object(id)
        if not song_instance:
            return Response(
                {"res": "Object with song id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = songSerializer(song_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):

        song_instance = self.get_object(id)
        if not song_instance:
            return Response(
                {"res": "Object with song id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            "id": request.data.get("id"),
            "artist": request.data.get("artist"),
            "songKey": request.data.get("songKey"),
            "tempo": request.data.get("tempo"),
        }
        serializer = songSerializer(instance = song_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, id):

        song_instance = self.get_object(id)
        if not song_instance:
            return Response(
                {"res": "Object with song id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        song_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class trackListApiView(APIView):

    def get(self, request):

        tracks = Track.objects.all()
        serializer = trackSerializer(tracks, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        data = {
            "uri": request.data.get("uri"),
            "name": request.data.get("name"),
            "id": request.data.get("id"),
            "danceability": request.data.get("danceability"),
            "energy": request.data.get("energy"),
            "loudness": request.data.get("loudness"),
            "speechiness": request.data.get("speechiness"),
            "acousticness": request.data.get("acousticness"),
            "instrumental": request.data.get("instrumentalness"),
            "liveness": request.data.get("liveness"),
            "valance": request.data.get("valence"),
            "tempo": request.data.get("tempo"),
            "duration_ms": request.data.get("duration_ms"),
            "time_signature": request.data.get("time_signature"),
            "camelot_key": request.data.get("camelot_key"),
            "popularity": request.data.get("popularity"),
            "explicit": request.data.get("explicit"),
            "preview_url": request.data.get("preview_url"),
            "spotify_url": request.data.get("spotify_url"),
        }

        serializer = trackSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)