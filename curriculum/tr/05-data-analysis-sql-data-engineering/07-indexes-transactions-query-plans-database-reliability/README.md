# Ders 7 — İndeksler, Transaction, Query Plan ve Veritabanı Güvenilirliği

**Seviye:** L2 · **Tahmini süre:** 22 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- B-tree indekslerin okuma hızını, yazma maliyetini ve disk kullanımını nasıl etkilediğini açıklayabileceksin.
- Tek kolonlu, birleşik, covering ve unique indeksleri sorgu iş yüküne göre tasarlayabileceksin.
- Birleşik indekslerde left-most prefix kuralını yorumlayabileceksin.
- `EXPLAIN QUERY PLAN` çıktısından full scan, index search ve temporary sort davranışını okuyabileceksin.
- ACID, isolation, lock, deadlock ve busy timeout kavramlarını SQLite bağlamında açıklayabileceksin.
- `DEFERRED`, `IMMEDIATE` ve `EXCLUSIVE` transaction modlarını doğru kullanım senaryosuyla eşleştirebileceksin.
- Savepoint ile uzun transaction içinde kısmi rollback sınırları kurabileceksin.
- Para transferi gibi kritik işlemleri atomik, idempotent ve bütünlük kontrollü biçimde geliştirebileceksin.
- Optimistic locking ile kayıp güncelleme riskini teşhis edebileceksin.
- WAL, retry/backoff, query-only connection, backup ve integrity check araçlarını uygulayabileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Transaction, savepoint ve backup araçları](src/database_reliability.py)
4. [İndeks ve query-plan analizi](src/index_analysis.py)
5. [Concurrency ve retry araçları](src/concurrency_control.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_database_reliability.py)
11. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/05-data-analysis-sql-data-engineering/07-indexes-transactions-query-plans-database-reliability/src/database_reliability.py
python curriculum/tr/05-data-analysis-sql-data-engineering/07-indexes-transactions-query-plans-database-reliability/src/index_analysis.py
pytest curriculum/tr/05-data-analysis-sql-data-engineering/07-indexes-transactions-query-plans-database-reliability/tests -q
```

SQLite Python standart kütüphanesiyle birlikte gelir; dersin çekirdek kodu ek veritabanı paketi gerektirmez.

## Mini proje

Hesap ve para transferi tablolarından oluşan güvenilir bir SQLite işlem sistemi geliştireceksin. Sistem; foreign key ve `CHECK` constraint'leri, atomik transfer, idempotency key, optimistic locking, savepoint, lock retry/backoff, WAL ve backup kullanacak. Sorgu iş yüküne göre birleşik indeksler tasarlanacak ve her indeks kararı `EXPLAIN QUERY PLAN` çıktısıyla kanıtlanacak. Bütünlük, rollback ve tekrar deneme davranışları otomatik testlerle doğrulanacak.
