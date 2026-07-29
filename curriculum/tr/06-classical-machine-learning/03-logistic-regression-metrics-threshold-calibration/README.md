# Ders 3 — Logistic Regression, Sınıflandırma Metrikleri, Threshold ve Calibration

**Seviye:** L2 · **Tahmini süre:** 25 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Logistic regression modelini odds, log-odds, sigmoid ve maksimum olabilirlik üzerinden açıklayabileceksin.
- Binary cross-entropy loss ve gradient descent ile sıfırdan logistic regression geliştirebileceksin.
- L1/L2 regularization ve class weight seçeneklerinin karar sınırına etkisini yorumlayabileceksin.
- Confusion matrix, precision, recall, F1, balanced accuracy, ROC-AUC, average precision ve log loss metriklerini doğru bağlamda kullanabileceksin.
- Sınıf dengesizliğinde threshold-independent ve threshold-dependent metrikleri ayırabileceksin.
- Yanlış pozitif ve yanlış negatif maliyetlerini kullanarak cost-sensitive threshold seçebileceksin.
- Minimum precision veya recall kısıtı altında karar eşiği optimize edebileceksin.
- Brier score, reliability diagram ve expected calibration error ile olasılık kalitesini değerlendirebileceksin.
- Platt scaling ve isotonic regression ile olasılık kalibrasyonu uygulayabileceksin.
- Leakage-safe preprocessing, logistic regression ve calibration içeren üretim odaklı bir scikit-learn pipeline'ı geliştirebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Sıfırdan logistic regression](src/logistic_models.py)
4. [Metrik, threshold ve calibration araçları](src/classification_metrics.py)
5. [Leakage-safe calibration pipeline'ı](src/calibration_pipeline.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_classification.py)
11. [Metadata](metadata.yml)

## Kurulum ve çalıştırma

```bash
python -m pip install numpy pandas scikit-learn pytest
pytest curriculum/tr/06-classical-machine-learning/03-logistic-regression-metrics-threshold-calibration/tests -q
```

## Mini proje

Bir churn, fraud veya kredi riski problemi için maliyet duyarlı ve kalibre edilmiş binary classification sistemi geliştireceksin. Sistem; leakage-safe preprocessing, regularized logistic regression, class weighting, ROC-AUC ve average precision değerlendirmesi, precision/recall kısıtlı threshold seçimi, yanlış karar maliyeti analizi, sigmoid/isotonic calibration, reliability tablosu ve sürümlü değerlendirme raporu üretecek. Başarı kriteri yalnızca doğru sınıf tahmini değil; karar eşiğinin iş maliyetlerine dayanması ve yayımlanan olasılıkların güvenilir olmasıdır.
