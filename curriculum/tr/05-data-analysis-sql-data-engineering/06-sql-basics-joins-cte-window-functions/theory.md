# Teori — SQL Temelleri, JOIN, CTE ve Window Function

## 1. İlişkisel model ve grain

İlişkisel veritabanında veri tablolarda tutulur. Her tablo tek bir varlık veya olay türünü temsil etmelidir. `customers` müşteri varlığını, `orders` sipariş olayını, `order_items` ise sipariş ile ürün arasındaki ilişkiyi temsil eder.

Bir tablonun **grain** tanımı, tek satırın neyi temsil ettiğini söyler:

- `customers`: müşteri başına bir satır,
- `orders`: sipariş başına bir satır,
- `order_items`: sipariş-ürün çifti başına bir satır.

Grain belirtilmeden yazılan JOIN ve aggregation sorguları güvenilir değildir.

## 2. Anahtarlar ve constraint'ler

`PRIMARY KEY` satırı benzersiz tanımlar. `FOREIGN KEY`, ilişkili kaydın var olmasını zorunlu kılar. `NOT NULL` eksik değeri, `CHECK` ise geçersiz iş kuralını engeller.

```sql
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('paid', 'cancelled')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

Constraint, uygulama kodundan bağımsız son savunma katmanıdır.

## 3. SELECT ve mantıksal sorgu sırası

Bir sorgunun yazım sırası ile değerlendirme sırası aynı değildir. Basitleştirilmiş mantıksal sıra şöyledir:

1. `FROM` ve `JOIN`
2. `WHERE`
3. `GROUP BY`
4. `HAVING`
5. `SELECT`
6. `ORDER BY`
7. `LIMIT`

Bu sıra, alias'ların neden bazı bölümlerde kullanılamadığını ve filtrelerin aggregation öncesi/sonrası farkını açıklar.

## 4. NULL ve üç değerli mantık

`NULL`, sıfır veya boş metin değildir; bilinmeyen değerdir. `WHERE region = NULL` yanlıştır. Doğru kullanım `IS NULL` veya `IS NOT NULL` biçimindedir. Aggregation fonksiyonlarının çoğu `NULL` değerleri yok sayar; `COUNT(*)` ise satırları sayar.

## 5. Aggregation ve GROUP BY

Aggregation satır grain'ini değiştirir. Sipariş kalemlerinden sipariş seviyesine geçerken:

```sql
SELECT order_id, SUM(quantity * unit_price) AS order_revenue
FROM order_items
GROUP BY order_id;
```

Her seçilen boyut kolonu `GROUP BY` içinde yer almalı veya açık bir aggregation ile ifade edilmelidir.

## 6. JOIN türleri

### INNER JOIN

Yalnızca iki tarafta eşleşen kayıtları döndürür. Siparişi olmayan müşteriler kaybolur.

### LEFT JOIN

Sol tablodaki tüm kayıtları korur. Müşteri kapsam raporlarında genellikle tercih edilir.

### Anti-join

Bir tarafta olup diğer tarafta olmayan kayıtları bulur. `NOT EXISTS`, `NOT IN` ifadesinin `NULL` tuzaklarına karşı daha güvenlidir.

```sql
SELECT c.*
FROM customers AS c
WHERE NOT EXISTS (
    SELECT 1 FROM orders AS o WHERE o.customer_id = c.customer_id
);
```

## 7. JOIN fan-out

Bir müşteri birden fazla siparişe, bir sipariş birden fazla kaleme sahiptir. Bu tablolar doğrudan birleştirildiğinde müşteri satırı kalem sayısı kadar çoğalır. `COUNT(order_id)` yanlış sonuç verebilir; `COUNT(DISTINCT order_id)` veya önce sipariş seviyesinde CTE üretmek gerekir.

## 8. CTE

Common Table Expression, sorguyu isimlendirilmiş aşamalara böler:

```sql
WITH order_totals AS (
    SELECT order_id, SUM(quantity * unit_price) AS revenue
    FROM order_items
    GROUP BY order_id
)
SELECT * FROM order_totals;
```

CTE her zaman performansı artırmaz. Temel faydası okunabilirlik, grain kontrolü ve test edilebilirliktir.

## 9. Window function

Window function, satır sayısını azaltmadan bir satıra grup bağlamı ekler.

### ROW_NUMBER

Her partition içinde tekil sıra üretir. Top-N seçimlerinde deterministik tie-breaker gerekir.

### DENSE_RANK

Eşit değerlere aynı sıra numarasını verir ve sonraki sırayı atlamaz.

### LAG

Önceki satırın değerini getirir. Siparişler arası süre veya metrik değişimi için kullanılır.

### Kümülatif SUM

```sql
SUM(revenue) OVER (
    PARTITION BY customer_id
    ORDER BY order_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

`ROWS` frame'inin açık yazılması duplicate zaman değerlerinde davranışı belirginleştirir.

## 10. Parametreli sorgular

Kullanıcı girdisi string birleştirme ile SQL'e eklenmemelidir:

```python
connection.execute(
    "SELECT * FROM orders WHERE status = ?",
    (status,),
)
```

Parametreler değerler içindir. Tablo veya kolon adı gibi identifier'lar parametrelenemez; allowlist ile doğrulanmalıdır.

## 11. Sorgu kalite kontrolleri

Analitik sorgu yalnızca çalıştığı için doğru sayılmaz. En az şu kontroller uygulanmalıdır:

- beklenen kolonlar,
- beklenen grain için benzersiz anahtar,
- negatif olmaması gereken metrikler,
- kapsam satır sayısı,
- NULL oranı,
- deterministik sıralama.

## 12. EXPLAIN QUERY PLAN

SQLite `EXPLAIN QUERY PLAN` ile tablo taraması, indeks kullanımı ve JOIN sırası hakkında özet verir. Bu ders sorgu planını tanımaya odaklanır; indeks tasarımı ve transaction ayrıntıları sonraki derste ele alınacaktır.

## 13. Yaygın hatalar

- `LEFT JOIN` sonrası sağ tablo filtresini `WHERE` içinde yazarak sorguyu fiilen `INNER JOIN` yapmak.
- Grain değişimini hesaba katmadan `COUNT` veya `SUM` yapmak.
- `NOT IN` içinde `NULL` davranışını gözden kaçırmak.
- Window function sonucunu `GROUP BY` sonucu sanmak.
- Tie-breaker olmadan top-N üretmek.
- Kullanıcı girdisini SQL string'ine eklemek.
- Çıktıyı test etmeden sorguyu doğru kabul etmek.
