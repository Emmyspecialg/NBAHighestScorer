from django.shortcuts import render
from .models import ScoreTable

def index(request):
    scoretables = ScoreTable.objects.all()
    context = {'scoretables': scoretables}
    return render(request, 'dashboard/index.html', context)
