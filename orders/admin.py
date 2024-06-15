from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from orders.models import Master, RepairRequest, Review, Service, WasherModel


# Inlines
class ReviewInline(admin.StackedInline):
    model = Review
    max_num = 1


# Models
@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "full_name",
        "phone",
        "email",
        "master",
        "model_washer",
        "status",
        "created_at",
        "updated_at",
    ]
    list_display_links = ["id", "full_name"]
    date_hierarchy = "created_at"
    list_editable = ["status"]
    search_fields = ["id", "name", "surname", "phone", "email"]
    list_filter = ["status", "model_washer", "master"]
    ordering = ["-created_at"]
    inlines = [ReviewInline]

    @admin.display(description="ФИО")
    def full_name(self, obj):
        return f"{obj.name} {obj.surname}"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("master", "model_washer")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "order_link", "rating", "created_at"]
    list_display_links = ["id", "order_link"]
    list_filter = ["rating"]
    search_fields = ["order__name", "order__surname"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    @admin.display(description="Заявка")
    def order_link(self, obj):
        url = reverse("admin:orders_repairrequest_change", args=[obj.order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.order)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("order")


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "surname",
        "phone",
        "email",
        "work_experience",
        "qualification",
        "orders_count",
    ]

    def orders_count(self, obj):
        return obj.orders_count

    orders_count.short_description = "Количество заказов"

    def get_queryset(self, request):
        queryset = Master.objects.all().annotate(orders_count=Count("orders"))
        return queryset


@admin.register(WasherModel)
class WasherModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price"]
    search_fields = ["name", "price"]
    list_editable = ["name", "price"]
    ordering = ["name"]


admin.site.site_title = "Моя админка"
admin.site.site_header = "Административная панель сайта"
admin.site.index_title = "Главная"
