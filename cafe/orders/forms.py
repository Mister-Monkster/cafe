from django import forms

from .models import Orders, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['table_number', 'status']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class SearchForm(forms.Form):
    statuses = [
        ('', ''),
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]
    status = forms.ChoiceField(choices=statuses, required=False, label="Статус")
    table_number = forms.IntegerField(required=False, min_value=0, label="Номер стола")


class DateForm(forms.Form):
    date = forms.DateField(label='Дата', widget=forms.SelectDateWidget(), required=False)
