from django.shortcuts import redirect, render

from orders.forms import RepairRequestForm
from orders.models import RepairRequest, Service, Review


def index(request):
    services = Service.objects.all()
    return render(request, "washer_repair/index.html", {"services": services})


def feedback(request):
    comments = Review.objects.all()
    return render(request, "orders/feedback.html", {"comments": comments})


def create_request(request):
    if request.method == "POST":
        form = RepairRequestForm(request.POST)
        if form.is_valid():
            repair_request = form.save()
            return redirect("orders:request_status", request_id=repair_request.id)
    form = RepairRequestForm()
    return render(request, "orders/create_request.html", {"form": form})


def request_status(request, request_id):
    repair_request = RepairRequest.objects.get(id=request_id)
    return render(
        request, "orders/request_status.html", {"repair_request": repair_request}
    )
