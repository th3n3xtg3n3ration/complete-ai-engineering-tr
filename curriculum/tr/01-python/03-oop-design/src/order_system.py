"""OOP ve tasarım ilkeleri için küçük sipariş alan modeli."""

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class Product:
    name: str
    unit_price: float

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Ürün adı boş olamaz.")
        if self.unit_price < 0:
            raise ValueError("Birim fiyat negatif olamaz.")


@dataclass(frozen=True)
class OrderItem:
    product: Product
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("Adet pozitif olmalıdır.")

    @property
    def subtotal(self) -> float:
        return self.product.unit_price * self.quantity


class DiscountPolicy(Protocol):
    def apply(self, total: float) -> float: ...


class NoDiscount:
    def apply(self, total: float) -> float:
        return total


@dataclass(frozen=True)
class PercentageDiscount:
    rate: float

    def __post_init__(self) -> None:
        if not 0 <= self.rate <= 1:
            raise ValueError("İndirim oranı 0 ile 1 arasında olmalıdır.")

    def apply(self, total: float) -> float:
        return total * (1 - self.rate)


class PaymentGateway(Protocol):
    def charge(self, amount: float) -> str: ...


@dataclass
class Order:
    items: list[OrderItem] = field(default_factory=list)

    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)

    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.items)


class CheckoutService:
    def __init__(self, gateway: PaymentGateway, discount: DiscountPolicy | None = None) -> None:
        self.gateway = gateway
        self.discount = discount or NoDiscount()

    def checkout(self, order: Order) -> str:
        if not order.items:
            raise ValueError("Boş sipariş ödenemez.")
        payable = self.discount.apply(order.total)
        return self.gateway.charge(round(payable, 2))


class FakePaymentGateway:
    """Ders ve testlerde kullanılan ağsız ödeme adaptörü."""

    def __init__(self) -> None:
        self.charged_amounts: list[float] = []

    def charge(self, amount: float) -> str:
        self.charged_amounts.append(amount)
        return f"payment-{len(self.charged_amounts)}"


if __name__ == "__main__":
    order = Order()
    order.add_item(OrderItem(Product("Python Kitabı", 450.0), 2))
    gateway = FakePaymentGateway()
    payment_id = CheckoutService(gateway, PercentageDiscount(0.10)).checkout(order)
    print(payment_id, gateway.charged_amounts)
