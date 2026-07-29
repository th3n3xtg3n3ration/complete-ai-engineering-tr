# Ödev — Üretim Kalitesinde EDA Rapor Paketi

## Görev

Gerçek veya sentetik bir tabular veri seti seç. Veri setinde en az:

- 500 satır,
- 3 sayısal kolon,
- 2 kategorik kolon,
- 1 tarih kolonu,
- 1 hedef veya ana iş metriği

bulunmalıdır.

Aşağıdaki çıktıları üreten yeniden kullanılabilir bir Python paketi geliştir:

1. Yapısal ve kalite profili
2. Sayısal summary tablosu
3. Kategorik count/rate tablosu
4. IQR aykırı değer raporu
5. Korelasyon çiftleri
6. En az iki segment özeti
7. En az bir zaman özeti
8. Missingness grafiği
9. En az üç dağılım veya ilişki grafiği
10. Markdown teknik raporu
11. Artefakt manifest'i
12. Otomatik testler

## Zorunlu kurallar

- Grafik kodu hesaplama kodundan ayrılmalıdır.
- Kaynak DataFrame fonksiyonlar tarafından mutate edilmemelidir.
- Missing satırlar sessizce düşürülmemelidir.
- Segment tablolarında count bulunmalıdır.
- Korelasyon nedensellik olarak yorumlanmamalıdır.
- Eksen ve ölçekler açıkça etiketlenmelidir.
- Aynı config ile çıktı dosya adları deterministik olmalıdır.
- En az 15 test yazılmalıdır.

## Teslim yapısı

```text
eda-project/
├── README.md
├── src/
├── tests/
├── config.yml
├── report/
│   ├── report.md
│   ├── tables/
│   └── figures/
└── findings.md
```

## Rubrik — 100 puan

- Veri sözleşmesi ve problem tanımı: 10
- Veri kalite profili: 10
- Sayısal/kategorik analiz: 15
- Segment ve zaman analizi: 15
- Görselleştirme doğruluğu: 15
- Tekrarlanabilir rapor mimarisi: 15
- Test kapsamı ve hata yönetimi: 10
- Bulguların teknik yorumu: 10

## Bonus — 10 puan

- Dataset fingerprint ve lineage bilgisi
- Drift karşılaştırması
- HTML rapor
- CI artefakt yayını
