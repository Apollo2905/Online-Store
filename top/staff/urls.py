from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('order/<int:pk>', views.order, name='order'),
    path('order_edit/<int:pk>', views.order_edit, name='order_edit'),
    path('product_create/', views.product_create, name='product_create'),
    path('cancel_requests/', views.cancel_requests, name='cancel_requests')
]
