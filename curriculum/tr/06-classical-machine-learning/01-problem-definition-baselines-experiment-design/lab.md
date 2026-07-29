# Laboratuvar — Güvenilir Bir Baseline Deneyi

## Amaç

Bir müşteri churn veri seti için model eğitmeden önce problem sözleşmesi, split stratejisi, baseline, metrik ve deney kaydı oluşturmak.

## 1. Ortam

```bash
python -m pip install numpy pandas scikit-learn pytest
```

## 2. Sentetik veri

`customer_id`, `snapshot_at`, `age`, `tenure_months`, `monthly_spend`, `support_ticket_count` ve `churned` alanlarını içeren en az 500 satırlık bir tablo üret. Aynı müşterinin birden fazla snapshot'ı varsa random split'in neden riskli olduğunu ayrıca göster.

## 3. Problem sözleşmesi

`ProblemDefinition` ile binary classification görevi, positive label, feature listesi, entity kolonları ve timestamp kolonunu tanımla.

## 4. Veri doğrulama

Eksik kolon, eksik target, sınıf sayısı, duplicate entity ve geçersiz timestamp kontrollerini çalıştır. Her hata için beklenen exception davranışını gözlemle.

## 5. Üç split karşılaştırması

Aynı veri üzerinde random, temporal ve entity split oluştur. Train/evaluation satır sayılarını, sınıf oranlarını ve entity overlap durumunu raporla.

## 6. Baseline

Training target üzerinde class-prior baseline fit et. Evaluation tarafında accuracy, balanced accuracy, precision, recall, F1, ROC-AUC ve log loss hesapla.

## 7. Metrik seçimi

İş senaryosu için birincil metrik, guardrail metrikler, minimum kabul eşiği ve metric direction belirle. Seçimini teknik ve iş gerekçesiyle yaz.

## 8. Bootstrap

Evaluation satırları üzerinde birincil metriğin %95 bootstrap güven aralığını üret. Yalnızca point estimate paylaşmanın neden yetersiz olduğunu açıkla.

## 9. Deney kaydı

`ExperimentResult` nesnesini JSON olarak kaydet ve yeniden yükle. Deney adı, problem adı, split, satır sayıları, baseline, metrikler ve seed alanlarını doğrula.

## 10. Testler

```bash
pytest curriculum/tr/06-classical-machine-learning/01-problem-definition-baselines-experiment-design/tests -q
```

Beklenen sonuç:

```text
27 passed
```

## Teslim artefaktları

- problem sözleşmesi,
- split karşılaştırma tablosu,
- baseline metrik raporu,
- bootstrap güven aralığı,
- deney JSON kaydı,
- leakage risk notu.
