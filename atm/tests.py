from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Account, Transaction

User = get_user_model()


class AccountModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass1234")
        self.account = Account.objects.create(user=self.user, name="Primary")

    def test_deposit_creates_transaction(self):
        self.account.deposit(Decimal("50.00"))
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("50.00"))
        self.assertEqual(self.account.transactions.count(), 1)

    def test_withdraw_validation(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(Decimal("10.00"))
        self.account.deposit(Decimal("20.00"))
        self.account.withdraw(Decimal("5.00"))
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("15.00"))

    def test_transfer_between_accounts(self):
        destination = Account.objects.create(user=self.user, name="Savings")
        self.account.deposit(Decimal("40.00"))
        self.account.transfer_to(destination, Decimal("15.00"))
        self.account.refresh_from_db()
        destination.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("25.00"))
        self.assertEqual(destination.balance, Decimal("15.00"))
        self.assertEqual(Transaction.objects.filter(account=self.account).count(), 2)
        self.assertEqual(Transaction.objects.filter(account=destination).count(), 1)


class DashboardViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", password="pass1234")
        self.client.login(username="bob", password="pass1234")

    def test_create_account_flow(self):
        response = self.client.post(reverse("create_account"), {"name": "Wallet"})
        self.assertEqual(response.status_code, 302)
        account = Account.objects.get(user=self.user)
        self.assertEqual(account.name, "Wallet")

    def test_deposit_view(self):
        account = Account.objects.create(user=self.user, name="Wallet")
        url = reverse("deposit", args=[account.pk])
        response = self.client.post(url, {"deposit-amount": "30.00", "deposit-note": "Cash"}, follow=True)
        self.assertEqual(response.status_code, 200)
        account.refresh_from_db()
        self.assertEqual(account.balance, Decimal("30.00"))
