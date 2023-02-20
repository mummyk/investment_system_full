from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

# Create your models here.


class Notification(models.Model):
    user = models.ForeignKey(User, verbose_name=_(
        "User"), on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    title = models.CharField(_("Title"), max_length=50)
    message = models.TextField(_("message"))

    def __str__(self):
        return self.user.email
