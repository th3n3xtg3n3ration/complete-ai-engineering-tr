from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).parents[1] / "src" / "order_system.py"
SPEC = spec_from_file_location("order_system", MODULE_PATH)
assert SPEC and SPEC.loader
order_system = module_from_spec(SPEC)
SPEC.loader.exec_module(order_system)

CheckoutService = order_system.CheckoutService
FakePaymentGateway = order_system.FakePaymentGateway
Order = order_system.Order
OrderItem = order_system.OrderItem
PercentageDiscount = order_system.PercentageDiscount
Product = order_system.Product


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
