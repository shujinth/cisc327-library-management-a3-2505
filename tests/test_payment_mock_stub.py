from unittest.mock import Mock

from services.library_service import pay_late_fees, refund_late_fee_payment
from services.payment_service import PaymentGateway
import pytest


# tests for pay_late_fees()

def test_pay_late_fees_success(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 10.0})
    mocker.patch("services.library_service.get_book_by_id", return_value={"id": 1, "title": "Fake Book"})

    # creating mock gateway
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_000", "Payment of $10.00 processed successfully")

    success, msg, txn_id = pay_late_fees("123456", 1, mock_gateway)

    assert success is True
    assert txn_id == "txn_000"
    assert " processed successfully" in msg
    mock_gateway.process_payment.assert_called_with(
        patron_id="123456",
        amount=10.0,
        description="Late fees for 'Fake Book'"
    )


def test_pay_late_fees_declined(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 1000.0})
    mocker.patch("services.library_service.get_book_by_id",return_value={"id": 1, "title": "Fake Book"})

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (False, "", "Payment declined: amount exceeds limit")


    success, msg, txn_id = pay_late_fees("999999", 1, mock_gateway)
    assert success is False
    assert txn_id is None
    assert "Payment failed" in msg
    mock_gateway.process_payment.assert_called_once()


def test_pay_late_fees_invalid_patron(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 10.0})
    mocker.patch("services.library_service.get_book_by_id",return_value={"id": 1, "title": "Fake Book"})

    mock_gateway = Mock(spec=PaymentGateway)

    success, msg, txn_id = pay_late_fees("999", 999, mock_gateway)
    assert success is False
    assert txn_id is None
    assert "Invalid patron ID" in msg
    mock_gateway.process_payment.assert_not_called()


def test_pay_late_fees_zero_late_fee(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 0.0})
    mocker.patch("services.library_service.get_book_by_id",return_value={"id": 1, "title": "Fake Book"})

    mock_gateway = Mock(spec=PaymentGateway)

    success, msg, txn_id = pay_late_fees("123456", 1, mock_gateway)

    assert success is False
    assert txn_id is None
    assert "No late fees" in msg
    mock_gateway.process_payment.assert_not_called()


def test_pay_late_fees_network_error(mocker):
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 10.0})
    mocker.patch("services.library_service.get_book_by_id",return_value={"id": 1, "title": "Fake Book"})

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.side_effect = Exception("Network error")

    success, msg, txn_id = pay_late_fees("123456", 1, mock_gateway)
    assert success is False
    assert "Payment processing error" in msg
    mock_gateway.process_payment.assert_called_once()


# tests for refund_late_fee_payment()

def test_refund_success():
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund OK")

    success, msg = refund_late_fee_payment("txn_123", 10.0, mock_gateway)

    assert success is True
    assert "Refund OK" in msg
    mock_gateway.refund_payment.assert_called_once_with("txn_123", 10.0)


def test_refund_invalid_transaction():
    mock_gateway = Mock(spec=PaymentGateway)

    success, msg = refund_late_fee_payment("invalid_txn", 10.0, mock_gateway)

    assert success is False
    assert "Invalid transaction ID" in msg
    mock_gateway.refund_payment.assert_not_called()


@pytest.mark.parametrize("amount", [0, -5, 20])
def test_refund_invalid_amount(mocker, amount):
    mock_gateway = Mock(spec=PaymentGateway)

    success, msg = refund_late_fee_payment("txn_123", amount, mock_gateway)

    assert success is False
    if amount <= 0:
        assert "greater than 0" in msg
    else:
        assert "exceeds maximum" in msg
    mock_gateway.refund_payment.assert_not_called()


def test_refund_gateway_error():
    """Network or gateway error during refund → should handle exception gracefully"""
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.side_effect = Exception("Network error")

    success, msg = refund_late_fee_payment("txn_123", 10.0, mock_gateway)

    assert success is False
    assert "Network error" in msg
    mock_gateway.refund_payment.assert_called_once_with("txn_123", 10.0)



