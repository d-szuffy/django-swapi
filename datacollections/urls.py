from django.urls import path, include
from datacollections import views

urlpatterns = [
    path('', views.view_collections, name='view_collections'),
    path('new_collection', views.new_collection, name='new_collection'),
    path('collection_details/<int:col_id>/', views.collection_details, name='collection_details'),
    path('collection_details/value_count/<int:col_id>/', views.value_count, name='value_count')
]
