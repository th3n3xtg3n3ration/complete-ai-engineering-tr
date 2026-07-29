# Ödev — Güvenilir Konut Fiyatı Regresyonu

## Senaryo

Bir emlak platformu, ilan yayınlanmadan önce önerilen fiyatı Türk lirası cinsinden tahmin etmek istiyor.

## Görev

Leakage-safe ve test edilen bir regresyon sistemi geliştir.

## Zorunlu teslimatlar

1. Problem ve prediction-time tanımı
2. Train/evaluation split
3. Mean ve median baseline
4. LinearRegression, Ridge, Lasso ve ElasticNet karşılaştırması
5. Polynomial + Ridge deneyi
6. Cross-validation sonuçları
7. MAE, RMSE, R² ve adjusted R²
8. Residual ve heteroskedasticity analizi
9. VIF veya katsayı kararlılığı raporu
10. Bölge ve fiyat dilimi slice analizi
11. Model/pipeline artefaktı
12. En az 20 otomatik test

## Rubrik

| Boyut | Puan |
|---|---:|
| Problem ve veri bölme | 10 |
| Leakage-safe preprocessing | 15 |
| Model uygulamaları | 20 |
| Regularization karşılaştırması | 15 |
| Metrik ve residual analizi | 15 |
| Multicollinearity ve slice analizi | 10 |
| Testler ve tekrarlanabilirlik | 10 |
| Teknik rapor | 5 |
| **Toplam** | **100** |
