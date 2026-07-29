# Teori — Lineer Dönüşümler, Özdeğer, Özvektör, SVD ve PCA

## 1. Lineer dönüşüm nedir?

Bir dönüşüm `T`, vektör toplamını ve skaler çarpmayı koruyorsa lineerdir:

```text
T(u + v) = T(u) + T(v)
T(cu) = cT(u)
```

Sonlu boyutlu uzaylarda lineer dönüşümler matrislerle temsil edilir. Bir vektörün dönüşümü:

```text
y = Ax
```

şeklindedir.

## 2. Geometrik dönüşümler

### Scaling

```text
[[sx, 0],
 [0, sy]]
```

### Rotation

```text
[[cos θ, -sin θ],
 [sin θ,  cos θ]]
```

### Shear

```text
[[1, k],
 [0, 1]]
```

### Projection

Birim bir `u` vektörü üzerine projection:

```text
proj_u(x) = (x · u)u
```

Projection matrisi:

```text
P = uuᵀ
```

## 3. Basis ve coordinate system

Bir basis, uzaydaki her vektörün benzersiz bir doğrusal birleşimle ifade edilmesini sağlar. Basis değişikliği veriyi değiştirmez; aynı geometrik nesnenin koordinat gösterimini değiştirir.

AI bağlamında özellik uzayı, embedding uzayı ve latent space birer koordinat sistemidir.

## 4. Rank ve null space

- **Rank:** Matrisin ürettiği bağımsız çıktı yönlerinin sayısıdır.
- **Null space:** `Ax = 0` koşulunu sağlayan vektörler kümesidir.

Rank düşüklüğü; redundant feature, sıkıştırılabilir veri veya eksik bilgi anlamına gelebilir.

## 5. Eigenvalue ve eigenvector

Bir `v` vektörü dönüşüm altında yalnızca ölçekleniyorsa:

```text
Av = λv
```

`v` bir eigenvector, `λ` ise eigenvalue'dur.

Yorum:

- Büyük mutlak eigenvalue: dönüşümün güçlü büyüttüğü yön.
- Küçük eigenvalue: zayıf veya ihmal edilebilir yön.
- Negatif eigenvalue: yön tersine döner.

## 6. Power iteration

Power iteration, baskın eigenvector'ü yaklaşık olarak bulur:

1. Rastgele veya sabit bir başlangıç vektörü seç.
2. `v ← Av` hesapla.
3. `v` vektörünü normalize et.
4. Yakınsayana kadar tekrarla.
5. Eigenvalue için Rayleigh quotient kullan:

```text
λ = (vᵀAv) / (vᵀv)
```

Yöntem en büyük mutlak eigenvalue'a karşılık gelen eigenvector'e yakınsar; başlangıç vektörünün bu yönde sıfır bileşeni olmaması gerekir.

## 7. SVD

Her uygun matris yaklaşık olarak:

```text
A = UΣVᵀ
```

şeklinde ayrıştırılabilir.

- `U`: çıktı uzayındaki ortonormal yönler
- `Σ`: singular value'lar
- `V`: girdi uzayındaki ortonormal yönler

SVD kullanım alanları:

- Düşük rank approximation
- Veri sıkıştırma
- Gürültü azaltma
- Latent semantic analysis
- Recommendation sistemleri
- Embedding compression

## 8. Covariance

Merkezlenmiş veri için covariance matrisi:

```text
C = XᵀX / (n - 1)
```

Diagonal elemanlar feature varyanslarını, diagonal dışı elemanlar feature'ların birlikte değişimini gösterir.

## 9. PCA

PCA, verideki en yüksek varyansı taşıyan ortogonal yönleri bulur.

Adımlar:

1. Veriyi doğrula.
2. Her feature'ın ortalamasını hesapla.
3. Veriyi merkezle.
4. Covariance matrisini oluştur.
5. En büyük eigenvalue/eigenvector çiftlerini bul.
6. Eigenvector'leri principal component olarak sırala.
7. Veriyi seçilen component'lere project et.

```text
Z = X_centered W
```

## 10. Explained variance

Bir component'in açıklanan varyans oranı:

```text
explained_ratio_i = λ_i / Σ λ_j
```

Toplam açıklanan varyans, seçilen boyut sayısının bilgi koruma kapasitesini gösterir.

## 11. Reconstruction

Düşürülmüş veri yaklaşık olarak eski uzaya döndürülebilir:

```text
X_reconstructed = ZWᵀ + mean
```

Reconstruction error, boyut indirgeme sonucundaki bilgi kaybını ölçer.

## 12. PCA ve SVD ilişkisi

Merkezlenmiş veri matrisi `X` için SVD uygulanırsa, `V` içindeki yönler PCA component'leriyle ilişkilidir. Singular value'ların karesi covariance eigenvalue'larıyla orantılıdır.

## 13. AI bağlamı

PCA ve SVD:

- Embedding boyutunu küçültür.
- Model girişlerini sıkıştırır.
- Gürültüyü azaltabilir.
- Görselleştirmeyi kolaylaştırır.
- Retrieval latency ve storage maliyetini düşürebilir.

Ancak boyut indirgeme semantik komşulukları bozabilir. Bu nedenle yalnızca explained variance değil, downstream görev metrikleri de ölçülmelidir.

## 14. Sayısal ve mühendislik riskleri

- Shape uyumsuzluğu
- Sıfır normlu vektör
- Simetrik olmayan covariance girdisi
- Yakın eigenvalue'larda yavaş convergence
- Floating-point yuvarlama hataları
- Çok küçük negatif eigenvalue'lar
- Yetersiz component sayısı
- Train/test veri sızıntısı

PCA yalnızca training data üzerinde fit edilmeli; aynı mean ve component matrisi validation/test verisine uygulanmalıdır.
