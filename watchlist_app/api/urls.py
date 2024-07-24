from django.urls import path
# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import *
from watchlist_app.api.views import WatchListAV, StreamPlatformAV

urlpatterns=[
    # path("list/", MovieListAV.as_view(),name='movie_list'),
    # path("<int:pk>/", MovieDetailAV.as_view(),name='movie_detail'),
    path("list/",WatchListAV.as_view(),name='movie_list'),
    path("<int:pk>/", WatchDetailAV.as_view(), name="movie-detail"),
    path("stream/",StreamPlatformAV.as_view(), name="stream")
]