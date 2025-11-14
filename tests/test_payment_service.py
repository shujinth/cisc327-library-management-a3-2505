from unittest.mock import Mock

from services.payment_service import PaymentGateway
import pytest

@pytest.fixture
def gateway():
    return PaymentGateway()


# test for process_payment()

def test_process_payment_invalid_amount_zero(gateway):
    success, txn, msg = gateway.process_payment("123456", 0)
    assert not success
    assert txn == ""
    assert "Invalid amount" in msg


def test_process_payment_invalid_amount_negative(gateway):
    success, txn, msg = gateway.process_payment("123456", -5)
    assert not success
    assert txn == ""
    assert "Invalid amount" in msg


def test_process_payment_invalid_amount_limit(gateway):
    success, txn, msg = gateway.process_payment("123456", 1500)
    assert not success
    assert txn == ""
    assert "exceeds limit" in msg


def test_process_payment_invalid_patron_id(gateway):
    success, txn, msg = gateway.process_payment("123", 50)
    assert not success
    assert txn == ""
    assert "Invalid patron ID" in msg


def test_process_payment_success(gateway):
    success, txn, msg = gateway.process_payment("123456", 50, "Test payment")
    assert success
    assert txn.startswith("txn_123456")
    assert "processed successfully" in msg


# tests for refund_payment()

def test_refund_invalid_transaction_id_empty(gateway):
    success, msg = gateway.refund_payment("", 10)
    assert not success
    assert "Invalid transaction ID" in msg


def test_refund_invalid_transaction_id_format(gateway):
    success, msg = gateway.refund_payment("abc123", 10)
    assert not success
    assert "Invalid transaction ID" in msg


def test_refund_invalid_amount(gateway):
    success, msg = gateway.refund_payment("txn_123456_1000", 0)
    assert not success
    assert "Invalid refund amount" in msg


def test_refund_success(gateway):
    success, msg = gateway.refund_payment("txn_123456_1000", 5.50)
    assert success
    assert "processed successfully" in msg
    assert "Refund ID:" in msg


# tests for verify_payment_status()

def test_verify_status_invalid_transaction(gateway):
    result = gateway.verify_payment_status("invalid_txn")
    assert result["status"] == "not_found"


def test_verify_status_empty_transaction(gateway):
    result = gateway.verify_payment_status("")
    assert result["status"] == "not_found"


def test_verify_status_success(gateway):
    result = gateway.verify_payment_status("txn_123456_999")
    assert result["status"] == "completed"
    assert result["transaction_id"] == "txn_123456_999"
    assert result["amount"] == 10.50