from django.urls import path
from . import views

urlpatterns = [
    path('homepage/', views.homepage),
    path('results/', views.results, name='results')
]
