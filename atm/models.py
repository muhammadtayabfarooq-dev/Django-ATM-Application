import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models, transaction as db_transaction
from django.utils import timezone

User = get_user_model()


def generate_account_number() -> str:
    """Generate a short pseudo-random account number."""
    return str(uuid.uuid4().int)[-10:]


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=100, default="Checking")
    account_number = models.CharField(max_length=20, unique=True, default=generate_account_number)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.name} ({self.account_number})"

    def deposit(self, amount: Decimal, note: str = ""):
        amount = Decimal(amount)
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        with db_transaction.atomic():
            locked = Account.objects.select_for_update().get(pk=self.pk)
            locked.balance = (locked.balance or Decimal("0")) + amount
            locked.save(update_fields=["balance"])
            Transaction.objects.create(
                account=locked,
                txn_type=Transaction.Type.DEPOSIT,
                amount=amount,
                balance_after=locked.balance,
                note=note,
            )
            self.balance = locked.balance
            return locked

    def withdraw(self, amount: Decimal, note: str = ""):
        amount = Decimal(amount)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        with db_transaction.atomic():
            locked = Account.objects.select_for_update().get(pk=self.pk)
            if locked.balance < amount:
                raise ValueError("Insufficient funds")
            locked.balance -= amount
            locked.save(update_fields=["balance"])
            Transaction.objects.create(
                account=locked,
                txn_type=Transaction.Type.WITHDRAWAL,
                amount=amount,
                balance_after=locked.balance,
                note=note,
            )
            self.balance = locked.balance
            return locked

    def transfer_to(self, destination: "Account", amount: Decimal, note: str = ""):
        if self.pk == destination.pk:
            raise ValueError("Cannot transfer to the same account")
        amount = Decimal(amount)
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        with db_transaction.atomic():
            source = Account.objects.select_for_update().get(pk=self.pk)
            dest = Account.objects.select_for_update().get(pk=destination.pk)
            if source.balance < amount:
                raise ValueError("Insufficient funds")
            source.balance -= amount
            dest.balance += amount
            source.save(update_fields=["balance"])
            dest.save(update_fields=["balance"])
            Transaction.objects.create(
                account=source,
                txn_type=Transaction.Type.TRANSFER_OUT,
                amount=amount,
                balance_after=source.balance,
                note=note or f"To {dest.account_number}",
                counterparty_account=dest.account_number,
            )
            Transaction.objects.create(
                account=dest,
                txn_type=Transaction.Type.TRANSFER_IN,
                amount=amount,
                balance_after=dest.balance,
                note=note or f"From {source.account_number}",
                counterparty_account=source.account_number,
            )
            self.balance = source.balance
            destination.balance = dest.balance
            return source, dest


class Transaction(models.Model):
    class Type(models.TextChoices):
        DEPOSIT = "deposit", "Deposit"
        WITHDRAWAL = "withdrawal", "Withdrawal"
        TRANSFER_IN = "transfer_in", "Transfer In"
        TRANSFER_OUT = "transfer_out", "Transfer Out"

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    txn_type = models.CharField(max_length=20, choices=Type.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    counterparty_account = models.CharField(max_length=20, blank=True)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at", "-id")

    def __str__(self) -> str:
        return f"{self.get_txn_type_display()} {self.amount} on {self.created_at:%Y-%m-%d}"
