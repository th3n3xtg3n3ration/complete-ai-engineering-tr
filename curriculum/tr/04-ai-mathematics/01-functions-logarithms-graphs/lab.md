# Laboratuvar — Fonksiyon Davranışlarını Ölçmek

## Amaç

Bu laboratuvarda fonksiyonları yalnızca formül olarak değil, çalışan ve ölçülebilen yazılım bileşenleri olarak inceleyeceksin. Saf Python implementasyonlarıyla domain doğrulama, sayısal kararlılık, örnekleme, yerel eğim ve loss davranışı üzerinde çalışacaksın.

## Ön koşullar

- Python 3.11+
- `pytest`
- Terminal kullanımı
- Fonksiyon ve temel liste bilgisi

Ders klasörünü çalışma dizini olarak kullanabilirsin:

```bash
cd curriculum/tr/04-ai-mathematics/01-functions-logarithms-graphs
```

## Bölüm 1 — Temel fonksiyon aileleri

Python REPL veya küçük bir script aç:

```python
from src.math_functions import exponential, linear, logarithm, polynomial

print(linear(4, slope=2.5, intercept=-3))
print(polynomial(3, [2, -3, 1]))
print(exponential(5, base=2))
print(logarithm(32, base=2))
```

Beklenen ilişkileri doğrula:

- `2.5 * 4 - 3 = 7`
- `2(3²) - 3(3) + 1 = 10`
- `2⁵ = 32`
- `log₂(32) = 5`

Ardından geçersiz domain denemeleri yap:

```python
from src.math_functions import logarithm

logarithm(0)
logarithm(-4)
logarithm(10, base=1)
```

Sorular:

1. Her çağrı neden reddediliyor?
2. Sessizce `NaN` döndürmek yerine exception üretmenin avantajı nedir?
3. Bu hata bir model servisinde hangi HTTP durum koduna dönüştürülebilir?

## Bölüm 2 — Bileşke ve ters fonksiyon

```python
from src.math_functions import compose, inverse_linear, linear, sigmoid

scale = lambda value: linear(value, slope=2, intercept=-1)
model = compose(sigmoid, scale)

for x in [-2, -1, 0, 1, 2]:
    print(x, model(x))

output = linear(4, slope=2.5, intercept=-3)
print(inverse_linear(output, slope=2.5, intercept=-3))
```

Bileşke sırasını kelimelerle açıkla: Önce hangi fonksiyon uygulanıyor? Çıktı neden `(0, 1)` aralığında kalıyor?

## Bölüm 3 — Aktivasyon eğrilerini üretmek

Deney aracını çalıştır:

```bash
python src/function_experiment.py
```

Varsayılan çıktı:

```text
generated/activation_curves.csv
```

İlk satırları incele:

```bash
python - <<'PY'
from pathlib import Path

path = Path("generated/activation_curves.csv")
for line in path.read_text(encoding="utf-8").splitlines()[:6]:
    print(line)
PY
```

Farklı örnekleme aralığı kullan:

```bash
python src/function_experiment.py \
  --start -4 \
  --stop 4 \
  --step 0.1 \
  --output generated/fine_curves.csv
```

CSV'yi tercih ettiğin görselleştirme aracında aç. Şu grafik çiftlerini karşılaştır:

- `x` — `sigmoid`
- `x` — `sigmoid_slope`
- `x` — `tanh`
- `x` — `tanh_slope`
- `x` — `relu`
- `x` — `softplus`

## Bölüm 4 — Doygunluk ve gradient sezgisi

```python
from src.math_functions import numerical_derivative, sigmoid, tanh

for x in [-10, -5, -2, 0, 2, 5, 10]:
    print(
        x,
        "sigmoid=", round(sigmoid(x), 6),
        "sigmoid_slope=", round(numerical_derivative(sigmoid, x), 6),
        "tanh_slope=", round(numerical_derivative(tanh, x), 6),
    )
```

Gözlemlerini yaz:

1. Sigmoid eğimi hangi noktada en büyüktür?
2. Büyük mutlak girdilerde eğime ne olur?
3. Çok katmanlı bir ağda küçük eğimlerin çarpılması hangi probleme yol açabilir?

## Bölüm 5 — Sayısal kararlılık deneyi

Kararlı implementasyonu dene:

```python
from src.math_functions import sigmoid, softmax, softplus

print(sigmoid(-1000))
print(sigmoid(1000))
print(softplus(-1000))
print(softplus(1000))
print(softmax([1000, 1001, 999]))
```

Sonra eğitim amaçlı kararsız sürümleri yaz:

```python
import math


def naive_sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def naive_softmax(values: list[float]) -> list[float]:
    exponents = [math.exp(value) for value in values]
    total = sum(exponents)
    return [value / total for value in exponents]
```

Aşırı girdilerde iki yaklaşımı karşılaştır. Kararsız kodun neden exception veya anlamsız değer ürettiğini açıklayan kısa bir not yaz.

## Bölüm 6 — Loss karşılaştırması

```python
from src.math_functions import binary_cross_entropy, mean_squared_error

targets = [1, 0, 1, 0]
models = {
    "good": [0.9, 0.1, 0.8, 0.2],
    "uncertain": [0.55, 0.45, 0.55, 0.45],
    "confident_wrong": [0.1, 0.9, 0.2, 0.8],
}

for name, predictions in models.items():
    print(
        name,
        "mse=", mean_squared_error(targets, predictions),
        "bce=", binary_cross_entropy(targets, predictions),
    )
```

Şu soruları cevapla:

- Hangi model en düşük loss değerine sahip?
- Kendinden emin yanlış tahmin BCE tarafından nasıl cezalandırılıyor?
- MSE ve BCE sıralaması aynı mı?
- Sınıflandırma olasılıklarında BCE neden daha doğal bir seçimdir?

## Bölüm 7 — Softmax ve skor kaydırma

```python
from src.math_functions import softmax

first = softmax([1, 2, 3])
second = softmax([101, 102, 103])

print(first)
print(second)
```

İki dağılımın aynı olmasını cebirsel olarak açıkla. Ardından sıcaklık parametresi ekle:

```python
def temperature_softmax(logits: list[float], temperature: float) -> list[float]:
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    return softmax([value / temperature for value in logits])
```

`temperature` değerlerini `0.5`, `1.0` ve `2.0` kullanarak karşılaştır. Dağılımın ne zaman daha keskin veya daha düz olduğunu raporla.

## Bölüm 8 — Testleri çalıştırmak

```bash
pytest tests -q
```

Kapsamı incelemek için ortamında `pytest-cov` varsa:

```bash
pytest tests --cov=src --cov-report=term-missing
```

## Teslim çıktısı

Laboratuvar sonunda şu dosyaları üret:

```text
generated/
├── activation_curves.csv
├── fine_curves.csv
└── observations.md
```

`observations.md` en az şu bölümleri içermeli:

- Domain hataları
- Aktivasyon karşılaştırması
- Doygunluk ve yerel eğim
- Sayısal kararlılık
- MSE ve cross-entropy karşılaştırması
- Softmax temperature gözlemleri

## Başarı kriterleri

- Tüm testler geçiyor.
- Aşırı girdiler kararlı biçimde işleniyor.
- Grafik verisi tekrarlanabilir komutla üretiliyor.
- Matematiksel davranış yalnızca tarif edilmiyor; deney çıktılarıyla destekleniyor.
