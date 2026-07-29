# Ödev — Sıfırdan PCA ile Embedding Sıkıştırma

## Senaryo

Bir semantik arama sisteminde dört ila sekiz boyutlu sentetik embedding'ler kullanılıyor. Amaç, embedding boyutunu azaltırken komşuluk yapısını ve açıklanan varyansı mümkün olduğunca korumaktır.

## Gereksinimler

1. Saf Python ile PCA modeli geliştir.
2. Model aşağıdaki adımları açıkça uygulamalı:
   - veri doğrulama
   - feature mean hesaplama
   - merkezleme
   - covariance matrisi
   - power iteration
   - deflation
   - component sıralama
   - transform
   - inverse transform
3. `n_components` veya minimum explained variance threshold destekle.
4. Training ve test verisini ayır; PCA'yı yalnızca training verisine fit et.
5. Aşağıdaki metrikleri raporla:
   - explained variance ratio
   - cumulative explained variance
   - reconstruction MSE
   - ilk-k komşuluk korunumu
6. En az üç farklı component sayısını karşılaştır.
7. Kod; ragged data, boş veri, geçersiz component sayısı ve feature uyuşmazlığı için açık hata vermeli.
8. En az 15 pytest testi yaz.
9. Sonuçları `report.md` içinde teknik olarak yorumla.

## Beklenen yapı

```text
solution/
├── pca.py
├── experiment.py
├── tests/
│   └── test_pca.py
├── outputs/
│   └── metrics.csv
└── report.md
```

## Rubrik — 100 puan

- Matematiksel doğruluk: 25
- PCA implementasyonu: 20
- Veri doğrulama ve hata yönetimi: 10
- Test kalitesi: 15
- Deney tasarımı ve tekrarlanabilirlik: 10
- Komşuluk korunumu analizi: 10
- Teknik rapor ve kod kalitesi: 10

## Başarı kriterleri

- Tüm testler geçmeli.
- Full-component reconstruction error sayısal tolerans içinde sıfıra yakın olmalı.
- Component sayısı arttıkça cumulative explained variance azalmamalı.
- Rapor yalnızca varyansı değil, retrieval/komşuluk kalitesini de tartışmalı.
