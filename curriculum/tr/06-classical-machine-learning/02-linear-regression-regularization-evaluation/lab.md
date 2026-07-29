# Laboratuvar — Leakage-Safe Regresyon Sistemi

## Amaç

Sentetik konut verisi üzerinde sıfırdan ve scikit-learn tabanlı regresyon modellerini karşılaştırmak.

## Adımlar

1. `size_m2`, `room_count`, `age_years`, `distance_km`, `district` ve `price_try` kolonlarını üret.
2. Veriyi train/evaluation olarak ayır.
3. Mean baseline MAE ve RMSE değerlerini hesapla.
4. `NormalEquationRegressor` modelini fit et.
5. `GradientDescentRegressor` ile convergence geçmişini incele.
6. `build_regression_pipeline` ile sayısal imputation, scaling ve kategorik one-hot encoding uygula.
7. LinearRegression, Ridge, Lasso ve ElasticNet modellerini karşılaştır.
8. PolynomialFeatures + Ridge pipeline'ını değerlendir.
9. Residual summary, heteroskedasticity sinyali ve VIF raporu üret.
10. En kötü absolute residual'a sahip satırları ve district slice metriklerini raporla.

## Test

```bash
pytest curriculum/tr/06-classical-machine-learning/02-linear-regression-regularization-evaluation/tests -q
```

Beklenen sonuç:

```text
31 passed
```

## Teslimatlar

- model karşılaştırma tablosu,
- residual raporu,
- VIF tablosu,
- slice metrikleri,
- seçilen model ve gerekçesi,
- pipeline konfigürasyonu.
