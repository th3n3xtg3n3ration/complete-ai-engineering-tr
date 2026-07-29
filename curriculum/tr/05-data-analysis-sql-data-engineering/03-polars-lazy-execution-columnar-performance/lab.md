# Laboratuvar — Lazy Sipariş Analitiği

## Amaç

Bu laboratuvarda eager ve lazy Polars yaklaşımlarını aynı iş problemi üzerinde uygulayacak; query planı, doğruluk, çalışma süresi ve bellek etkilerini karşılaştıracaksın.

## Veri şeması

`orders.csv`:

- `order_id`: sipariş kimliği
- `customer_id`: müşteri kimliği
- `order_at`: sipariş zamanı
- `quantity`: adet
- `unit_price`: birim fiyat
- `status`: durum

`customers.csv`:

- `customer_id`
- `segment`
- `country`
- `signup_at`

## Bölüm 1 — Ortam

```bash
python -m pip install "polars>=1.43,<2" pytest
```

Sürümü kaydet:

```python
import polars as pl
pl.show_versions()
```

## Bölüm 2 — Eager keşif

1. `pl.read_csv` ile siparişleri oku.
2. `shape`, `schema`, `null_count` ve `estimated_size` sonuçlarını raporla.
3. Kolon adlarını snake_case yap.
4. Tarih, miktar ve fiyat kolonlarını güvenli biçimde dönüştür.
5. Geçersiz kayıtları ayrı tabloya ayır.
6. `revenue = quantity * unit_price` üret.
7. Müşteri bazında toplam gelir ve sipariş sayısı hesapla.

Kontrol sorusu: Her adım bir ara tablo oluşturuyor mu? Bunların tahmini boyutu nedir?

## Bölüm 3 — Lazy pipeline

1. Aynı dosyayı `pl.scan_csv` ile tara.
2. Yalnızca gereken kolonları seç.
3. `status == "paid"` filtresini uygula.
4. `revenue` kolonunu üret.
5. `customers.csv` ile `m:1` doğrulamalı join yap.
6. Müşteri bazında aggregation kur.
7. `collect` çağırmadan önce planı yazdır.

```python
print(query.explain(optimized=True))
```

Plan üzerinde predicate ve projection pushdown izlerini açıklayan kısa not yaz.

## Bölüm 4 — Streaming

Sorguyu iki biçimde çalıştır:

```python
normal = query.collect()
streamed = query.collect(engine="streaming")
```

Sonuç eşitliğini `polars.testing.assert_frame_equal` ile doğrula. Süre ve peak memory ölçümü yapabiliyorsan iki motoru karşılaştır.

## Bölüm 5 — Sink

Sonuçları doğrudan Parquet'e yaz:

```python
query.sink_parquet("customer_features.parquet")
```

Yazılan dosyayı yeniden tara ve şema ile satır sayısını doğrula.

## Bölüm 6 — Anti-pattern deneyi

Aynı metin temizleme işini iki biçimde yaz:

1. Native string expression
2. `map_elements` ile Python fonksiyonu

Küçük ve orta büyüklükte veri üzerinde süreyi karşılaştır. Sonucun neden yalnızca “Rust hızlıdır” açıklamasıyla sınırlı olmadığını query optimization ve Python çağrı maliyeti üzerinden anlat.

## Bölüm 7 — Benchmark protokolü

- En az üç tekrar çalıştır.
- İlk ısınma çalıştırmasını ayrı tut.
- Medyan süreyi raporla.
- Sonuç eşitliğini her koşulda doğrula.
- Veri satırı sayısı ve kolon sayısını kaydet.
- Kullanılan Polars ve Python sürümünü rapora ekle.

## Teslim

- Çalışan kaynak kodu
- Optimize edilmiş query planı
- Eager/lazy/streaming karşılaştırma tablosu
- Veri kalite raporu
- En az beş otomatik test
- 500–800 kelimelik teknik değerlendirme
