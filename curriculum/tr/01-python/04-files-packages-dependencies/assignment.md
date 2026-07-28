# Ödev — Yapılandırılabilir Veri Arşivi

Komut satırından çalışan küçük bir veri arşivi paketi geliştir.

## Gereksinimler

- `src/` yerleşimi ve `pyproject.toml` kullan.
- Kayıt ekleme, listeleme, filtreleme ve özetleme komutları sun.
- Verileri UTF-8 JSON veya JSON Lines biçiminde sakla.
- Veri dizinini komut satırı seçeneği veya ortam değişkeniyle al.
- Girdileri doğrula ve kullanıcıya açıklayıcı hata mesajı göster.
- Yazma işlemini atomik gerçekleştir.
- En az 10 otomatik test yaz; testlerde `tmp_path` kullan.
- Kurulum ve kullanım komutlarını README içinde açıkla.
- Sır, yerel veri ve sanal ortam dosyalarını `.gitignore` ile dışarıda bırak.

## Rubrik — 100 puan

- Paket ve modül tasarımı: 20
- Dosya işlemlerinin güvenliği: 20
- Veri doğrulama ve hata yönetimi: 15
- Komut satırı deneyimi: 15
- Test kapsamı ve izolasyon: 20
- Dokümantasyon ve kod kalitesi: 10

## Ek çalışma

Dosya biçimini bir `Storage` protocol arkasında soyutla ve aynı servis katmanını hem JSON hem JSON Lines uygulamasıyla çalıştır.