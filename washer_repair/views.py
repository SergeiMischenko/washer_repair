from django.shortcuts import render


def index(request):
    return render(request, "washer_repair/index.html")