# Ders 5 — Asenkron Python ve Eşzamanlılık

**Seviye:** L1 · **Tahmini süre:** 10 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- `asyncio` event loop ve coroutine modelini açıklayabileceksin.
- `async` / `await`, task, `gather`, timeout ve cancellation kullanabileceksin.
- `Semaphore` ile eşzamanlılık sınırı uygulayabileceksin.
- `Queue` ile producer-consumer akışı kurabileceksin.
- Async, thread ve process yaklaşımlarını karşılaştırabileceksin.
- Retry ve backoff içeren test edilebilir bir async crawler geliştirebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Async crawler örneği](src/async_crawler.py)
3. [Alıştırmalar](exercises.md)
4. [Quiz](quiz.md)
5. [Ödev ve rubrik](assignment.md)
6. [Mülakat soruları](interview-questions.md)
7. [Otomatik testler](tests/test_async_crawler.py)
8. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/01-python/05-async-python-concurrency/src/async_crawler.py
pytest curriculum/tr/01-python/05-async-python-concurrency/tests -q
```

## Mini proje

Ders projesi, en fazla belirlenen sayıda işi eşzamanlı çalıştıran; timeout, retry ve sonuç toplama davranışları bulunan bağımlılıksız bir async crawler çekirdeğidir.
