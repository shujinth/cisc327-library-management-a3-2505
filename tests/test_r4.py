from services.library_service import (
    return_book_by_patron, borrow_book_by_patron
)

def test_return_book_valid_input():
    """Test returning a book that was borrowed by the patron. """
    borrow_book_by_patron("999999", 1)
    success, message = return_book_by_patron("999999", 1)

    assert success == True
    assert "successfully returned" in message.lower()


def test_return_book_invalid_patron_id():
    """Test return with invalid patron ID."""
    success, message = return_book_by_patron("123", 1)

    assert success == False
    assert "invalid patron id" in message.lower()


def test_return_book_not_borrowed():
    """Test returning a book the patron did not borrow. """
    success, message = return_book_by_patron("999999", 1)  # book that wasnt borrowed

    assert success == False
    assert "not borrowed" in message.lower()

def test_return_book_not_found():
    """Test returning a book that does not exist.. """
    success, message = return_book_by_patron("999999", 99)  # nonexistent book

    assert success == False
    assert "not found" in message.lower()


def test_return_book_updates_availability():
    """Test that returning increases available copies."""
    borrow_book_by_patron("999999", 1)
    return_book_by_patron("999999", 1)

    # Try borrowing again should now succeed
    success, message = borrow_book_by_patron("999999", 1)

    assert success == True
    assert "successfully borrowed" in message.lower()
