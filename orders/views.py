import json
import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from orders.forms import RepairRequestForm, RequestStatusForm
from orders.models import RepairRequest, Review, Service


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
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "showMessage": f"Заявка успешно создана. № вашей заявки: {repair_request.pk}. Ожидайте звонка."
                        }
                    )
                },
            )
    form = RepairRequestForm(request.POST or None)
    return render(request, "orders/create_request.html", {"form": form})


def request_status(request):
    if request.method == "POST":
        form = RequestStatusForm(request.POST)
        if form.is_valid():
            surname = form.cleaned_data["surname"]
            phone = form.cleaned_data["phone"]
            requests = RepairRequest.objects.filter(
                surname__iexact=surname, phone__icontains=phone
            )
            if requests.exists():
                name = requests[0].name
                phone = requests[0].phone
                return render(
                    request,
                    "orders/request_status.html",
                    {
                        "requests": requests,
                        "name": name,
                        "surname": surname,
                        "phone": phone,
                    },
                )
            error_message = "Заявка не найдена. Проверьте данные."
            return render(
                request,
                "orders/request_status_modal.html",
                {"form": form, "error_message": error_message},
            )
    form = RequestStatusForm(request.POST or None)
    return render(request, "orders/request_status_modal.html", {"form": form})


def privacy(request):
    file_path = os.path.join(settings.BASE_DIR, "static", "privacy.txt")
    with open(file_path, "r", encoding="utf-8") as file:
        policy_text = file.read()

    return render(request, "washer_repair/privacy.html", {"policy_text": policy_text})
