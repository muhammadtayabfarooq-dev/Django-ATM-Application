from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Account

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class AccountCreateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("name",)


class AmountForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)
    note = forms.CharField(max_length=255, required=False)


class TransferForm(AmountForm):
    destination = forms.ModelChoiceField(queryset=Account.objects.none())

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["destination"].queryset = Account.objects.filter(user=user)
