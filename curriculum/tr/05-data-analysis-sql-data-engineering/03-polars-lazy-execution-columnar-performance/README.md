# Ders 3 — Polars, Lazy Execution ve Kolon Tabanlı Performans

**Seviye:** L2 · **Tahmini süre:** 20 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Polars'ın kolon tabanlı veri modelini ve Apache Arrow uyumlu bellek yaklaşımını açıklayabileceksin.
- Eager `DataFrame` ile lazy `LazyFrame` yürütme modellerini karşılaştırabileceksin.
- Expression API ile Python döngüsü veya satır bazlı UDF kullanmadan dönüşüm yazabileceksin.
- `scan_csv`, `scan_parquet`, predicate pushdown ve projection pushdown kavramlarını uygulayabileceksin.
- Lazy query planını `explain` ile okuyup gereksiz tarama, kolon ve ara sonuçları teşhis edebileceksin.
- `group_by`, aggregation, join, sort ve top-N işlemlerini deterministik biçimde kurabileceksin.
- Streaming engine kullanarak bellek baskısını azaltan sorgular çalıştırabileceksin.
- Polars ve pandas zihinsel modelleri arasındaki temel farkları yorumlayabileceksin.
- Eager ve lazy pipeline'ları doğruluk, süre ve bellek açısından ölçebileceksin.
- Ham sipariş verisinden test edilen, tekrar kullanılabilir ve kolon tabanlı analitik veri ürünü geliştirebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Polars temel araçları](src/polars_foundations.py)
4. [Lazy veri pipeline'ı](src/lazy_pipeline.py)
5. [Eager/lazy performans karşılaştırması](src/performance_comparison.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_polars_foundations.py)
11. [Metadata](metadata.yml)

## Kurulum ve çalıştırma

```bash
python -m pip install "polars>=1.43,<2" pytest
python curriculum/tr/05-data-analysis-sql-data-engineering/03-polars-lazy-execution-columnar-performance/src/polars_foundations.py
python curriculum/tr/05-data-analysis-sql-data-engineering/03-polars-lazy-execution-columnar-performance/src/lazy_pipeline.py
python curriculum/tr/05-data-analysis-sql-data-engineering/03-polars-lazy-execution-columnar-performance/src/performance_comparison.py
pytest curriculum/tr/05-data-analysis-sql-data-engineering/03-polars-lazy-execution-columnar-performance/tests -q
```

## Mini proje

CSV veya Parquet sipariş verisini `scan_*` ile tembel olarak okuyan, native expression'larla temizleyen, müşteri tablosuyla kardinalitesi doğrulanmış biçimde birleştiren ve müşteri bazlı analitik özellikler üreten bir Polars veri ürünü geliştireceksin. Aynı iş yükünün eager ve lazy sürümlerini doğruluk, sorgu planı, çalışma süresi ve tahmini bellek kullanımı açısından karşılaştıracak; streaming engine'in hangi sorgularda avantaj sağladığını teknik raporla açıklayacaksın.
