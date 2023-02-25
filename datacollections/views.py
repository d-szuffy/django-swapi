from django.shortcuts import render
from django.http import HttpResponse
from .fetch import FetchData
from .models import DataSet
# Create your views here.


def home_page(request):
    return render(request, 'datacollections/home.html')


def new_collection(request):
    err = False
    if request.method == "POST":
        try:
            filename, path = FetchData().create_csv_file()
            new_file = DataSet.objects.create(filename=filename, file_path=path)
            new_file.save()
        except TypeError:
            err = True
    data = DataSet.objects.all()

    return render(request, 'datacollections/collections.html', {"data": data, "err": err})


def view_collections(request):
    data = DataSet.objects.all()

    return render(request, 'datacollections/collections.html', {"data": data})


def collection_details(request, col_id):
    print("Co tu sie")
    print(col_id)
    try:
        dataset = DataSet.objects.get(id=col_id)
    except DataSet.DoesNotExist:
        print("upsi")
    return render(request, 'datacollections/collection_details.html', {"dataset": dataset})

