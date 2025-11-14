from services.library_service import (
    borrow_book_by_patron
)


def test_borrow_book_valid_input():
    """Test borrowing a book with valid input. THIS TEST WILL ONLY WORK ONCE."""
    success, message = borrow_book_by_patron("999999", 1)

    assert success == True
    assert "successfully borrowed" in message.lower()


def test_borrow_book_invalid_id():
    """Test borrowing a book with invalid id."""
    success, message = borrow_book_by_patron("4143", 1)

    assert success == False
    assert "invalid patron id" in message.lower()

def test_borrow_book_book_not_found():
    """Test borrowing a book with book not found."""
    """Still passes with no database, incur further"""
    success, message = borrow_book_by_patron("999999", 17)

    assert success == False
    assert "book not found" in message.lower()

def test_borrow_book_no_books_avail():
    """Test borrowing a book with no books available."""
    success, message = borrow_book_by_patron("999999", 3)

    assert success == False
    assert "not available" in message.lower()

def test_borrow_book_repeat_books():
    """Test borrowing a book more than once."""
    borrow_book_by_patron("999999", 4)
    success, message = borrow_book_by_patron("999999", 4)

    assert success == False
    assert "already borrowed" in message.lower()

def test_borrow_book_max_books_allowed():
    """Test pushing past max books allowed threshold."""
    borrow_book_by_patron("529535", 1)
    borrow_book_by_patron("529535", 2)
    borrow_book_by_patron("529535", 4)
    borrow_book_by_patron("529535", 5)
    borrow_book_by_patron("529535", 6)
    success, message = borrow_book_by_patron("529535", 7)

    assert success == False
    assert "maximum" in message.lower()
