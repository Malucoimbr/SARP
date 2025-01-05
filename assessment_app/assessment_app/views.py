#from django.http import HttpResponse

#def index(request):
#    return HttpResponse("Welcome to the Assessment App")

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')  # Renderiza o template index.html