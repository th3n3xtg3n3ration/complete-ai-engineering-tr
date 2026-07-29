# Ödev — Sızıntısız Sayısal Veri Hazırlama Paketi

## Senaryo

Bir AI ekibi farklı kaynaklardan gelen sayısal özellikleri model eğitimine hazırlamak istiyor. Veride eksik değerler, farklı ölçekler, sabit sütunlar ve aykırı değerler bulunuyor. Eğitim, validation ve test ayrımı bozulmadan yeniden kullanılabilir bir NumPy paketi geliştirmen gerekiyor.

## Zorunlu bileşenler

### 1. Veri sözleşmesi

- Yalnız 2-D sayısal input kabul et.
- Boş matris, sonsuz değer ve feature-count değişimi için açık hata üret.
- Input'u mutate etme.
- `float64` çıktı sözleşmesini belgele.

### 2. Transformer

Aşağıdaki API'yi uygula:

```python
pipeline.fit(X_train)
X_train_ready = pipeline.transform(X_train)
X_valid_ready = pipeline.transform(X_valid)
X_test_ready = pipeline.transform(X_test)
```

Pipeline:

- median imputation,
- quantile clipping,
- standardization,
- sabit feature raporu,
- immutable state

içermelidir.

### 3. Vektörleştirilmiş analiz

- cosine similarity,
- pairwise squared Euclidean distance,
- top-k neighbor retrieval,
- feature summary

fonksiyonlarını ekle.

### 4. Benchmark

En az iki eşdeğer işlemi loop ve NumPy sürümleriyle karşılaştır:

- aynı input,
- aynı output,
- warm-up,
- en az 5 tekrar,
- medyan süre,
- maksimum mutlak hata.

### 5. Testler

En az 20 test yaz. Şunlar zorunludur:

- shape doğrulama
- all-missing feature
- constant feature
- transform-before-fit
- train state'in transform sırasında değişmemesi
- NaN imputation
- clipping
- inverse transform
- cosine invariant'ları
- distance invariant'ları
- benchmark doğruluk eşitliği
- tekrarlanabilir seed

### 6. Teknik rapor

Raporunda:

- veri sözleşmesini,
- leakage riskini,
- view/copy kararlarını,
- benchmark yöntemini,
- bellek maliyetini,
- edge case politikasını,
- test sonuçlarını

açıkla.

## Kabul kriterleri

```bash
pytest -q
```

başarılı olmalı. Kod type hint, docstring ve açık hata mesajları içermeli. Test/validation verisi preprocessing state'ini değiştirmemeli.

## Rubrik — 100 puan

| Alan | Puan |
|---|---:|
| Veri sözleşmesi ve doğrulama | 15 |
| Fit/transform mimarisi | 20 |
| Eksik değer, clipping ve scaling | 15 |
| Vektörleştirilmiş similarity/distance | 15 |
| Benchmark kalitesi | 10 |
| Test kapsamı | 15 |
| Kod kalitesi ve dokümantasyon | 5 |
| Teknik rapor ve leakage analizi | 5 |
