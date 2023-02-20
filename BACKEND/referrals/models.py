from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from .utils import generate_ref_code
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from client.models import UserInfoModel
from django.db.models.signals import post_save

# Create your models here.


class ReferralModel (models.Model):
    user = models.OneToOneField(User, verbose_name=_(
        "Account User"), on_delete=models.CASCADE)
    code = models.CharField(_("Referral Code"), max_length=50, blank=True)
    referred = models.ForeignKey(User, verbose_name=_(
        "Referred by"), related_name='referred_by', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(
        _("Created"),  auto_now_add=True)
    updated = models.DateTimeField(_("updated"),  auto_now=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        return super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def post_save_create_ref(sender, instance, created, *args, **kwargs):
    if created:
        ReferralModel.objects.create(user=instance)


@receiver(user_signed_up)
def after_user_signed_up(sender, request, user, **kwargs):
    profile_id = request.session.get('ref_profile')
    print('profile_id', profile_id)
    if profile_id is not None:
        referred_by_profile = ReferralModel.objects.get(id=profile_id)
        registered_user = user.id
        registered_profile = ReferralModel.objects.get(user=registered_user)
        registered_profile.referred = referred_by_profile.user
        registered_profile.save()
    else:
        pass


class Ref_bonus_withdrawal(models.Model):
    user = models.ForeignKey(User, verbose_name=_(
        "User"), on_delete=models.CASCADE)
    amount = models.FloatField(_("Ref withdrawal amount"), blank=True)
    withdrawal_confirmation = models.BooleanField(
        _("Confirmed withdraw"), default=True)
    created = models.DateTimeField(
        _("Created"),  auto_now_add=True)
    updated = models.DateTimeField(_("updated"),  auto_now=True)

    def __str__(self):
        return self.user.email
