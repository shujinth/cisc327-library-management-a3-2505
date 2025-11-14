from datetime import datetime, timedelta
from unittest.mock import patch

from services import library_service as ls


# ---------------------- R1: add_book_to_catalog ----------------------

@patch("library_service.get_book_by_isbn", return_value=None)
@patch("library_service.insert_book", return_value=True)
def test_add_book_success(mock_insert, mock_get):
    result = ls.add_book_to_catalog("Book A", "Author X", "1234567890123", 3)
    assert result == (True, 'Book "Book A" has been successfully added to the catalog.')

def test_add_book_invalid_title():
    result = ls.add_book_to_catalog("", "Author", "1234567890123", 3)
    assert result == (False, "Title is required.")

def test_add_book_invalid_isbn_length():
    result = ls.add_book_to_catalog("Title", "Author", "12345", 2)
    assert result == (False, "ISBN must be exactly 13 digits.")

@patch("library_service.get_book_by_isbn", return_value={"title": "Exists"})
def test_add_book_duplicate_isbn(mock_get):
    result = ls.add_book_to_catalog("Book", "Author", "1234567890123", 1)
    assert result == (False, "A book with this ISBN already exists.")

@patch("library_service.get_book_by_isbn", return_value=None)
@patch("library_service.insert_book", return_value=False)
def test_add_book_database_error(mock_insert, mock_get):
    result = ls.add_book_to_catalog("Book", "Author", "1234567890123", 1)
    assert result == (False, "Database error occurred while adding the book.")


# ---------------------- R3: borrow_book_by_patron ----------------------

@patch("library_service.update_book_availability", return_value=True)
@patch("library_service.insert_borrow_record", return_value=True)
@patch("library_service.get_patron_borrow_count", return_value=1)
@patch("library_service.get_book_by_id", return_value={"title": "Book A", "available_copies": 2})
def test_borrow_success(mock_book, mock_count, mock_insert, mock_update):
    success, msg = ls.borrow_book_by_patron("123456", 1)
    assert success
    assert "Successfully borrowed" in msg

def test_borrow_invalid_patron_id():
    success, msg = ls.borrow_book_by_patron("12AB", 1)
    assert not success
    assert "Invalid patron ID" in msg

@patch("library_service.get_book_by_id", return_value=None)
def test_borrow_book_not_found(mock_get):
    success, msg = ls.borrow_book_by_patron("123456", 10)
    assert not success
    assert msg == "Book not found."

@patch("library_service.get_book_by_id", return_value={"title": "Book", "available_copies": 0})
def test_borrow_no_available_copies(mock_get):
    success, msg = ls.borrow_book_by_patron("123456", 1)
    assert not success
    assert "not available" in msg

@patch("library_service.get_book_by_id", return_value={"title": "Book", "available_copies": 1})
@patch("library_service.get_patron_borrow_count", return_value=6)
def test_borrow_too_many_books(mock_count, mock_book):
    success, msg = ls.borrow_book_by_patron("123456", 1)
    assert not success
    assert "maximum borrowing limit" in msg


# ---------------------- R4: return_book_by_patron ----------------------

@patch("library_service.calculate_late_fee_for_book", return_value={"fee_amount": 0})
@patch("library_service.update_book_availability", return_value=True)
@patch("library_service.update_borrow_record_return_date", return_value=True)
@patch("library_service.get_patron_borrowed_books", return_value=[{"book_id": 1}])
@patch("library_service.get_book_by_id", return_value={"title": "Book"})
def test_return_success_no_fee(mock_book, mock_borrowed, mock_return, mock_update, mock_fee):
    success, msg = ls.return_book_by_patron("123456", 1)
    assert success
    assert "No late fees" in msg

@patch("library_service.get_book_by_id", return_value=None)
def test_return_book_not_found(mock_get):
    success, msg = ls.return_book_by_patron("123456", 1)
    assert not success
    assert "Book not found" in msg

@patch("library_service.get_book_by_id", return_value={"title": "Book"})
@patch("library_service.get_patron_borrowed_books", return_value=[])
def test_return_not_borrowed(mock_borrowed, mock_book):
    success, msg = ls.return_book_by_patron("123456", 1)
    assert not success
    assert "not borrowed" in msg


# ---------------------- R5: calculate_late_fee_for_book ----------------------

@patch("library_service.get_patron_borrowed_books", return_value=[
    {"book_id": 1, "due_date": datetime.now() + timedelta(days=1)}
])
def test_late_fee_on_time(mock_get):
    res = ls.calculate_late_fee_for_book("123456", 1)
    assert res["fee_amount"] == 0.0
    assert res["status"] == "On time"

@patch("library_service.get_patron_borrowed_books", return_value=[
    {"book_id": 1, "due_date": datetime.now() - timedelta(days=3)}
])
def test_late_fee_under_7_days(mock_get):
    res = ls.calculate_late_fee_for_book("123456", 1)
    assert res["fee_amount"] == 1.5  # 3 * 0.5
    assert res["status"] == "Overdue"

@patch("library_service.get_patron_borrowed_books", return_value=[
    {"book_id": 1, "due_date": datetime.now() - timedelta(days=10)}
])
def test_late_fee_over_7_days(mock_get):
    res = ls.calculate_late_fee_for_book("123456", 1)
    assert res["fee_amount"] == 8.5  # 7*0.5 + 3*1.0
    assert res["status"] == "Overdue"

@patch("library_service.get_patron_borrowed_books", return_value=[
    {"book_id": 1, "due_date": datetime.now() - timedelta(days=30)}
])
def test_late_fee_max_cap(mock_get):
    res = ls.calculate_late_fee_for_book("123456", 1)
    assert res["fee_amount"] == 15.00


# ---------------------- R6: search_books_in_catalog ----------------------

@patch("library_service.get_all_books", return_value=[
    {"title": "Python 101", "author": "Guido", "isbn": "111"},
    {"title": "Java Basics", "author": "James", "isbn": "222"},
])
def test_search_by_title(mock_all):
    res = ls.search_books_in_catalog("python", "title")
    assert len(res) == 1
    assert res[0]["title"] == "Python 101"

@patch("library_service.get_all_books", return_value=[
    {"title": "Python 101", "author": "Guido", "isbn": "111"}
])
def test_search_by_author(mock_all):
    res = ls.search_books_in_catalog("guido", "author")
    assert len(res) == 1

@patch("library_service.get_all_books", return_value=[
    {"title": "Book", "author": "X", "isbn": "123"}
])
def test_search_by_isbn(mock_all):
    res = ls.search_books_in_catalog("123", "isbn")
    assert len(res) == 1


# ---------------------- R7: get_patron_status_report ----------------------

@patch("library_service.calculate_late_fee_for_book", return_value={"fee_amount": 2.0})
@patch("library_service.get_patron_borrowed_books", return_value=[
    {"book_id": 1, "title": "Book1", "author": "A", "due_date": datetime.now(), "is_overdue": False}
])
def test_patron_status_with_books(mock_books, mock_fee):
    report = ls.get_patron_status_report("123456")
    assert report["borrow_count"] == 1
    assert report["total_late_fees"] == 2.0
    assert report["status"] == "Active"

@patch("library_service.get_patron_borrowed_books", return_value=[])
def test_patron_status_no_books(mock_books):
    report = ls.get_patron_status_report("123456")
    assert report["status"] == "No borrowed books"
    assert report["borrow_count"] == 0
