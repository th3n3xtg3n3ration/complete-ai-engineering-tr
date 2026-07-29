# Laboratuvar — Tekrarlanabilir EDA Raporu

## Amaç

Sentetik müşteri verisi üzerinde otomatik EDA raporu üretmek ve çıktıları analitik açıdan yorumlamak.

## 1. Ortam

```bash
python -m pip install numpy pandas matplotlib pytest
```

## 2. Demo veriyi üret

```python
from eda_report import make_demo_data

frame = make_demo_data(row_count=500, seed=42)
print(frame.head())
print(frame.shape)
```

## 3. Yapısal profil

```python
from eda_foundations import profile_frame

profile = profile_frame(frame)
print(profile)
```

Missing hücre, dtype ve bellek bilgilerini yorumla.

## 4. Sayısal özet

```python
from eda_foundations import numeric_summary

summary = numeric_summary(
    frame,
    ["age", "annual_income", "tenure_months"],
)
print(summary)
```

Mean, median, IQR ve skew değerlerini karşılaştır.

## 5. Kategorik özet

```python
from eda_foundations import categorical_summary

print(categorical_summary(frame, ["segment", "region"]))
```

Sınıf oranlarının dengeli olup olmadığını değerlendir.

## 6. Korelasyon ve aykırı değer

```python
from eda_foundations import correlation_pairs, outlier_summary_iqr

print(correlation_pairs(frame, ["age", "annual_income", "tenure_months"]))
print(outlier_summary_iqr(frame, ["age", "annual_income", "tenure_months"]))
```

Yüksek korelasyon görürsen nedensellik iddiasında bulunmadan olası mekanizmaları listele.

## 7. Segment analizi

```python
from eda_foundations import segment_summary

print(
    segment_summary(
        frame,
        segment_columns=["segment"],
        metric_columns=["annual_income", "tenure_months"],
    )
)
```

Her segmentin count değerini raporla.

## 8. Grafik üretimi

```python
from visualization import (
    category_bar_figure,
    correlation_heatmap_figure,
    histogram_figure,
    missingness_figure,
    save_figure,
)

save_figure(histogram_figure(frame, "annual_income"), "output/income.png")
save_figure(category_bar_figure(frame, "segment"), "output/segment.png")
save_figure(
    correlation_heatmap_figure(
        frame,
        ["age", "annual_income", "tenure_months"],
    ),
    "output/correlation.png",
)
save_figure(missingness_figure(frame), "output/missingness.png")
```

## 9. Uçtan uca rapor

```python
from eda_report import EDAConfig, generate_eda_report

config = EDAConfig(
    numeric_columns=("age", "annual_income", "tenure_months"),
    categorical_columns=("segment", "region"),
    segment_columns=("segment",),
    target_column="churned",
)

artifacts = generate_eda_report(frame, "eda-output", config)
for name, path in artifacts.items():
    print(name, path)
```

## 10. Doğrulama

```bash
pytest curriculum/tr/05-data-analysis-sql-data-engineering/05-exploratory-data-analysis-visualization/tests -q
```

Beklenen sonuç: 23 test geçer.

## 11. Teknik rapor

Şunları yaz:

1. En önemli üç kalite bulgusu
2. En çarpık iki değişken
3. En güçlü iki korelasyon
4. Segmentler arasındaki en belirgin fark
5. Hedef dağılımı riski
6. Bir sonraki veri toplama veya modelleme adımı
