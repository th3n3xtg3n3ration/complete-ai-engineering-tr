# Asenkron Python ve Eşzamanlılık

## 1. Neden asenkron programlama?

Senkron bir program, I/O işlemi tamamlanana kadar bekler. Ağ isteği, dosya erişimi veya veritabanı sorgusu sırasında CPU çoğu zaman boşta kalır. Asenkron programlama bu bekleme süresinde başka görevlerin ilerlemesini sağlar.

Asenkronluk paralellik değildir. Tek thread üzerinde birçok I/O-bound görev sırayla ilerleyebilir. CPU-bound işler için çoğunlukla process tabanlı paralellik gerekir.

## 2. Coroutine ve event loop

`async def` ile tanımlanan fonksiyon coroutine üretir. Coroutine doğrudan çalışmaz; event loop tarafından yürütülür.

```python
import asyncio

async def greet() -> None:
    await asyncio.sleep(0.1)
    print("Merhaba")

asyncio.run(greet())
```

`await`, coroutine'in beklediği noktada kontrolü event loop'a bırakır.

## 3. Task ve gather

`asyncio.create_task` coroutine'i planlar. `asyncio.gather` birden fazla awaitable sonucu birlikte bekler.

```python
async def main() -> None:
    tasks = [asyncio.create_task(greet()) for _ in range(3)]
    await asyncio.gather(*tasks)
```

Task oluşturup sonucunu beklememek hata ve kaynak sızıntısına yol açabilir.

## 4. Timeout, cancellation ve hata yönetimi

`asyncio.timeout` belirli sürede bitmeyen işlemi iptal eder. İptal, `CancelledError` üzerinden coroutine zincirine yayılır. Temizlik işlemleri `finally` bloklarında yapılmalıdır.

```python
async with asyncio.timeout(2):
    await operation()
```

Bir grup görevden birinin hata vermesi durumunda diğer görevlerin kaderi bilinçli biçimde tasarlanmalıdır. Hataları yok saymak yerine sonuç modelinde görünür kılmak daha güvenlidir.

## 5. Semaphore

Sınırsız eşzamanlılık uzak servisi, ağ bağlantı havuzunu veya yerel kaynakları tüketebilir. `Semaphore`, aynı anda kritik bölgeye girebilecek görev sayısını sınırlar.

```python
semaphore = asyncio.Semaphore(10)

async with semaphore:
    return await fetch(url)
```

## 6. Queue ve backpressure

`asyncio.Queue`, producer ve consumer görevleri arasında veri taşır. `maxsize` kullanıldığında üretici kuyruk dolunca bekler; buna backpressure denir.

İş tamamlandığında consumer `task_done`, koordinatör ise `join` çağırabilir.

## 7. Retry ve backoff

Geçici ağ hatalarında retry yararlıdır; doğrulama hatalarında değildir. Denemeler sınırlı olmalı ve aralarında artan gecikme bulunmalıdır.

```python
for attempt in range(max_retries + 1):
    try:
        return await fetch(url)
    except TransientError:
        if attempt == max_retries:
            raise
        await asyncio.sleep(base_delay * 2**attempt)
```

## 8. Async, thread ve process karşılaştırması

- Async: Çok sayıda I/O-bound iş, async uyumlu kütüphaneler.
- Thread: Bloklayan I/O kütüphaneleri veya mevcut senkron kod.
- Process: CPU-bound işler ve gerçek paralellik ihtiyacı.

`asyncio.to_thread`, bloklayan kısa bir fonksiyonu event loop dışındaki thread'de çalıştırabilir.

## 9. Yarış durumları

Coroutine'ler `await` noktalarında görev değiştirebilir. Paylaşılan mutable state birden fazla görev tarafından güncelleniyorsa yarış durumu oluşabilir. Lock, immutable veri veya message passing tercih edilmelidir.

## 10. Üretim ilkeleri

- Eşzamanlılığı sınırla.
- Her dış çağrıya timeout koy.
- Retry politikasını hata türüne göre uygula.
- Cancellation'ı yutma.
- Kaynakları async context manager ile kapat.
- Log ve metriklerle kuyruk, gecikme ve hata oranlarını izle.
- Async kodu deterministik fake bağımlılıklarla test et.
