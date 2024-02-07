from django.shortcuts import render
from django.http import HttpResponse

# This function calls HttpResponse and simply returns 'Musiquita Homepage' 
# def homepage(request):
#     return HttpResponse('Musiquita Homepage')

# This function calls render and returns the 'homepage.html' file
def homepage(request):
    return render(request, 'homepage.html')