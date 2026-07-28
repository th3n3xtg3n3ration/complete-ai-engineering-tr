# Laboratuvar — Veri Yapısı Seçimi

## Senaryo

Bir AI inference servisi geliştiriyorsun. Sistem:

- gelen istekleri sırayla işlemeli,
- son yapılan yönetim işlemlerini geri alabilmeli,
- aktif oturumları hızlı bulmalı,
- son 100 gecikme ölçümünü tutmalıdır.

## Görevler

1. İstekler için `BoundedQueue` kullan ve kapasite dolduğunda kontrollü hata üret.
2. Yönetim işlemleri için `Stack` ile undo geçmişi oluştur.
3. Oturumları `SessionStore` içinde sakla.
4. Sliding window için `collections.deque(maxlen=100)` kullan.
5. Her seçimin beklenen zaman karmaşıklığını tablo halinde yaz.
6. Aynı çözümü yalnızca Python list ile kursaydın hangi işlemlerin pahalılaşacağını açıkla.

## Beklenen analiz

| İşlem | Yapı | Beklenen maliyet |
|---|---|---|
| İstek ekleme | Queue/deque | `O(1)` |
| Sıradaki isteği alma | Queue/deque | `O(1)` |
| Undo ekleme/çıkarma | Stack/list sonu | amortized `O(1)` |
| Oturum arama | Hash table/dict | ortalama `O(1)` |
| Sliding window güncelleme | bounded deque | `O(1)` |

## Ek görev

10.000 eleman üzerinde list üyelik kontrolü ile set üyelik kontrolünü `timeit` kullanarak karşılaştır. Tek ölçüme güvenme; birden fazla tekrar çalıştır ve sonucu bağlama göre yorumla.
