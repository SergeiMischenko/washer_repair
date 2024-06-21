import uuid

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    """
    Карта-сайта для статичных страниц и примерной страницы с токеном
    """

    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return [
            "orders:index",
            "orders:feedback",
            "orders:privacy",
        ]

    def location(self, item):
        return reverse(item)
