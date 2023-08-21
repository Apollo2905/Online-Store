from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm, RateForm
from django.contrib.auth.decorators import login_required
from staff.models import CancelRequest


def home(request):
    products = Product.objects.all()
    slides = SliderImage.objects.all()
    category = request.GET.get('category')
    brand = request.GET.get('brand')

    action = request.GET.get('action')
    if action:
        favourite(request)
        return redirect('store:home')

    products = products.filter(category=category) \
        if category else products
    products = products.filter(brand=brand) \
        if brand else products

    amount = show_amount(request)
    return render(request, 'home.html',
                  {'products': products,
                   'slides': slides,
                   'amount': amount})


def product(request, pk=None):
    product_data = Product.objects.get(pk=pk)
    action = request.GET.get('action')

    # система отзывов
    form = RateForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.customer = request.user
        instance.product = product_data
        instance.save()
        return redirect('store:product', pk=product_data.pk)

    if action:
        favourite(request, pk)
        return redirect('store:product', pk=pk)
    amount = show_amount(request)
    return render(request, 'product.html', {'product': product_data, 'form': form, 'amount': amount})


def guest_register(request, pk):
    token = request.COOKIES['csrftoken']
    guest = Guest.objects.filter(token=token)

    if not guest:
        Guest.objects.create(token=token)
        guest = Guest.objects.filter(token=token)

    cart_item = CartItem.objects.filter(
        product=pk,
        guest=guest[0] if request.user.is_anonymous else None,
        customer=request.user if request.user.is_authenticated else None
    )

    if not cart_item:
        CartItem.objects.create(
            guest=guest[0] if request.user.is_anonymous else None,
            product=Product.objects.get(pk=pk),
            quantity=1,
            customer=request.user if request.user.is_authenticated else None
        )

    else:
        cart_item[0].quantity += 1
        cart_item[0].save()

    pk = request.GET.get('pk')
    return redirect('store:home') if not pk else redirect('store:product', pk=pk)


def cart(request):
    token = request.COOKIES['csrftoken']
    guest = Guest.objects.filter(token=token)

    action = request.GET.get('action')
    cart_item_pk = request.GET.get('pk')

    if action == 'increment' or action == 'decrement':
        edit_cart(action, cart_item_pk)
        return redirect('store:cart')
    elif action == 'favourite':
        favourite(request)
        return redirect('store:cart')
    elif action == 'add_chosen':
        CartItem.objects.filter(pk=cart_item_pk).update(chosen=True)
    elif action == 'remove_chosen':
        CartItem.objects.filter(pk=cart_item_pk).update(chosen=False)
    elif action == 'delete':
        pk = request.COOKIES.get('pk')
        CartItem.objects.get(pk=pk).delete()
        return redirect('store:cart')

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(customer=request.user)
    else:
        cart_items = CartItem.objects.filter(guest=guest[0]) if guest else []

    if action == 'choose_all':
        cart_items.update(chosen=True)
    if action == 'remove_chosen':
        cart_items.update(chosen=False)
    if action == 'delete_all':
        cart_items.delete()

    chosen_items = cart_items.filter(chosen=True)
    total_quantity = sum([i.quantity for i in chosen_items])
    total_sum = sum([i.total_price() for i in chosen_items])

    return render(request,
                  'cart.html',
                  {'cart_items': cart_items,
                   'total_quantity': total_quantity,
                   'total_sum': total_sum,
                   'chosen_items': chosen_items})


# def delete_cart_item(request, pk):


def edit_cart(action, pk):
    cart_item = CartItem.objects.get(pk=pk)
    if action == 'increment':
        cart_item.quantity += 1
        cart_item.save()

    if action == 'decrement' and cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()


@login_required(login_url='/users/sign_in/')
def create_order(request):
    cart_items = CartItem.objects.filter(customer=request.user, chosen=True)
    if not cart_items:
        return render(request, 'error.html', {})

    total_price = sum(item.total_price() for item in cart_items)
    amount = sum(item.quantity for item in cart_items)

    form = OrderForm(request.POST or None)

    if form.is_valid():
        order = Order.objects.create(
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            comment=request.POST.get('comment'),
            total_price=total_price,
            customer=request.user
        )
        for item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=item.product,
                amount=item.quantity,
                total=item.total_price()
            )
        cart_items.delete()
        return redirect('store:home')

    return render(request, 'order_create.html',
                  {'cart_items': cart_items,
                   'total_price': total_price,
                   'amount': amount,
                   'form': form
                   })


def favourite(request, pk=None):
    product_pk = request.GET.get('product') if not pk else pk

    product_detail = Product.objects.get(pk=product_pk)
    product_detail.favourite.add(request.user) \
        if request.user not in product_detail.favourite.all() \
        else product_detail.favourite.remove(request.user)


def favourite_page(request):
    favourite_products = Product.objects.filter(favourite=request.user)
    action = request.GET.get('action')
    if action:
        favourite(request)
        return redirect('store:favourite')

    amount = show_amount(request)
    return render(request, 'favourite.html', {'favourites': favourite_products, 'amount': amount})


@login_required(login_url='/users/sign_in/')
def orders(request):
    orders_list = Order.objects.filter(customer=request.user)
    amount = show_amount(request)
    return render(request, 'orders.html', {'orders': orders_list, 'amount': amount})


def show_amount(request):
    token = request.COOKIES['csrftoken']
    guest = Guest.objects.filter(token=token).last()

    cart_items = CartItem.objects.filter(
        customer=request.user
        if request.user.is_authenticated else None,
        guest=guest if request.user.is_anonymous else None
    )
    return sum([i.quantity for i in cart_items])


@login_required(login_url='/users/sign_in/')
def order_cancel(request, pk):
    order_data = Order.objects.get(pk=pk)
    CancelRequest.objects.create(order=order_data)
    return render(request, 'order_cancel.html', {'order': order_data})
