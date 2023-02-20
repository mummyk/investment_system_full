from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from payments.models import Deposit, Withdrawal
from .models import Profit, Bonus
from django.db.models import Sum
# Create your views here.


@ login_required
def invest(request):
    total_profit = 0.00
    today_profit = 0.00
    total_deposit = 0.00
    total_withdrawal = 0.00
    available_balance = 0.00
    user_total_profit = 0.00
    # get date of the first deposit
    if Deposit.objects.all().exists() or Withdrawal.objects.all().exists:
        deposit = Deposit.objects.all()
        deposit = deposit.filter(user=request.user, pending=False)
        withdraw = Withdrawal.objects.all()
        withdraw = withdraw.filter(user=request.user, pending=False)
        first_deposit = deposit.first()
        # get total deposit and withdraw
        total_deposit = deposit.aggregate(Sum('amount'))
        total_withdrawal = withdraw.aggregate(Sum('amount'))
        # get the available balance
        available_balance = {
            key: abs(total_deposit[key]-total_withdrawal[key]) for key in total_deposit}
        # profit from the day of deposit
        if Profit.objects.all().exists():
            profit = Profit.objects.all()
            first_day = first_deposit.created
            # add the profit from the day of the first deposit
            profits = profit.filter(created__gte=first_day)
            user_total_profit = profits.aggregate(Sum('amount'))
        available_balance_and_profit = available_balance['amount__sum'] * \
            (user_total_profit['amount__sum']/100)
        available_balance = available_balance['amount__sum'] + \
            available_balance_and_profit

    else:
        messages.error(request, "No deposit")

    context = {'title': 'Investment',
               'invests': True,

               }
    return render(request, 'invest.html', context)


def get_balance(request):
    total_profit = 0.00
    total_deposit = 0.00
    total_withdrawal = 0.00
    available_balance = 0.00
    user_total_profit = 0.00
    # get date of the first deposit
    if Deposit.objects.all().exists() or Withdrawal.objects.all().exists:
        deposit = Deposit.objects.all()
        deposit = deposit.filter(user=request.user, pending=False)
        withdraw = Withdrawal.objects.all()
        withdraw = withdraw.filter(user=request.user, pending=False)
        first_deposit = deposit.first()
        # get total deposit and withdraw
        total_deposit = deposit.aggregate(Sum('amount'))
        total_withdrawal = withdraw.aggregate(Sum('amount'))
        # get the available balance
        available_balance = {
            key: abs(total_deposit[key]-total_withdrawal[key]) for key in total_deposit}
        # profit from the day of deposit
        if Profit.objects.all().exists():
            profit = Profit.objects.all()
            first_day = first_deposit.created
            # add the profit from the day of the first deposit
            profits = profit.filter(created__gte=first_day)
            user_total_profit = profits.aggregate(Sum('amount'))
        available_balance_and_profit = available_balance['amount__sum'] * \
            (user_total_profit['amount__sum']/100)
        available_balance = available_balance['amount__sum'] + \
            available_balance_and_profit

    else:
        messages.error(request, "No deposit")

    return available_balance


def bonus_cat(request):
    # get bouns
    if Bonus.objects.all().exists():
        bonus = Bonus.objects.all()
        result = bonus.filter(user=request.user)
    return result
