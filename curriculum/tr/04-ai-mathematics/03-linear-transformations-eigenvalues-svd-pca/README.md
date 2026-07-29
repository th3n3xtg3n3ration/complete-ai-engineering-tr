# Ders 3 — Lineer Dönüşümler, Özdeğer, Özvektör, SVD ve PCA

**Seviye:** L2 · **Tahmini süre:** 18 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Lineer dönüşüm kavramını geometrik ve cebirsel olarak açıklayabileceksin.
- Rotation, scaling, shear ve projection dönüşümlerini matrislerle uygulayabileceksin.
- Basis, coordinate system, rank ve null space kavramlarını yorumlayabileceksin.
- Eigenvalue ve eigenvector kavramlarını model dinamikleriyle ilişkilendirebileceksin.
- Power iteration algoritmasını saf Python ile uygulayabileceksin.
- SVD'nin veri sıkıştırma ve boyut indirgeme bağlamındaki rolünü açıklayabileceksin.
- PCA adımlarını merkezleme, covariance, bileşen seçimi ve projection olarak kurabileceksin.
- Embedding boyut indirgeme ve bilgi kaybı analizi yapabileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [Lineer dönüşümler](src/linear_transformations.py)
4. [Power iteration](src/power_iteration.py)
5. [Sıfırdan PCA](src/pca_from_scratch.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_advanced_linear_algebra.py)
11. [Metadata](metadata.yml)

## Çalıştırma

```bash
python curriculum/tr/04-ai-mathematics/03-linear-transformations-eigenvalues-svd-pca/src/linear_transformations.py
python curriculum/tr/04-ai-mathematics/03-linear-transformations-eigenvalues-svd-pca/src/power_iteration.py
python curriculum/tr/04-ai-mathematics/03-linear-transformations-eigenvalues-svd-pca/src/pca_from_scratch.py
pytest curriculum/tr/04-ai-mathematics/03-linear-transformations-eigenvalues-svd-pca/tests -q
```

## Mini proje

Saf Python ile küçük bir PCA paketi geliştirecek; sentetik embedding verisini daha düşük boyuta projekte edip açıklanan varyans, reconstruction error ve arama sıralaması değişimini teknik bir raporla analiz edeceksin.
