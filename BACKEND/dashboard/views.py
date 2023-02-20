from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from investments.views import get_balance
from client.models import UserInfoModel
from payments.models import Deposit, Withdrawal
from investments.models import Bonus, Profit
from django.db.models import Sum
from datetime import datetime

# Create your views here.


@login_required
def dashboard(request):
    profiles = UserInfoModel.objects.all()
    balance = 0.0
    user_total_profit = 0.00

    # Get all deposit, withdraws and profit
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
        # todays profit
        today = timezone.now().date()
        daily_profit_percent = profit.filter(
            created__date=today)
        if daily_profit_percent.exists():
            daily_profit_percent = daily_profit_percent.aggregate(
                Sum('amount'))
            daily_profit_percent = daily_profit_percent['amount__sum']
            daily_profit = get_balance(
                request)*(daily_profit_percent/100)
        else:
            daily_profit_percent = 0
            daily_profit = 0

    # Your bonuses
    if Bonus.objects.filter(user=request.user).exists():
        bonus = Bonus.objects.all()
        bonus = bonus.get(user=request.user)
        bonus = bonus.get_bonus(balance)
    else:
        bonus = 0

    # chart data config
    labels = []
    data = []
    for p in profits:
        date = p.created
        day_of_week = date.strftime("%A")
        labels.append(day_of_week)
        data.append(p.amount)

    if profiles.exists():

        context = {'title': 'Dashboard',
                   'dashboard': True, 'deposit': total_deposit['amount__sum'], 'withdraw': total_withdraw['amount__sum'],
                   'balance': get_balance(request), 'bonus': bonus, 'daily_profit': daily_profit,
                   'total_profit': user_total_profit['amount__sum'], 'growth': daily_profit_percent, 'label': labels, 'data': data,
                   }
    else:
        return redirect('/create_profile')
    return render(request, 'dashboard.html', context)


def notification(request):
    messages.info(request, 'You have no notification')
    return redirect('/profiles')
