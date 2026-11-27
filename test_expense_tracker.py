from expense_tracker import add_expense, list_expenses, total_by_category


def test_add_and_total(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    add_expense("Coffee", "food", 4.5)
    add_expense("Tea", "food", 2.5)
    assert total_by_category("food") == 7.0
    assert len(list_expenses()) == 2
