from django.contrib import admin

from .models import Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "account_number", "balance", "created_at")
    search_fields = ("account_number", "user__username", "name")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "txn_type", "amount", "balance_after", "created_at")
    list_filter = ("txn_type", "created_at")
    search_fields = ("account__account_number", "note")
