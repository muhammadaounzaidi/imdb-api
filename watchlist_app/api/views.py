from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from watchlist_app.api.serializers import (
    ReviewSerializer,
    StreamPlatformSerializer,
    WatchListSerializer,
)
from watchlist_app.models import Review, StreamPlatform, WatchList
from rest_framework import mixins
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from .permissions import *
from rest_framework.permissions import IsAuthenticated

# class ReviewList(
#     mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
# ):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


class ReviewList(generics.ListAPIView):

    serializer_class = ReviewSerializer
    permission_classes =[IsAuthenticated ]
    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes=[IsReviewUserOrReadOnly]


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return Review.objects.all()
    def perform_create(self, serializer):
        
        pk = self.kwargs["pk"]
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset=Review.objects.filter(review_user=review_user,watchlist=watchlist)
        
        if review_queryset.exists():
            raise ValidationError("You have already submitted the review.")
        
        if watchlist.number_rating==0:
            watchlist.avg_rating=serializer.validated_data['rating']
        else:
            watchlist.avg_rating=(watchlist.avg_rating +serializer.validated_data['rating'])/2
            
        watchlist.number_rating=watchlist.number_rating+1
        watchlist.save()
        serializer.save(watchlist=watchlist,review_user=review_user)


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]

# class StreamPlatformVS(viewsets.ViewSet):

#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# class StreamDetailAV(APIView):
#     def get(self, request, pk):
#         try:
#             streaming_platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({"error": "not found"}, status=status.HTTP_400_BAD_REQUEST)
#         serializer = StreamPlatformSerializer(
#             streaming_platform, context={"request": request}
#         )
#         return Response(serializer.data)

#     def put(self, request, pk):
#         streaming_platform = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(streaming_platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     def delete(self, request, pk):
#         streaming_platform = StreamPlatform.objects.get(pk=pk)
#         streaming_platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class StreamPlatformAV(APIView):
#     def get(self, request):
#         platform = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platform, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
