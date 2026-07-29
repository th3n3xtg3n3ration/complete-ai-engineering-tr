# Ödev — Güvenilir Transfer ve İndeks Analiz Sistemi

## Senaryo

Bir ödeme platformu hesaplar arasında para transferi yapıyor. İstemciler ağ hatası nedeniyle aynı isteği tekrar gönderebilir; eş zamanlı güncellemeler bakiyeyi ezebilir; büyüyen transfer tablosu bazı sorguları yavaşlatabilir. Güvenilir bir SQLite prototipi geliştir.

## Zorunlu özellikler

1. `accounts`, `transfers` ve `idempotency_keys` tabloları
2. Primary key, foreign key ve `CHECK` constraint'leri
3. Atomik para transferi
4. Yetersiz bakiyede tam rollback
5. Idempotency key ile tekrar koruması
6. Version tabanlı optimistic locking
7. Savepoint kullanan en az bir çok adımlı akış
8. WAL ve busy timeout konfigürasyonu
9. Geçici lock hatalarında sınırlı exponential backoff
10. En az iki workload-driven indeks
11. İndeks öncesi ve sonrası query-plan raporu
12. Integrity ve foreign-key check
13. Backup ve restore testi
14. Query-only raporlama bağlantısı
15. Otomatik test paketi

## Rapor

`REPORT.md` içinde:

- Transaction sınırları
- Failure mode analizi
- Idempotency tasarımı
- Optimistic locking senaryosu
- İndeks kolon sırası gerekçesi
- Query-plan karşılaştırması
- Backup/restore kanıtı
- Kalan üretim riskleri

bulunmalıdır.

## Rubrik

| Alan | Puan |
|---|---:|
| Şema ve constraint tasarımı | 15 |
| Atomik transfer ve rollback | 20 |
| Idempotency ve optimistic locking | 15 |
| Savepoint, WAL ve retry | 10 |
| İndeks ve query-plan analizi | 15 |
| Backup, restore ve integrity | 10 |
| Otomatik testler | 10 |
| Teknik rapor ve kod kalitesi | 5 |
| **Toplam** | **100** |

## Başarı koşulu

- En az 75 puan
- Atomik transfer ve rollback testleri zorunlu
- Aynı idempotency key'in bakiyeyi ikinci kez değiştirmemesi zorunlu
- Backup restore testi zorunlu
