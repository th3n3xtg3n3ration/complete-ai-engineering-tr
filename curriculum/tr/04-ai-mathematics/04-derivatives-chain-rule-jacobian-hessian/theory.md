# Teori — Türevden Hessian'a

## 1. Türev

Bir fonksiyonun türevi, girdideki çok küçük değişimin çıktıyı hangi hızla değiştirdiğini ölçer:

\[
f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}
\]

Geometrik olarak teğetin eğimidir. Model eğitiminde loss'un parametreye duyarlılığını temsil eder.

## 2. Sayısal türev

Merkezi fark yaklaşımı:

\[
f'(x)\approx\frac{f(x+h)-f(x-h)}{2h}
\]

Çok büyük `h` yaklaşım hatası, çok küçük `h` floating-point iptali üretir. Bu nedenle gradient checking toleransla yapılır.

## 3. Kısmi türev ve gradient

Çok değişkenli `f(x, y)` fonksiyonunda diğer değişkenler sabit tutulur:

\[
\nabla f = [\partial f/\partial x,\partial f/\partial y]
\]

Gradient en hızlı artış yönüdür; `-gradient` yerel olarak en hızlı azalış yönüdür.

## 4. Directional derivative

Birim `u` yönündeki değişim:

\[
D_u f=\nabla f\cdot u
\]

Bu ifade dot product'ın optimizasyondaki anlamını gösterir.

## 5. Zincir kuralı

`y=f(g(x))` için:

\[
\frac{dy}{dx}=\frac{dy}{dg}\frac{dg}{dx}
\]

Derin ağlarda her katman yerel türevini üretir; backpropagation bu yerel türevleri ters yönde çarpar.

## 6. Hesaplama grafiği

Bir ifade küçük operasyon düğümlerine ayrılır. Örneğin `L=(wx+b-y)^2` grafiğinde ileri geçiş değerleri, geri geçiş ise her düğümün gradyanı hesaplanır. Aynı değer birden fazla yoldan kullanılıyorsa gradient katkıları toplanır.

## 7. Jacobian

Vektör değerli `F: R^n -> R^m` fonksiyonunun tüm birinci türevleri:

\[
J_{ij}=\frac{\partial F_i}{\partial x_j}
\]

Neural network katmanları, softmax ve koordinat dönüşümleri Jacobian ile incelenebilir. Büyük modellerde tam Jacobian yerine Jacobian-vector veya vector-Jacobian product kullanılır.

## 8. Hessian

Skaler fonksiyonun ikinci türev matrisi:

\[
H_{ij}=\frac{\partial^2 f}{\partial x_i\partial x_j}
\]

Hessian yerel eğriliği gösterir. Pozitif definite yapı yerel minimuma, negatif definite yapı maksimuma; karışık işaretli özdeğerler saddle point'e işaret edebilir.

## 9. Gradient checking

Analitik gradient ile merkezi fark sonucu karşılaştırılır:

\[
\text{relative error}=\frac{|g_a-g_n|}{\max(1,|g_a|,|g_n|)}
\]

Bu yöntem eğitim için değil, backward implementasyonlarını doğrulamak için kullanılır.

## 10. AI mühendisliği bağlantıları

- Backpropagation zincir kuralının sistematik uygulamasıdır.
- Gradient clipping türev büyüklüğünü kontrol eder.
- Vanishing/exploding gradients uzun çarpım zincirleriyle ilişkilidir.
- Hessian optimizasyon yüzeyinin eğriliğini açıklar.
- Automatic differentiation sembolik veya tamamen sayısal türev değildir; operasyon grafiği üzerinde türev kurallarını uygular.
