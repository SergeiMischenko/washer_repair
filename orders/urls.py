from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path("", views.index, name="index"),
    path("feedback/", views.feedback, name="feedback"),
    path("add_review/<uuid:token>/", views.add_review, name="add_review"),
    path("create_request/", views.create_request, name="create_request"),
    path("status_request/", views.request_status, name="request_status"),
    path("privacy/", views.privacy, name="privacy"),
]
