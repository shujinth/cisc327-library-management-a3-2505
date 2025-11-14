# Assignment 1 - Project implementation Status Report
**Name:** Shujinth Sasithevan  
**Student ID:** 20352505

## 1. Summary
This document lists project functions, their implementation status, and missing elements (if any).

---

## 2. Function Status Table

| Function Name   | Implementation status | What's missing / Notes                                           |
|-----------------|----------------------:|------------------------------------------------------------------|
| catalog         |              Complete | displays all books using get_all_books()                         |
| add_book        |              Complete |                                                                  |
| search          |               Partial | not yet fully implemented; missing catalog search                |
| borrow          |               Partial | check availability, due date logic funstions not implemented     |
| return          |               Partial | missing logic for calculating fines                              |
| API late_fee    |               Partial | missing calculation function                                     |
| API book_search |               Partial | needs search catalog implementation, but json formated correctly |


---

## 3. Unit tests summary
All test scripts are stored in `tests/`. The testing approach:
- Use the Flask test client (`app.test_client()`) and a temporary SQLite DB.
- For each core function we include 4–5 tests: positive, edge-case, invalid input, unauthorized access, and duplicate handling.
- Run tests:
```bash
# from repo root, venv activated
pytest -q
