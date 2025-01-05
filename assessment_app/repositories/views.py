from django.shortcuts import render
from .models import Repository

def repository_list(request):
    repositories = Repository.objects.all()
    return render(request, 'repository_list.html', {'repositories': repositories})