from services.library_service import (
    add_book_to_catalog
)


def test_add_book_valid_input():
    """Test adding a book with valid input. THIS TEST WILL ONLY WORK ONCE."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "9999999999999", 5)

    assert success == True
    assert "successfully added" in message.lower()


def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)

    assert success == False
    assert "13 digits" in message

# Add more test methods for each function and edge case. You can keep all your test in a separate folder named `tests`.

def test_add_book_empty_title():
    """Test adding a book with no title."""
    success, message = add_book_to_catalog("", "Test Author", "1234567890123", 5)

    assert success == False
    assert "required" in message.lower()

def test_add_book_empty_author():
    """Test adding a book with no author. """
    success, message = add_book_to_catalog("Test Book", "", "1234567890123", 5)

    assert success == False
    assert "required" in message.lower()

def test_add_book_author_name_too_long():
    """Test adding a book with invalid author name. """
    success, message = add_book_to_catalog("Test Book", "eejvfndijpvndsdufsdufbvdbvsdfubvdubfdpsdufbvpsdofuvbspdoufbvspdvspdfuvpsdofuvbsdiufvbdpsfuvbsdpfuvbspdofuberjnvuprubwqornovier", "1234567890123", 5)

    assert success == False
    assert "less than 100" in message.lower()

def test_add_book_name_too_long():
    """Test adding a book with invalid author name. """
    success, message = add_book_to_catalog("eejvfndijpvndsdufsdufbvdbvsdfubvdubfdpsdufbvpsdofuvbspdoufbvspdvspdfuvpsdofuvbsdiufvbdpsfuvbsdpfuvbspdofuberjnvuprubwqornoviereejvfndijpvndsdufsdufbvdbvsdfubvdubfdpsdufbvpsdofuvbspdoufbvspdvspdfuvpsdofuvbsdiufvbdpsfuvbsdpfuvbspdofuberjnvuprubwqornoviereejvfndijpvndsdufsdufbvdbvsdfubvdubfdpsdufbvpsdofuvbspdoufbvspdvspdfuvpsdofuvbsdiufvbdpsfuvbsdpfuvbspdofuberjnvuprubwqornovier", "Test Author", "1234567890123", 5)

    assert success == False
    assert "less than 200" in message.lower()

def test_add_book_invalid_total_copies():
    """Test adding a book with zero or negative total copies."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 0)

    assert success == False
    assert "positive integer" in message.lower()

def test_add_book_repeat_isbn():
    """Test adding a book with an ISBN that already exists."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "9780743273565", 5)

    assert success == False
    assert "ISBN already exists" in message

