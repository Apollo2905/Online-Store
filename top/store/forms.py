from django import forms
from .bulma_mixin import BulmaMixin
from .models import *


class OrderForm(BulmaMixin, forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Напишите адрес доставки'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Напишите номер телефона'
    }))
    comment = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Пожелания к заказу'
    }))

    class Meta:
        model = Order
        fields = ['address', 'phone', 'comment']


class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'textarea'}
    ), label='Можете оставить ваш отзыв здесь')
    rating = forms.ChoiceField(choices=RATE_CHOICES, required=True, label='Оцените продукт')

    class Meta:
        model = Review
        fields = ['text', 'rating']
