# Laboratuvar — Sızıntısız Tabular Preprocessing

## Amaç

Müşteri verisi üzerinde veri kalitesi profili çıkaracak, eğitim verisinden imputation/clipping/encoding istatistikleri öğrenecek ve leakage kontrolleri uygulayacaksın.

## 1. Örnek veri

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "row_id": [1, 2, 3, 4, 5, 6],
        "event_at": [
            "2026-01-01", "2026-01-02", "2026-01-03",
            "2026-02-01", "2026-02-02", "2026-02-03",
        ],
        "age": [22, 35, None, 41, 999, 29],
        "income": [30000, 52000, 47000, None, 900000, 39000],
        "city": ["Ankara", "İzmir", None, "Ankara", "Bursa", "Yeni Şehir"],
        "converted": [0, 1, 0, 1, 1, 0],
        "post_outcome_score": [0.1, 0.9, 0.2, 0.8, 0.95, 0.15],
    }
)
```

## 2. Kalite profili

```python
from data_quality import missingness_report, profile_frame

print(profile_frame(customers))
print(missingness_report(customers))
```

Eksik kolonları, duplicate anahtarları ve iş kuralı ihlallerini ayrı raporla.

## 3. Zaman tabanlı split

```python
from leakage_audit import temporal_split

train, evaluation = temporal_split(
    customers,
    time_column="event_at",
    cutoff="2026-02-01",
)
```

Train ve evaluation satırlarının zaman sınırını elle doğrula.

## 4. Fit/transform pipeline

```python
from preprocessing_pipeline import TabularCleaner

cleaner = TabularCleaner(
    numeric_columns=("age", "income"),
    categorical_columns=("city",),
    rare_category_min_count=2,
)

x_train = cleaner.fit_transform(train)
x_evaluation = cleaner.transform(evaluation)

print(cleaner.medians_)
print(cleaner.bounds_)
print(cleaner.categories_)
print(x_train.columns)
```

Evaluation'daki `Yeni Şehir` değerinin `__OTHER__` kolonuna gittiğini kontrol et.

## 5. Leakage denetimi

```python
from leakage_audit import audit_feature_target_leakage

findings = audit_feature_target_leakage(
    customers,
    target_column="converted",
)
for finding in findings:
    print(finding)
```

`post_outcome_score` feature'ının neden üretimde kullanılamayacağını açıklayan kısa bir teknik not yaz.

## 6. Testler

```bash
pytest curriculum/tr/05-data-analysis-sql-data-engineering/04-data-cleaning-missing-outliers-encoding-leakage/tests -q
```

## 7. Beklenen rapor

Raporunda şunlar bulunmalı:

- Veri kalite özeti
- Eksik değer politikası ve gerekçesi
- Aykırı değer politikası ve gerekçesi
- Encoding sözlüğü
- Train/evaluation split kanıtı
- Leakage bulguları
- Fit istatistiklerinin yalnızca train'den geldiğini gösteren test
