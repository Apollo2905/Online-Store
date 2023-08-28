from django.contrib.sites import requests
from django.shortcuts import render, redirect
from store.models import Order, STATUS
from .forms import OrderEditForm, ProductForm
from .models import CancelRequest
from django.db.models import Q


def home(request):
    orders = Order.objects.all()
    status = request.GET.get('status')
    orders = orders.filter(status=status) if status else orders

    search = request.GET.get('search')
    orders = orders.filter(
        Q(pk__icontains=search) |
        Q(customer__username__icontains=search)) \
        if search else orders

    return render(request, 'admin.html', {'orders': orders, 'status': STATUS})


def order(request, pk):
    order_data = Order.objects.get(pk=pk)
    return render(request, 'order.html', {'order': order_data})


def order_edit(request, pk):
    order_data = Order.objects.get(pk=pk)
    form = OrderEditForm(request.POST or None, instance=order_data)
    allowed_status = ['Создан', 'Принят', 'В сборке']

    if not request.POST.get('address'):
        form.address = order_data.address

    if form.is_valid():
        form.save()
        return redirect('staff:order', pk=pk)
    return render(request, 'order_edit.html', {'form': form, 'order': order_data, 'allowed_status': allowed_status})


def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('store:home')
    return render(request, 'product_create.html', {'form': form})


def cancel_requests(request):
    requests = CancelRequest.objects.all()
    action = request.GET.get('action')
    pk = request.GET.get('pk')

    if action:
        if action == 'confirm':
            CancelRequest.objects.get(pk=pk).order.delete()
        elif action == 'cancel':
            CancelRequest.objects.get(pk=pk).delete()
        return redirect('staff:cancel_requests')
    return render(request, 'cancel_requests.html', {'requests': requests})
