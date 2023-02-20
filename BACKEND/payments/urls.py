from django.urls import path
from payments import views

urlpatterns = [
    path('deposits', views.deposit_transaction, name='deposits'),
    path('transactions', views.transactions, name='transactions'),
    path('withdraws', views.withdraw_transaction, name='withdraws'),
    path('withform', views.withdrawForm, name='withform'),
]
