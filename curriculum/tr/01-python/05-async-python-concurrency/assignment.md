# Ödev — Dayanıklı Async URL İşleyici

Bir URL listesini eşzamanlı işleyen komut satırı uygulaması geliştir.

## Gereksinimler

- Girdiyi metin veya JSON dosyasından oku.
- Eşzamanlılık sınırını komut satırı argümanı olarak al.
- Her işleme timeout uygula.
- Geçici hatalarda exponential backoff ile en fazla üç retry yap.
- Başarılı ve başarısız sonuçları ayrı alanlarla JSON'a yaz.
- Cancellation sırasında kaynakları güvenli biçimde kapat.
- En az sekiz otomatik test yaz.
- Gerçek ağ erişimi olmadan fake fetcher ile test edilebilir tasarım kur.

## Rubrik — 100 puan

- Async mimari ve doğru `await` kullanımı: 20
- Eşzamanlılık sınırı ve kaynak yönetimi: 15
- Timeout, retry ve hata sınıflandırması: 20
- Cancellation ve temiz kapanış: 10
- Veri modeli ve JSON çıktı: 10
- Otomatik testlerin kapsamı: 15
- Type hint, dokümantasyon ve kod kalitesi: 10

70 puan geçme sınırıdır. Cancellation'ın yutulması veya sınırsız görev oluşturulması kritik tasarım hatası sayılır.
