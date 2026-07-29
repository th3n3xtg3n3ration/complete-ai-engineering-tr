# Ders 4 — Decision Tree, Random Forest, Gradient Boosting ve Ensemble

**Seviye:** L2 · **Tahmini süre:** 26 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- CART tabanlı karar ağaçlarını split, impurity ve leaf prediction üzerinden açıklayabileceksin.
- Gini, entropy, information gain ve regresyon varyans azaltımını hesaplayabileceksin.
- `max_depth`, `min_samples_leaf` ve cost-complexity pruning ile model karmaşıklığını kontrol edebileceksin.
- Bagging, random subspace ve bootstrap örneklemenin random forest davranışına etkisini yorumlayabileceksin.
- Out-of-bag değerlendirme ile ek bir validation sinyali üretebileceksin.
- Gradient boosting ve AdaBoost algoritmalarını ardışık hata düzeltme mantığıyla açıklayabileceksin.
- Bagging ile boosting arasındaki bias–variance farkını karşılaştırabileceksin.
- Voting ve stacking ensemble'ları kurabileceksin.
- Impurity importance ile permutation importance arasındaki farkları yorumlayabileceksin.
- Cross-validation, generalization gap ve slice analizi içeren güvenilir ensemble raporu yayımlayabileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Karar ağacı araçları](src/tree_models.py)
4. [Ensemble model araçları](src/ensemble_models.py)
5. [Değerlendirme araçları](src/ensemble_evaluation.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_ensembles.py)
11. [Metadata](metadata.yml)

## Kurulum ve çalıştırma

```bash
python -m pip install numpy pandas scikit-learn pytest
pytest curriculum/tr/06-classical-machine-learning/04-decision-tree-random-forest-gradient-boosting-ensemble/tests -q
```

## Mini proje

Bir churn veya risk sınıflandırma problemi için decision tree, random forest, AdaBoost, gradient boosting, voting ve stacking modellerini leakage-safe split üzerinde karşılaştıracaksın. Proje; pruning, OOB skor, cross-validation, generalization gap, permutation importance, threshold değerlendirmesi ve segment bazlı hata analizini tek raporda birleştirecek.
