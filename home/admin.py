from django.contrib import admin
from . models import Destination, Expense,Category
# Register your models here.
admin.site.register(Destination)
admin.site.register(Expense)
admin.site.register(Category)
