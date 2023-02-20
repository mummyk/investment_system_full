from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class ContactModel(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, null=True)
    phone_number = models.IntegerField(_("Phone number"))
    subject = models.CharField(max_length=100)
    message = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Agreement(models.Model):
    policy = models.TextField(null=True, blank=True)
    terms = models.TextField(null=True, blank=True)
    How_it_works = models.TextField(null=True, blank=True)
    disclaimer = models.TextField(null=True, blank=True)


class Blog(models.Model):
    created = models.DateTimeField(
        _("Created"), auto_now_add=True)
    title = models.CharField(_("Title"), max_length=100)
    content = models.TextField(_("Content"))
    tag = models.CharField(_("Tags"), max_length=50)
    category = models.CharField(_("Category"), max_length=50)

    def __str__(self):
        return self.title


class Tags(models.Model):
    created = models.DateTimeField(
        _("Created"), auto_now_add=True)
    tag = models.CharField(_("Tags"), max_length=50)

    def __str__(self):
        return self.tag


class Category(models.Model):
    created = models.DateTimeField(
        _("Created"), auto_now_add=True)
    category = models.CharField(_("Category"), max_length=50)

    def __str__(self):
        return self.category
