from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
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
        # Проверяем, есть ли уже модель в базе данных
        existing_models = WasherModel.objects.filter(name=self.name)
        if self.pk:  # Если это обновление, исключаем текущую модель
            existing_models = existing_models.exclude(pk=self.pk)
        if existing_models.exists():
            raise ValidationError("Модель уже существует")



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
    phone = models.CharField(max_length=30, verbose_name="Телефон")
    email = models.CharField(max_length=100, blank=True, verbose_name="Email")
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
        # Проверяем, есть ли уже отзыв для этого заказа
        existing_reviews = Review.objects.filter(order=self.order)
        if self.pk:  # Если это обновление, исключаем текущий отзыв
            existing_reviews = existing_reviews.exclude(pk=self.pk)
        if existing_reviews.exists():
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
