from django.contrib import admin
from games.models import Game, Genre

class GameAdmin(admin.ModelAdmin):
    list_display = ('game_cover', 'name', 'release_date', 'platforms', 'genre', 'developer', 'publisher')
    search_fields = ('name',)

class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre',)
    search_fields = ('genre',)
    
admin.site.register(Game, GameAdmin) 
admin.site.register(Genre, GenreAdmin)