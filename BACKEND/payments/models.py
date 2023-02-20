from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
import re
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib import admin
# Create your models here.


class Deposit(models.Model):
    user = models.ForeignKey(User, verbose_name=_(
        "Users_info"), on_delete=models.CASCADE)
    wallet = models.CharField(_("Wallet ID"), max_length=200)
    amount = models.FloatField(_("Amount"))
    pending = models.BooleanField(_("Pending Transactions"), default=True)
    rejected = models.BooleanField(
        _("Rejected/Canceled Transactions"), default=False)
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    def __str__(self):
        return self.user.email + '--' + self.created.strftime('%A')


class Withdrawal(models.Model):
    user = models.ForeignKey(User, verbose_name=_(
        "Users_info"), on_delete=models.CASCADE)
    wallet = models.CharField(_("Wallet ID"), max_length=200)
    amount = models.FloatField(_("Amount"))
    pending = models.BooleanField(_("Pending Transactions"), default=True)
    rejected = models.BooleanField(
        _("Rejected/Canceled Transactions"), default=False)
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    def __str__(self):
        return self.user.email + '--' + self.created.strftime('%A')

    def save(self, *args, **kwargs):

        # For all possible BTC & ETH wallet configuration
        BTC_ADDRESS_MATCH = '([13]{1}[a-km-zA-HJ-NP-Z1-9]{27,34}|bc1[a-z0-9]{39,59})'
        ETH_ADDRESS_MATCH = '0x[a-fA-F0-9]{40}'

        # matching btc address
        btc = re.match(BTC_ADDRESS_MATCH, self.wallet)
        eth = re.match(ETH_ADDRESS_MATCH, self.wallet)

        return super().save(*args, **kwargs)


class Wallet(models.Model):
    name = models.CharField(_("Wallet name"), max_length=50)
    bitcoin = models.CharField(_("Bitcoin Wallet"), max_length=100, blank=True)
    etherium = models.CharField(
        _("Etherium Wallet"), max_length=100, blank=True)
    usdt = models.CharField(_("USDT Wallet"), max_length=100, blank=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_("updated"),  auto_now=True, blank=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Wallet)
def valid_wallet(sender, instance, *args, **kwargs):
    # For all possible BTC & ETH wallet configuration
    BTC_ADDRESS_MATCH = '([13]{1}[a-km-zA-HJ-NP-Z1-9]{27,34}|bc1[a-z0-9]{39,59})'
    ETH_ADDRESS_MATCH = '0x[a-fA-F0-9]{40}'

    # matching btc address
    if re.match(BTC_ADDRESS_MATCH, instance.bitcoin) is None or re.match(ETH_ADDRESS_MATCH, instance.etherium) is None:
        raise Exception('Address does not match')


""" @admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('name', 'bitcoin', 'etherium', 'usdt')

    def save_model(self, request, obj, form, change):
        try
        return super().save_model(request, obj, form, change) """
