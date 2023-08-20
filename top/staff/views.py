from django.shortcuts import render
from store.models import Order


def home(request):
    orders = Order.objects.all()
    return render(request, 'admin.html', {'orders': orders})


def order(request, pk):
    order_data = Order.objects.get(pk=pk)
    return render(request, 'order.html', {'order': order_data})
