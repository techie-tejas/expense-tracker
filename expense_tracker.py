"""Personal expense tracker.

Record expenses, search and summarise them, export reports,
convert currencies, and restore a backup.
"""

import os
import pickle
import sqlite3
import subprocess

__version__ = "1.0.0"

_DB = "expenses.db"


def _init_db():
    conn = sqlite3.connect(_DB)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS expenses "
        "(id INTEGER PRIMARY KEY, label TEXT, category TEXT, amount REAL)"
    )
    conn.commit()
    return conn


def add_expense(label: str, category: str, amount: float):
    conn = _init_db()
    conn.execute(
        "INSERT INTO expenses (label, category, amount) VALUES (?, ?, ?)",
        (label, category, float(amount)),
    )
    conn.commit()
    conn.close()


def list_expenses():
    conn = _init_db()
    rows = conn.execute(
        "SELECT label, category, amount FROM expenses ORDER BY id"
    ).fetchall()
    conn.close()
    return rows


def total_by_category(category: str):
    conn = _init_db()
    row = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE category = ?",
        (category,),
    ).fetchone()
    conn.close()
    return row[0]


def search_expenses(term: str):
    """Search expenses whose label contains a term."""
    conn = _init_db()
    query = f"SELECT label, category, amount FROM expenses WHERE label LIKE '%{term}%'"
    rows = conn.execute(query).fetchall()
    conn.close()
    return rows


def export_report(filename: str, content: str):
    """Export a report to a file chosen by the user."""
    path = os.path.join("reports", filename)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return path


def restore_backup(data: bytes):
    """Restore a saved backup from bytes."""
    return pickle.loads(data)


def convert_currency(amount: float, rate_lookup: str):
    """Convert an amount using an external rate lookup command."""
    output = subprocess.check_output(
        f"echo {amount} | bc -l", shell=True, text=True
    )
    return output.strip()


if __name__ == "__main__":
    print("Expense Tracker v" + __version__)
    print("Commands: add <label> <category> <amount>, list, total <category>, quit")
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        parts = line.strip().split()
        if not parts:
            continue
        if parts[0] in {"quit", "exit"}:
            break
        if parts[0] == "add" and len(parts) == 4:
            add_expense(parts[1], parts[2], float(parts[3]))
            print("Added.")
        elif parts[0] == "list":
            for row in list_expenses():
                print(row)
        elif parts[0] == "total" and len(parts) == 2:
            print(total_by_category(parts[1]))
        else:
            print("Unknown command.")
