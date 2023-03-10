# Generated by Django 4.1.6 on 2023-02-20 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='Daily percentage')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
        ),
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus', models.CharField(choices=[('welcome_bonus', 'Welcome'), ('trading_bonus', 'Trading'), ('special_bonus', 'Special'), ('Deposit_bonus', 'Deposit')], max_length=50, verbose_name='Bonus Type')),
                ('bonuses', models.FloatField(verbose_name='User bonus')),
                ('bonus_type', models.CharField(choices=[('percentage', 'Percentage'), ('amount', 'Amount')], max_length=10, verbose_name='Bonus value')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
