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
    list_editable = ["status", "master"]
    list_filter = ["status", "master", "model_washer"]
    autocomplete_fields = ["master", "model_washer"]
    date_hierarchy = "created_at"
    search_fields = ["name", "surname", "phone", "email"]
    filter_horizontal = ["services"]
    inlines = [ReviewInline]

    @admin.display(description="ФИО")
    def full_name(self, obj):
        return f"{obj.name} {obj.surname}"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("master", "model_washer")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "order_link", "rating", "created_at"]
    list_display_links = ["id", "order_link"]
    list_filter = ["rating"]
    search_fields = ["order__name", "order__surname"]
    date_hierarchy = "created_at"
    list_select_related = ["order"]

    @admin.display(description="Заявка")
    def order_link(self, obj):
        url = reverse("admin:orders_repairrequest_change", args=[obj.order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.order)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "phone",
        "email",
        "work_experience",
        "qualification",
        "orders_link",
    ]
    list_display_links = ["full_name", "orders_link"]
    search_fields = ["name", "surname"]

    @admin.display(description="ФИО")
    def full_name(self, obj):
        return f"{obj.name} {obj.surname}"

    @admin.display(description="Количество заказов")
    def orders_link(self, obj):
        url = (
            reverse("admin:orders_repairrequest_changelist")
            + f"?master__id__exact={obj.pk}"
        )
        return format_html('<a href="{}">{}</a>', url, obj.orders_count)

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
    list_editable = ["name", "price"]
    search_fields = ["name", "price"]


admin.site.site_title = "Моя админка"
admin.site.site_header = "Административная панель сайта"
admin.site.index_title = "Главная"
