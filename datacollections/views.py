from django.shortcuts import render

# Create your views here.


def home_page(request):
    return render(request, 'datacollections/home.html')


def view_collections(request):
    return render(request, 'datacollections/collections.html')
