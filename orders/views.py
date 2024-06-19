import asyncio
import json
import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from telegram import Bot

from orders.forms import AddReviewForm, RepairRequestForm, RequestStatusForm
from orders.models import RepairRequest, Review, Service


async def send_telegram_message(message):
    """
    Отправляет асинхронно сообщения в Telegram.
    :param message: Текст сообщения для отправки.
    """
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    await bot.send_message(
        chat_id=settings.TELEGRAM_CHAT_ID, text=message, parse_mode="HTML"
    )


def index(request):
    """
    Отображает главную страницу с перечнем услуг.
    :param request: Объект запроса.
    :return: HTML страница с перечнем услуг из модели Service.
    """
    services = Service.objects.all()
    return render(request, "washer_repair/index.html", {"services": services})


def feedback(request):
    """
    Отображает страницу с отзывами.
    :param request: Объект запроса.
    :return: HTML страница с отзывами.
    """
    comments = Review.objects.all().select_related("order")
    return render(request, "orders/feedback.html", {"comments": comments})


def add_review(request, token):
    """
    Добавляет отзыв к заявке на ремонт используя уникальный токен заявки.
    :param request: Объект запроса.
    :param token: Токен заявки на ремонт.
    :return: HTML страница для добавления отзыва.
    """
    order = get_object_or_404(RepairRequest, token=token)
    comment = None
    if request.method == "POST":
        form = AddReviewForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.order = order
            comment.save()
            return redirect("orders:feedback")
    form = AddReviewForm(initial={"order": order})
    return render(request, "orders/add_review.html", {"form": form, "order": order})


def create_request(request):
    """
    Создает заявку на ремонт и отправляет уведомление о новой заявке в Telegram.
    :param request: Объект запроса.
    :return: HTML страница для создания заявки.
    """
    if request.method == "POST":
        form = RepairRequestForm(request.POST)
        if form.is_valid():
            # Все телефонные номера из существующих заявок
            orders_phone = set(RepairRequest.objects.values_list("phone", flat=True))
            repair_request = form.save()
            phone = form.cleaned_data["phone"]
            # Проверка на повторную заявку от абонента с тем же номером
            repeated_phone = any(phone in order for order in orders_phone)
            asyncio.run(
                send_telegram_message(
                    generate_request_message(
                        request, repair_request, phone, repeated_phone
                    ),
                )
            )
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


def generate_request_message(request, repair_request, phone, repeated_phone):
    """
    Генерирует сообщение о новой заявке.
    :param request: Объект запроса.
    :param repair_request: Заявка на ремонт.
    :param phone: Телефонный номер.
    :param repeated_phone: Флаг повторной заявки с тем же номером.
    :return: Строка сообщения о заявке.
    """
    # URL для перехода в админку к заявке
    admin_url = request.build_absolute_uri(
        reverse("admin:orders_repairrequest_change", args=[repair_request.pk])
    )
    # URL списка заявок с тем же номером в админке
    admin_url_search = (
        request.build_absolute_uri(
            reverse("admin:orders_repairrequest_changelist") + f"?q={phone[1:]}"
        )
        if repeated_phone
        else ""
    )
    model = (
        repair_request.model_washer.name
        if repair_request.model_washer
        else "Не указана"
    )
    message = [
        f"\U00002705 У вас новая заявка: {repair_request}",
        f"\U0000260E Телефон указанный в заявке: {phone}",
        f"\U0001F9FA Модель машинки: {model}",
        f"\U0001F50D Более подробно о заявке - <a href='{admin_url}'>Тут!</a>",
    ]
    # К сообщению добавляется строка при повторной заявке
    if repeated_phone:
        message.insert(
            3,
            f"\U000027F3 Повторная заявка этого абонента. Остальные - <a href='{admin_url_search}'>Здесь!</a>",
        )
    return "\n".join(message)


def request_status(request):
    """
    Отображает статус заявки на ремонт.
    :param request: Объект запроса.
    :return: HTML страница с информацией о статусе заявок.
    """
    if request.method == "POST":
        form = RequestStatusForm(request.POST)
        if form.is_valid():
            surname = form.cleaned_data["surname"]
            phone = form.cleaned_data["phone"]
            requests = RepairRequest.objects.filter(
                surname__iexact=surname, phone__icontains=phone
            ).select_related("model_washer")
            if requests.exists():
                name = requests[0].name
                surname = requests[0].surname
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
    """
    Отображает страницу с политикой конфиденциальности.
    :param request: Объект запроса.
    :return: HTML страница с текстом политики конфиденциальности.
    """
    file_path = os.path.join(settings.BASE_DIR, "static", "privacy.txt")
    with open(file_path, "r", encoding="utf-8") as file:
        policy_text = file.read()
    return render(request, "washer_repair/privacy.html", {"policy_text": policy_text})
