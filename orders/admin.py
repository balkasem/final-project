from django.contrib import admin

# Register your models here.
from .models import MenuItem, Order

admin.site.register(MenuItem)
admin.site.register(Order)
