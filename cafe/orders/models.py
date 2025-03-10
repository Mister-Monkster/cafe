import datetime

from django.db import models
from django.db.models import QuerySet


class Products(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=100)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)

    def __str__(self) -> str: #Данный метод отвечает за представление модели в виде строки
        return f'{self.name} - {self.price}руб.'

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


class Orders(models.Model):
    statuses = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.PositiveIntegerField(verbose_name='Номер стола')
    status = models.CharField(verbose_name='Статус заказа', max_length=20, choices=statuses, default='pending')
    created_at = models.DateField(verbose_name='Время заказа', auto_now_add=True)
    updated_at = models.DateField(verbose_name='Время изменения статуса', auto_now=True)

    def total_price(self) -> float: #Рассчет стоимости заказа
        return sum(item.product.price * item.quantity for item in self.items.all())

    def profit(self, orders: QuerySet) -> float: #Расчет прибыли
        profit = 0
        for item in orders:
            profit += item.total_price()
        return profit

    def __str__(self) -> str: #Данный метод отвечает за представление модели в виде строки
        return f"Order {self.id} (Table {self.table_number})"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Блюдо')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self) -> str: #Данный метод отвечает за представление модели в виде строки
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'
