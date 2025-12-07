# Django ATM Application

A backend-focused Django application that simulates basic ATM operations. Users can sign up, create multiple accounts, deposit, withdraw, transfer between their own accounts, and review transaction history. The interface uses simple HTML/CSS to emphasize backend logic.

---

## Overview

* **User Authentication:** Signup, login, logout; redirects to dashboard after login.
* **Accounts:** Create personal accounts (e.g., Checking, Savings) with generated account numbers and running balances.
* **Money Actions:** Deposit, withdraw, transfer between accounts; balances updated atomically with validation.
* **Transactions:** Each action logs a transaction with type, amount, balance after the action, note/counterparty, and timestamp.
* **Dashboard:** Displays all accounts and recent transactions.
* **Account Detail:** View balance, recent transactions, and forms for deposit/withdraw/transfer.
* **Admin Panel (Optional):** Manage users, accounts, and transactions via Django admin.

---

## Technologies Used

* Python 3.9+
* Django 4.2
* SQLite (default, can be swapped for PostgreSQL/MySQL via `DATABASES` in `atm_project/settings.py`)
* HTML/CSS templates (no JavaScript build tools required)

---

## Project Structure (High-Level)

```
atm_project/
├── atm_project/settings.py       # Settings, templates/static config, login redirects
├── atm_project/urls.py           # Project URL routes (auth + atm app)
│
├── atm/
│   ├── models.py                 # Account + Transaction models and helpers
│   ├── views.py                  # Dashboard, account detail, deposit/withdraw/transfer, signup
│   ├── forms.py                  # Signup, account creation, amount/transfer forms
│   ├── urls.py                   # App URL routes
│   ├── admin.py                  # Admin registrations
│   └── tests.py                  # Model and view tests
│
├── templates/                     # Base layout, auth, dashboard, account detail
└── static/                        # Static files
```

---

## Getting Started (Windows, PowerShell)

### 1. Activate virtual environment

```
.\venv\Scripts\Activate.ps1
```

### 2. Apply migrations

```
python manage.py migrate
```

### 3. Run tests (optional)

```
python manage.py test
```

### 4. Start the development server

```
python manage.py runserver
```

Open the app in a browser:

```
http://127.0.0.1:8000/
```

---

## Usage

1. Sign up for an account.
2. Create one or more personal accounts from the dashboard.
3. Use the Deposit, Withdraw, and Transfer forms to manage funds. Transactions are logged automatically.
4. View recent activity on the dashboard or individual account pages.

---

## Admin Access (Optional)

### Create superuser

```
python manage.py createsuperuser
```

### Access admin panel

```
http://127.0.0.1:8000/admin/
```

---

## Common Django Commands

```
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
python manage.py test
python manage.py collectstatic
```

---

## Deployment Notes

* Set `DEBUG = False` and update `ALLOWED_HOSTS` in `atm_project/settings.py`.
* Configure `DATABASES` for your production database.
* Run `python manage.py collectstatic` before deployment and serve static files via a web server or CDN.
* Use a process manager (e.g., Gunicorn or Uvicorn behind Nginx) for production deployment.

---

## Data and Defaults

* Default database: SQLite (`db.sqlite3`).
* Account numbers are generated automatically.
* Each money action records a Transaction with a balance-after snapshot for auditability.

---

## Author

**Muhammad Tayab Farooq**
Email: **[muhammadtayabfarooq@gmail.com](mailto:muhammadtayabfarooq@gmail.com)**
Experience: **2 years with Python and Django**
