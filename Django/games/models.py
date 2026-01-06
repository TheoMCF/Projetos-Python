from django.db import models

class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.genre
        
class Game(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    release_date = models.DateField(blank=True, null=True)
    platforms = models.CharField(max_length=100, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='game_genre', null=True, blank=True)
    developer = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    game_cover = models.ImageField(upload_to='games/', blank=True, null=True)
    
    def __str__(self):
        return self.name