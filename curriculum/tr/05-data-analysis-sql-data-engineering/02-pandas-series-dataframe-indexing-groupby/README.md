# Ders 2 — pandas Series, DataFrame, İndeksleme ve GroupBy

**Seviye:** L2 · **Tahmini süre:** 20 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- `Series` ve `DataFrame` veri modellerini, index alignment davranışıyla birlikte açıklayabileceksin.
- `loc`, `iloc`, boolean mask, `query`, kolon seçimi ve güvenli atama yöntemlerini uygulayabileceksin.
- View/copy belirsizliğini ve chained assignment riskini teşhis edebileceksin.
- Veri tiplerini, nullable dtype'ları, kategorik ve tarih-saat kolonlarını yönetebileceksin.
- `groupby`, `agg`, `transform`, `filter` ve çok seviyeli özetleri kurabileceksin.
- `merge`, `join` ve `concat` işlemlerinde anahtar kardinalitesini doğrulayabileceksin.
- Eksik değer, duplicate kayıt, kolon standardizasyonu ve şema kontrolleri uygulayabileceksin.
- Eğitim verisinde fit edilen median ve kategori sözlüklerini yeni verilere sızıntısız biçimde uygulayabileceksin.
- Müşteri ve işlem tablolarından tekrarlanabilir bir analitik veri ürünü geliştirebileceksin.
- Bellek tüketimi, kopyalama maliyeti ve vektörleştirilmiş işlem tasarımını yorumlayabileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [pandas temel araçları](src/pandas_foundations.py)
4. [Fit/transform DataFrame pipeline'ı](src/dataframe_pipeline.py)
5. [Müşteri analitiği mini sistemi](src/customer_analytics.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_pandas_foundations.py)
11. [Metadata](metadata.yml)

## Kurulum ve çalıştırma

```bash
python -m pip install pandas pytest
python curriculum/tr/05-data-analysis-sql-data-engineering/02-pandas-series-dataframe-indexing-groupby/src/pandas_foundations.py
python curriculum/tr/05-data-analysis-sql-data-engineering/02-pandas-series-dataframe-indexing-groupby/src/dataframe_pipeline.py
python curriculum/tr/05-data-analysis-sql-data-engineering/02-pandas-series-dataframe-indexing-groupby/src/customer_analytics.py
pytest curriculum/tr/05-data-analysis-sql-data-engineering/02-pandas-series-dataframe-indexing-groupby/tests -q
```

## Mini proje

İşlem ve müşteri tablolarını alan üretim odaklı bir pandas analitik paketi geliştireceksin. Sistem; kolon ve anahtar doğrulama, duplicate işlem çözümleme, tarih-saat ayrıştırma, gelir hesaplama, müşteri bazlı `GroupBy` metrikleri, kardinalitesi doğrulanmış `merge` ve eğitim verisinden öğrenilen sızıntısız tabular preprocessing adımlarını içerecek. Sonuç veri seti için kalite profili, bellek kullanımı ve doğrulama raporu üretilecek.