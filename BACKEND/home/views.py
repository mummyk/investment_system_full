from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

# Create your views here.


def home(request):
    context = {'title': 'Trusty Trade', 'home': True}
    return render(request, 'home/home.html', context)


def contactUs(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            messages.success(request, "Message sent")
            return redirect('/contact')
        else:
            message = messages.error(request, "Message sent unsuccessfully")
    context = {'title': 'Contact Us', 'form': form}
    return render(request, 'home/contact.html', context)


def aboutUs(request):
    context = {'title': 'About Us'}
    return render(request, 'home/about.html', context)


def faqs(request):
    context = {'title': 'FAQs'}
    return render(request, 'home/faq.html', context)


def blog(request):
    context = {'title': 'Blog'}
    return render(request, 'home/blog.html', context)
