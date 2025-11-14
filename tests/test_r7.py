from services.library_service import (
    borrow_book_by_patron, get_patron_status_report
)

def test_patron_status_initial_empty():
    """Test status report for new patron that hasn't borrowed books."""
    status = get_patron_status_report("325895")
    assert status["currently_borrowed"] == []
    assert status["total_late_fees"] == 0
    assert status["borrow_count"] == 0


def test_patron_status_with_borrowed_books():
    """Test status after borrowing a book"""
    borrow_book_by_patron("123456", 1)
    status = get_patron_status_report("123456")

    assert status["borrow_count"] >= 1
    assert any("due_date" in b for b in status["currently_borrowed"])
    # ensuring borrowed books displays a due date
