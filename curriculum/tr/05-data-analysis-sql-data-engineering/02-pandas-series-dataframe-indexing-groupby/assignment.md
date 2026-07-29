# Ödev — Üretim Odaklı Müşteri Analitiği Pipeline'ı

## Problem

Bir e-ticaret sisteminden gelen müşteri ve işlem tablolarını işleyerek modelleme ve raporlama için güvenilir bir müşteri analitiği veri ürünü geliştir.

## Girdi tabloları

### `customers`

- `customer_id`
- `city`
- `segment`
- `age`
- `signup_timestamp`

### `transactions`

- `transaction_id`
- `customer_id`
- `timestamp`
- `quantity`
- `unit_price`
- `channel`

Veri setinde şu sorunlar bulunmalıdır:

- Duplicate işlem kimlikleri
- Eksik yaş ve şehir
- Yeni/veri setinde görülmeyen kategoriler
- Hatalı tarih değerleri
- Negatif adet veya fiyat
- İşlemi olmayan müşteriler
- Müşteri boyut tablosunda duplicate anahtar denemesi

## Zorunlu gereksinimler

1. Kolon isimlerini deterministik snake_case biçimine dönüştür.
2. Gerekli kolonları doğrula.
3. Tarihleri UTC datetime olarak ayrıştır.
4. Duplicate işlemleri açık bir iş kuralıyla çöz.
5. Negatif adet ve fiyatları reddet.
6. `revenue = quantity * unit_price` özelliğini üret.
7. Müşteri bazında en az şu metrikleri hesapla:
   - Sipariş sayısı
   - Toplam gelir
   - Ortalama sipariş değeri
   - İlk ve son işlem zamanı
   - Kanal çeşitliliği
8. Müşteri ve işlem özetlerini kardinalite doğrulamasıyla birleştir.
9. İşlemi olmayan müşterileri raporda koru.
10. Sayısal eksik değer istatistiklerini yalnızca eğitim verisinde öğren.
11. Kategorik seviyeleri yalnızca eğitim verisinde öğren ve yeni değerleri `__unknown__` olarak işle.
12. Deterministik one-hot encoding üret.
13. Ham ve hazırlanmış tablolar için kalite profili üret.
14. En az 20 otomatik test yaz.
15. Girdi DataFrame'lerinin mutasyona uğramadığını test et.

## Beklenen proje yapısı

```text
customer_analytics_project/
├── README.md
├── src/
│   ├── validation.py
│   ├── preparation.py
│   ├── aggregation.py
│   └── pipeline.py
├── tests/
│   ├── test_validation.py
│   ├── test_preparation.py
│   └── test_pipeline.py
├── data/
│   └── sample_input.csv
└── reports/
    └── findings.md
```

## Teknik rapor

`reports/findings.md` içinde şunları açıkla:

- Veri sözleşmesi ve kolon tipleri
- Duplicate çözümleme kuralı
- Merge kardinalitesi
- Fit/transform ayrımı
- Bilinmeyen kategori politikası
- Eksik değer stratejisi
- Bellek tüketimi ve dtype iyileştirmeleri
- En az üç veri kalitesi riski
- En az iki performans iyileştirmesi
- Test kapsamı ve başarısızlık örnekleri

## Rubrik — 100 puan

| Ölçüt | Puan |
|---|---:|
| Şema ve gerekli kolon doğrulaması | 10 |
| Tarih, dtype ve negatif değer kontrolleri | 10 |
| Duplicate çözümleme ve deterministik sıralama | 10 |
| GroupBy metriklerinin doğruluğu | 15 |
| Merge kardinalitesi ve işlemi olmayan müşteriler | 10 |
| Sızıntısız fit/transform pipeline'ı | 15 |
| Kategorik veri ve bilinmeyen kategori yönetimi | 10 |
| Test kalitesi ve edge-case kapsamı | 10 |
| Kod tasarımı, type hint ve hata mesajları | 5 |
| Teknik rapor | 5 |

## Kabul kriterleri

- Tüm testler geçmelidir.
- Aynı girdide aynı çıktı üretilmelidir.
- Test verisi pipeline'ın öğrenilmiş durumunu değiştirmemelidir.
- Duplicate dimension key sessizce kabul edilmemelidir.
- Geçersiz tarih ve negatif parasal değerler raporlanmalıdır.
- Çıktı şeması açık ve sabit olmalıdır.

## Bonus

- Parquet çıktısı ve dtype koruması
- Büyük CSV için parça bazlı okuma
- Kalite metriklerini JSON olarak yayımlama
- Pipeline durumunu güvenli biçimde serileştirme
- pandas ve Polars uygulamalarının performans karşılaştırması