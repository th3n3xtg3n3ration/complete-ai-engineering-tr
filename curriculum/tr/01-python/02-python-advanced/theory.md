# İleri Python — Teori

## 1. Comprehension yapıları

Comprehension, bir koleksiyondan yeni bir koleksiyon üretmenin kısa yoludur.

```python
squares = [number ** 2 for number in range(10) if number % 2 == 0]
```

Kısa olmak her zaman iyi olmak değildir. Bir comprehension birden fazla koşul ve dönüşüm içeriyorsa normal döngü daha okunabilir olabilir.

## 2. Iterator ve generator

Iterator, `__iter__` ve `__next__` protokolünü izler. Generator ise bu protokolü `yield` ile kolaylaştırır ve tüm veriyi belleğe yüklemeden elemanları sırayla üretir.

```python
def read_batches(items, batch_size):
    for start in range(0, len(items), batch_size):
        yield items[start:start + batch_size]
```

Generator'lar büyük veri akışlarında bellek kullanımını azaltır; ancak tek kullanımlı oldukları unutulmamalıdır.

## 3. Decorator

Decorator bir fonksiyonu değiştirmeden davranışını saran fonksiyondur. Loglama, süre ölçme, yetkilendirme ve tekrar deneme mekanizmalarında kullanılır.

```python
from functools import wraps
from time import perf_counter


def timed(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        started = perf_counter()
        result = function(*args, **kwargs)
        print(f"{function.__name__}: {perf_counter() - started:.4f}s")
        return result
    return wrapper
```

## 4. Context manager

Context manager, kaynakların güvenli açılıp kapanmasını sağlar. Dosya, ağ bağlantısı ve kilit yönetiminde `with` kullanılır.

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(resource):
    try:
        yield resource
    finally:
        resource.close()
```

## 5. Type hint ve dataclass

Type hint çalışma zamanında zorunlu değildir; editör, linter ve statik analiz araçlarına bilgi verir. `dataclass`, veri taşıyan sınıflarda tekrar eden kodu azaltır.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Record:
    name: str
    score: float
```

## 6. Exception tasarımı

Beklenen hata durumları için anlamlı özel exception sınıfları tanımlanmalıdır. Genel `except Exception` blokları hataları gizleyebilir.

```python
class InvalidRecordError(ValueError):
    """Girdi kaydı doğrulanamadığında yükseltilir."""
```

## 7. Modüler tasarım

İyi bir veri hattı şu sorumlulukları ayırır:

1. Girdi doğrulama
2. Dönüştürme
3. Filtreleme
4. Özetleme
5. Çıktı üretme

Saf fonksiyonlar yan etki üretmez ve aynı girdiye aynı çıktıyı verir. Bu özellik test yazmayı kolaylaştırır.

## 8. Kalite kontrol listesi

- Fonksiyonlar tek sorumluluğa sahip mi?
- İsimler amacı açıklıyor mu?
- Hata mesajları kullanıcıya çözüm gösteriyor mu?
- Type hint'ler mevcut mu?
- Sınır durumları test edildi mi?
- Gereksiz global durumdan kaçınıldı mı?
