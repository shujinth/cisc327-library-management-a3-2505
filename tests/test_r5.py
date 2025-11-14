from services.library_service import (
    calculate_late_fee_for_book
)
from datetime import datetime, timedelta

def test_late_fee_no_overdue(monkeypatch):
    """R5: Book returned on or before due date -> no fee"""
    due_date = datetime.now() + timedelta(days=1)
    borrowed = [{"book_id": 1, "due_date": due_date}]
    monkeypatch.setattr("services.library_service.get_patron_borrowed_books", lambda x: borrowed)

    result = calculate_late_fee_for_book("123456", 1)
    assert result["fee_amount"] == 0
    assert result["days_overdue"] == 0
    assert result["status"] == "On time"


def test_book_not_borrowed(monkeypatch):
    """R5: Testing a book id that was not borrowed"""
    due_date = datetime.now() + timedelta(days=1)
    borrowed = [{"book_id": 1, "due_date": due_date}]
    monkeypatch.setattr("services.library_service.get_patron_borrowed_books", lambda x: borrowed)

    result = calculate_late_fee_for_book("123456", 9)
    assert result["fee_amount"] == 0
    assert result["days_overdue"] == 0
    assert "not borrowed" in result["status"].lower()



def test_late_fee_within_7_days(monkeypatch):
    """R5: Overdue ≤ 7 days → $0.50/day"""
    due_date = datetime.now() - timedelta(days=5)
    borrowed = [{"book_id": 1, "due_date": due_date}]
    monkeypatch.setattr("services.library_service.get_patron_borrowed_books", lambda x: borrowed)

    result = calculate_late_fee_for_book("123456", 1)
    assert result["fee_amount"] == 2.5
    assert result["days_overdue"] == 5
    assert result["status"] == "Overdue"


def test_late_fee_more_than_7_days(monkeypatch):
    """R5: Overdue > 7 days → $0.50/day for 7 days, then $1/day"""
    due_date = datetime.now() - timedelta(days=10)
    borrowed = [{"book_id": 1, "due_date": due_date}]
    monkeypatch.setattr("services.library_service.get_patron_borrowed_books", lambda x: borrowed)

    result = calculate_late_fee_for_book("123456", 1)
    # 7 * 0.5 + 3 * 1 = 6.5
    assert result["fee_amount"] == 6.5
    assert result["status"] == "Overdue"



def test_late_fee_max_cap(monkeypatch):
    """R5: Fee capped at $15"""
    due_date = datetime.now() - timedelta(days=100)
    borrowed = [{"book_id": 1, "due_date": due_date}]
    monkeypatch.setattr("services.library_service.get_patron_borrowed_books", lambda x: borrowed)

    result = calculate_late_fee_for_book("123456", 1)
    assert result["fee_amount"] == 15.0
    assert result["status"] == "Overdue"
    assert result["days_overdue"] == 100