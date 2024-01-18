from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at Musiquita app.")
# Create your views here.
