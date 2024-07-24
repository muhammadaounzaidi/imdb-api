from django.db import models
import rest_framework

# Create your models here.

class StreamPlatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.TextField(max_length=360)
    website = models.URLField(max_length=255)
    def __str__(self):
        return self.name
    
class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.TextField(max_length=360)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    platform=models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")
    def __str__(self):
        return self.title
     