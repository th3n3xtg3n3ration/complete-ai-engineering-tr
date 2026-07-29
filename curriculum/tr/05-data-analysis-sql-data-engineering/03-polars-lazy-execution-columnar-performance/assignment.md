# Ödev — Kolon Tabanlı Sipariş Veri Ürünü

## Senaryo

Bir e-ticaret sistemi günlük sipariş CSV'leri ve müşteri boyut tablosu üretmektedir. Analitik ekip, her müşteri için gelir, sipariş sayısı, ortalama sipariş değeri, son sipariş zamanı ve segment bilgisini içeren Parquet veri ürünü istemektedir.

## Zorunlu gereksinimler

1. Kaynakları `scan_csv` veya `scan_parquet` ile lazy tara.
2. Zorunlu kolonları materialization olmadan doğrula.
3. Kolon adlarını deterministik snake_case biçimine getir.
4. Tarih ve sayısal alanları güvenli cast et.
5. Geçersiz satırları karantina tablosuna ayır.
6. Duplicate siparişler için açık bir iş kuralı uygula.
7. `revenue = quantity × unit_price` üret.
8. Müşteri tablosuyla `m:1` kardinalite doğrulamalı join yap.
9. Müşteri özelliklerini native expression ve aggregation ile üret.
10. Sonucu Parquet'e sink et.
11. Optimize edilmiş query planını rapora ekle.
12. Eager ve lazy sürümün sonuç eşitliğini test et.
13. Normal ve streaming engine'i karşılaştır.
14. En az 15 otomatik test yaz.
15. Kullanılan Polars ve Python sürümlerini kaydet.

## Beklenen çıktı şeması

- `customer_id`
- `segment`
- `order_count`
- `total_revenue`
- `average_order_value`
- `latest_order_at`
- `days_since_last_order`
- `high_value_customer`

`high_value_customer` eşiği raporda açıklanmalıdır. Örneğin toplam geliri `25.000 ₺` ve üzeri müşteriler yüksek değerli olarak tanımlanabilir; eşik kod içinde sihirli sayı yerine konfigürasyon olmalıdır.

## Teknik rapor

1. Kaynak ve hedef veri sözleşmeleri
2. Query plan yorumu
3. Predicate/projection pushdown gözlemleri
4. Join kardinalite kontrolü
5. Veri kaybı ve karantina sayıları
6. Eager/lazy/streaming benchmark metodolojisi
7. Süre ve bellek sonuçları
8. Sınırlamalar ve sonraki iyileştirmeler

## Rubrik — 100 puan

- Doğru lazy mimari ve terminal materialization: 15
- Expression API ve kod kalitesi: 15
- Şema ve veri kalitesi kontrolleri: 15
- Join kardinalitesi ve aggregation doğruluğu: 15
- Test kapsamı ve determinism: 15
- Benchmark metodolojisi: 10
- Query plan analizi: 5
- Dokümantasyon ve çalıştırılabilirlik: 10

## Başarısızlık koşulları

- Sonuç eşitliğini doğrulamadan performans iddiası
- Join satır patlamasını kontrol etmeme
- Pipeline ortasında tekrarlı `collect`
- Native expression mümkünken yoğun Python UDF kullanımı
- Eğitim veya kaynak istatistiklerini hedef veriyle karıştıran leakage
- Test veya kurulum talimatı bulunmaması
