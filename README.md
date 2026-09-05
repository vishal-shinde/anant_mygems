# MYGEMS ERP

This project has been restructured from a collection of standalone Tkinter scripts into a single, executable app shell.

## Run

1. Create a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set your PostgreSQL values.
4. Apply database migrations:
   `python3 -m app.db.migrate`
5. Launch app:
   `python3 -m app.main`

## Project structure

- `app/main.py` – app entry point
- `app/ui/login_window.py` – login window
- `app/ui/dashboard.py` – dashboard shell
- `app/services/auth_service.py` – authentication logic
- `app/db/migrate.py` – schema migrations
- `app/db/migrations/*.sql` – database schema and index files

## Notes

- This is the new app shell for long-term use.
- Legacy scripts remain in the root for reference, but they are not the execution path.
- Sales, purchases, customers, employees, and expense modules are now bridged into the unified dashboard.
- Use database migrations to evolve schema as the app grows.
