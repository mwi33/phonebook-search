# Phonebook Search (Flask + SQLite)

Simple surname prefix search against a local SQLite database.

## Local dev
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Put your SQLite DB at: instance/phonebook.sqlite3 (or set DATABASE_PATH)

export $(grep -v '^#' .env | xargs)  # quick-and-dirty for bash
flask --app wsgi run --host 127.0.0.1 --port 5000
