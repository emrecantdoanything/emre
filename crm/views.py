from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import Customer, PotentialCustomer, Category
from .serializers import CustomerSerializer
from .forms import CustomerForm, PotentialCustomerForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta

# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    potential_customers = PotentialCustomer.objects.all()
    
    # Arama
    search_query = request.GET.get('search', '')
    if search_query:
        customers = customers.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
        potential_customers = potential_customers.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # Filtreleme
    status_filter = request.GET.get('status', '')
    if status_filter:
        customers = customers.filter(status=status_filter)
    
    category_filter = request.GET.get('category', '')
    if category_filter:
        customers = customers.filter(category_id=category_filter)
    
    # Sıralama
    sort_by = request.GET.get('sort', '-created_at')
    customers = customers.order_by(sort_by)
    potential_customers = potential_customers.order_by('-created_at')
    
    # Sayfalama
    page = request.GET.get('page', 1)
    paginator = Paginator(customers, 10)
    customers = paginator.get_page(page)
    
    context = {
        'customers': customers,
        'potential_customers': potential_customers,
        'categories': Category.objects.all(),
        'status_choices': Customer.STATUS_CHOICES,
    }
    return render(request, 'crm/customer_list.html', context)

@login_required
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    context = {
        'customer': customer,
        'status_choices': Customer.STATUS_CHOICES,
    }
    return render(request, 'crm/customer_detail.html', context)

@login_required
def customer_add(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, 'Müşteri başarıyla eklendi.')
            return redirect('crm:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()
    
    context = {
        'form': form,
        'title': 'Yeni Müşteri Ekle',
    }
    return render(request, 'crm/customer_form.html', context)

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            messages.success(request, 'Müşteri başarıyla güncellendi.')
            return redirect('crm:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    
    context = {
        'form': form,
        'customer': customer,
        'title': 'Müşteri Düzenle',
    }
    return render(request, 'crm/customer_form.html', context)

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Müşteri başarıyla silindi.')
        return redirect('crm:customer_list')
    
    context = {
        'customer': customer,
        'title': 'Müşteri Sil',
    }
    return render(request, 'crm/customer_confirm_delete.html', context)

@login_required
def change_status(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Customer.STATUS_CHOICES):
            customer.status = new_status
            customer.save()
            messages.success(request, f'Müşteri durumu başarıyla güncellendi: {customer.get_status_display()}')
        else:
            messages.error(request, 'Geçersiz durum seçimi!')
    return redirect('crm:customer_detail', customer_id=customer_id)

@login_required
def calendar_view(request):
    # Takvim görünümü için müşterileri al
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    
    customers = Customer.objects.all()
    
    if start_date and end_date:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        customers = customers.filter(created_at__range=(start, end))
    
    events = []
    for customer in customers:
        events.append({
            'id': customer.id,
            'title': customer.name,
            'start': customer.created_at.isoformat(),
            'end': (customer.created_at + timedelta(hours=1)).isoformat(),
            'url': f'/crm/customer/{customer.id}/',
            'backgroundColor': '#3788d8' if customer.status == 'potential' else '#28a745',
        })
    
    return JsonResponse(events, safe=False)

@login_required
def potential_customer_add(request):
    if request.method == 'POST':
        form = PotentialCustomerForm(request.POST)
        if form.is_valid():
            potential = form.save()
            messages.success(request, 'Potansiyel müşteri başarıyla eklendi.')
            return redirect('crm:customer_list')
    else:
        form = PotentialCustomerForm()
    
    context = {
        'form': form,
        'title': 'Yeni Potansiyel Müşteri Ekle',
    }
    return render(request, 'crm/potential_customer_form.html', context)

@login_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, 'Kategori başarıyla eklendi.')
            return redirect('crm:customer_list')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'title': 'Yeni Kategori Ekle',
    }
    return render(request, 'crm/category_form.html', context)
