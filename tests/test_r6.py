from services.library_service import (
    search_books_in_catalog
)

def test_search_by_title_partial():
    """Test partial, case-insensitive search by title """
    results = search_books_in_catalog("great", "title")
    assert any("great" in book["title"].lower() for book in results)
    # returns true if any book in the result contains the partial phrase


def test_search_by_author_partial():
    """Test partial, case-insensitive search by author."""
    results = search_books_in_catalog("harper", "author")
    assert any("harper" in book["author"].lower() for book in results)
    # returns true if any book in the result contains the partial name


def test_search_by_isbn_exact_match():
    """Test exact search by 13 digit ISBN """
    results = search_books_in_catalog("9780743273565", "isbn")
    assert len(results) == 1
    assert results[0]["title"] == "The Great Gatsby"


def test_search_no_results():
    """Test search returns empty when no matches found. """
    results = search_books_in_catalog("N/A", "title")
    assert results == []
