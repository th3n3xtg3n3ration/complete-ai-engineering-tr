# Laboratuvar — NumPy ile Sızıntısız Sayısal Veri Hattı

## Amaç

Bu laboratuvarda ham sayısal veriyi inceleyecek, vektörleştirecek, eksik değerleri eğitim istatistikleriyle dolduracak ve train/validation ayrımına saygılı bir pipeline kuracaksın.

## 1. Ortam

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install numpy pytest
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 2. Sentetik veri üret

```python
import numpy as np

rng = np.random.default_rng(42)
X = rng.normal(size=(1_000, 6))
X[:, 1] *= 100.0
X[:, 2] += 50.0
X[rng.choice(len(X), 40, replace=False), 3] = np.nan
X[0, 4] = 1_000.0
```

İncele:

```python
print(X.shape, X.dtype, X.nbytes)
print(np.sum(~np.isfinite(X), axis=0))
```

## 3. Axis deneyi

Aşağıdaki sonuçların shape'ini kodu çalıştırmadan tahmin et:

```python
X.mean(axis=0)
X.mean(axis=0, keepdims=True)
X.mean(axis=1)
X[:, None, :].shape
```

Sonra çalıştır ve tahminini doğrula.

## 4. View/copy deneyi

```python
sample = np.arange(12).reshape(3, 4)
view = sample[:, :2]
copy = sample[:, [0, 1]]

print(np.shares_memory(sample, view))
print(np.shares_memory(sample, copy))
```

Her iki alt diziyi değiştirip kaynak diziye etkisini gözlemle.

## 5. Broadcasting

Özellik bazında merkezleme:

```python
means = np.nanmean(X, axis=0, keepdims=True)
centered = X - means
```

Her sütunun yaklaşık sıfır ortalamaya sahip olduğunu doğrula.

## 6. Pipeline

```python
from feature_pipeline import NumericFeaturePipeline

train, valid = X[:800], X[800:]

pipeline = NumericFeaturePipeline(clip_quantiles=(0.01, 0.99))
pipeline.fit(train)

train_ready = pipeline.transform(train)
valid_ready = pipeline.transform(valid)

print(train_ready.shape, valid_ready.shape)
print(np.isfinite(train_ready).all())
print(np.isfinite(valid_ready).all())
```

Kontrol et:

- `valid` üzerinde `fit` çağrılmadı.
- Feature sayısı korunuyor.
- Çıktıda NaN/inf yok.
- Eğitim çıktısının sütun ortalamaları yaklaşık sıfır.
- Aykırı değer clipping sonrası sınırlandı.

## 7. Similarity ve distance

```python
from numpy_foundations import cosine_similarity_matrix, pairwise_squared_euclidean

vectors = train_ready[:10]
cosine = cosine_similarity_matrix(vectors)
distance = pairwise_squared_euclidean(vectors)

print(np.diag(cosine))
print(np.diag(distance))
```

Beklentiler:

- cosine diagonal yaklaşık 1,
- distance diagonal yaklaşık 0,
- distance matrisi simetrik.

## 8. Benchmark

```python
from vectorization_benchmark import run_benchmark

report = run_benchmark(size=500_000, repeats=5, seed=42)
print(report)
```

Tek bir koşudan kesin sonuç çıkarma. CPU frekansı, arka plan süreçleri, veri boyutu ve warm-up ölçümü etkiler.

## 9. Veri sızıntısı deneyi

Validation verisine büyük bir sabit ekle:

```python
shifted_valid = valid + 1_000.0
```

İki yaklaşımı karşılaştır:

1. Pipeline'ı train'de fit edip shifted validation'a transform et.
2. Pipeline'ı train+validation birleşiminde fit et.

İkinci yaklaşım validation dağılımını preprocessing state'ine taşıdığı için sızıntılıdır.

## 10. Teslim

Aşağıdakileri raporla:

- Input ve output shape/dtype
- Eksik değer sayıları
- Sabit ve düşük varyanslı özellikler
- Train/validation istatistiklerinin ayrılması
- Loop ve vectorized benchmark medyanları
- Cosine ve distance invariant kontrolleri
- En az üç edge case testi
