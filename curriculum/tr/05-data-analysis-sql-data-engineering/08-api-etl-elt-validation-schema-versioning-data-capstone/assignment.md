# Ödev — Sürümlü Sipariş Analitiği Veri Ürünü

## Senaryo

Bir e-ticaret ekibi müşteri, ürün ve sipariş verilerini üç farklı kaynaktan alıyor:

- Cursor pagination kullanan müşteri API'si
- Günlük JSON sipariş export'u
- CSV ürün kataloğu

Analitik ve makine öğrenmesi ekipleri müşteri başına güvenilir özellik seti bekliyor. Kaynaklarda geçici API hataları, duplicate kayıtlar, bilinmeyen kategoriler, geç gelen güncellemeler ve zaman zaman kırıcı şema değişiklikleri oluşuyor.

## Görev

Uçtan uca çalışan bir veri pipeline'ı geliştir:

1. API istemcisinde timeout, retry, backoff, `Retry-After` ve pagination uygula.
2. Her kaynağın ham verisini immutable bronze snapshot olarak sakla.
3. Customer, product ve order için sürümlü veri sözleşmeleri tanımla.
4. Tip, null, enum, aralık, pattern ve primary-key kontrolleri uygula.
5. Geçersiz kayıtları quarantine katmanına ayrıntılı hata kodlarıyla yaz.
6. Silver kayıtları normalize edilmiş JSONL veya Parquet olarak yayımla.
7. SQLite veya PostgreSQL hedefinde idempotent upsert gerçekleştir.
8. Geç gelen eski güncellemelerin yeni kayıtları ezmesini önle.
9. SQL ile müşteri başına en az sekiz analitik özellik üret.
10. Gold veri setini CSV veya Parquet olarak yayımla.
11. Dataset version, input checksum, contract fingerprint ve pipeline version üret.
12. Lineage, satır sayıları ve artefakt checksum'larını içeren manifest yaz.
13. Manifest bütünlüğünü doğrulayan komut geliştir.
14. En az 30 otomatik test yaz.
15. Operasyon, güvenlik ve backfill yaklaşımını teknik raporda açıkla.

## Zorunlu özellikler

Gold veri seti en az şunları içermelidir:

- `customer_id`
- `paid_order_count`
- `total_paid_amount`
- `average_paid_order_amount`
- `latest_paid_order_at`
- `days_since_latest_paid_order`
- `distinct_product_count`
- `refund_rate`
- `dataset_version`

## Kalite kapıları

Pipeline aşağıdaki koşullardan biri gerçekleşirse başarısız olmalıdır:

- Kaynak erişimi retry sınırını aşıyor.
- Contract dosyası geçersiz.
- Reddedilen kayıt oranı belirlenen kritik eşiği aşıyor.
- Gold tabloda primary-key duplicate oluşuyor.
- Manifest artefakt checksum'ı eşleşmiyor.
- Warehouse transaction tamamlanamıyor.

## Teslim yapısı

```text
project/
├── README.md
├── contracts/
├── src/
├── tests/
├── sql/
├── sample-data/
├── docs/
└── pyproject.toml
```

## Rubrik — 100 puan

| Ölçüt | Puan |
|---|---:|
| API extraction, pagination ve retry tasarımı | 12 |
| Bronze snapshot ve checksum bütünlüğü | 10 |
| Veri sözleşmesi ve şema evrimi | 15 |
| Validation ve quarantine | 12 |
| Idempotent/incremental load | 14 |
| SQL dönüşümleri ve gold grain doğruluğu | 12 |
| Dataset version, lineage ve manifest | 10 |
| Otomatik testler ve hata senaryoları | 10 |
| Güvenlik, gözlemlenebilirlik ve teknik rapor | 5 |

## Bonus

- Watermark ve overlap-window incremental extraction
- Dead-letter replay komutu
- Docker Compose ile PostgreSQL
- CI pipeline'ında contract compatibility gate
- OpenLineage uyumlu event üretimi
- Parquet partitioning ve schema evolution deneyi
