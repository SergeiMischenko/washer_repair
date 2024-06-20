import uuid

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import RepairRequest, Review, Service, WasherModel


class StaticSitemap(Sitemap):
    """
    Карта-сайта для статичных страниц и примерной страницы с токеном
    """

    def items(self):
        return [
            "orders:index",
            "orders:feedback",
            "orders:privacy",
        ]

    def location(self, item):
        return reverse(item)
