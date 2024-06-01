from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path("", views.index, name="index"),
    path("feedback/", views.feedback, name="feedback"),
    path("create_request/", views.create_request, name="create_request"),
    path(
        "status_request/<int:request_id>/", views.request_status, name="request_status"
    ),
]
