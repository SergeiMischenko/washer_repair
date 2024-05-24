from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from orders.models import RepairRequest, Review, Service, WasherModel


@admin.register(WasherModel)
class WasherModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


class ReviewInline(admin.StackedInline):
    model = Review
    max_num = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price"]
    search_fields = ["name", "price"]
    list_editable = ["name", "price"]
    ordering = ["name"]


@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "full_name",
        "phone",
        "email",
        "model_washer",
        "status",
        "created_at",
        "updated_at",
    ]
    list_display_links = ["id", "full_name"]
    date_hierarchy = "created_at"
    list_editable = ["status"]
    radio_fields = {"model_washer": admin.HORIZONTAL}
    search_fields = ["id", "name", "surname", "phone", "email"]
    list_filter = ["status", "model_washer"]
    ordering = ["-created_at"]
    inlines = [ReviewInline]

    def full_name(self, obj):
        return f"{obj.name} {obj.surname}"

    full_name.short_description = "ФИО"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "order_link", "rating", "created_at")
    list_display_links = ("id", "order_link")
    list_filter = ("rating",)
    search_fields = ("order__name", "order__surname")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    def order_link(self, obj):
        url = reverse("admin:orders_repairrequest_change", args=[obj.order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.order)

    order_link.short_description = "Заявка"


admin.site.site_title = "Моя админка"
admin.site.site_header = "Административная панель сайта"
admin.site.index_title = "Главная"
