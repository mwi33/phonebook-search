
### `tests/test_search.py`
```python
import os
import tempfile
import sqlite3

import pytest
from app import create_app

@pytest.fixture()
def client():
    db_fd, db_path = tempfile.mkstemp(suffix=".sqlite3")
    os.close(db_fd)

    # Build a tiny test DB
    conn = sqlite3.connect(db_path)
    conn.executescript("""
        CREATE TABLE phonebook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            surname TEXT NOT NULL,
            given_names TEXT,
            address TEXT,
            suburb TEXT,
            state TEXT,
            postcode TEXT,
            phone TEXT
        );
        INSERT INTO phonebook (surname, given_names, phone) VALUES
            ('Smith', 'John', '0400000000'),
            ('Smith', 'Jane', '0400000001'),
            ('Smythe', 'Zed', '0400000002'),
            ('Ng', 'Amy', '0400000003');
    """)
    conn.commit()
    conn.close()

    os.environ["DATABASE_PATH"] = db_path
    os.environ["SECRET_KEY"] = "test"

    app = create_app()
    app.config.update(TESTING=True)

    with app.test_client() as c:
        yield c

    os.remove(db_path)

def test_search_prefix(client):
    r = client.get("/search?surname=Smi")
    assert r.status_code == 200
    body = r.data.decode("utf-8")
    assert "Smith" in body
    assert "Smythe" not in body  # because we use prefix "Smi"

def test_search_case_insensitive(client):
    r = client.get("/search?surname=ng")
    assert r.status_code == 200
    assert "Ng" in r.data.decode("utf-8")