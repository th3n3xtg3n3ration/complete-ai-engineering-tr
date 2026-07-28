import pytest

from curriculum.tr.01_python.03_oop_design.src.order_system import (
    CheckoutService,
    FakePaymentGateway,
    Order,
    OrderItem,
    PercentageDiscount,
    Product,
)


def test_product_rejects_negative_price():
    with pytest.raises(ValueError):
        Product("Hatalı", -1)


def test_order_item_rejects_zero_quantity():
    with pytest.raises(ValueError):
        OrderItem(Product("Kitap", 100), 0)


def test_order_total_is_sum_of_subtotals():
    order = Order([
        OrderItem(Product("A", 100), 2),
        OrderItem(Product("B", 50), 1),
    ])
    assert order.total == 250


def test_percentage_discount_is_applied():
    order = Order([OrderItem(Product("A", 200), 1)])
    gateway = FakePaymentGateway()
    payment_id = CheckoutService(gateway, PercentageDiscount(0.25)).checkout(order)
    assert payment_id == "payment-1"
    assert gateway.charged_amounts == [150.0]


def test_empty_order_cannot_be_checked_out():
    with pytest.raises(ValueError):
        CheckoutService(FakePaymentGateway()).checkout(Order())
