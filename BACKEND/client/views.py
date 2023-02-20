from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress
from django.conf import settings
from .models import UserInfoModel
from referrals.models import ReferralModel
from .forms import ClientInfoForm

# Create your views here.

# The client profile


@login_required
def profiles(request):
    referral_code = ''
    try:
        referral_code = ReferralModel.objects.all()
        referral_code = referral_code.get(user=request.user).code
        referral_code = f'{settings.ALLOWED_HOSTS[0]}/{referral_code}'

        # get email verified
        if EmailAddress.objects.filter(user=request.user, verified=True).exists():
            verified = True
        else:
            verified = False
    except:
        messages.info(request, 'You have no referral code')
    profile = UserInfoModel.objects.filter(user=request.user)
    if profile.exists():
        context = {'title': 'Profile', 'profile': profile,
                   'referral_code': referral_code, 'verified': verified, }
    else:
        return redirect('/client/create_profile')

    return render(request, 'client/profile_display.html', context)


@login_required
def create_profile(request):
    profile_form = ClientInfoForm(
        request.POST or None)
    # profile_form = ClientInfoForm(
    # request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile creation successful')
            return redirect(to='/dashboard')
    else:
        messages.error(request, 'Profile creation unsuccessful')
        profile_form = ClientInfoForm(
            request.POST or None, request.FILES or None)

    context = {'title': 'Create Profile', 'form': profile_form,
               'prof': profiles}
    return render(request, 'client/create_profile.html', context)


@ login_required
def edit(request):

    if request.method == 'POST':
        profile_form = ClientInfoForm(
            request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='/client/profiles')
    else:
        profile_form = ClientInfoForm(instance=request.user.profile)

    context = {'title': 'Edit', 'form': profile_form,
               'prof': profiles}
    return render(request, 'client/edit_profile.html', context)
