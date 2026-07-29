# Ödev — Saf Python Bilgi Teorisi ve Softmax Regression Capstone

## Amaç

Bu ödevde Yapay Zekâ Matematiği modülünün tamamını bir araya getiren, yeniden kullanılabilir ve test edilebilir bir çok sınıflı sınıflandırma sistemi geliştireceksin.

## Senaryo

Üç veya daha fazla sınıfa sahip sentetik bir veri kümesi üzerinde softmax regression modeli eğitilecek. Sistem yalnızca tahmin doğruluğunu değil; loss, confidence, calibration, predictive entropy ve distribution shift davranışını da raporlayacak.

## Zorunlu gereksinimler

### 1. Bilgi teorisi kütüphanesi

Aşağıdaki fonksiyonları sıfırdan geliştir:

- `entropy`
- `cross_entropy`
- `kl_divergence`
- `jensen_shannon_divergence`
- `softmax`
- `log_softmax`
- `mutual_information`
- `perplexity`

Girdi doğrulama, sıfır olasılık ve logaritma tabanı davranışı belgelenmelidir.

### 2. Loss kütüphanesi

Aşağıdaki loss fonksiyonlarını uygula:

- binary cross-entropy from logits
- categorical cross-entropy from logits
- label-smoothed cross-entropy
- binary focal loss
- multiclass Brier score

Tüm logit tabanlı işlemler sayısal kararlı olmalıdır.

### 3. Softmax regression

Model aşağıdaki özelliklere sahip olmalıdır:

- çok sınıflı lineer skor üretimi,
- kararlı softmax,
- cross-entropy gradient'i,
- bias,
- L2 regularization,
- label smoothing,
- seed kontrollü initialization,
- full-batch veya mini-batch gradient descent,
- `fit`, `predict_proba` ve `predict` API'leri.

### 4. Değerlendirme

En az aşağıdaki metrikleri üret:

- train ve validation loss,
- accuracy,
- per-class precision ve recall,
- confusion matrix,
- Brier score,
- expected calibration error,
- ortalama predictive entropy.

### 5. Deney matrisi

En az altı deney çalıştır:

- iki learning rate,
- en az iki L2 değeri,
- label smoothing açık ve kapalı,
- en az iki random seed.

Her deney için konfigürasyon ve sonuçları kaydet.

### 6. Distribution shift

Test verisine kontrollü feature shift veya noise ekle. Shift öncesi ve sonrası:

- accuracy,
- cross-entropy,
- ECE,
- predictive entropy,
- tahmin dağılımlarının Jensen–Shannon divergence değeri

karşılaştırılmalıdır.

### 7. Testler

En az 25 otomatik test yaz. Testler şunları kapsamalıdır:

- giriş doğrulama,
- bilinen entropi değerleri,
- cross-entropy ayrışımı,
- KL yönü,
- softmax kararlılığı,
- loss fonksiyonlarının sınır durumları,
- seed tekrarlanabilirliği,
- eğitim loss'unun azalması,
- confusion matrix toplamı,
- calibration ölçüm sınırları.

## Teknik rapor

Rapor aşağıdaki bölümleri içermelidir:

1. Problem tanımı
2. Matematiksel model
3. Gradient türetimi
4. Sayısal kararlılık kararları
5. Deney tasarımı
6. Sonuç tablosu
7. Calibration analizi
8. Distribution shift analizi
9. Hata analizi
10. Sınırlılıklar ve sonraki adımlar

## Teslim yapısı

```text
submission/
├── README.md
├── report.md
├── src/
│   ├── information_theory.py
│   ├── losses.py
│   ├── model.py
│   ├── metrics.py
│   └── experiment.py
├── tests/
│   ├── test_information_theory.py
│   ├── test_losses.py
│   └── test_model.py
└── results/
    ├── experiments.json
    └── summary.md
```

## Rubrik — 100 puan

| Kriter | Puan |
|---|---:|
| Bilgi teorisi fonksiyonlarının doğruluğu | 15 |
| Loss fonksiyonları ve sayısal kararlılık | 15 |
| Softmax regression implementasyonu | 20 |
| Gradient ve optimizasyon doğruluğu | 15 |
| Metrikler ve calibration analizi | 10 |
| Distribution shift deneyi | 10 |
| Otomatik testler | 10 |
| Teknik rapor ve kod kalitesi | 5 |

## Kabul ölçütleri

- Kod üçüncü taraf makine öğrenmesi kütüphanesine bağımlı olmamalıdır.
- Aynı seed aynı sonucu üretmelidir.
- Eğitim loss'u anlamlı biçimde azalmalıdır.
- Kolay sentetik veri üzerinde yüksek doğruluk elde edilmelidir.
- Tüm olasılık çıktıları sonlu ve bire toplamlanmalıdır.
- Testler tek komutla çalışmalıdır.
- Sonuçlar yalnızca accuracy ile yorumlanmamalıdır.

## Bonus

- mini-batch eğitim,
- momentum veya Adam,
- temperature scaling,
- early stopping,
- gradient checking,
- reliability diagram verisi,
- model konfigürasyonu için dataclass,
- deney çıktıları için Markdown rapor üretici.
