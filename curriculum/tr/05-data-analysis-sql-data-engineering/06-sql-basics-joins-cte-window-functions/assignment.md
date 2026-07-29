# Ödev — SQLite Analitik Veri Katmanı

## Senaryo

Bir e-ticaret ekibi müşteri, sipariş, ürün ve sipariş kalemi verilerinden tekrarlanabilir analitik tablolar üretmek istiyor. Ham tabloların bütünlüğü korunmalı ve sorgular veri grain'i açık biçimde test edilmelidir.

## Gereksinimler

### 1. Şema

- En az dört ilişkili tablo oluştur.
- Primary key, foreign key, `NOT NULL` ve `CHECK` constraint kullan.
- Her tablonun grain'ini README içinde belgele.

### 2. Seed veri

- Deterministik örnek veri ekle.
- Siparişi olmayan en az bir müşteri bulunmalı.
- İptal veya iade edilmiş en az bir sipariş bulunmalı.
- Bir siparişte birden fazla ürün bulunmalı.

### 3. Analitik sorgular

En az şu sorguları geliştir:

1. Parametreli paid-order filtresi.
2. Müşteri gelir özeti; siparişi olmayan müşterileri korumalı.
3. Aylık gelir CTE'si.
4. Müşteri gelir sıralaması.
5. Kümülatif müşteri geliri.
6. Önceki siparişe göre gün farkı.
7. Category başına en yüksek gelirli ürün.
8. Siparişi olmayan müşteri anti-join'i.

### 4. Kalite kontrolleri

- Beklenen kolon şeması.
- Her sorgu için beklenen grain.
- Negatif olmaması gereken metrikler.
- Deterministik sıralama.
- Parametre kullanım testi.
- Transaction rollback testi.

### 5. Teknik rapor

Rapor şu bölümleri içermeli:

- tablo grain'leri,
- JOIN kardinaliteleri,
- CTE aşamaları,
- window function seçimleri,
- güvenlik kararları,
- test sonuçları,
- en az iki query-plan gözlemi.

## Teslim yapısı

```text
sql-project/
├── README.md
├── schema.sql
├── seed.sql
├── queries.sql
├── src/
│   └── runner.py
├── tests/
│   └── test_queries.py
└── report.md
```

## Rubrik — 100 puan

- Şema ve veri bütünlüğü: 20
- JOIN ve grain doğruluğu: 20
- CTE ve aggregation tasarımı: 15
- Window function uygulamaları: 15
- Parametre güvenliği ve transaction: 10
- Otomatik testler: 15
- Teknik rapor ve tekrarlanabilirlik: 5

## Başarı ölçütü

En az 75 puan, tüm kritik sorgular için geçen testler ve SQL injection riski taşımayan parametre kullanımı gerekir.
