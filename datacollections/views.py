from django.shortcuts import render
from .fetch import FetchData
# Create your views here.


def home_page(request):
    return render(request, 'datacollections/home.html')


def new_collection(request):
    data = FetchData().create_csv_file()
    # data = FetchData().fetch_data("https://swapi.dev/api/people/")
    if data is None:
        data = "Something went wrong"

    return render(request, 'datacollections/collections.html', {"data": data})


def view_collections(request):
    return render(request, 'datacollections/collections.html')
