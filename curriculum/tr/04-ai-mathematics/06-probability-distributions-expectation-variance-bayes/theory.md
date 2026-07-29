# Teori — Olasılık, Dağılımlar, Beklenti, Varyans ve Bayes

## 1. Belirsizliği matematikle ifade etmek

Yapay zekâ sistemleri çoğu zaman kesin bilgiyle değil, eksik ve gürültülü gözlemlerle çalışır. Olasılık teorisi bu belirsizliği ölçülebilir hale getirir. Bir modelin çıktısı yalnızca bir sınıf etiketi değil, çoğu zaman bir olayın gerçekleşme derecesidir.

Örnek uzay `Ω`, bir deneyin tüm olası sonuçlarını içerir. Bir olay, `Ω` içindeki sonuçların bir alt kümesidir. Olasılık fonksiyonu şu üç aksiyomu sağlar:

1. `P(A) >= 0`
2. `P(Ω) = 1`
3. Birbirini dışlayan olaylar için `P(A ∪ B) = P(A) + P(B)`

Tümleyen kuralı:

`P(A^c) = 1 - P(A)`

Birleşim kuralı:

`P(A ∪ B) = P(A) + P(B) - P(A ∩ B)`

## 2. Koşullu olasılık ve bağımsızlık

Bir olay hakkında yeni bilgi geldiğinde olasılık güncellenir:

`P(A | B) = P(A ∩ B) / P(B)`

Burada `P(B) > 0` olmalıdır. İki olay bağımsızsa:

`P(A ∩ B) = P(A)P(B)`

Bağımsızlık ile ilişkisizlik aynı şey değildir. Sıfır covariance, genel durumda bağımsızlık anlamına gelmez. Gaussian değişkenler gibi özel ailelerde daha güçlü sonuçlar elde edilebilir.

Toplam olasılık kuralı, örnek uzayı ayrık parçalara bölen `B_i` olayları için:

`P(A) = Σ_i P(A | B_i)P(B_i)`

## 3. Rassal değişkenler

Rassal değişken, deney sonuçlarını sayılara eşleyen fonksiyondur.

- Ayrık rassal değişken: Sayılabilir değerler alır.
- Sürekli rassal değişken: Bir aralıkta değer alır.

Ayrık değişkenler probability mass function (PMF), sürekli değişkenler probability density function (PDF) ile tanımlanır. Sürekli durumda tek bir noktanın olasılığı sıfırdır; olasılık bir aralık üzerinde integral ile hesaplanır.

Cumulative distribution function (CDF):

`F_X(x) = P(X <= x)`

CDF her dağılım türü için tanımlıdır ve azalmayan bir fonksiyondur.

## 4. Temel dağılımlar

### Bernoulli

Tek bir ikili deney:

`P(X = 1) = p`, `P(X = 0) = 1 - p`

`E[X] = p`, `Var(X) = p(1-p)`

AI örneği: Bir etiketin mevcut olup olmaması, tıklama olayı veya doğru/yanlış tahmin.

### Binomial

`n` bağımsız Bernoulli deneyindeki başarı sayısı:

`P(X=k) = C(n,k)p^k(1-p)^(n-k)`

`E[X] = np`, `Var(X) = np(1-p)`

### Categorical

Birden fazla sınıftan tam bir sınıf seçimi. Softmax çıktıları categorical dağılım parametreleri olarak yorumlanabilir.

### Uniform

Belirli bir aralıktaki tüm eşit uzunluklu alt aralıklar aynı olasılık yoğunluğuna sahiptir. Random initialization ve Monte Carlo örneklemesinde kullanılır.

### Normal

Ortalama `μ` ve varyans `σ²` ile tanımlanır:

`f(x) = 1/(σ√(2π)) exp(-(x-μ)^2/(2σ²))`

Merkezi limit teoremi nedeniyle ölçüm hataları ve toplamsal etkilerde sık görülür. Ancak gerçek verinin normal olduğunu otomatik olarak varsaymak hatalıdır.

### Poisson

Sabit bir zaman veya alan aralığındaki olay sayısını modeller:

`P(X=k) = exp(-λ) λ^k / k!`

`E[X] = Var(X) = λ`

### Exponential

Poisson sürecinde olaylar arası bekleme süresini modeller. Memoryless özelliğine sahiptir:

`P(X > s+t | X > s) = P(X > t)`

## 5. Beklenti ve varyans

Beklenti, uzun dönem ortalamasıdır:

`E[X] = Σ_x xP(X=x)`

veya sürekli durumda:

`E[X] = ∫ x f(x) dx`

Lineerlik özelliği bağımsızlık gerektirmez:

`E[aX+bY+c] = aE[X] + bE[Y] + c`

Varyans:

`Var(X) = E[(X-E[X])²] = E[X²] - E[X]²`

Standart sapma, varyansın kareköküdür ve değişkenle aynı birimdedir.

Covariance:

`Cov(X,Y) = E[(X-E[X])(Y-E[Y])]`

Correlation:

`Corr(X,Y) = Cov(X,Y) / (σ_X σ_Y)`

Correlation yalnızca doğrusal ilişkiyi ölçer. Nedensellik göstermez ve aykırı değerlere duyarlı olabilir.

## 6. Büyük sayılar yasası ve merkezi limit teoremi

Law of Large Numbers, bağımsız ve uygun koşulları sağlayan örneklerin ortalamasının gerçek beklentiye yaklaşacağını söyler.

Central Limit Theorem, birçok bağımsız değişkenin normalize edilmiş toplamının geniş koşullar altında normal dağılıma yaklaşmasını açıklar. CLT, ham verinin normal olduğu anlamına gelmez; örnek ortalamasının dağılımı hakkında sonuç verir.

Bu iki sonuç, mini-batch tahminlerinin neden veri miktarı arttıkça daha kararlı hale geldiğini anlamaya yardım eder.

## 7. Bayes teoremi

Bayes teoremi:

`P(H | D) = P(D | H)P(H) / P(D)`

- `P(H)`: prior
- `P(D | H)`: likelihood
- `P(D)`: evidence veya marginal likelihood
- `P(H | D)`: posterior

Posterior, yeni veri geldikten sonra hipotez hakkındaki güncellenmiş inançtır. Evidence çoğu zaman tüm olası hipotezler üzerinden normalize edilir:

`P(D) = Σ_h P(D | h)P(h)`

Bayesçi yaklaşım, parametreleri sabit ama bilinmeyen değerler yerine dağılımlar olarak modelleyebilir. Frequentist yaklaşım ise tekrarlı örnekleme davranışına odaklanır. İki yaklaşımın araçları bağlama göre birlikte kullanılabilir.

## 8. Naive Bayes

Naive Bayes, özelliklerin sınıf koşullu bağımsız olduğunu varsayar:

`P(y | x_1,...,x_d) ∝ P(y) Π_j P(x_j | y)`

Çarpımlar çok küçük sayılara yol açabileceği için log-uzayı kullanılır:

`log P(y | x) = constant + log P(y) + Σ_j log P(x_j | y)`

Gaussian Naive Bayes, her özelliğin sınıf içinde normal dağıldığını varsayar. Bu varsayım tam doğru olmasa bile model güçlü bir baseline olabilir.

Üretim ortamında dikkat edilmesi gerekenler:

- Varyansın sıfıra yaklaşmasını önlemek için smoothing kullan.
- Sınıf prior'larını eğitim verisinden veya domain bilgisinden açıkça belirle.
- Veri sızıntısını önlemek için istatistikleri yalnızca eğitim bölmesinde hesapla.
- Posterior skorlarını calibration analizi olmadan güven olasılığı gibi yorumlama.

## 9. Monte Carlo tahmini

Analitik çözümü zor bir beklenti, örnekleme ile tahmin edilebilir:

`E[f(X)] ≈ (1/N) Σ_i f(x_i)`

Hata tipik olarak `1/√N` ölçeğinde azalır. Örnek sayısını dört katına çıkarmak standart hatayı yaklaşık yarıya indirir. Variance reduction teknikleri aynı örnek bütçesiyle daha iyi tahmin sağlayabilir.

## 10. Calibration ve karar eşikleri

İyi calibration, yaklaşık `0.8` olasılık verilen örneklerin uzun dönemde yaklaşık `%80` oranında doğru olması anlamına gelir. Accuracy yüksek olsa bile calibration kötü olabilir.

Karar eşiği, maliyetlere göre seçilmelidir. Yanlış negatif ile yanlış pozitif aynı maliyete sahip değilse varsayılan `0.5` eşiği uygun olmayabilir.

## 11. Sayısal kararlılık

Olasılık hesaplarında yaygın sorunlar:

- Çok küçük olasılıkların çarpımında underflow
- `log(0)`
- Sıfıra yakın varyans
- Büyük kombinasyon değerlerinde overflow

Çözümler:

- Çarpım yerine log-olasılık toplamı
- Olasılıkları güvenli epsilon ile sınırlama
- Log-sum-exp tekniği
- Varyans smoothing
- Faktöriyel yerine log-gamma kullanımı

## 12. AI mühendisliği bağlantıları

- Cross-entropy, tahmin dağılımı ile hedef dağılım arasındaki uyumsuzluğu ölçer.
- Dropout, rassal maskeleme uygular.
- Diffusion modelleri gürültü dağılımlarıyla çalışır.
- Bayesian optimization belirsizliği kullanarak pahalı fonksiyonları arar.
- Language model sampling, categorical dağılımdan token seçer.
- Evaluation metriklerinin güven aralıkları örnekleme değişkenliğine dayanır.

Bu dersin amacı yalnızca formül ezberlemek değil; bir model çıktısının hangi varsayımlar altında olasılık olarak yorumlanabileceğini ve belirsizlik bilgisinin nasıl güvenilir biçimde taşınacağını anlamaktır.
