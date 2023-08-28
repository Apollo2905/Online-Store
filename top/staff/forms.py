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
    name = forms.CharField(label='Имя продукта', widget=forms.TextInput(attrs={'class': 'input'}))
    slug = forms.CharField(label='Slug', widget=forms.TextInput(attrs={'class': 'input'}))
    description = forms.CharField(label='Описание', widget=forms.TextInput(attrs={'class': 'input'}))
    price = forms.IntegerField(label='Цена', widget=forms.NumberInput(attrs={'class': 'input'}))
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
