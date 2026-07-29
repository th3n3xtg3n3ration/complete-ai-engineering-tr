# Laboratuvar — API'den Sürümlü Müşteri Özellik Veri Setine

## Amaç

Bu laboratuvarda dış ağa bağlı olmayan, tamamen tekrarlanabilir bir capstone çalıştıracaksın. Sahte API transport'u cursor pagination ile müşteri ve sipariş kayıtları döndürecek. Pipeline bu kayıtları bronze, silver ve gold katmanlarında yayımlayacak.

## 1. Ortamı doğrula

```bash
python --version
pytest --version
```

Python 3.11 veya üzeri önerilir.

## 2. API istemcisini çalıştır

`src/api_client.py` içindeki `ApiClient` transport bağımlılığını dışarıdan alır. Bu sayede:

- Gerçek HTTP adaptörü kullanılabilir.
- Testte ağ çağrısı yapılmaz.
- Timeout ve header değerleri doğrulanabilir.
- Retry beklemeleri sahte `sleep_fn` ile ölçülebilir.

Aşağıdaki davranışları incele:

1. `503` sonrası retry
2. `Retry-After` önceliği
3. Cursor query parametresi
4. Cursor loop koruması
5. Maksimum sayfa sınırı

## 3. Raw snapshot üret

Python kabuğunda:

```python
from datetime import datetime, timezone
from pathlib import Path

from api_client import write_raw_snapshot

snapshot = write_raw_snapshot(
    Path("capstone-output/bronze"),
    source="customers",
    payload=[{"customer_id": "c1"}],
    fetched_at=datetime.now(timezone.utc),
    schema_version="1.0.0",
)
print(snapshot)
```

Dosya adındaki hash ile dosya içeriğinin SHA-256 değerini karşılaştır. Aynı payload ve aynı fetch zamanı ile fonksiyonu yeniden çağır; yeni kopya oluşmadığını doğrula.

## 4. Veri sözleşmesini incele

`CUSTOMER_CONTRACT` ve `ORDER_CONTRACT` şu kontrolleri uygular:

- Zorunlu alanlar
- String pattern
- Enum değerleri
- Non-negative amount
- ISO-8601 ve timezone
- Primary-key tekilliği
- Unknown field reddi

Aşağıdaki hataları ayrı ayrı oluştur:

- Eksik `region`
- Bilinmeyen `status`
- Negatif `amount`
- Duplicate `order_id`
- Timezone içermeyen tarih
- Fazladan alan

Her hata için `ValidationIssue.code`, `field` ve `message` değerlerini kaydet.

## 5. Sözleşme evrimini değerlendir

Müşteri sözleşmesine opsiyonel ve nullable bir `email` alanı ekle. `compatibility_issues` sonucunun boş olduğunu doğrula.

Ardından aynı alanı zorunlu ekle. Bunun kırıcı değişiklik olarak raporlandığını doğrula.

## 6. Pipeline'ı çalıştır

```bash
python curriculum/tr/05-data-analysis-sql-data-engineering/08-api-etl-elt-validation-schema-versioning-data-capstone/src/data_pipeline.py
```

Oluşan klasör yapısı:

```text
capstone-output/
├── bronze/
│   ├── customers/
│   └── orders/
├── silver/
│   ├── customers_<dataset_version>.jsonl
│   └── orders_<dataset_version>.jsonl
├── gold/
│   └── customer_features_<dataset_version>.csv
├── manifests/
│   └── <dataset_version>.json
└── warehouse.db
```

## 7. Warehouse'u sorgula

```python
import sqlite3

connection = sqlite3.connect("capstone-output/warehouse.db")
connection.row_factory = sqlite3.Row

for row in connection.execute("SELECT * FROM customer_features ORDER BY customer_id"):
    print(dict(row))
```

Şu grain'leri doğrula:

- `customers`: customer_id başına bir satır
- `orders`: order_id başına bir satır
- `customer_features`: customer_id başına bir satır

## 8. Quarantine senaryosu

Bir müşteri kaydında `region="moon"` kullan. Bir siparişte mevcut olmayan `customer_id="c999"` kullan.

Pipeline sonrasında:

```sql
SELECT entity, record_index, issues_json
FROM rejected_records
ORDER BY entity, record_index;
```

sorgusunu çalıştır. Şema hatası ile foreign-key hatasının farklı kodlarla saklandığını incele.

## 9. Idempotency deneyi

Aynı input ile pipeline'ı iki farklı zamanda çalıştır.

Beklenen:

- Dataset version aynı kalır.
- İkinci sonuçta `reused=True` olur.
- Gold dosyası çoğalmaz.
- `pipeline_runs` tablosunda dataset version başına tek satır bulunur.

## 10. Geç gelen veri deneyi

Önce `updated_at=2026-07-30` olan müşteri kaydını yükle. Ardından aynı müşteri için `updated_at=2026-07-28` olan eski kaydı çalıştır.

Eski kaydın yeni müşteri adını ezmediğini doğrula. Bunun event-time ve late-arriving data bağlamındaki sınırlarını tartış.

## 11. Manifest bütünlüğü

```python
from data_pipeline import verify_manifest

errors = verify_manifest("capstone-output", "capstone-output/manifests/<version>.json")
print(errors)
```

Gold CSV dosyasına elle bir satır ekle ve doğrulamayı tekrar çalıştır. `checksum mismatch` hatası beklenir.

## 12. Testleri çalıştır

```bash
pytest curriculum/tr/05-data-analysis-sql-data-engineering/08-api-etl-elt-validation-schema-versioning-data-capstone/tests -q
```

Testler API retry/pagination, snapshot bütünlüğü, sözleşme doğrulaması, uyumluluk, quarantine, upsert, idempotency, lineage, feature üretimi ve manifest checksum davranışlarını kapsar.

## 13. Teknik rapor

Aşağıdaki başlıklarla kısa rapor yaz:

1. ETL/ELT kararın
2. Veri sözleşmesi ve kırıcı değişiklik politikası
3. Quarantine eşiği ve alarm planı
4. Dataset version formülü
5. Incremental load ve watermark stratejisi
6. Lineage ve manifest tasarımı
7. Güvenlik ve secret yönetimi
8. Üretime geçişte SQLite yerine seçilecek sistem ve gerekçesi
