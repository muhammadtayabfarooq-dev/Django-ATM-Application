from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .forms import AccountCreateForm, AmountForm, SignUpForm, TransferForm
from .models import Account, Transaction


class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Account created and logged in.")
        return response


@login_required
def dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    recent_transactions = Transaction.objects.filter(account__user=request.user)[:10]
    account_form = AccountCreateForm()
    return render(
        request,
        "atm/dashboard.html",
        {
            "accounts": accounts,
            "recent_transactions": recent_transactions,
            "account_form": account_form,
        },
    )


@login_required
def create_account(request):
    if request.method != "POST":
        return redirect("dashboard")
    form = AccountCreateForm(request.POST)
    if form.is_valid():
        account = form.save(commit=False)
        account.user = request.user
        account.save()
        messages.success(request, "Account created.")
    else:
        messages.error(request, "Could not create account.")
    return redirect("dashboard")


@login_required
def account_detail(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    deposit_form = AmountForm(prefix="deposit")
    withdraw_form = AmountForm(prefix="withdraw")
    transfer_form = TransferForm(prefix="transfer", user=request.user)
    transfer_form.fields["destination"].queryset = Account.objects.filter(user=request.user).exclude(pk=account.pk)
    transactions = account.transactions.all()[:20]
    return render(
        request,
        "atm/account_detail.html",
        {
            "account": account,
            "deposit_form": deposit_form,
            "withdraw_form": withdraw_form,
            "transfer_form": transfer_form,
            "transactions": transactions,
        },
    )


@login_required
def deposit(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    form = AmountForm(request.POST, prefix="deposit")
    if form.is_valid():
        try:
            account.deposit(form.cleaned_data["amount"], note=form.cleaned_data.get("note", ""))
            messages.success(request, "Deposit successful.")
        except ValueError as exc:
            messages.error(request, str(exc))
    else:
        messages.error(request, "Invalid deposit data.")
    return redirect("account_detail", pk=pk)


@login_required
def withdraw(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    form = AmountForm(request.POST, prefix="withdraw")
    if form.is_valid():
        try:
            account.withdraw(form.cleaned_data["amount"], note=form.cleaned_data.get("note", ""))
            messages.success(request, "Withdrawal successful.")
        except ValueError as exc:
            messages.error(request, str(exc))
    else:
        messages.error(request, "Invalid withdrawal data.")
    return redirect("account_detail", pk=pk)


@login_required
def transfer(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    form = TransferForm(request.POST, prefix="transfer", user=request.user)
    form.fields["destination"].queryset = Account.objects.filter(user=request.user).exclude(pk=account.pk)
    if form.is_valid():
        destination = form.cleaned_data["destination"]
        try:
            account.transfer_to(destination, amount=form.cleaned_data["amount"], note=form.cleaned_data.get("note", ""))
            messages.success(request, "Transfer completed.")
        except ValueError as exc:
            messages.error(request, str(exc))
    else:
        messages.error(request, "Invalid transfer data.")
    return redirect("account_detail", pk=pk)
