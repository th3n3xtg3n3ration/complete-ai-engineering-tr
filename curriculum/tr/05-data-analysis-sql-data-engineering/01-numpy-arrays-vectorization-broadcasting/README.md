# Ders 1 — NumPy Dizileri, Vektörleştirme ve Broadcasting

**Seviye:** L2 · **Tahmini süre:** 18 saat · **Durum:** Tamamlandı

## Öğrenme hedefleri

Bu dersin sonunda:

- Python listeleri ile NumPy `ndarray` arasındaki bellek ve yürütme farklarını açıklayabileceksin.
- `shape`, `ndim`, `size`, `dtype`, `itemsize`, `strides` ve bellek düzenini yorumlayabileceksin.
- Dizi oluşturma, indeksleme, slicing, boolean mask ve fancy indexing işlemlerini güvenli biçimde uygulayabileceksin.
- `axis`, aggregation ve `keepdims` davranışını çok boyutlu veriler üzerinde açıklayabileceksin.
- Broadcasting kurallarını tahmin edip shape uyuşmazlıklarını teşhis edebileceksin.
- Python döngülerini vektörleştirilmiş NumPy işlemlerine dönüştürebileceksin.
- View ve copy farkını, beklenmeyen mutasyon riskleriyle birlikte açıklayabileceksin.
- NaN ve sonsuz değerleri tespit edip sayısal veri kalitesini kontrol edebileceksin.
- Standardization, min–max scaling, cosine similarity ve pairwise distance işlemlerini uygulayabileceksin.
- Eğitim verisine `fit`, yeni veriye `transform` uygulayan sızıntısız bir sayısal özellik hattı geliştirebileceksin.

## Ders dosyaları

1. [Ayrıntılı teori](theory.md)
2. [Uygulama laboratuvarı](lab.md)
3. [NumPy temel araçları](src/numpy_foundations.py)
4. [Vektörleştirme benchmark'ı](src/vectorization_benchmark.py)
5. [Sayısal özellik hattı](src/feature_pipeline.py)
6. [Alıştırmalar](exercises.md)
7. [Quiz](quiz.md)
8. [Ödev ve rubrik](assignment.md)
9. [Mülakat soruları](interview-questions.md)
10. [Testler](tests/test_numpy_foundations.py)
11. [Metadata](metadata.yml)

## Kurulum ve çalıştırma

```bash
python -m pip install numpy pytest
python curriculum/tr/05-data-analysis-sql-data-engineering/01-numpy-arrays-vectorization-broadcasting/src/numpy_foundations.py
python curriculum/tr/05-data-analysis-sql-data-engineering/01-numpy-arrays-vectorization-broadcasting/src/vectorization_benchmark.py
python curriculum/tr/05-data-analysis-sql-data-engineering/01-numpy-arrays-vectorization-broadcasting/src/feature_pipeline.py
pytest curriculum/tr/05-data-analysis-sql-data-engineering/01-numpy-arrays-vectorization-broadcasting/tests -q
```

## Mini proje

Saf NumPy ile yeniden kullanılabilir bir sayısal veri hazırlama paketi geliştireceksin. Paket; eksik değer doldurma, clipping, standardization, cosine similarity ve pairwise distance işlemlerini kapsayacak. Pipeline yalnızca eğitim verisinde `fit` edilecek; doğrulama ve test verisine aynı istatistikler uygulanarak veri sızıntısı engellenecek. Döngü tabanlı ve vektörleştirilmiş sürümlerin çalışma süresi ile doğruluğu karşılaştırılacak.
