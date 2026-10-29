# Django Signals and Rectangle Assignment

This is a complete Django project demonstrating:
1. Django signals execute synchronously by default.
2. Django signal receivers run in the same thread as the caller by default.
3. A signal receiver invoked inside `transaction.atomic()` uses the same database transaction by default.
4. A `Rectangle` class that can be iterated over, yielding length first and width second.

## Requirements
- Python 3.9+
- pip

## Run in VS Code (Windows PowerShell)

Open this folder in VS Code, then run:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py test signals_demo -v 2
python manage.py demonstrate_signals
python manage.py demonstrate_rectangle
```

If PowerShell blocks virtual environment activation, run this for the current terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## What to expect
- The tests verify that the receiver runs before the caller continues.
- Thread IDs match for the caller and receiver.
- A receiver's database write is rolled back when the surrounding `atomic()` transaction is rolled back.
- Rectangle iteration prints:
  `{'length': 10}`
  `{'width': 5}`


Django signals do not automatically create a transaction. In autocommit mode, a receiver's database write may commit independently. The transaction demonstration deliberately wraps the caller in `transaction.atomic()` and forces a rollback to prove that the receiver's write participates in that transaction.
