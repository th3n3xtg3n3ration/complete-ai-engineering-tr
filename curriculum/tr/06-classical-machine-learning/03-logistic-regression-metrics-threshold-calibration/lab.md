# Laboratuvar — Maliyet Duyarlı ve Kalibre Edilmiş Sınıflandırıcı

## Amaç

Sentetik bir churn veri setinde leakage-safe logistic regression kurmak, karar eşiğini iş maliyetlerine göre seçmek ve olasılıkları kalibre etmek.

## 1. Veri üretimi

En az 2.000 müşteri için `age`, `tenure_months`, `monthly_spend`, `support_tickets`, `region`, `plan_type` ve `churned` alanlarını üret. Pozitif sınıf oranını yüzde 10–25 aralığında tut.

## 2. Split

Train, validation ve test kümeleri oluştur. Sınıf oranını koru. Threshold ve calibration kararlarında test verisine bakma.

## 3. Baseline

Majority ve class-prior baseline sonuçlarını hesapla. Accuracy'nin neden tek başına yeterli olmadığını göster.

## 4. Sıfırdan model

`LogisticRegressionGD` ile modeli fit et. Loss eğrisini, coefficient işaretlerini ve threshold değişiminin pozitif tahmin oranına etkisini incele.

## 5. Pipeline

`build_classifier_pipeline` ile sayısal kolonlarda median imputation ve scaling, kategorik kolonlarda most-frequent imputation ve one-hot encoding uygula. L1, L2 ve `class_weight="balanced"` seçeneklerini karşılaştır.

## 6. Ranking metrikleri

Validation kümesinde ROC-AUC ve average precision hesapla. Pozitif prevalence ile average precision baseline'ını karşılaştır.

## 7. Threshold tablosu

`threshold_table` ile 0.00–1.00 arasındaki eşikleri değerlendir. Aşağıdaki üç eşiği raporla:

- en yüksek F1,
- recall en az 0.80 iken en yüksek precision,
- yanlış negatif maliyeti yanlış pozitif maliyetinin beş katıyken en düşük maliyet.

## 8. Calibration

Sigmoid ve isotonic calibration uygula. Calibration öncesi ve sonrası log loss, Brier score ve expected calibration error değerlerini karşılaştır.

## 9. Test değerlendirmesi

Validation üzerinde seçilen model, calibration yöntemi ve threshold'u test kümesine yalnızca bir kez uygula. Confusion matrix, threshold metrikleri, probability metrikleri ve maliyet raporu üret.

## 10. Otomatik testler

```bash
pytest curriculum/tr/06-classical-machine-learning/03-logistic-regression-metrics-threshold-calibration/tests -q
```

Beklenen sonuç:

```text
36 passed
```

## Teslim artefaktları

- split özeti,
- model karşılaştırma tablosu,
- threshold tablosu,
- calibration tablosu,
- test metrik raporu,
- iş maliyeti gerekçesi,
- model ve preprocessing konfigürasyonu.
