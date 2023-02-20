from django import forms
from .models import ContactModel

# contact form


class ContactForm(forms.ModelForm):
    full_name = forms.CharField(required=True, label="Full Name:", widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': "cname", 'placeholder': 'Your full name'}))
    email = forms.EmailField(required=True, label="Your Email:", widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': "cemail", 'placeholder': 'Your email'}))
    phone_number = forms.IntegerField(required=True, label="Phone Number:", widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': "cnumber", 'placeholder': 'Your phone number'}))
    subject = forms.CharField(required=True, label="Subject:", widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': "csubject", 'placeholder': 'message subject'}))
    message = forms.CharField(required=True, label="Message:", widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': "cmessa", 'placeholder': 'Your message'}))

    class Meta:
        model = ContactModel
        fields = ['full_name', 'email', 'phone_number', 'subject', 'message']


""" message = forms.CharField(required=True, label="Message:", widget=forms.Textarea(
    attrs={'class': 'title flex-1 w-full px-4 py-3 bg-gray-200 rounded-xl', 'placeholder': 'Your message'}))
 """
