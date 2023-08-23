from django import forms
from .bulma_mixin import BulmaMixin
from store.models import Order, STATUS, Product, Category, Brand


class OrderEditForm(BulmaMixin, forms.ModelForm):
    address = forms.CharField(label="Изменить адрес")
    status = forms.ChoiceField(label="Изменить статус", choices=STATUS)

    class Meta:
        model = Order
        fields = ['address', 'status']


class ProductForm(BulmaMixin, forms.ModelForm):
    name = forms.CharField(label='Имя продукта')
    slug = forms.CharField(label='Slug')
    description = forms.CharField(label='Описание')
    price = forms.IntegerField(label='Цена')
    is_new = forms.CharField(widget=forms.CheckboxInput(), label='Новый продукт', required=False)
    is_discounted = forms.CharField(widget=forms.CheckboxInput(), label='Скидка', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    brand = forms.ModelChoiceField(queryset=Brand.objects.all())
    image = forms.ImageField()

    class Meta:
        model = Product
        fields = [
            'name',
            'slug',
            'description',
            'price',
            'is_new',
            'is_discounted',
            'category',
            'brand',
            'image',
        ]
