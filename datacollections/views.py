import itertools

from django.shortcuts import render, redirect
import os
from django.core.paginator import Paginator
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
    context = {}
    try:
        dataset = DataSet.objects.get(id=col_id)
        table_headers = InspectData().get_headers(dataset)
        table_data = InspectData().get_data(dataset)
        paginator = Paginator(table_data, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        all_pages = [list(paginator.get_page(i)) for i in range(1, int(page_number) + 1)]
        all_pages = itertools.chain.from_iterable(all_pages)

        context = {
            "dataset": dataset,
            "data": all_pages,
            "page_obj": page_obj,
            "headers": table_headers,
        }
    except DataSet.DoesNotExist:
        print("upsi")

    return render(request, 'datacollections/collection_details.html', context)
