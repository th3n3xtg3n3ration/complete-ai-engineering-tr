# Ders 5 — SVM, Margin, Kernel ve Ölçekleme

**Seviye:** L2 · **Tahmini süre:** 24 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

- Maksimum margin, hard/soft margin ve hinge loss yaklaşımını açıklamak
- Linear, polynomial ve RBF kernel fonksiyonlarını uygulamak
- `C`, `gamma`, degree ve `coef0` etkilerini yorumlamak
- Feature scaling, class weight ve threshold tuning farkını göstermek
- OvR/OvO çok sınıflı stratejileri karşılaştırmak
- Probability calibration ve leakage-safe SVM pipeline geliştirmek

## Ders dosyaları

1. [Teori](theory.md)
2. [Laboratuvar](lab.md)
3. [Kernel araçları](src/kernel_functions.py)
4. [SVM model araçları](src/svm_models.py)
5. [Pipeline araçları](src/svm_pipeline.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_svm.py)
11. [Metadata](metadata.yml)

```bash
python -m pip install numpy pandas scikit-learn pytest
pytest curriculum/tr/06-classical-machine-learning/05-svm-margin-kernel-scaling/tests -q
```
