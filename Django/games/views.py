from django.shortcuts import render
from games.models import Game

def games_list(request):
    if request.GET.get('search') != None:
        games = Game.objects.filter(genre__genre=request.GET.get('search'))
    else:
        games = Game.objects.all()
    
    return render(
        request,
        'games.html', 
        {'games': games})