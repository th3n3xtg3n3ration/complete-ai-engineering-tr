# Ödev — Üretim Kalitesinde Gaussian Naive Bayes ve Belirsizlik Raporu

## Amaç

Saf Python ile log-uzayında çalışan, test edilebilir ve tekrarlanabilir bir Gaussian Naive Bayes paketi geliştir. Modeli sınıf dengesizliği bulunan sentetik veri üzerinde değerlendir; prior, smoothing, calibration ve karar eşiği seçimlerinin etkisini teknik olarak raporla.

## Zorunlu teslimler

```text
assignment/
├── src/
│   ├── model.py
│   ├── metrics.py
│   ├── calibration.py
│   └── experiment.py
├── tests/
│   ├── test_model.py
│   ├── test_metrics.py
│   └── test_reproducibility.py
├── report.md
├── experiment_config.json
└── results.json
```

## Fonksiyonel gereksinimler

### Model

- `fit`, `predict`, `predict_proba` ve `predict_log_proba` arayüzleri sunulmalı.
- En az iki sınıf ve birden fazla özellik desteklenmeli.
- Sınıf prior'ları veriden öğrenilebilmeli veya kullanıcı tarafından verilebilmeli.
- Varyans smoothing uygulanmalı.
- Posterior hesapları log-uzayında yapılmalı.
- Fit edilmemiş model tahminde açık hata üretmeli.
- NaN, infinity, boş veri ve tutarsız shape girdileri doğrulanmalı.

### Metrikler

En az şu metrikler uygulanmalı:

- Accuracy
- Precision
- Recall
- F1
- Confusion matrix
- Binary log-loss
- Brier score
- Expected calibration error

### Deney

En az dört yapılandırma karşılaştırılmalı:

1. Veriden öğrenilen prior ve varsayılan smoothing
2. Uniform prior
3. Domain prior
4. Değiştirilmiş smoothing

Her yapılandırma en az beş farklı seed ile çalıştırılmalı. Ortalama ve standart sapma raporlanmalı.

### Karar eşiği

`0.05` ile `0.95` arasında eşik taraması yap. Aşağıdaki iki hedef için ayrı eşik seç:

- En yüksek F1
- Verilen false-positive ve false-negative maliyetleri altında en düşük beklenen maliyet

## Veri sızıntısı kuralları

- Train/test bölmesi deneyden önce yapılmalı.
- Mean, variance ve prior yalnızca eğitim verisinden hesaplanmalı.
- Eşik seçimi için test verisi kullanılamaz; validation bölmesi ayrılmalı.
- Son test sonucu yalnızca nihai yapılandırma seçildikten sonra hesaplanmalı.

## Test gereksinimleri

En az 20 otomatik test yaz:

- Kapalı form posterior doğrulaması
- Olasılıkların bire toplamı
- Sıfır varyans koruması
- Custom prior doğrulaması
- Fit öncesi hata
- Shape doğrulaması
- NaN ve infinity reddi
- Metriklerin bilinen küçük örneklerde doğruluğu
- Sabit seed ile aynı sonuç
- Farklı seed ile farklı veri
- Train/test ayrıklığı
- Log-loss clipping davranışı
- Calibration bin sayımı

## Teknik rapor

`report.md` şu başlıkları içermelidir:

1. Problem tanımı
2. Olasılıksal varsayımlar
3. Veri üretim süreci
4. Model tasarımı
5. Sayısal kararlılık kararları
6. Deney protokolü
7. Sonuç tablosu
8. Calibration analizi
9. Karar eşiği ve maliyet analizi
10. Hata analizi
11. Sınırlılıklar
12. Üretime geçiş önerileri

## Rubrik — 100 puan

| Alan | Puan |
|---|---:|
| Matematiksel doğruluk | 20 |
| Model API ve kod kalitesi | 15 |
| Sayısal kararlılık | 15 |
| Test kapsamı | 15 |
| Deney tasarımı ve tekrarlanabilirlik | 15 |
| Calibration ve eşik analizi | 10 |
| Teknik rapor | 10 |

## Kritik hata koşulları

Aşağıdakilerden biri varsa toplam puan en fazla 50 olabilir:

- Test verisinden eğitim istatistiği hesaplanması
- Olasılık çarpımlarının doğrudan yapılıp underflow riskinin görmezden gelinmesi
- Random seed ve deney yapılandırmasının kaydedilmemesi
- Yalnızca accuracy raporlanması
- Otomatik test bulunmaması

## İleri seviye bonus — 15 puan

- Multiclass Brier score veya log-loss: 5 puan
- Isotonic ya da Platt calibration karşılaştırması: 5 puan
- Model drift için prior ve feature dağılım izleme tasarımı: 5 puan
