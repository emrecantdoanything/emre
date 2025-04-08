from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('customer/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customer/add/', views.customer_add, name='customer_add'),
    path('customer/<int:customer_id>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:customer_id>/delete/', views.customer_delete, name='customer_delete'),
    path('customer/<int:customer_id>/change-status/', views.change_status, name='change_status'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('potential-customer/add/', views.potential_customer_add, name='potential_customer_add'),
    path('category/add/', views.category_add, name='category_add'),
] 