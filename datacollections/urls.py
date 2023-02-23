from django.urls import path, include
from datacollections import views

urlpatterns = [
    path('', views.view_collections, name='view_collections')
]
