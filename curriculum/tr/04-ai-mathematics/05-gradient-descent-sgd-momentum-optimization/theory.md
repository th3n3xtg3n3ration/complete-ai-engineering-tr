# Teori — Gradient Tabanlı Optimizasyon

## 1. Optimizasyon problemi nedir?

Makine öğrenmesinde eğitim, model parametrelerini bir amaç fonksiyonunu küçültecek biçimde seçme problemidir.

Bir parametre vektörü \(\theta\) ve loss fonksiyonu \(L(\theta)\) için temel problem:

\[
\theta^* = \arg\min_\theta L(\theta)
\]

Burada:

- **Parametreler:** Modelin öğrendiği ağırlık ve bias değerleridir.
- **Loss:** Tahminlerin hedeflerden ne kadar uzak olduğunu ölçer.
- **Optimizer:** Parametrelerin hangi yönde ve ne kadar değiştirileceğini belirler.
- **Gradient:** Loss'un parametrelere göre en hızlı artış yönüdür.

Bu nedenle loss'u azaltmak için negatif gradient yönünde hareket edilir.

## 2. Gradient descent

Temel güncelleme kuralı:

\[
\theta_{t+1} = \theta_t - \eta \nabla_\theta L(\theta_t)
\]

- \(t\): iterasyon numarası
- \(\eta\): learning rate
- \(\nabla L\): gradient vektörü

Gradient yalnızca yönü değil, yerel değişim hassasiyetini de taşır. Büyük bileşenler ilgili parametrenin loss üzerinde daha güçlü yerel etkisi olduğunu gösterir.

### Geometrik yorum

Loss yüzeyini bir arazi gibi düşün. Gradient bulunduğun noktadaki en dik yukarı yönü gösterir. Negatif gradient ise en dik aşağı yönü verir. Bu yerel bilgi global minimumu garanti etmez; ancak küçük ve düzenli adımlarla düşük loss bölgelerine ulaşmayı sağlar.

## 3. Learning rate

Learning rate optimizasyonun en kritik hiperparametrelerinden biridir.

- Çok küçükse eğitim güvenli fakat yavaştır.
- Çok büyükse minimum çevresinde salınım veya divergence oluşabilir.
- Uygun değer başlangıçta hızlı ilerler, minimuma yaklaşırken kararlı davranır.

Tek bir sabit değer her eğitim aşamasında ideal olmayabilir. Bu nedenle schedule kullanılır.

### Yaygın schedule türleri

- **Step decay:** Belirli dönemlerde learning rate'i çarparak azaltır.
- **Exponential decay:** Her adımda üstel olarak azaltır.
- **Cosine decay:** Yumuşak ve periyodik olmayan bir düşüş sağlar.
- **Warmup:** İlk adımlarda learning rate'i küçükten hedef değere yükseltir.

Warmup özellikle derin ağlarda ve büyük batch eğitiminde ilk adımların kararsızlığını azaltabilir.

## 4. Batch, SGD ve mini-batch

### Batch gradient descent

Gradient tüm eğitim verisi üzerinden hesaplanır.

Avantajları:

- Deterministik güncelleme
- Düzgün loss eğrisi
- Küçük veri setlerinde kolay analiz

Dezavantajları:

- Büyük veri setlerinde pahalıdır.
- Her güncelleme için tüm veriyi bekler.
- Bellek kullanımı yüksek olabilir.

### Stochastic gradient descent

Her güncellemede tek örnek kullanılır.

\[
\theta_{t+1} = \theta_t - \eta \nabla L_i(\theta_t)
\]

Avantajları:

- Ucuz ve sık güncelleme
- Online learning için uygunluk
- Gürültünün bazı düz bölgelerden çıkmaya yardım edebilmesi

Dezavantajları:

- Yüksek varyanslı gradient
- Dalgalı loss eğrisi
- Learning rate seçimine yüksek hassasiyet

### Mini-batch gradient descent

Pratikte en yaygın yaklaşımdır. Her adımda küçük bir örnek grubu kullanılır.

- Donanım vektörizasyonundan yararlanır.
- SGD'ye göre daha düşük gradient varyansı üretir.
- Batch yönteme göre daha sık güncelleme sağlar.

Batch size yalnızca performans ayarı değildir; optimizer gürültüsünü ve genelleme davranışını da etkiler.

## 5. Momentum

Dar ve uzun vadilerde vanilla gradient descent bir eksende salınırken diğer eksende yavaş ilerleyebilir. Momentum geçmiş gradient yönlerini bir hız değişkeninde biriktirir.

\[
v_t = \beta v_{t-1} + g_t
\]

\[
\theta_{t+1} = \theta_t - \eta v_t
\]

Burada \(\beta\) genellikle 0 ile 1 arasındadır. Büyük \(\beta\), geçmiş yönlerin daha uzun süre hatırlanmasını sağlar.

Momentum:

- Tutarlı yönlerde hareketi hızlandırır.
- Birbirini iptal eden salınımları yumuşatır.
- Gürültülü gradient'lerde daha kararlı bir yön oluşturabilir.

## 6. Nesterov momentum

Nesterov yöntemi gradient'i mevcut parametrelerde değil, momentumun götüreceği yaklaşık gelecekteki noktada değerlendirir.

\[
\tilde{\theta}_t = \theta_t - \eta \beta v_{t-1}
\]

\[
v_t = \beta v_{t-1} + \nabla L(\tilde{\theta}_t)
\]

Bu ileri bakış, optimizer'ın minimumu aşmadan önce yönünü düzeltmesine yardımcı olabilir.

## 7. AdaGrad

AdaGrad her parametre için geçmiş kare gradient toplamına göre uyarlanmış learning rate kullanır.

\[
r_t = r_{t-1} + g_t^2
\]

\[
\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{r_t}+\epsilon}g_t
\]

Seyrek özelliklerde faydalıdır; ancak kare gradient toplamı sürekli büyüdüğü için effective learning rate zamanla aşırı küçülebilir.

## 8. RMSProp

RMSProp, AdaGrad'ın sınırsız birikim sorununu üstel hareketli ortalama ile azaltır.

\[
r_t = \rho r_{t-1} + (1-\rho)g_t^2
\]

\[
\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{r_t}+\epsilon}g_t
\]

Yakın geçmişteki gradient ölçeğine uyum sağlar ve non-stationary problemlerde daha kullanışlıdır.

## 9. Adam

Adam, momentumun birinci moment tahmini ile RMSProp benzeri ikinci moment tahminini birleştirir.

\[
m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t
\]

\[
v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2
\]

Başlangıçta momentler sıfıra yakın yanlı olduğu için bias correction uygulanır:

\[
\hat{m}_t = \frac{m_t}{1-\beta_1^t}, \qquad
\hat{v}_t = \frac{v_t}{1-\beta_2^t}
\]

\[
\theta_{t+1} = \theta_t - \eta \frac{\hat{m}_t}{\sqrt{\hat{v}_t}+\epsilon}
\]

Adam hızlı bir başlangıç ve parametre bazlı ölçekleme sağladığı için güçlü bir varsayılan seçimdir. Buna rağmen her problemde en iyi genelleme sonucunu garanti etmez.

## 10. Weight decay ve L2 regularization

L2 regularization loss'a parametre büyüklüğü cezası ekler:

\[
L_{reg}(\theta) = L(\theta) + \frac{\lambda}{2}\|\theta\|_2^2
\]

Gradient'e \(\lambda\theta\) terimi eklenir.

Weight decay ise parametreyi doğrudan küçültür. SGD için iki yaklaşım çoğu durumda eşdeğer görünse de adaptive optimizer'larda aynı değildir. AdamW, weight decay'i gradient tabanlı moment hesaplarından ayırır.

## 11. Gradient clipping

Exploding gradient durumunda update çok büyüyebilir. Global norm clipping:

\[
g \leftarrow g \cdot \min\left(1, \frac{c}{\|g\|_2 + \epsilon}\right)
\]

Burada \(c\) maksimum gradient normudur. Clipping sorunun kök nedenini çözmez; ancak eğitimin sayısal olarak dağılmasını önleyen bir güvenlik mekanizmasıdır.

## 12. Loss yüzeyinin geometrisi

### Convex fonksiyon

Her yerel minimum global minimumdur. Linear regression'ın mean squared error loss'u uygun koşullarda convex yapıdadır.

### Non-convex fonksiyon

Derin ağlar çok sayıda local minimum, plato ve saddle point içeren yüzeyler üretir. Eğitim başarısı yalnızca global minimumu bulmakla açıklanmaz; düşük loss ve iyi genelleme sağlayan bir bölge yeterlidir.

### Ill-conditioning

Hessian özdeğerleri çok farklı ölçeklerdeyse yüzey bazı yönlerde dik, bazı yönlerde düzdür. Gradient descent zikzak çizebilir. Momentum ve adaptive learning-rate yöntemleri bu sorunu hafifletebilir.

### Saddle point

Bazı yönlerde minimum, bazı yönlerde maksimum davranışı gösteren durağan noktadır. Gradient sıfıra yakın olabilir; Hessian'ın hem pozitif hem negatif özdeğerleri vardır.

## 13. Yakınsama tanılaması

Yalnızca final loss'a bakmak yeterli değildir. Şunlar birlikte izlenmelidir:

- Training ve validation loss
- Gradient norm
- Update norm
- Parametre normu
- Learning rate
- Epoch süresi
- NaN veya infinity oluşumu

### Yaygın belirtiler

- **Divergence:** Loss hızla artar veya NaN olur.
- **Oscillation:** Loss düzenli biçimde aşağı-yukarı hareket eder.
- **Plateau:** Gradient ve update çok küçülür, loss değişmez.
- **Exploding update:** Parametre normu aniden büyür.
- **Overfitting:** Training loss düşerken validation loss yükselir.

## 14. Early stopping

Validation metriği belirli sayıda değerlendirme boyunca iyileşmezse eğitim durdurulur. Bu sayı **patience** olarak adlandırılır. En iyi validation skoruna ait parametreler saklanmalıdır; yalnızca son epoch parametrelerini kullanmak doğru değildir.

## 15. Linear regression örneği

Model:

\[
\hat{y}_i = wx_i + b
\]

Mean squared error:

\[
L(w,b)=\frac{1}{n}\sum_{i=1}^{n}(\hat{y}_i-y_i)^2
\]

Gradient'ler:

\[
\frac{\partial L}{\partial w}=\frac{2}{n}\sum_i x_i(\hat{y}_i-y_i)
\]

\[
\frac{\partial L}{\partial b}=\frac{2}{n}\sum_i(\hat{y}_i-y_i)
\]

Bu problem optimizer davranışlarını karşılaştırmak için idealdir; çünkü loss, gradient ve optimum kolayca analiz edilebilir.

## 16. Üretim perspektifi

Üretim kalitesinde bir eğitim sistemi:

1. Rastgelelik kaynaklarını seed ile kontrol eder.
2. Veri sıralamasını her epoch yeniden karıştırır.
3. Gradient ve parametrelerde finite değer kontrolü yapar.
4. Hiperparametreleri yapılandırmadan alır.
5. Eğitim metriklerini yapılandırılmış biçimde kaydeder.
6. En iyi checkpoint'i saklar.
7. Kesintiden devam edebilmek için optimizer state'i de kaydeder.
8. Train ve evaluation modlarını açıkça ayırır.
9. Küçük bir veri diliminde overfit testi yapar.
10. Gradient checking ve birim testlerle matematiksel doğruluğu denetler.

## 17. Temel çıkarımlar

- Gradient descent yerel birinci mertebe bilgi kullanır.
- Learning rate, optimizer seçiminden çoğu zaman daha kritik olabilir.
- Mini-batch gürültüsü hem zorluk hem de faydalı regularization kaynağıdır.
- Momentum yön tutarlılığını biriktirir; adaptive yöntemler koordinat bazlı ölçek ayarlar.
- Adam güçlü bir başlangıç noktasıdır ancak otomatik olarak en iyi çözüm değildir.
- Sağlıklı optimizasyon, loss ile birlikte gradient, update ve validation davranışını izlemeyi gerektirir.
