from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("", views.dashboard, name="dashboard"),
    path("accounts/create/", views.create_account, name="create_account"),
    path("accounts/<int:pk>/", views.account_detail, name="account_detail"),
    path("accounts/<int:pk>/deposit/", views.deposit, name="deposit"),
    path("accounts/<int:pk>/withdraw/", views.withdraw, name="withdraw"),
    path("accounts/<int:pk>/transfer/", views.transfer, name="transfer"),
]
