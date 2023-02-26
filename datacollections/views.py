from django.shortcuts import render, redirect
import os
from .fetch import FetchData
from .models import DataSet
from django.contrib import messages
from .utils import InspectData
# Create your views here.


def home_page(request):

    return render(request, 'datacollections/home.html')


def new_collection(request):

    if request.method == "POST":
        try:
            filename, path, _ = FetchData().create_csv_file()
            new_file = DataSet.objects.create(filename=filename, file_path=path)
            new_file.save()
            messages.success(
                request,
                "Data fetched successfully."
            )
        except TypeError:
            messages.error(
                request,
                "Something went wrong"
            )

    return redirect('view_collections')


def view_collections(request):
    data = DataSet.objects.all()

    return render(request, 'datacollections/collections.html', {"data": data})


def collection_details(request, col_id):
    table_data = {}
    table_headers = {}
    dataset = {}
    try:
        dataset = DataSet.objects.get(id=col_id)
        table_headers = InspectData().get_headers(dataset)
        table_data = InspectData().get_data(dataset)
    except DataSet.DoesNotExist:
        print("upsi")

    context = {
        "dataset": dataset,
        "data": table_data,
        "headers": table_headers,
    }

    return render(request, 'datacollections/collection_details.html', context)
