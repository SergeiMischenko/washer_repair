from django.core.exceptions import ValidationError
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models


class WasherModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Модель стиральной машины")

    class Meta:
        verbose_name = "Модель стиральной машины"
        verbose_name_plural = "Модели стиральных машин"
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name

    def clean(self):
        if WasherModel.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError(f"Модель {self.name} уже существует")


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name="Услуга")
    price = models.PositiveIntegerField(
        validators=[
            MinValueValidator(100),
            MaxValueValidator(100000),
        ],
        verbose_name="Цена",
    )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["name"]
        indexes = [models.Index(fields=["price"])]

    def __str__(self):
        return f"{self.name} - {self.price} руб."


class RepairRequest(models.Model):
    STATUS_CHOICES = (
        ("Принято в обработку", "Принято в обработку"),
        ("В ожидании запчастей", "В ожидании запчастей"),
        ("В процессе ремонта", "В процессе ремонта"),
        ("Тестирование и проверка", "Тестирование и проверка"),
        ("Готово к выдаче", "Готово к выдаче"),
        ("Заявка закрыта", "Заявка закрыта"),
    )
    name = models.CharField(max_length=100, verbose_name="Имя")
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    phone_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = models.CharField(validators=[phone_regex], max_length=16, verbose_name="Телефон")
    email = models.EmailField(max_length=100, blank=True, verbose_name="Email")
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default="Принято в обработку",
        verbose_name="Статус",
    )
    model_washer = models.ForeignKey(
        WasherModel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="orders",
        verbose_name="Модель",
    )
    services = models.ManyToManyField(
        Service, blank=True, verbose_name="Услуги", related_name="orders"
    )
    description = models.TextField(blank=True, verbose_name="Описание поломки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Заявка на ремонт"
        verbose_name_plural = "Заявки на ремонт"
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["-updated_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"№{self.pk} {self.name} {self.surname}"

    def get_absolute_url(self):
        return f"/orders/{self.pk}/"


class Review(models.Model):
    order = models.ForeignKey(
        RepairRequest,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Заявка",
    )
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Рейтинг"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    def clean(self):
        if Review.objects.filter(order=self.order).exclude(pk=self.pk).exists():
            raise ValidationError("Можно оставить только один отзыв на один заказ")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["rating"]),
        ]

    def __str__(self):
        return f"{self.order}: {self.text}"
