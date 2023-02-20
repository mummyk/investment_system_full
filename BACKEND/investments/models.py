from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
from datetime import datetime, timedelta


class Bonus(models.Model):
    BONUS_TYPE = ((_('welcome_bonus'), 'Welcome'),
                  (_('trading_bonus'), 'Trading'),
                  (_('special_bonus'), 'Special'),
                  (_('Deposit_bonus'), 'Deposit'))

    VALUE = ((_('percentage'), 'Percentage'),
             (_('amount'), 'Amount'))

    user = models.ForeignKey(User, verbose_name=_(
        "User"), on_delete=models.CASCADE)
    bonus = models.CharField(
        _("Bonus Type"), max_length=50, choices=BONUS_TYPE)
    bonuses = models.FloatField(_("User bonus"))
    bonus_type = models.CharField(
        _("Bonus value"), max_length=10, choices=VALUE)
    created = models.DateTimeField(_('Created'), auto_now_add=True,)

    def __str__(self):
        return self.user.email
# calculate the bonus either % or absolute amount

    def get_bonus(self, amount):
        bonus = 0
        if self.bonus_type == 'percentage':
            bonus = amount * (self.bonuses/100)
        else:
            bonus = amount + self.bonuses
        return bonus


class Profit(models.Model):
    amount = models.FloatField(_("Daily percentage"))
    created = models.DateTimeField(_('Created'), auto_now_add=True,)

    def __str__(self):
        return self.created.strftime('%A')


"""  def save(self, *args, **kwargs):
        self.start = datetime.now()
        pack = Package.objects.all()
        pack = pack.get(name=self.packages)
        self.end = self.start+timedelta(pack.duration)
        return super().save(*args, **kwargs) """
