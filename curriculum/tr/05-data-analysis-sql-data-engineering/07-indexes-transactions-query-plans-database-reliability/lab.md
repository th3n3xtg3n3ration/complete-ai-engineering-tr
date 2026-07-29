# Laboratuvar — Güvenilir SQLite İşlem Sistemi

## Amaç

Atomik para transferi, idempotency, optimistic locking, savepoint, indeks ve query-plan analizi içeren küçük fakat üretim mantığı taşıyan bir SQLite sistemi geliştirmek.

## Adım 1 — Veritabanını oluştur

```python
from database_reliability import build_demo_database

database = build_demo_database("bank.db")
```

`foreign_keys`, `busy_timeout` ve dosya tabanlı veritabanında WAL ayarlarını kontrol et.

## Adım 2 — Atomik transfer çalıştır

```python
from database_reliability import transfer_funds

transfer_funds(
    database,
    transfer_id="t-001",
    source_account_id="a1",
    target_account_id="a2",
    amount_kurus=25_000,
    idempotency_key="checkout-2026-001",
)
```

Aynı isteği ikinci kez çalıştır. Bakiyelerin yalnızca bir kez değiştiğini ve transfer tablosunda tek kayıt bulunduğunu kanıtla.

## Adım 3 — Rollback senaryosu

Yetersiz bakiye ile transfer dene. Kaynak ve hedef bakiyelerinin değişmediğini doğrula. Daha sonra transaction içinde bilinçli hata üretip eklenen satırın rollback edildiğini kontrol et.

## Adım 4 — Savepoint

Dış transaction içinde bir hesap ekle. Savepoint içinde ikinci hesap ekleyip hata üret. Dış işlemdeki ilk hesabın kaldığını, savepoint içindeki hesabın silindiğini göster.

## Adım 5 — Optimistic locking

Aynı hesabın `version=0` durumunu iki istemcinin okuduğunu varsay. İlk güncelleme başarılı olduktan sonra ikinci güncellemeyi eski version ile dene. Çatışmanın açık hata olarak döndüğünü raporla.

## Adım 6 — İndeksleri oluştur

```python
from index_analysis import create_recommended_indexes

create_recommended_indexes(database)
```

`transfers(source_account_id, created_at DESC)` indeksinin hangi sorgu iş yükünü desteklediğini yaz.

## Adım 7 — Query planı karşılaştır

İndeks öncesi ve sonrası şu sorgunun planını kaydet:

```sql
SELECT *
FROM transfers
WHERE source_account_id = ?
ORDER BY created_at DESC;
```

`SCAN`, `SEARCH`, `USING INDEX` ve geçici sıralama ifadelerini yorumla.

## Adım 8 — Lock retry

İlk iki çağrıda `sqlite3.OperationalError("database is locked")` üreten sahte bir operasyon yaz. Exponential backoff gecikmelerinin `0.1`, `0.2` olarak ilerlediğini test et.

## Adım 9 — Backup ve restore

Backup API ile `backup.db` üret. Yeni bağlantı üzerinden bakiyeleri ve bütünlük raporunu doğrula. Backup varlığını değil restore edilebilirliğini başarı ölçütü olarak kullan.

## Teslim çıktıları

- Çalışan kaynak kod
- Query-plan karşılaştırma tablosu
- İndeks gerekçesi
- Transaction ve rollback testleri
- Backup restore kanıtı
- Lock/retry risk değerlendirmesi
