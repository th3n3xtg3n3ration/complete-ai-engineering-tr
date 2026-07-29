# Ders 2 — Linear Regression, Regularization ve Regresyon Değerlendirmesi

**Seviye:** L2 · **Tahmini süre:** 24 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Simple ve multiple linear regression varsayımlarını açıklayabileceksin.
- Normal equation ve gradient descent ile linear regression geliştirebileceksin.
- MAE, MSE, RMSE, R² ve adjusted R² metriklerini yorumlayabileceksin.
- Ridge, Lasso ve Elastic Net regularization yöntemlerini karşılaştırabileceksin.
- Feature scaling ile regularization gücü arasındaki ilişkiyi açıklayabileceksin.
- Polynomial feature kullanarak doğrusal olmayan ilişkileri lineer modellerle temsil edebileceksin.
- Underfitting, overfitting ve bias–variance davranışını tanılayabileceksin.
- Residual, heteroskedasticity, multicollinearity ve influential-point kontrolleri uygulayabileceksin.
- Leakage-safe scikit-learn Pipeline ve ColumnTransformer kurabileceksin.
- Test edilen ve tekrarlanabilir bir regresyon değerlendirme raporu yayımlayabileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Sıfırdan lineer modeller](src/linear_models.py)
4. [Regresyon değerlendirme ve tanılama araçları](src/regression_diagnostics.py)
5. [Leakage-safe scikit-learn pipeline](src/regression_pipeline.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_regression.py)
11. [Metadata](metadata.yml)

## Kurulum ve çalıştırma

```bash
python -m pip install numpy pandas scikit-learn pytest
python curriculum/tr/06-classical-machine-learning/02-linear-regression-regularization-evaluation/src/linear_models.py
pytest curriculum/tr/06-classical-machine-learning/02-linear-regression-regularization-evaluation/tests -q
```

## Mini proje

Konut fiyatı veya talep tahmini için leakage-safe bir regresyon sistemi geliştireceksin. Sistem; sıfırdan normal equation ve gradient descent modellerini scikit-learn LinearRegression, Ridge, Lasso ve ElasticNet ile karşılaştıracak; polynomial feature, scaling ve cross-validation kullanacak; MAE, RMSE, R², adjusted R², residual dağılımı, heteroskedasticity sinyali, VIF ve en kötü hata dilimlerini raporlayacak. Model artefaktı, feature listesi, eğitim konfigürasyonu ve metrikler birlikte yayımlanacak.
