from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    STATUS_CHOICES = [
        ('potential', 'Potansiyel'),
        ('contacted', 'İletişime Geçildi'),
        ('responded', 'Dönüş Alındı'),
        ('converted', 'Müşteriye Dönüştü'),
        ('lost', 'Kaybedildi'),
    ]

    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='potential')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Müşteri'
        verbose_name_plural = 'Müşteriler'

class PotentialCustomer(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Potansiyel Müşteri'
        verbose_name_plural = 'Potansiyel Müşteriler'

    def convert_to_customer(self):
        customer = Customer.objects.create(
            name=self.name,
            website=self.website,
            instagram=self.instagram,
            email=self.email,
            phone=self.phone,
            notes=self.notes
        )
        self.delete()
        return customer

class Communication(models.Model):
    CONTACT_METHODS = [
        ('meeting', 'Toplantı'),
        ('call', 'Telefon Görüşmesi'),
        ('email', 'E-posta'),
        ('whatsapp', 'WhatsApp'),
        ('instagram', 'Instagram'),
        ('other', 'Diğer'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='communications')
    contact_method = models.CharField(max_length=20, choices=CONTACT_METHODS)
    contact_date = models.DateTimeField()
    response_received = models.BooleanField(default=False)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name} - {self.get_contact_method_display()} - {self.contact_date.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = 'İletişim'
        verbose_name_plural = 'İletişimler'
        ordering = ['-contact_date']

class Reminder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    reminder_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.customer.name}"

    class Meta:
        verbose_name = 'Hatırlatma'
        verbose_name_plural = 'Hatırlatmalar'
        ordering = ['-reminder_date']
