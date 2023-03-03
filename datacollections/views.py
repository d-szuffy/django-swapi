import itertools
from django.shortcuts import get_object_or_404

from django.shortcuts import render, redirect
import os
from django.core.paginator import Paginator
from .fetch import FetchData
from .models import DataSet
from django.contrib import messages
from datacollections import utils
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
    data = DataSet.objects.all().order_by("-id")

    return render(request, 'datacollections/collections.html', {"data": data})


def collection_details(request, col_id):
    dataset = get_object_or_404(DataSet, id=col_id)
    try:
        table_headers = utils.get_headers(dataset.file_path)
        table_data = utils.get_data(dataset.file_path)
        paginator = Paginator(table_data, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        all_pages = [list(paginator.get_page(i)) for i in range(1, int(page_number) + 1)]

        context = {
            "dataset": dataset,
            "data": all_pages,
            "page_obj": page_obj,
            "headers": table_headers,
        }
    except FileNotFoundError:
        context = {
            'dataset': dataset
        }
        messages.error(
            request,
            "Sorry, the file you are looking for was not found."
        )

    return render(request, 'datacollections/collection_details.html', context)


def value_count(request, col_id):
    columns = request.GET.getlist("checks[]")
    dataset = get_object_or_404(DataSet, id=col_id)
    try:
        table_headers = utils.get_headers(dataset.file_path, columns)
        table_data = utils.get_data(dataset.file_path)
        grouped_data = utils.group_by(dataset.file_path, columns)
        context = {
            "dataset": dataset,
            "data": grouped_data,
            "headers": table_headers,
        }
    except FileNotFoundError:
        context = {
            'dataset': dataset
        }
        messages.error(
            request,
            "Sorry, the file you are looking for was not found."
        )

    return render(request, 'datacollections/value_count.html', context)
