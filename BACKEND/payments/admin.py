from django.contrib import admin
from .models import Deposit, Withdrawal, Wallet

# Register your models here.
admin.site.register(Deposit)
admin.site.register(Withdrawal)
admin.site.register(Wallet)
