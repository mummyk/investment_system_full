from django.shortcuts import render, redirect
from .models import ReferralModel, Ref_bonus_withdrawal
from payments.models import Deposit, Withdrawal
from .forms import ReferralForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum

# Create your views here.


@login_required
def ref_dashboard(request):
    cod = []
    total_ref = []
    amount = 0
    person = ''
    if Deposit.objects.all().exists():
        deposit = Deposit.objects.all()
        ref = ReferralModel.objects.all()
        # to get the users who referred them
        for r in ref:
            cod.append(r)

        # compare if the referred user is equal to the current user
        my_recs = []
        for r in cod:
            if request.user == r.referred:
                my_recs.append(r.user)
        total_ref = len(my_recs)

    # get the deposit of the referred user
        ref_deposits = ref_deposit(deposit, my_recs)
        person = ref_deposits['person']
        amount = ref_deposits['amount']
    # get the available ref balance
        ref_withdraws = ref_withdraw(Withdrawal, my_recs)
        ref_bonus_withdraw = ref_bonus_withdraws(request)
        total_ref_balance = (amount+ref_withdraws)-ref_bonus_withdraw

    # Verify the amount to withdraw withe the available balance
        form = ReferralForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid:
                amount = float(form['amount'].value())
                if amount >= total_ref_balance:
                    form.add_error(
                        'amount', f'Amount should not be more that {total_ref_balance}')
                else:
                    ref_form = form.save(commit=False)
                    ref_form.user = request.user
                    ref_form.save()

    else:
        messages.info(request,  'No Referral bonus yet')

    context = context = {'title': 'Referral Dashboard',
                         'my_record': my_recs,  'person': person,
                         'Total_user_ref': amount, 'total_ref': total_ref, 'form': form,
                         }
    return render(request, 'referrals_dashboard.html', context)


@login_required
def ref_view(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        if ReferralModel.objects.all().exists():
            referrals = ReferralModel.objects.all()
            referral = referrals.get(code=code)
            request.session['ref_profile'] = referral.user.id
            redirect('/accounts/signup')
        else:
            messages.info(request, 'You do not have a referral code')
    except:
        pass

    context = {'title': 'Referrals'}
    return render(request, 'ref_views.html', context)


# TODO track confirmed deposits and link then to the referred_by user and assign 5%
# TODO track confirmed withdrawals and link then to thr referred_by user and assign 5%
# TODO track the withdrawn referred bonus and save to database


# allowing referral withdraw
def ref_withdraw(db, val):
    available_ref_balance = 0.00
    amount = 0.00
    for i in val:
        if db.objects.all().exists():
            db_val = db.objects.all()
            if db_val.filter(user=i):
                j = db_val.filter(user=i)
                if j.filter(pending=False):
                    person = i
                    amount = j.filter(user=i, pending=False).aggregate(
                        Sum('amount'))
                    amount = amount['amount__sum']
            # All confirmed withdraw
            available_ref_balance = amount * 0.05
            # get all referred bonus amount

    return available_ref_balance


def ref_bonus_withdraws(request):
    if Ref_bonus_withdrawal.objects.all().exists():
        ref_bonus_withdraw = Ref_bonus_withdrawal.objects.all()
        ref_bonus_withdraw = ref_bonus_withdraw.filter(
            user=request.user, withdrawal_confirmation=False).aggregate(
            Sum('amount'))
        ref_bonus_withdraw = ref_bonus_withdraw['amount__sum']
    return ref_bonus_withdraw


# referral balance
def ref_deposit(db, val):
    for i in val:
        if db.filter(user=i):
            j = db.filter(user=i)
            if j.get(pending=False):
                person = i
                amount = sum(j.filter(
                    user=i).values_list('amount', flat=True))
                # 5% for the deposit
                amount = amount * 0.05
                amount = round(amount, 2)
    return {'amount': amount, 'person': person}


# referral number of downlink
def downlink(number_of_downlink=3):
    if ReferralModel.object.all().exists():
        ref = ReferralModel.objects.all()
        ref_downlink = number_of_downlink
        return ref_downlink
    