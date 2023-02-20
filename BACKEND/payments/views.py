
import requests
import urllib.request
# Data Source
from yahoofinancials import YahooFinancials as yf
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from investments.views import get_balance
from investments.models import Profit
from referrals.models import ReferralModel
from .models import Wallet, Deposit, Withdrawal
from .forms import DepositForm, WithdrawalForm
from django.db.models import Sum
from django.contrib import messages

# Create your views here.


@login_required
def transactions(request):
    # Get all deposit, withdraws and profit
    balance = 0.0

    if Deposit.objects.filter(user=request.user).exists() or Withdrawal.objects.filter(user=request.user).exists():
        deposit = Deposit.objects.all()
        withdraw = Withdrawal.objects.all()

        # history
        deposit_history = deposit.filter(user=request.user)
        withdraw_history = withdraw.filter(user=request.user)

        # total of all deposits and withdraw
        total_deposit = deposit.filter(
            user=request.user).aggregate(Sum('amount'))
        total_withdraw = withdraw.filter(
            user=request.user).aggregate(Sum('amount'))

        # get total deposit that are not pending
        total_actual_deposit = deposit.filter(
            user=request.user, pending=False).aggregate(Sum('amount'))

        # total pending depoist and withdrawal
        total_deposit_pending = deposit.filter(
            user=request.user, pending=True)
        total_withdraw_pending = withdraw.filter(
            user=request.user, pending=True)

        # total rejected deposit and withdraw
        total_deposit_rejected = deposit.filter(
            user=request.user, rejected=True)
        total_withdraw_rejected = withdraw.filter(
            user=request.user, rejected=True)

        # aggregate for all pending, rejected and actual
        # pending
        total_deposit_pending_arg = total_deposit_pending.aggregate(
            Sum('amount'))
        total_withdraw_pending_arg = total_withdraw_pending.aggregate(
            Sum('amount'))

        # rejected
        total_deposit_rejected_arg = total_deposit_rejected.aggregate(
            Sum('amount'))
        total_withdraw_rejected_arg = total_withdraw_rejected.aggregate(
            Sum('amount'))

        total_transactions = {
            key: abs(total_deposit[key]+total_withdraw[key]) for key in total_deposit}
    else:
        total_actual_deposit = 0.00
        total_deposit = 0.00
        total_deposit_pending = 0.00
        total_transactions = 0.00
        deposit_history = 0.00
        withdraw_history = 0.00
        user_total_profit = 0.00
        profit = 0.00
        total_withdraw = 0.00

     # Your total profit
    if Profit.objects.all().exists():
        first_deposit = deposit.filter(
            user=request.user, pending=False).first()
        profit = Profit.objects.all()
        first_day = first_deposit.created
        profits = profit.filter(
            created__gte=first_day)
        # add the profit from the day of the first deposit
        user_total_profit = profit.filter(
            created__gte=first_day).aggregate(Sum('amount'))

    context = {'title': 'Transactions', 'deposit': total_deposit['amount__sum'], 'balance': total_transactions['amount__sum'],
               'withdraw': total_withdraw['amount__sum'], 'total_profit': user_total_profit['amount__sum'], 'profit': profits,
               'deposits': deposit_history, 'withdraws': withdraw_history, 'transactions': True
               }

    return render(request, 'dashboard_pay.html', context)


@login_required
def deposit_transaction(request):
    btcRate = 0
    ethRate = 0
    investment_minimum = 1000
    investment_maximum = 10000000000
    btc = ''
    eth = ''
    usdt = ''
    # Get all deposit, withdraws and profit
    if Deposit.objects.filter(user=request.user).exists():
        deposit = Deposit.objects.all()

        # history
        deposit_history = deposit.filter(user=request.user)

        # total of all deposits and withdraw
        total_deposit = deposit.filter(
            user=request.user).aggregate(Sum('amount'))

        # get total deposit that are not pending
        total_actual_deposit = deposit.filter(
            user=request.user, pending=False).aggregate(Sum('amount'))

        # total pending depoist and withdrawal
        total_deposit_pending = deposit.filter(
            user=request.user, pending=True)

        # total rejected deposit and withdraw
        total_deposit_rejected = deposit.filter(
            user=request.user, rejected=True)

        # aggregate for all pending, rejected and actual
        # pending
        total_deposit_pending_arg = total_deposit_pending.aggregate(
            Sum('amount'))

        # rejected
        total_deposit_rejected_arg = total_deposit_rejected.aggregate(
            Sum('amount'))

    else:
        total_actual_deposit = 0.00
        total_deposit = 0.00
        total_deposit_rejected = 0.00
        total_deposit_pending = 0.00
        total_deposit_rejected_arg = 0.00
        total_deposit_pending_arg = 0.00
        deposit_history = 0.00

    if connect():
        try:
            cryptocurrencies = ['BTC-USD', 'ETH-USD']
            crypto = yf(cryptocurrencies)
            yc = crypto.get_current_price()
            btcRate = yc['BTC-USD']+(yc['BTC-USD']*0.01)
            ethRate = yc['ETH-USD']+(yc['ETH-USD']*0.1)
        except:
            pass
    else:
        messages.error(request, 'You are offline')

    wallet = Wallet.objects.all()

    if ReferralModel.objects.all().exists:
        ref = ReferralModel.objects.all()
        if ref.filter(user=request.user).exists():
            ref_user = ref.get(user=request.user)
            if wallet.filter(name=ref_user.referred).exists():
                user_wallet = wallet.get(name=ref_user.referred)
            else:
                user_wallet = wallet.get(name='main')
            addresses = {'bitcoin': user_wallet.bitcoin,
                         'etherium': user_wallet.etherium,
                         'usdt': user_wallet.usdt}
            btc = addresses['bitcoin']
            eth = addresses['etherium']
            usdt = addresses['usdt']
        else:
            user_wallet = wallet.get(name='main')
            addresses = {'bitcoin': user_wallet.bitcoin,
                         'etherium': user_wallet.etherium,
                         'usdt': user_wallet.usdt}
            btc = addresses['bitcoin']
            eth = addresses['etherium']
            usdt = addresses['usdt']

        messages.info(request, 'Wallet generated on main-net')

    else:

        messages.error(request, 'No wallet available at the moment')

    form = DepositForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            amount = float(form['amount'].value())
            if amount < investment_minimum-0.01 or amount > investment_maximum:
                messages.error(
                    request, f'Amount below minimum amount of {investment_minimum} or above {investment_maximum}')
            else:
                deposits = form.save(commit=False)
                deposits.wallet = addresses
                deposits.user = request.user
                deposits.save()
                messages.success(request, 'Deposit successful and pending')
                return redirect(to='/deposits')
        else:
            messages.error(request, 'Invalid deposit')

    context = {'title': 'deposit', 'deposits': True, 'data': deposit_history, 'form': form, 'total_deposit': total_actual_deposit['amount__sum'],
               'total_pending': total_deposit_pending_arg['amount__sum'], 'total_rejected': total_deposit_rejected_arg['amount__sum'],
               'btcRate': btcRate, 'ethRate': ethRate, 'btc_address': btc, 'ethereum': eth,
               'usdt_address': usdt
               }
    return render(request, 'deposits.html', context)


@login_required
def withdraw_transaction(request):
    btcRate = 0.00
    ethRate = 0.00

    # Get all deposit, withdraws and profit
    if Withdrawal.objects.filter(user=request.user).exists():
        deposit = Deposit.objects.all()
        withdraw = Withdrawal.objects.all()

        # history
        deposit_history = deposit.filter(user=request.user)
        withdraw_history = withdraw.filter(user=request.user)

        # total of all deposits and withdraw
        total_deposit = deposit.filter(
            user=request.user).aggregate(Sum('amount'))
        total_withdraw = withdraw.filter(
            user=request.user).aggregate(Sum('amount'))

        # get total deposit and withdraws that are not pending
        total_actual_deposit = deposit.filter(
            user=request.user, pending=False).aggregate(Sum('amount'))
        total_actual_withdraw = withdraw.filter(
            user=request.user, pending=False).aggregate(Sum('amount'))

        # total pending depoist and withdrawal
        total_deposit_pending = deposit.filter(
            user=request.user, pending=True)
        total_withdraw_pending = withdraw.filter(
            user=request.user, pending=True)

        # total rejected deposit and withdraw
        total_deposit_rejected = deposit.filter(
            user=request.user, rejected=True)
        total_withdraw_rejected = withdraw.filter(
            user=request.user, rejected=True)

        # aggregate for all pending, rejected and actual
        # pending
        total_deposit_pending_arg = total_deposit_pending.aggregate(
            Sum('amount'))
        total_withdraw_pending_arg = total_withdraw_pending.aggregate(
            Sum('amount'))

        # rejected
        total_deposit_rejected_arg = total_deposit_rejected.aggregate(
            Sum('amount'))
        total_withdraw_rejected_arg = total_withdraw_rejected.aggregate(
            Sum('amount'))

    else:
        total_actual_deposit = 0.00
        total_deposit = 0.00
        total_deposit_pending = 0.00
        total_transactions = 0.00
        deposit_history = 0.00
        withdraw_history = 0.00
        user_total_profit = 0.00
        profit = 0.00
        total_withdraw = 0.00

     # Your total profit
    if Profit.objects.all().exists():
        first_deposit = deposit.filter(
            user=request.user, pending=False).first()
        profit = Profit.objects.all()
        first_day = first_deposit.created
        # add the profit from the day of the first deposit
        user_total_profit = profit.filter(
            created__gte=first_day).aggregate(Sum('amount'))

    # get total available profit and total actual deposit
    available_balance = total_actual_deposit['amount__sum'] + \
        (total_actual_deposit['amount__sum'] *
         (user_total_profit['amount__sum']/100))

    # Crypto rate
    if connect():
        try:
            cryptocurrencies = ['BTC-USD', 'ETH-USD']
            crypto = yf(cryptocurrencies)
            yc = crypto.get_current_price()
            btcRate = yc['BTC-USD']+(yc['BTC-USD']*0.01)
            ethRate = yc['ETH-USD']+(yc['ETH-USD']*0.1)
        except:
            pass
    else:
        messages.error(request, 'You are offline')

    # withdrawal form
    form = WithdrawalForm(request.POST or None)

    context = {'title': 'Withdraw', 'withdraws': True, 'data': withdraw_history, "balance": get_balance(request),
               'total_withdraw': total_withdraw['amount__sum'], 'actual_withdraw': total_actual_withdraw['amount__sum'],
               'total_pending': total_withdraw_pending_arg['amount__sum'], 'total_rejected': total_withdraw_rejected_arg['amount__sum'],
               'form': form, 'btcRate': btcRate, 'ethRate': ethRate
               }

    return render(request, 'withdraw.html', context)


@login_required
def withdrawForm(request):
    # get available balance

    form = WithdrawalForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            balance = get_balance(request)
            amount = float(form['amount'].value())
            if amount <= balance:
                withdraw = form.save(commit=False)
                withdraw.user = request.user
                withdraw.save()
                megs = messages.success(
                    request, 'Withdraw successful and pending')
                return redirect('/withdraws', megs)
            else:
                megs = messages.success(
                    request, 'Insufficient funds, Top_up is required')
                return redirect('/deposit', megs)
        else:
            meg = messages.error(request, 'You have low balance, Top up')
            return redirect('/deposits', meg)


def connect():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False
