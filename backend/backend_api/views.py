from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Songs
from .serializers import songSerializer

class SongListApiView(APIView):

    def get(self, request):

        songs = Songs.objects.all()
        serializer = songSerializer(songs, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        data = {
            'id': request.data.get('id'),
            'artist': request.data.get('artist'),
            'songKey': request.data.get('songKey'),
            'tempo': request.data.get('tempo'),
        }

        serializer = songSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)