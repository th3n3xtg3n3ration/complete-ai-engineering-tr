# Laboratuvar — Bilgi Teorisi ve Matematik Capstone

## Amaç

Bu laboratuvarda entropi, cross-entropy, KL divergence, softmax ve calibration araçlarını çalıştıracak; ardından saf Python softmax regression modelini eğitip değerlendireceksin.

## Ön koşullar

Repository kökünde çalış:

```bash
python --version
pytest --version
```

Ders yolu:

```bash
cd curriculum/tr/04-ai-mathematics/08-entropy-cross-entropy-kl-divergence-math-capstone
```

## Bölüm 1 — Entropi deneyi

`src/information_theory.py` dosyasını çalıştır:

```bash
python src/information_theory.py
```

Aşağıdaki dağılımları karşılaştır:

```python
from src.information_theory import entropy

certain = (1.0, 0.0, 0.0, 0.0)
uniform = (0.25, 0.25, 0.25, 0.25)
skewed = (0.7, 0.1, 0.1, 0.1)

for distribution in (certain, uniform, skewed):
    print(distribution, entropy(distribution, base=2.0))
```

Beklenti:

- `certain` en düşük entropiye,
- `uniform` en yüksek entropiye,
- `skewed` ara bir değere sahip olmalıdır.

## Bölüm 2 — Cross-entropy ve KL ayrışımı

```python
from src.information_theory import cross_entropy, entropy, kl_divergence

p = (0.7, 0.2, 0.1)
q = (0.5, 0.3, 0.2)

left = cross_entropy(p, q)
right = entropy(p) + kl_divergence(p, q)
print(left, right, abs(left - right))
```

Farkın kayan nokta toleransı içinde sıfıra yakın olduğunu doğrula.

## Bölüm 3 — KL yönü

```python
from src.information_theory import kl_divergence

p = (0.9, 0.1)
q = (0.5, 0.5)

print("KL(P || Q):", kl_divergence(p, q))
print("KL(Q || P):", kl_divergence(q, p))
```

İki değerin neden farklı olduğunu yazılı olarak açıkla.

## Bölüm 4 — Sayısal kararlı softmax

```python
from src.information_theory import softmax

print(softmax((1000.0, 1001.0, 999.0)))
print(softmax((-1000.0, -999.0, -1001.0)))
```

Sonuçların sonlu ve toplamlarının bire yakın olduğunu doğrula.

## Bölüm 5 — Loss fonksiyonları

```bash
python src/classification_losses.py
```

Aşağıdaki deneyi ekle:

```python
from src.classification_losses import (
    categorical_cross_entropy_from_logits,
    label_smoothed_cross_entropy,
)

logits = (4.0, 1.0, -2.0)
print(categorical_cross_entropy_from_logits(0, logits))
print(label_smoothed_cross_entropy(0, logits, smoothing=0.1))
```

Label smoothing'in aşırı güvenli doğru tahmin üzerindeki loss'u neden artırabildiğini açıkla.

## Bölüm 6 — Focal loss

Kolay ve zor pozitif örneği karşılaştır:

```python
from src.classification_losses import focal_loss_binary_from_logits

print("easy:", focal_loss_binary_from_logits(1.0, 5.0))
print("hard:", focal_loss_binary_from_logits(1.0, -1.0))
```

`gamma` değerini `0`, `1`, `2` ve `4` yaparak sonuçları tabloya kaydet.

## Bölüm 7 — Capstone modelini çalıştır

```bash
python src/math_capstone.py
```

Beklenen davranış:

- final loss başlangıç loss'undan düşük olmalı,
- accuracy yüksek olmalı,
- confusion matrix çoğunlukla diagonal olmalı,
- ECE sıfır olmak zorunda değildir.

## Bölüm 8 — Hiperparametre karşılaştırması

Aşağıdaki deney matrisini uygula:

| Deney | Learning rate | L2 | Label smoothing |
|---|---:|---:|---:|
| A | 0.03 | 0.000 | 0.00 |
| B | 0.15 | 0.001 | 0.00 |
| C | 0.15 | 0.001 | 0.10 |
| D | 0.50 | 0.001 | 0.00 |

Her deney için raporla:

- initial loss,
- final loss,
- accuracy,
- ECE,
- ağırlıkların L2 normu,
- eğitim kararlılığı.

## Bölüm 9 — Distribution shift

Eğitim verisindeki tüm feature değerlerine sabit bir kayma ekleyerek yeni test kümesi oluştur:

```python
shifted = [[row[0] + 1.5, row[1] - 0.8] for row in x_values]
```

Orijinal ve shifted veri için:

- accuracy,
- ortalama predictive entropy,
- ECE

ölçümlerini karşılaştır.

## Bölüm 10 — Testleri çalıştır

```bash
pytest tests -q
```

Bir test başarısızsa önce hata mesajını oku; ardından giriş doğrulama, logaritma tabanı, tolerans ve seed ayarlarını kontrol et.

## Teslim çıktısı

Aşağıdakileri içeren kısa bir teknik rapor hazırla:

1. Entropi ve KL deneyleri
2. Softmax kararlılık kontrolü
3. Loss fonksiyonu karşılaştırması
4. Dört hiperparametre deneyinin tablosu
5. Distribution shift sonuçları
6. En az üç mühendislik çıkarımı
