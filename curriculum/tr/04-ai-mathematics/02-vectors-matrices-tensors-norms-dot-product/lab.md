# Laboratuvar — Lineer Cebir ve Embedding Benzerliği

## Amaç

Bu laboratuvarda saf Python ile vektör ve matris işlemlerini çalıştıracak, shape hatalarını bilinçli olarak üretecek ve küçük bir embedding arama deneyini yorumlayacaksın.

## Ön koşullar

- Python 3.11+
- `pytest`
- Dersin `src/` ve `tests/` dosyaları

## Bölüm 1 — Vektör aritmetiği

Python REPL veya küçük bir script aç:

```python
from linear_algebra import dot, l1_norm, l2_norm, normalize, vector_add

left = [1.0, 2.0, 3.0]
right = [4.0, 5.0, 6.0]

print(vector_add(left, right))
print(dot(left, right))
print(l1_norm(left))
print(l2_norm(left))
print(normalize(left))
```

Kontrol et:

- Dot product sonucu neden skalerdir?
- Normalize edilmiş vektörün L2 normu neden yaklaşık 1'dir?
- L1 ve L2 normları aynı büyüklük kavramını neden farklı ölçer?

## Bölüm 2 — Shape uyumluluğu

Aşağıdaki işlemleri dene:

```python
from linear_algebra import matrix_multiply

valid = matrix_multiply(
    [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
    [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],
)
print(valid)
```

Shape akışı:

```text
(2, 3) @ (3, 2) -> (2, 2)
```

Şimdi iç boyutları boz:

```python
matrix_multiply([[1.0, 2.0]], [[1.0, 2.0]])
```

Beklenen sonuç sessiz ve yanlış bir matris değil, açıklayıcı bir `ValueError` olmalıdır.

## Bölüm 3 — Tensor shape ve reshape

```python
from linear_algebra import flatten_tensor, reshape, tensor_shape

tensor = [
    [[1, 2], [3, 4]],
    [[5, 6], [7, 8]],
]

print(tensor_shape(tensor))
flat = flatten_tensor(tensor)
print(flat)
print(reshape(flat, (2, 2, 2)))
```

Ardından ragged veri dene:

```python
tensor_shape([[1, 2], [3]])
```

Ragged yapıların neden batch işlemlerinde sorun çıkardığını kısa notla açıkla.

## Bölüm 4 — Cosine similarity ve Euclidean distance

```python
from linear_algebra import cosine_similarity, euclidean_distance

query = [1.0, 0.0]
same_direction = [10.0, 0.0]
nearby = [0.9, 0.1]

print(cosine_similarity(query, same_direction))
print(euclidean_distance(query, same_direction))
print(cosine_similarity(query, nearby))
print(euclidean_distance(query, nearby))
```

Yorumla:

- `same_direction` cosine açısından neden mükemmel benzer olabilir?
- Euclidean distance neden büyüklük farkını cezalandırır?
- Embedding retrieval probleminde hangi metriğin daha uygun olduğu neye bağlıdır?

## Bölüm 5 — Embedding deneyi

Ders klasörünün kökünden:

```bash
python src/embedding_experiment.py --output embedding_results.csv
```

CSV içinde dört deney grubu bulunur:

1. cosine, normalize edilmemiş
2. Euclidean, normalize edilmemiş
3. cosine, normalize edilmiş
4. Euclidean, normalize edilmiş

Her grup için ilk üç dokümanı çıkar ve şu tabloyu doldur:

| Metrik | Normalize | İlk sonuç | İkinci sonuç | Üçüncü sonuç |
|---|---|---|---|---|
| Cosine | Hayır |  |  |  |
| Euclidean | Hayır |  |  |  |
| Cosine | Evet |  |  |  |
| Euclidean | Evet |  |  |  |

## Bölüm 6 — Dense layer simülasyonu

Bir batch girdisini ağırlık matrisiyle çarp ve bias ekle:

```python
from linear_algebra import add_bias, matrix_multiply

inputs = [
    [1.0, 0.5, -1.0],
    [0.0, 2.0, 1.0],
]
weights = [
    [0.2, 0.8],
    [-0.4, 0.1],
    [0.6, -0.3],
]
bias = [0.1, -0.2]

outputs = add_bias(matrix_multiply(inputs, weights), bias)
print(outputs)
```

Shape akışını yaz:

```text
inputs:  (?, ?)
weights: (?, ?)
output:  (?, ?)
bias:    (?,)
```

## Bölüm 7 — Testleri çalıştır

```bash
pytest tests -q
```

Ardından bilinçli olarak `dot` fonksiyonundaki boyut kontrolünü kaldır, testlerin hangi hatayı yakaladığını gözlemle ve değişikliği geri al.

## Teslim çıktıları

- `embedding_results.csv`
- Dense layer shape açıklaması
- Cosine ve Euclidean karşılaştırması
- Normalizasyonun sıralamaya etkisini anlatan 300–500 kelimelik teknik not
- Başarılı pytest çıktısı

## Kontrol listesi

- [ ] Shape kurallarını işlem öncesinde yazdım.
- [ ] Sıfır vektörü edge case'ini denedim.
- [ ] Ragged tensör hatasını gözlemledim.
- [ ] Dört embedding deneyini karşılaştırdım.
- [ ] Normalizasyonun bilgi kaybı oluşturabileceği durumu açıkladım.
- [ ] Tüm testleri çalıştırdım.
