# Teori — OOP ve Tasarım İlkeleri

## 1. Neden nesne yönelimli tasarım?

Nesne yönelimli programlama; veri ile bu veri üzerinde çalışan davranışları aynı modelde toplar. Amaç yalnızca sınıf yazmak değil, değişime dayanıklı sınırlar kurmaktır.

```python
class Temperature:
    def __init__(self, celsius: float) -> None:
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius
```

## 2. Temel kavramlar

- **Encapsulation:** İç durumu kontrollü bir arayüz arkasında saklamak.
- **Abstraction:** Gereksiz ayrıntıları gizleyip anlamlı sözleşmeler sunmak.
- **Inheritance:** Bir türün davranışını başka bir türden devralmak.
- **Composition:** Bir nesneyi başka nesnelerden oluşturarak davranış kazanmak.
- **Polymorphism:** Aynı arayüzü farklı gerçekleştirimlerle kullanmak.

Python'da çoğu durumda composition, sıkı inheritance zincirlerinden daha esnektir.

## 3. Dataclass ve değer nesneleri

`@dataclass`, veri taşıyan sınıflarda tekrar eden kodu azaltır. Değer nesneleri çoğunlukla immutable tasarlanır.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "TRY"
```

## 4. Abstract Base Class ve Protocol

ABC çalışma zamanında soyut sözleşme kurar. `Protocol` ise yapısal tip kontrolü sağlar.

```python
from typing import Protocol

class PaymentGateway(Protocol):
    def charge(self, amount: float) -> str: ...
```

## 5. SOLID

- **S — Single Responsibility:** Bir sınıfın tek değişim nedeni olmalı.
- **O — Open/Closed:** Yeni davranış eklenebilmeli, mevcut kod gereksiz yere değiştirilmemeli.
- **L — Liskov Substitution:** Alt tür, üst türün yerine davranış bozmadan geçebilmeli.
- **I — Interface Segregation:** Büyük arayüzler yerine küçük ve odaklı sözleşmeler kullanılmalı.
- **D — Dependency Inversion:** Yüksek seviye kod somut sınıflara değil soyutlamalara bağımlı olmalı.

## 6. Dependency injection

Bağımlılıkları sınıf içinde oluşturmak yerine dışarıdan vermek test edilebilirliği artırır.

```python
class CheckoutService:
    def __init__(self, gateway: PaymentGateway) -> None:
        self.gateway = gateway
```

## 7. Yaygın hatalar

- Her kavram için sınıf üretmek.
- Kalıtımı kod tekrarını azaltma aracı sanmak.
- Global bağımlılık kullanmak.
- Domain kurallarını controller veya CLI içine gömmek.
- Bir sınıfa çok fazla sorumluluk yüklemek.

## 8. Tasarım kontrol listesi

1. Domain kuralı nerede yaşıyor?
2. Sınıfın tek ve anlaşılır sorumluluğu var mı?
3. Harici servisler soyutlama üzerinden mi kullanılıyor?
4. Yeni bir davranış eklemek için kaç dosya değişiyor?
5. Birim testte ağ veya dosya sistemi gerekiyor mu?
