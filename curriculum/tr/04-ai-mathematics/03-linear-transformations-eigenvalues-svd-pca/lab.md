# Laboratuvar — Lineer Dönüşümlerden PCA'ya

## Amaç

Bu laboratuvarda geometrik dönüşümleri, power iteration yöntemini ve küçük bir PCA iş akışını saf Python ile uygulayacaksın.

## Bölüm 1 — Geometrik dönüşümler

1. `(2, 1)` vektörüne aşağıdaki dönüşümleri uygula:
   - x ekseninde 2 kat scaling
   - 90 derece rotation
   - x yönünde `k=0.5` shear
2. Her dönüşümden sonra vektör normunu hesapla.
3. Hangi dönüşümlerin uzunluğu koruduğunu açıkla.

## Bölüm 2 — Projection

1. `(3, 4)` vektörünü `(1, 1)` yönüne project et.
2. Projection ve residual vektörlerinin dot product'ının yaklaşık sıfır olduğunu doğrula.
3. Projection matrisini oluştur ve aynı sonucu verdiğini kontrol et.

## Bölüm 3 — Power iteration

Aşağıdaki simetrik matris için baskın eigenpair'i bul:

```python
matrix = [
    [4.0, 1.0],
    [1.0, 3.0],
]
```

1. 100 iterasyon çalıştır.
2. Rayleigh quotient ile eigenvalue hesapla.
3. `Av ≈ λv` ilişkisini kontrol et.
4. Farklı başlangıç vektörlerinin yakınsamaya etkisini incele.

## Bölüm 4 — Covariance

Aşağıdaki veri kümesini merkezle:

```python
data = [
    [2.5, 2.4],
    [0.5, 0.7],
    [2.2, 2.9],
    [1.9, 2.2],
    [3.1, 3.0],
    [2.3, 2.7],
    [2.0, 1.6],
    [1.0, 1.1],
    [1.5, 1.6],
    [1.1, 0.9],
]
```

1. Feature mean'lerini hesapla.
2. Covariance matrisini üret.
3. En yüksek varyans yönünü power iteration ile bul.

## Bölüm 5 — PCA

1. Veriyi bir principal component'e düşür.
2. Tekrar iki boyuta reconstruct et.
3. Mean squared reconstruction error hesapla.
4. Bir ve iki component için explained variance oranını karşılaştır.

## Bölüm 6 — Embedding senaryosu

En az 12 adet dört boyutlu sentetik embedding oluştur.

1. PCA'yı iki component ile fit et.
2. Embedding'leri dönüştür.
3. Orijinal ve düşürülmüş uzaylarda cosine similarity sıralamalarını karşılaştır.
4. İlk üç komşunun ne kadar korunduğunu ölç.
5. Sonuçları kısa bir teknik rapora dönüştür.

## Teslim kriterleri

- Kod shape doğrulaması yapmalı.
- Sıfır vektörü ve boş veri açık hata üretmeli.
- Rastgelelik kullanılıyorsa seed sabitlenmeli.
- PCA yalnızca training bölümünde fit edilmeli.
- En az 12 pytest testi yazılmalı.
- Sonuç raporunda explained variance ve reconstruction error birlikte yorumlanmalı.
