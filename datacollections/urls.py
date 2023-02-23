from django.urls import path, include
from datacollections import views

urlpatterns = [
    path('', views.view_collections, name='view_collections'),
    path('new_collection', views.new_collection, name='new_collection')
]
