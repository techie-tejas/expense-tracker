# expense-tracker

A personal expense tracker in Python.

Record expenses with a label, category, and amount. Expenses are saved
to a local database, can be listed and searched, totalled by category,
and exported as a report. Backups can be restored, and amounts can be
converted using an external lookup.

## Usage

```bash
python expense_tracker.py
```

```
> add Coffee food 4.50
Added.
> add Taxi travel 12.00
Added.
> list
('Coffee', 'food', 4.5)
('Taxi', 'travel', 12.0)
> total food
4.5
```

Or from Python:

```python
from expense_tracker import add_expense, list_expenses, search_expenses

add_expense("Coffee", "food", 4.50)
list_expenses()
search_expenses("Coffee")
```

## Files

- `expense_tracker.py` — tracker, database, search, export, backup, conversion
- `test_expense_tracker.py` — basic tests

## Version

1.0.0

## License

MIT
