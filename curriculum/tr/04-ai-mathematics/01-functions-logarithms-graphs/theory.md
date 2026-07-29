# Teori — Fonksiyonlar, Logaritmalar ve Grafikler

## 1. Fonksiyon nedir?

Fonksiyon, izin verilen her girdiyi tam olarak bir çıktıya eşleyen kuraldır. Genellikle

\[
f: X \rightarrow Y
\]

şeklinde yazılır.

- **Domain:** Fonksiyonun kabul ettiği girdiler kümesi.
- **Codomain:** Çıktının ait olmasının beklendiği küme.
- **Range:** Fonksiyonun gerçekten ürettiği çıktılar kümesi.

Bir model katmanı da fonksiyondur: özellik vektörünü başka bir temsile veya tahmine dönüştürür.

## 2. Fonksiyon gösterimleri

Aynı fonksiyon farklı biçimlerde incelenebilir:

- cebirsel ifade: `f(x) = 2x + 1`
- tablo: seçilmiş `x` ve `f(x)` değerleri
- grafik: koordinat düzlemindeki noktalar
- program: girdiyi çıktıya dönüştüren kod

AI mühendisliğinde bu gösterimler birlikte kullanılır. Kod çalışır, denklem davranışı açıklar, grafik ise örüntüyü görünür kılar.

## 3. Temel fonksiyon aileleri

### 3.1 Doğrusal fonksiyon

\[
f(x) = mx + b
\]

- `m`: eğim
- `b`: y ekseni kesişimi

Eğim, `x` bir birim değiştiğinde çıktının ne kadar değiştiğini gösterir. Linear regression bu yapının çok boyutlu hâlidir.

### 3.2 Polinom fonksiyonu

\[
f(x) = a_nx^n + \dots + a_2x^2 + a_1x + a_0
\]

Polinomlar eğrilik üretebilir. Derece yükseldikçe temsil gücü artar; fakat aşırı karmaşık polinomlar eğitim verisine gereğinden fazla uyum sağlayabilir.

### 3.3 Üstel fonksiyon

\[
f(x) = a^x, \quad a > 0
\]

Üstel fonksiyonlar hızlı büyüme veya azalma gösterir. Olasılık normalizasyonu, softmax ve bazı öğrenme oranı schedule'ları üstel yapıları kullanır.

### 3.4 Logaritmik fonksiyon

\[
y = \log_b(x) \iff b^y = x
\]

Koşullar:

- `b > 0`
- `b != 1`
- `x > 0`

Logaritma, üstel fonksiyonun tersidir. Büyük değer aralıklarını sıkıştırır ve çarpımları toplamlara dönüştürür.

## 4. Logaritma kuralları

\[
\log_b(xy) = \log_b(x) + \log_b(y)
\]

\[
\log_b(x/y) = \log_b(x) - \log_b(y)
\]

\[
\log_b(x^k) = k\log_b(x)
\]

Makine öğrenmesinde doğal logaritma, yani tabanı `e` olan `ln`, en sık kullanılan logaritmadır.

### Neden log-loss kullanılır?

Bir doğru sınıfa verilen olasılık `p` ise negatif log-loss:

\[
L = -\log(p)
\]

şeklindedir.

- `p` 1'e yaklaşırsa loss 0'a yaklaşır.
- `p` 0'a yaklaşırsa loss hızla büyür.
- Kendinden emin fakat yanlış tahminler ağır cezalandırılır.

Kodda `log(0)` tanımsız olduğu için olasılıklar küçük bir epsilon ile güvenli aralığa sıkıştırılır.

## 5. Bileşke fonksiyon

\[
(f \circ g)(x) = f(g(x))
\]

Sinir ağı, çok sayıda fonksiyonun bileşkesidir:

\[
\hat{y} = f_3(f_2(f_1(x)))
\]

Bu bakış açısı daha sonra zincir kuralı ve backpropagation için temel oluşturur.

## 6. Ters fonksiyon

Bir fonksiyonun tersi, çıktıyı yeniden girdiye dönüştürür:

\[
f^{-1}(f(x)) = x
\]

Her fonksiyon terslenebilir değildir. Ters fonksiyon için ilgili aralıkta birebirlik gerekir. Örneğin `f(x) = x^2`, tüm gerçek sayılarda birebir değildir; ancak domain `x >= 0` ile sınırlandırılırsa tersi kareköktür.

## 7. Grafik okuma

Bir grafik yorumlanırken şu sorular sorulur:

1. Domain ve range nedir?
2. Fonksiyon nerede artıyor veya azalıyor?
3. Sıfır noktaları nerede?
4. Eğim nerede büyük veya küçüktür?
5. Doygunluk, kırılma veya asimptot var mı?
6. Küçük bir girdi değişimi çıktıyı ne kadar etkiliyor?

Loss curve yorumunda yalnızca son değere değil; düşüş hızına, plato oluşumuna, dalgalanmaya ve train-validation ayrışmasına bakılır.

## 8. Değişim oranı ve sayısal eğim

Bir noktadaki yerel eğim merkezi fark ile yaklaşık hesaplanabilir:

\[
f'(x) \approx \frac{f(x+h)-f(x-h)}{2h}
\]

Bu, analitik türevin yerine geçmez; fakat fonksiyon davranışını kontrol etmek ve gradient doğrulamak için kullanışlıdır.

## 9. Aktivasyon fonksiyonları

### 9.1 Sigmoid

\[
\sigma(x) = \frac{1}{1+e^{-x}}
\]

Çıktı aralığı `(0, 1)`'dir. İkili sınıflandırma çıkışlarında olasılık üretmek için uygundur. Büyük mutlak girdilerde doygunlaşır ve gradient küçülebilir.

Sayısal kararlılık için pozitif ve negatif girdiler ayrı formüllerle hesaplanabilir.

### 9.2 Tanh

\[
\tanh(x) = \frac{e^x-e^{-x}}{e^x+e^{-x}}
\]

Çıktı aralığı `(-1, 1)`'dir ve sıfır merkezlidir. O da büyük mutlak girdilerde doygunlaşır.

### 9.3 ReLU

\[
\operatorname{ReLU}(x) = \max(0, x)
\]

Pozitif bölgede doğrusal, negatif bölgede sıfırdır. Hesaplaması ucuzdur. Negatif bölgede sürekli sıfır gradient oluşması dead ReLU problemine yol açabilir.

### 9.4 Softplus

\[
\operatorname{softplus}(x) = \log(1 + e^x)
\]

ReLU'nun yumuşak yaklaşımıdır. Büyük pozitif `x` için doğrudan `log(1 + exp(x))` hesaplamak overflow üretebilir; kararlı eşdeğer form kullanılır.

### 9.5 Softmax

\[
\operatorname{softmax}(z_i)=\frac{e^{z_i}}{\sum_j e^{z_j}}
\]

Bir skor vektörünü toplamı 1 olan olasılık dağılımına dönüştürür. `exp` taşmasını önlemek için tüm skorlardan maksimum skor çıkarılır:

\[
\frac{e^{z_i-m}}{\sum_j e^{z_j-m}}, \quad m=\max(z)
\]

Bu dönüşüm sonucu değiştirmez, sayısal kararlılığı artırır.

## 10. Loss fonksiyonları

### 10.1 Mean Squared Error

\[
\operatorname{MSE}=\frac{1}{n}\sum_{i=1}^n(y_i-\hat{y}_i)^2
\]

Büyük hataları karesel biçimde daha fazla cezalandırır. Regresyonda yaygındır.

### 10.2 Binary Cross-Entropy

\[
L=-\frac{1}{n}\sum_i[y_i\log(p_i)+(1-y_i)\log(1-p_i)]
\]

İkili hedefler ve olasılık tahminleri için kullanılır.

### 10.3 Categorical Cross-Entropy

Tek örnek ve one-hot hedef için:

\[
L=-\sum_i y_i\log(p_i)
\]

One-hot hedefte yalnızca doğru sınıfın negatif log olasılığı kalır.

## 11. Sayısal kararlılık

Matematiksel olarak doğru formül, floating-point ortamında her zaman güvenli değildir.

Yaygın önlemler:

- `log(0)` için olasılıkları epsilon ile kırpmak
- softmax öncesi maksimum skoru çıkarmak
- softplus ve sigmoid için overflow-safe dallar kullanmak
- boş koleksiyon ve uzunluk uyuşmazlıklarını açıkça reddetmek
- `NaN` ve sonsuz değerleri erken kontrol etmek

AI sistemlerinde kararlılık, formülün kendisi kadar önemlidir.

## 12. AI bağlantıları

- Linear layer: doğrusal/afin fonksiyon
- Activation: doğrusal olmayan dönüşüm
- Deep network: fonksiyon bileşkesi
- Loss: tahmin kalitesini skora dönüştüren fonksiyon
- Optimizer: loss fonksiyonunu küçülten arama süreci
- Calibration: tahmin olasılıklarının gerçek frekanslarla uyumu
- Learning curve: zaman veya epoch'a göre metriğin grafiği

Bu dersin ana fikri şudur: Model eğitimi, birbirine bağlanmış fonksiyonların davranışını ölçme ve iyileştirme problemidir.
