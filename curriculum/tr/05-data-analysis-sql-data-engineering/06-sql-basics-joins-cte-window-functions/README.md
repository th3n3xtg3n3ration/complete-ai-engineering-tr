# Ders 6 — SQL Temelleri, JOIN, CTE ve Window Function

**Seviye:** L2 · **Tahmini süre:** 22 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- İlişkisel tablo, satır, kolon, primary key, foreign key ve constraint kavramlarını açıklayabileceksin.
- `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `CASE`, `NULL` ve aggregation ifadelerini güvenli biçimde kullanabileceksin.
- `INNER`, `LEFT` ve anti-join davranışlarını veri grain'i ve kardinalite üzerinden yorumlayabileceksin.
- `GROUP BY` sorgularında yanlış toplulaştırma ve satır çoğalması sorunlarını teşhis edebileceksin.
- CTE kullanarak karmaşık sorguları okunabilir ve test edilebilir aşamalara ayırabileceksin.
- `ROW_NUMBER`, `DENSE_RANK`, `LAG` ve kümülatif `SUM` window function'larını uygulayabileceksin.
- Parametreli sorgularla SQL injection riskini azaltabileceksin.
- `NOT EXISTS` ile güvenli anti-join sorguları kurabileceksin.
- Sorgu çıktılarını kolon şeması, benzersiz grain ve negatif metrik kontrolleriyle doğrulayabileceksin.
- SQLite üzerinde test edilen, yeniden kullanılabilir bir analitik SQL paketi geliştirebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [SQLite veritabanı ve seed araçları](src/database.py)
4. [JOIN, CTE ve window sorguları](src/analytics_queries.py)
5. [Sorgu kalite ve plan kontrolleri](src/query_quality.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_sql_analytics.py)
11. [Metadata](metadata.yml)

## Kurulum ve çalıştırma

```bash
python curriculum/tr/05-data-analysis-sql-data-engineering/06-sql-basics-joins-cte-window-functions/src/database.py
python curriculum/tr/05-data-analysis-sql-data-engineering/06-sql-basics-joins-cte-window-functions/src/analytics_queries.py
pytest curriculum/tr/05-data-analysis-sql-data-engineering/06-sql-basics-joins-cte-window-functions/tests -q
```

SQLite Python standart kütüphanesiyle birlikte gelir; dersin çekirdek kodu ek veritabanı paketi gerektirmez.

## Mini proje

Müşteri, sipariş, ürün ve sipariş kalemi tablolarından oluşan bir SQLite analitik sistemi geliştireceksin. Sistem; foreign key ve `CHECK` constraint'leriyle veri bütünlüğünü koruyacak, parametreli filtreler kullanacak, JOIN kardinalitesini açıkça tanımlayacak, CTE'lerle sipariş ve müşteri gelirlerini hesaplayacak ve window function'larla sıralama, kümülatif gelir ve siparişler arası süre üretecek. Çıktıların grain, kolon şeması ve iş kuralı kontrolleri otomatik testlerle doğrulanacak.
