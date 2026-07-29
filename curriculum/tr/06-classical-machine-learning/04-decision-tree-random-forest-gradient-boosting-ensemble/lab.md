# Laboratuvar — Ensemble Model Karşılaştırması

## Amaç

Aynı veri ve aynı split üzerinde decision tree, random forest, AdaBoost, gradient boosting, voting ve stacking modellerini karşılaştırmak.

## Adımlar

1. En az 2.000 satırlık dengesiz bir binary classification veri seti üret.
2. Train, validation ve test ayrımı yap.
3. Derin bir decision tree eğit ve train–validation farkını ölç.
4. `max_depth`, `min_samples_leaf` ve `ccp_alpha` deneyleri yap.
5. Random forest eğit; validation ve OOB skorlarını karşılaştır.
6. AdaBoost, GradientBoosting ve HistGradientBoosting modellerini değerlendir.
7. Soft voting ve stacking kur.
8. ROC-AUC, average precision, log loss, balanced accuracy ve F1 raporla.
9. Impurity ve permutation importance sıralamalarını karşılaştır.
10. En kötü performans gösteren veri dilimini analiz et.
11. Seçilen modeli test setine yalnızca bir kez uygula.
12. Tekrarlanabilir model karşılaştırma raporu yayımla.

## Test

```bash
pytest curriculum/tr/06-classical-machine-learning/04-decision-tree-random-forest-gradient-boosting-ensemble/tests -q
```

Beklenen sonuç: `32 passed`.
