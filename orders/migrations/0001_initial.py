# Generated by Django 5.0.6 on 2024-05-24 12:11

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WasherModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, verbose_name="Модель стиральной машины"
                    ),
                ),
            ],
            options={
                "verbose_name": "Модель стиральной машины",
                "verbose_name_plural": "Модели стиральных машин",
                "ordering": ["name"],
                "indexes": [
                    models.Index(fields=["name"], name="orders_wash_name_a97618_idx")
                ],
            },
        ),
        migrations.CreateModel(
            name="RepairRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Имя")),
                ("surname", models.CharField(max_length=100, verbose_name="Фамилия")),
                ("phone", models.CharField(max_length=30, verbose_name="Телефон")),
                (
                    "email",
                    models.CharField(blank=True, max_length=100, verbose_name="Email"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Принято в обработку", "Принято в обработку"),
                            ("В ожидании запчастей", "В ожидании запчастей"),
                            ("В процессе ремонта", "В процессе ремонта"),
                            ("Тестирование и проверка", "Тестирование и проверка"),
                            ("Готово к выдаче", "Готово к выдаче"),
                            ("Заявка закрыта", "Заявка закрыта"),
                        ],
                        default="Принято в обработку",
                        max_length=100,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Описание поломки"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
                ),
                (
                    "model_washer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to="orders.washermodel",
                        verbose_name="Модель стиральной машины",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заявка на ремонт",
                "verbose_name_plural": "Заявки на ремонт",
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст отзыва")),
                (
                    "rating",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                        verbose_name="Рейтинг",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="orders.repairrequest",
                        verbose_name="Заявка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Отзыв",
                "verbose_name_plural": "Отзывы",
                "indexes": [
                    models.Index(
                        fields=["-created_at"], name="orders_revi_created_65cd35_idx"
                    ),
                    models.Index(
                        fields=["rating"], name="orders_revi_rating_a6c99c_idx"
                    ),
                ],
            },
        ),
        migrations.AddIndex(
            model_name="repairrequest",
            index=models.Index(
                fields=["-created_at"], name="orders_repa_created_75f812_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="repairrequest",
            index=models.Index(
                fields=["-updated_at"], name="orders_repa_updated_0b86ef_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="repairrequest",
            index=models.Index(fields=["status"], name="orders_repa_status_14418e_idx"),
        ),
    ]
