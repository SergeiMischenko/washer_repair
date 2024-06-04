import json
import os

from django.conf import settings
from django.http import HttpResponse
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
            # return redirect("orders:request_status", request_id=repair_request.id)
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "showMessage": f"Заявка успешно создана. № вашей заявки: {repair_request.pk}. Ожидайте звонка."
                    })
                })
    form = RepairRequestForm(request.POST or None)
    return render(request, "orders/create_request.html", {"form": form})


def request_status(request, request_id):
    repair_request = RepairRequest.objects.get(id=request_id)
    return render(
        request, "orders/request_status.html", {"repair_request": repair_request}
    )


def privacy(request):
    file_path = os.path.join(settings.BASE_DIR, 'static', 'privacy.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        policy_text = file.read()

    return render(request, 'washer_repair/privacy.html', {'policy_text': policy_text})
