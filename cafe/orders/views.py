import datetime

from django.shortcuts import render, get_list_or_404

from django.shortcuts import render, get_object_or_404, redirect
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Orders, Products, OrderItem
from .forms import OrderForm, OrderItemForm, SearchForm, DateForm
from .serializers import ProductsSerializer, OrdersItemSerializer, OrdersSerializer


def order_list(request):
    form = SearchForm(request.GET)
    if request.method == 'GET':
        if form.is_valid():
            cd = form.cleaned_data
            if cd['status'] and cd['table_number']: #Если пользователь ввели в поисковой форме и статус заказа, и номер стола, то выполнится блок кода ниже
                orders = Orders.objects.filter(status=cd['status'], table_number=cd['table_number'])
            elif cd['status']: #Если пользователь ввел только статус заказа
                orders = Orders.objects.filter(status=cd['status'])
            elif cd['table_number']: #Если пользователь ввел только номер стола
                orders = Orders.objects.filter(table_number=cd['table_number'])
            else:
                orders = Orders.objects.all()
    return render(request,
                  'orders/order_list.html',
                  {'Title': 'Заказы',
                   'orders': orders,
                   "form": form})


def order_detail(request, pk: int):
    order = get_object_or_404(Orders, pk=pk)
    return render(request,
                  'orders/order_detail.html',
                  {'order': order, 'Title': 'Информация о заказе'})


def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})


def order_update(request, pk: int):
    order = get_object_or_404(Orders, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_form.html', {'form': form,
                                                      "Title": f'Редактировать заказ {pk}'})


def order_delete(request, pk: int):
    order = get_object_or_404(Orders, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request,
                  'orders/order_confirm_delete.html',
                  {'order': order,
                   'Title': 'Удалить заказ'})


def add_order_item(request, pk: int):
    order = get_object_or_404(Orders, pk=pk)  #Получение заказа или 404 ошибка при его отсутствии
    if request.method == 'POST':
        form = OrderItemForm(request.POST) #Определение формы
        if form.is_valid():
            product = form.cleaned_data['product']  #Получение данных из поля формы product
            quantity = form.cleaned_data['quantity']  #Получение данных из поля формы quantity
            position, created = OrderItem.objects.get_or_create(
                order=order,
                product=product,
                defaults={'quantity': quantity}
            )  #Получение объекта или создание, если его не существует
            if not created:
                position.quantity += int(quantity) #Если объект существует к его количеству добавляется количество с формы
                position.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderItemForm()
    return render(request,
                  'orders/add_order_item.html',
                  {'form': form,
                   'order': order,
                   'Title': 'Добавить блюда в заказ'})


def delete_order_item(request, pk: int):
    order_item = get_object_or_404(OrderItem, pk=pk)
    order_item.delete()
    return redirect('order_detail', pk=order_item.order.pk)


def get_profit(request, date: datetime.date = datetime.date.today()):  #Расчет выручки
    orders = Orders.objects.filter(created_at=date,
                                   status='paid')  #Получение заказов по дате (по умолчанию текущая дата) и по статусу "Оплачено"
    form = DateForm(request.GET)  #Определение формы
    if request.method == 'GET':
        if form.is_valid():
            cd = form.cleaned_data['date']  #Получение данных с формы
            orders = Orders.objects.filter(created_at=cd,
                                           status='paid')  #Получение заказов по дате, введенной пользователем, и по статусу "Оплачено"
    profit = 0
    for item in orders:
        profit += item.total_price()  #Расчет выручки
    return render(request,
                  'orders/orders_profit.html',
                  {'orders': orders,
                   'profit': profit,
                   'Title': 'Прибыль за сегодня',
                   'form': form}
                  )


class OrderFilter(filters.FilterSet):
    table_number = filters.NumberFilter(field_name='table_number')
    status = filters.CharFilter(field_name='status')

    class Meta:
        model = Orders
        fields = ['table_number', 'status']


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrdersItemSerializer
    permission_classes = [IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filter_backends = [filters.DjangoFilterBackend]
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]