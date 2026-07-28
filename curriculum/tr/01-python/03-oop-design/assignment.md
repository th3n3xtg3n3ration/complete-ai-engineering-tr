# Ödev — Genişletilebilir Abonelik Sistemi

Bir dijital eğitim platformu için abonelik alan modeli geliştir.

## Gereksinimler

- `Plan`, `Subscription` ve `Customer` modelleri.
- Aylık ve yıllık fiyatlandırma politikaları.
- En az iki indirim politikası.
- Ödeme servisi için `Protocol` veya ABC.
- Dependency injection kullanan checkout servisi.
- Geçersiz durumlar için özel exception sınıfları.
- En az 12 birim test.
- Kısa tasarım kararları belgesi.

## Kısıtlar

- Gerçek ağ isteği yapılmamalı.
- Global mutable state kullanılmamalı.
- Para değerleri negatif olamamalı.
- Domain kuralları CLI veya kullanıcı arayüzünde bulunmamalı.

## Rubrik — 100 puan

- Domain modelinin doğruluğu: 20
- Encapsulation ve invariants: 15
- SOLID ilkelerinin uygulanması: 20
- Soyutlama ve dependency injection: 15
- Test kapsamı ve hata senaryoları: 20
- Kod okunabilirliği ve dokümantasyon: 10
