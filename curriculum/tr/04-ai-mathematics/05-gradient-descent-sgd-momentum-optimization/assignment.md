# Ödev — Saf Python Optimizer Benchmark Sistemi

## Senaryo

Bir ekip, küçük ve denetlenebilir matematik deneyleri için harici sayısal kütüphaneye ihtiyaç duymayan bir optimizer benchmark aracı istiyor. Sistem farklı optimizer'ları aynı problemde çalıştırmalı, eğitim metriklerini kaydetmeli ve başarısız koşuları açıklanabilir kurallarla işaretlemelidir.

## Amaç

Saf Python ile:

- Gradient Descent / SGD
- Momentum
- Nesterov Momentum
- AdaGrad
- RMSProp
- Adam veya AdamW

algoritmalarını içeren modüler bir optimizer paketi geliştir.

Ardından en az iki problem üzerinde benchmark yap:

1. Ill-conditioned quadratic fonksiyon
2. Sentetik linear regression

## Zorunlu gereksinimler

### 1. Ortak optimizer arayüzü

Her optimizer şu davranışı sunmalıdır:

```python
updated_parameters = optimizer.step(parameters, gradients)
```

State kullanan optimizer'lar state boyutunu doğrulamalı ve parametre boyutu beklenmedik biçimde değişirse açık hata üretmelidir.

### 2. Girdi doğrulama

- Boş parametre veya gradient reddedilmeli.
- Parametre ve gradient uzunlukları eşit olmalı.
- NaN ve infinity değerleri reddedilmeli.
- Learning rate ve decay hiperparametreleri geçerli aralıklarda olmalı.

### 3. Gradient clipping

Global norm clipping ekle. Clipping açık ve kapalı deneyleri karşılaştır.

### 4. Learning-rate schedule

En az iki schedule destekle:

- Step veya exponential decay
- Cosine decay

Schedule seçimi yapılandırmadan yapılmalıdır.

### 5. Veri üretimi

Linear regression verisi için:

```text
y = 3.5x - 1.25 + noise
```

kullan. Seed, örnek sayısı ve noise seviyesi yapılandırılabilir olmalıdır.

### 6. Mini-batch eğitimi

- Batch size yapılandırılabilir olmalı.
- Veri her epoch yeniden karıştırılmalı.
- Son küçük batch doğru ölçeklenmeli.
- Batch size `1` ve full-batch koşuları desteklenmeli.

### 7. Metrik kaydı

Her epoch için en az şu alanları kaydet:

```text
epoch
training_loss
validation_loss veya holdout_loss
gradient_norm
update_norm
parameter_norm
learning_rate
```

### 8. Early stopping

- `patience`
- `minimum_delta`
- best epoch
- best parameters

alanlarını destekle.

### 9. Tanılama

En az şu durumları belirleyen açıklanabilir kurallar yaz:

- Divergence / non-finite loss
- Oscillation
- Plateau
- Exploding gradient
- Negligible update
- Overfitting

Tanılama sonucunda yalnızca etiket değil, insan tarafından okunabilir gerekçe döndür.

### 10. Testler

En az 15 test yaz. Şunları kapsa:

- Bilinen tek adımlı SGD sonucu
- Momentum state birikimi
- Adam bias correction
- Gradient clipping norm sınırı
- Schedule sınır değerleri
- Gradient'in finite-difference ile doğrulanması
- Regression yakınsaması
- Geçersiz girdiler
- Early stopping
- Tanılama kuralları
- Seed ile tekrarlanabilirlik

## Benchmark matrisi

En az şu koşuları çalıştır:

| Optimizer | Learning rate | Momentum/decay | Batch size | Schedule |
|---|---:|---:|---:|---|
| SGD | 0.03 | — | full | sabit |
| SGD | 0.02 | 0.9 | 16 | sabit |
| Nesterov | 0.02 | 0.9 | 16 | cosine |
| AdaGrad | 0.1 | — | 16 | sabit |
| RMSProp | 0.03 | 0.9 | 16 | sabit |
| Adam | 0.05 | 0.9 / 0.999 | 16 | sabit |

Learning rate değerlerini problemine göre ayarlayabilirsin; değişiklikleri raporda gerekçelendir.

## Teknik rapor

Rapor şu bölümleri içermelidir:

1. Problem tanımı
2. Matematiksel denklemler
3. Yazılım mimarisi
4. Doğrulama ve test stratejisi
5. Deney yapılandırmaları
6. Sonuç tablosu
7. Loss, gradient normu ve update normu grafikleri
8. Yakınsama ve kararlılık analizi
9. Başarısız koşuların kök neden analizi
10. Üretim ortamına taşımak için gerekli iyileştirmeler

## Kabul kriterleri

- Kod saf Python ile çalışır.
- Fonksiyon ve sınıflarda type hint bulunur.
- Hata mesajları açıklayıcıdır.
- Aynı seed aynı veri ve eğitim sırasını üretir.
- En az bir optimizer quadratic problemde loss'u başlangıcın `%0.1` altına indirir.
- Linear regression deneyi slope ve intercept değerlerini makul toleransla geri kazanır.
- Testlerin tamamı geçer.
- Rapor deney sonuçlarıyla uyumludur.

## Rubrik — 100 puan

| Alan | Puan |
|---|---:|
| Matematiksel doğruluk | 20 |
| Optimizer arayüzü ve implementasyon kalitesi | 20 |
| Eğitim pipeline'ı ve mini-batch desteği | 15 |
| Metrik, early stopping ve tanılama | 15 |
| Test kapsamı ve edge-case doğrulaması | 15 |
| Benchmark tasarımı ve analiz | 10 |
| Dokümantasyon ve tekrarlanabilirlik | 5 |

## Bonus — 15 puana kadar

- Warmup + cosine schedule: 3 puan
- AdamW ile Adam karşılaştırması: 3 puan
- Optimizer state serialization: 3 puan
- Learning-rate range test: 3 puan
- Komut satırı arayüzü ve JSON/CSV çıktı: 3 puan

## Teslim yapısı

```text
optimizer-benchmark/
├── README.md
├── pyproject.toml
├── src/
│   ├── optimizers.py
│   ├── schedules.py
│   ├── problems.py
│   ├── training.py
│   └── diagnostics.py
├── tests/
├── reports/
│   ├── benchmark.md
│   └── metrics.csv
└── run_benchmark.py
```
