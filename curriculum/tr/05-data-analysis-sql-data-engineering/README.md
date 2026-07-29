# Modül 5 — Veri Analizi, SQL ve Veri Mühendisliği

Bu modül; ham veriyi güvenilir, tekrarlanabilir ve modellemeye hazır veri ürünlerine dönüştürebilen AI mühendisleri yetiştirmeyi amaçlar. NumPy ve DataFrame işlemlerinden SQL sorgularına, veri kalitesi kontrollerinden ETL/ELT hatlarına kadar üretim odaklı bir temel kurar.

**Modül durumu:** Devam ediyor

## Tamamlanan dersler

1. [NumPy Dizileri, Vektörleştirme ve Broadcasting](01-numpy-arrays-vectorization-broadcasting/README.md) — ndarray, dtype, shape, axis, broadcasting, vektörleştirme, sayısal kararlılık ve sızıntısız özellik hattı
2. [pandas Series, DataFrame, İndeksleme ve GroupBy](02-pandas-series-dataframe-indexing-groupby/README.md) — index alignment, loc/iloc, nullable dtype, GroupBy, güvenli merge, duplicate yönetimi ve sızıntısız tabular pipeline
3. [Polars, Lazy Execution ve Kolon Tabanlı Performans](03-polars-lazy-execution-columnar-performance/README.md) — expression API, LazyFrame, query planı, pushdown, streaming, kardinalite doğrulaması ve eager/lazy benchmark
4. [Veri Temizleme, Eksik Değer, Aykırı Değer, Encoding ve Veri Sızıntısı](04-data-cleaning-missing-outliers-encoding-leakage/README.md) — veri kalite profili, MCAR/MAR/MNAR, IQR, robust z-score, rare/unknown category, fit/transform ve leakage denetimi
5. [Keşifsel Veri Analizi ve Görselleştirme](05-exploratory-data-analysis-visualization/README.md) — descriptive statistics, missingness, korelasyon, segment/zaman analizi, Matplotlib ve tekrarlanabilir EDA raporu
6. [SQL Temelleri, JOIN, CTE ve Window Function](06-sql-basics-joins-cte-window-functions/README.md) — ilişkisel grain, constraint, parametreli sorgu, JOIN kardinalitesi, CTE, anti-join, ranking, LAG ve running total

## Sıradaki dersler

7. İndeksler, transaction, query plan ve veritabanı güvenilirliği
8. API, ETL/ELT, veri doğrulama, şema, versiyonlama ve veri capstone

## Modül çıktıları

Bu modülü tamamlayan öğrenci:

- NumPy ile bellek verimli ve vektörleştirilmiş sayısal işlemler geliştirir.
- pandas ve Polars ile tablo verisini dönüştürür, birleştirir ve özetler.
- Eksik veri, aykırı değer, tip ve leakage sorunlarını teşhis eder.
- Tekrarlanabilir EDA ve görselleştirme raporları üretir.
- SQL ile analitik ve operasyonel sorgular yazar.
- JOIN, CTE, window function, index ve transaction davranışını yorumlar.
- API kaynaklarından idempotent ETL/ELT hatları geliştirir.
- Veri sözleşmesi, şema doğrulama, lineage ve versiyonlama uygular.
- Test edilen bir veri pipeline'ını uçtan uca paketler.

## Modül capstone

Son derste API ve dosya kaynaklarından veri alan, ham veriyi katmanlı biçimde saklayan, şema ve kalite kontrolleri uygulayan, SQL tabanlı analitik tablolar üreten ve modellemeye hazır özellik seti yayımlayan tekrarlanabilir bir veri hattı geliştirilecektir.

Her ders; Türkçe teori, İngilizce kod, laboratuvar, alıştırmalar, quiz, ödev, mülakat soruları, testler ve metadata ile yayımlanır.
