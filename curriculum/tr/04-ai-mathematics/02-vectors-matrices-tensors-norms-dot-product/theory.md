# Teori — Vektörler, Matrisler, Tensörler, Normlar ve Dot Product

## 1. Neden lineer cebir?

Yapay zekâ sistemleri metin, görüntü, ses ve tablo verisini sayısal yapılara dönüştürür. Bir metin embedding'i bir vektör, gri tonlu bir görüntü bir matris, renkli görüntü veya batch halinde veri ise daha yüksek boyutlu bir tensör olarak temsil edilir. Bu nedenle lineer cebir, model mimarisinin ve veri akışının ortak dilidir.

## 2. Skaler, vektör, matris ve tensör

- **Skaler:** Tek bir sayı. Örnek: learning rate `0.001`.
- **Vektör:** Sıralı sayı listesi. Örnek: bir örneğin özellikleri `[age, income, score]`.
- **Matris:** Satır ve sütunlardan oluşan iki boyutlu yapı. Örnek: `batch_size × feature_count` veri matrisi.
- **Tensör:** Sıfır veya daha fazla ekseni olan genel sayı dizisi. Skaler rank-0, vektör rank-1, matris rank-2 tensördür.

## 3. Shape, rank ve axis

Bir tensörün **shape** bilgisi her eksendeki eleman sayısını gösterir.

- `(4,)`: dört elemanlı vektör
- `(32, 128)`: 32 örnek ve 128 özellik
- `(16, 3, 224, 224)`: 16 görüntü, 3 kanal, 224×224 piksel
- `(8, 512, 768)`: 8 sequence, 512 token, 768 hidden dimension

**Rank**, eksen sayısıdır. `(8, 512, 768)` shape'ine sahip tensör rank-3'tür.

Bir **axis**, işlem yapılan yönü belirtir. Örneğin `(batch, token, hidden)` tensöründe:

- axis 0: batch örnekleri
- axis 1: token konumları
- axis 2: temsil özellikleri

## 4. Vektör işlemleri

İki vektörün toplanabilmesi için boyutları aynı olmalıdır:

\[
[1,2,3] + [4,5,6] = [5,7,9]
\]

Skaler çarpma her bileşeni aynı sayı ile çarpar:

\[
2[1,2,3] = [2,4,6]
\]

### Dot product

İki eşit boyutlu vektörün dot product'ı karşılıklı bileşen çarpımlarının toplamıdır:

\[
a \cdot b = \sum_i a_i b_i
\]

Örnek:

\[
[1,2,3] \cdot [4,5,6] = 1\times4 + 2\times5 + 3\times6 = 32
\]

Dot product; benzerlik, projeksiyon, attention score ve lineer katmanların temelinde bulunur.

### Outer product

Bir `m` boyutlu vektör ile `n` boyutlu vektörün outer product'ı `m × n` matris üretir:

\[
(a \otimes b)_{ij} = a_i b_j
\]

Bu işlem özellik etkileşimleri ve bazı gradient hesaplarında görülür.

## 5. Matris işlemleri

### Toplama

İki matris yalnızca aynı shape'e sahipse eleman bazında toplanabilir.

### Transpose

Transpose satırları sütun, sütunları satır yapar:

\[
A \in \mathbb{R}^{m\times n} \Rightarrow A^T \in \mathbb{R}^{n\times m}
\]

### Matrix multiplication

`A` matrisi `(m, n)`, `B` matrisi `(n, p)` shape'ine sahipse sonuç `(m, p)` olur:

\[
C_{ij} = \sum_k A_{ik} B_{kj}
\]

İç boyutların eşit olması zorunludur. Bu kural model katmanlarında shape hatalarını anlamanın temelidir.

Bir dense katmanda:

- input: `(batch, input_features)`
- weights: `(input_features, output_features)`
- output: `(batch, output_features)`

## 6. Normlar

Norm, bir vektörün büyüklüğünü ölçer.

### L1 norm

\[
\lVert x \rVert_1 = \sum_i |x_i|
\]

L1 norm, sparsity teşvik eden regularization yaklaşımlarında kullanılır.

### L2 norm

\[
\lVert x \rVert_2 = \sqrt{\sum_i x_i^2}
\]

Euclidean uzunluk olarak da düşünülebilir. Weight decay ve embedding normalizasyonunda sık görülür.

### Infinity norm

\[
\lVert x \rVert_\infty = \max_i |x_i|
\]

En büyük mutlak bileşeni ölçer ve worst-case büyüklük kontrolünde yararlıdır.

## 7. Mesafe ve benzerlik

### Euclidean distance

\[
d(a,b) = \sqrt{\sum_i (a_i-b_i)^2}
\]

Mutlak konuma ve vektör büyüklüğüne duyarlıdır.

### Cosine similarity

\[
\cos(\theta) = \frac{a\cdot b}{\lVert a\rVert_2\lVert b\rVert_2}
\]

Yön benzerliğini ölçer. Pozitif vektörlerde 1'e yakın değer yüksek benzerlik, 0'a yakın değer düşük ilişki anlamına gelir. Genel durumda sonuç `[-1, 1]` aralığındadır.

Sıfır vektörünün yönü olmadığı için cosine similarity hesaplanamaz; üretim kodu bu durumu açıkça ele almalıdır.

## 8. Normalizasyon

L2 normalizasyonu:

\[
\hat{x} = \frac{x}{\lVert x\rVert_2}
\]

Normalizasyon sonrası vektörün L2 normu 1 olur. Birim vektörlerde dot product ile cosine similarity eşittir. Bu özellik embedding retrieval sistemlerinde hesaplamayı kolaylaştırabilir.

Ancak normalizasyon her problem için doğru değildir. Vektör büyüklüğü anlam taşıyorsa normalizasyon bilgi kaybına neden olabilir.

## 9. Broadcasting sezgisi

Broadcasting, uyumlu shape'lerde küçük bir yapının daha büyük yapı boyunca tekrar kullanılmasıdır. Örneğin `(batch, features)` matrise `(features,)` bias vektörü eklenebilir.

Saf Python uygulamasında broadcasting otomatik değildir; açık döngü veya doğrulanmış yardımcı fonksiyon gerekir. NumPy ve PyTorch kullanırken broadcasting kurallarını bilmeden yazılan kod sessiz mantık hataları üretebilir.

## 10. Tensör yerleşimleri

### Görüntü

- Channels-first: `(batch, channels, height, width)`
- Channels-last: `(batch, height, width, channels)`

### NLP

- Token IDs: `(batch, sequence_length)`
- Hidden states: `(batch, sequence_length, hidden_size)`
- Attention scores: `(batch, heads, query_length, key_length)`

### Tabular veri

- `(batch, features)`

Shape yalnızca teknik metadata değildir; her eksenin semantik anlamını taşır.

## 11. Sayısal ve mühendislik riskleri

- Farklı uzunlukta vektörlerin sessizce `zip` ile kesilmesi hatadır.
- Düzensiz satırlı matrisler rectangular değildir.
- Sıfır vektörü normalize edilmemelidir.
- Floating-point eşitliği doğrudan `==` ile test edilmemelidir.
- Büyük tensörleri saf Python listeleriyle kopyalamak bellek maliyetini artırır.
- Shape doğrulaması API sınırında yapılmalıdır.

## 12. AI mühendisliği bağlantıları

- Embedding retrieval: cosine similarity veya dot product
- Dense layer: matrix multiplication ve bias broadcasting
- Attention: query-key dot product
- Regularization: L1 ve L2 normları
- Gradient clipping: gradient normu
- Computer vision: rank-4 görüntü tensörleri
- Language models: rank-3 hidden-state tensörleri
- Batch processing: ilk eksende örnek gruplama

## 13. Seçim rehberi

- Yön benzerliği önemliyse: cosine similarity
- Mutlak geometrik uzaklık önemliyse: Euclidean distance
- Sparsity hedefleniyorsa: L1 yaklaşımı
- Genel büyüklük ve enerji ölçümü gerekiyorsa: L2 norm
- En büyük bileşen kontrol edilecekse: infinity norm
- Lineer dönüşüm uygulanacaksa: matrix multiplication

Bu dersin amacı formülleri ezberlemek değil; shape, işlem uyumluluğu ve geometrik anlam arasında güvenilir bağ kurmaktır.
