from __future__ import annotations

from flask import Blueprint, current_app, render_template, request
from .db import get_db

bp = Blueprint("routes", __name__)

def _sanitize_surname(raw: str) -> str:
    # Keep it simple: trim, collapse spaces.
    # (Do NOT build SQL strings directly; we parameterize below.)
    return " ".join((raw or "").strip().split())

@bp.get("/")
def index():
    return render_template("index.html")

@bp.get("/search")
def search():
    surname = _sanitize_surname(request.args.get("surname", ""))
    page = max(int(request.args.get("page", "1") or "1"), 1)
    per_page = current_app.config["MAX_RESULTS_PER_PAGE"]
    max_total = current_app.config["MAX_TOTAL_RESULTS"]

    results = []
    total_estimate = 0

    if surname:
        db = get_db()

        # Count (capped) so we can show pagination responsibly
        # Note: counting can be expensive on huge DBs; index on surname helps.
        count_row = db.execute(
            """
            SELECT COUNT(*) AS c
            FROM phonebook
            WHERE surname LIKE ? COLLATE NOCASE
            """,
            (surname + "%",),
        ).fetchone()
        total_estimate = int(count_row["c"]) if count_row else 0

        # Hard cap total results exposed (prevents “download the whole phonebook” vibes)
        total_capped = min(total_estimate, max_total)

        offset = (page - 1) * per_page
        if offset < total_capped:
            results = db.execute(
                """
                SELECT id, surname, given_names, address, suburb, state, postcode, phone
                FROM phonebook
                WHERE surname LIKE ? COLLATE NOCASE
                ORDER BY surname ASC, given_names ASC
                LIMIT ? OFFSET ?
                """,
                (surname + "%", per_page, offset),
            ).fetchall()

    return render_template(
        "results.html",
        surname=surname,
        results=results,
        page=page,
        per_page=per_page,
        total=total_estimate,
        max_total=max_total,
    )
