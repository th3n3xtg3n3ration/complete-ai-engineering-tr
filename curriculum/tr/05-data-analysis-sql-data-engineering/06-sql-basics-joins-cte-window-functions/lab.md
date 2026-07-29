# Laboratuvar — SQLite Analitik SQL Sistemi

## Amaç

Bu laboratuvarda müşteri, ürün, sipariş ve sipariş kalemi tablolarından oluşan küçük bir ilişkisel veri tabanı kuracak; temel sorguları JOIN, CTE ve window function kullanarak geliştireceksin.

## 1. Veritabanını çalıştır

```bash
python curriculum/tr/05-data-analysis-sql-data-engineering/06-sql-basics-joins-cte-window-functions/src/database.py
```

Beklenen tablo sayıları:

- `customers`: 4
- `products`: 4
- `orders`: 5
- `order_items`: 7

## 2. Şemayı incele

`database.py` içindeki `SCHEMA_SQL` sabitinde primary key, foreign key, `NOT NULL`, `CHECK` ve birleşik anahtarları belirle.

## 3. Temel SELECT

SQLite bağlantısı üzerinden şu sorguları yaz:

1. Bölgesi `north` olan müşteriler.
2. Fiyatı 100'den yüksek ürünler.
3. En yeni üç sipariş.
4. Her status için sipariş sayısı.

Her sorguya açık `ORDER BY` ekle.

## 4. JOIN grain analizi

```python
from analytics_queries import order_line_details
from database import build_demo_database

connection = build_demo_database()
rows = order_line_details(connection)
print(rows)
```

Çıktının grain'i sipariş değil, **sipariş-ürün kalemi** seviyesidir. `order_id` tek başına benzersiz değildir.

## 5. LEFT JOIN kapsamı

`customer_revenue_summary` sorgusunda siparişi olmayan `c4` müşterisinin neden korunduğunu açıkla. `LEFT JOIN` yerine `JOIN` kullanıp farkı gözlemle.

## 6. CTE ile sipariş geliri

Önce `paid_order_totals` CTE'sini tek başına çalıştır. Ardından aylık gelir, müşteri toplamı ve ortalama sipariş değeri üret. Her aşamanın grain'ini yazılı olarak belirt.

## 7. Window function

Aşağıdaki fonksiyonları çalıştır:

- `customer_revenue_rank`
- `running_customer_revenue`
- `order_gap_days`
- `top_product_per_category`

Her birinde `PARTITION BY`, `ORDER BY` ve window frame'in ne yaptığını açıkla.

## 8. Anti-join

`customers_without_orders` fonksiyonunu `LEFT JOIN ... IS NULL` biçiminde yeniden yaz. İki sonucun aynı olduğunu test et.

## 9. Parametre güvenliği

`paid_orders` fonksiyonuna farklı eşik değerleri gönder. SQL string birleştirme ile eşdeğer bir kötü örnek yaz ve neden güvenli olmadığını açıkla. Kötü örneği üretim koduna ekleme.

## 10. Query plan

```python
from query_quality import explain_query_plan

plan = explain_query_plan(
    connection,
    "SELECT * FROM orders WHERE customer_id = ?",
    ("c1",),
)
for step in plan:
    print(step)
```

`SCAN` ve `SEARCH` ifadelerini ayırt et. İndeks eklemeyi sonraki derse bırak.

## 11. Testleri çalıştır

```bash
pytest curriculum/tr/05-data-analysis-sql-data-engineering/06-sql-basics-joins-cte-window-functions/tests -q
```

## 12. Genişletme görevleri

- Bölge bazlı aylık gelir sorgusu ekle.
- Her müşteri için en yüksek gelirli siparişi `ROW_NUMBER` ile bul.
- İptal oranını region bazında hesapla.
- Son siparişten bu yana geçen gün sayısını referans tarihe göre hesapla.
- Her sorguya beklenen grain testi ekle.
