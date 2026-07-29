# Teori — NumPy Dizileri, Vektörleştirme ve Broadcasting

## 1. Neden NumPy?

Python listesi genel amaçlıdır: aynı koleksiyonda farklı türde nesneler tutabilir ve her eleman bir Python nesnesine işaret eder. NumPy dizisi ise çoğunlukla tek bir `dtype` ile, yoğun ve düzenli bir bellek bölgesinde çalışır. Bu düzen:

- daha az nesne ek yükü,
- daha iyi CPU cache kullanımı,
- C/Fortran seviyesinde döngüler,
- SIMD ve optimize edilmiş BLAS rutinleri

sayesinde büyük sayısal işlemleri hızlandırır.

Vektörleştirme “döngü yoktur” anlamına gelmez. Döngü Python yorumlayıcısından daha düşük seviyeli, optimize edilmiş koda taşınır.

## 2. ndarray anatomisi

Bir dizinin temel özellikleri:

- `shape`: her eksendeki uzunluklar
- `ndim`: eksen sayısı
- `size`: toplam eleman sayısı
- `dtype`: eleman türü
- `itemsize`: bir elemanın bayt cinsinden boyutu
- `nbytes`: veri tamponunun toplam boyutu
- `strides`: her eksende bir adım atmak için kaç bayt ilerlenmesi gerektiği

`shape=(100, 20)` olan bir matris, 100 gözlem ve 20 özellik olarak yorumlanabilir. Fakat NumPy bu semantiği bilmez; eksenlerin anlamını veri sözleşmesi belirler.

## 3. Dizi oluşturma ve dtype

Yaygın oluşturucular:

```python
np.array(...)
np.zeros(...)
np.ones(...)
np.full(...)
np.arange(...)
np.linspace(...)
np.eye(...)
np.random.default_rng(seed)
```

`dtype` seçimi doğruluk, bellek ve hız arasında bir dengedir. `float32`, derin öğrenmede yaygındır; ancak istatistiksel toplamlarda `float64` daha güvenli olabilir. Büyük integer değerlerini `float32`ye dönüştürmek hassasiyet kaybına yol açabilir.

## 4. İndeksleme, slicing ve maskeler

Temel slicing çoğu zaman **view** döndürür:

```python
view = matrix[:, :2]
view[0, 0] = 999
```

Bu değişiklik kaynak matrise yansıyabilir. Bağımsız veri gerekiyorsa açıkça `.copy()` kullanılır.

Boolean mask:

```python
valid = values[np.isfinite(values)]
```

Fancy indexing genellikle copy üretir:

```python
selected = values[[0, 3, 7]]
```

View/copy davranışını tahmin edemediğin kodda `np.shares_memory` ile kontrol yap.

## 5. Axis ve keepdims

İki boyutlu `X` için:

```python
X.sum(axis=0)  # sütunlar boyunca; her özellik için sonuç
X.sum(axis=1)  # satırlar boyunca; her gözlem için sonuç
```

`keepdims=True`, indirgenen ekseni uzunluğu 1 olan bir eksen olarak korur. Bu, broadcasting ile sonraki işlemleri kolaylaştırır:

```python
means = X.mean(axis=0, keepdims=True)
centered = X - means
```

## 6. Broadcasting

NumPy shape'leri sağdan sola karşılaştırır. İki boyut uyumludur:

1. eşitse veya
2. boyutlardan biri 1 ise.

Örnek:

- `(32, 128)` ile `(128,)` uyumludur.
- `(32, 128)` ile `(1, 128)` uyumludur.
- `(32, 128)` ile `(32, 1)` uyumludur.
- `(32, 128)` ile `(32,)` uyumlu değildir.

Broadcasting çoğu durumda fiziksel veri kopyalamadan sanal genişleme yapar. Ancak son işlem büyük bir geçici dizi üretebilir; bellek maliyetini ayrıca değerlendirmek gerekir.

## 7. Vektörleştirme kalıpları

Döngü:

```python
result = []
for value in values:
    result.append((value - mean) / std)
```

Vektörleştirilmiş sürüm:

```python
result = (values - mean) / std
```

Sık kullanılan kalıplar:

- element-wise işlem: `x * x`, `np.exp(x)`
- reduction: `sum`, `mean`, `max`
- koşullu seçim: `np.where`
- matris çarpımı: `@`
- broadcasting ile feature-wise dönüşüm
- batch similarity: normalize et ve `A @ B.T` kullan

Vektörleştirme her zaman otomatik olarak daha iyi değildir. Çok büyük geçici diziler, gereksiz kopyalar veya küçük verilerde çağrı maliyeti avantajı azaltabilir.

## 8. Sayısal kararlılık

Sayısal veri hattında şu kontroller önemlidir:

```python
np.isfinite(X)
np.isnan(X)
np.isinf(X)
```

Standard deviation sıfırsa bölme hatası oluşur. Üretim kodu açık bir politika seçmelidir:

- hata ver,
- paydayı 1 kabul et,
- özelliği kaldır,
- sabit özelliği ayrıca raporla.

Bu dersteki yardımcı fonksiyonlar varsayılan olarak sabit özellikte paydayı 1 yapar; böylece merkezlenmiş değerler sıfır olur.

## 9. Standardization ve min–max scaling

Standardization:

```text
z = (x - mean) / standard_deviation
```

Min–max scaling:

```text
scaled = (x - minimum) / (maximum - minimum)
```

Bu istatistikler yalnızca eğitim verisinden hesaplanmalıdır. Tüm veri üzerinde hesaplamak, doğrulama/test dağılımından bilgi sızdırır.

## 10. Benzerlik ve uzaklık

Cosine similarity:

```text
cos(a, b) = dot(a, b) / (norm(a) * norm(b))
```

Batch işleminde satırları normalize edip matris çarpımı yapılır:

```python
normalized = X / np.linalg.norm(X, axis=1, keepdims=True)
similarities = normalized @ normalized.T
```

Pairwise squared Euclidean distance:

```text
||a-b||^2 = ||a||^2 + ||b||^2 - 2 * dot(a, b)
```

Bu kimlik, üç boyutlu broadcast fark dizisi oluşturmadan mesafe matrisi hesaplamayı sağlar.

## 11. Fit/transform sözleşmesi

Üretim tipi bir transformer:

1. `fit(X_train)` ile istatistikleri öğrenir.
2. Öğrenilen state'i saklar.
3. `transform(X_valid)` ve `transform(X_test)` sırasında state'i değiştirmez.
4. Feature sayısı ve dtype gibi sözleşmeleri doğrular.
5. Fit edilmeden kullanımda açık hata verir.

Bu ayrım, scikit-learn pipeline'larının ve veri mühendisliği dönüşümlerinin temelidir.

## 12. Yaygın hatalar

- `axis` yönünü ters yorumlamak
- validation/test verisinde yeniden `fit` etmek
- basic slice'ın view olduğunu unutmak
- integer array'e float sonuç yazmak
- NaN içeren veride normal `mean` kullanmak
- broadcasting sonucu dev geçici diziler üretmek
- sabit özellikte sıfıra bölmek
- benchmark'ı tek ölçümle ve warm-up olmadan yorumlamak
- aynı seed kullanılmadan performans/doğruluk karşılaştırmak

## 13. Üretim kontrol listesi

- Input shape açıkça doğrulanıyor mu?
- `dtype` dönüşümü bilinçli mi?
- NaN/inf politikası belgelenmiş mi?
- State yalnızca training split'te öğreniliyor mu?
- Sabit sütunlar raporlanıyor mu?
- Fonksiyonlar input'u beklenmedik biçimde mutate ediyor mu?
- Büyük ara dizilerin bellek maliyeti ölçülüyor mu?
- Seed ve benchmark yöntemi tekrarlanabilir mi?
- Testler edge case'leri kapsıyor mu?
