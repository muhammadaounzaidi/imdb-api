from django.urls import path, include

# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import *
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('stream', StreamPlatformVS,basename='streamplatform')

urlpatterns=[
    # path("list/", MovieListAV.as_view(),name='movie_list'),
    # path("<int:pk>/", MovieDetailAV.as_view(),name='movie_detail'),
    path("list/",WatchListAV.as_view(),name='movie_list'),
    path("<int:pk>/", WatchDetailAV.as_view(), name="movie-detail"),
    path('',include(router.urls)),
    # path("stream/",StreamPlatformAV.as_view(), name="stream"),
    # path("stream/<int:pk>/", StreamDetailAV.as_view(), name="stream-detail"),
    # path("review/",ReviewList.as_view(),name="review-list"),
    # path("review/<int:pk>",ReviewDetail.as_view(),name="review-detail"),
    path("stream/<int:pk>/review-create",ReviewCreate.as_view(), name="stream-detail"),
    path("stream/<int:pk>/review",ReviewList.as_view(), name="stream-detail"),
    path("stream/review/<int:pk>",ReviewDetail.as_view(),name="review-detail"),
    
]