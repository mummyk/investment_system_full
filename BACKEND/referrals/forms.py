from django import forms

from .models import Ref_bonus_withdrawal


class ReferralForm(forms.ModelForm):
    amount = forms.FloatField(required=True, label="", widget=forms.TextInput(
        attrs={'class': 'title flex-1 w-full p-4  bg-gray-200 rounded-xl', 'placeholder': 'Enter amount'}))

    class Meta:
        model = Ref_bonus_withdrawal
        fields = ['amount']
