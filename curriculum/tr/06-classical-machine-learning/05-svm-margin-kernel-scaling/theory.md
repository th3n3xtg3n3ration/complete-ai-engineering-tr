# Teori — SVM, Margin, Kernel ve Ölçekleme

## 1. Sınıflandırma geometrisi

İkili sınıflandırmada doğrusal karar fonksiyonu

\[
f(x)=w^Tx+b
\]

biçimindedir. `f(x)=0` karar hiper-düzlemini, `sign(f(x))` ise tahmin edilen sınıfı verir. `w` vektörü hiper-düzleme diktir; `b` sınırın konumunu belirler.

Bir örneğin karar sınırına signed uzaklığı

\[
\frac{w^Tx_i+b}{\|w\|}
\]

olarak yazılır. Etiketler `y_i ∈ {-1,+1}` olduğunda doğru tarafta bulunmayı ölçen signed geometric margin

\[
\gamma_i=\frac{y_i(w^Tx_i+b)}{\|w\|}
\]

şeklindedir.

## 2. Functional ve geometric margin

Functional margin

\[
\hat\gamma_i=y_i(w^Tx_i+b)
\]

ölçekten etkilenir. `w` ve `b` aynı pozitif sabitle çarpıldığında karar sınırı değişmez fakat functional margin değişir. Geometric margin bu ölçek bağımlılığını `||w||` ile normalize eder.

Canonical ölçeklemede en yakın örnekler için

\[
y_i(w^Tx_i+b)=1
\]

seçilir. Bu durumda iki margin düzlemi arasındaki toplam genişlik

\[
\frac{2}{\|w\|}
\]

olur. Maksimum margin problemi bu genişliği büyütmekle eşdeğerdir.

## 3. Hard-margin SVM

Veri doğrusal olarak hatasız ayrılabiliyorsa primal problem

\[
\min_{w,b}\frac{1}{2}\|w\|^2
\]

kısıtlarıyla

\[
y_i(w^Tx_i+b)\ge1
\]

çözülür. `1/2` katsayısı türevleri sadeleştirir; asıl hedef `||w||` değerini küçültüp margin'i büyütmektir.

Hard margin şu durumlarda kırılgandır:

- etiket gürültüsü,
- aykırı değerler,
- sınıfların çakışması,
- yüksek boyutta yanlış ayrılabilirlik algısı.

## 4. Soft margin, slack variables ve C

Gerçek veride ihlalleri kabul etmek gerekir. Her örnek için `ξ_i ≥ 0` slack variable tanımlanır:

\[
y_i(w^Tx_i+b)\ge1-\xi_i
\]

Amaç fonksiyonu

\[
\min_{w,b,\xi}\frac{1}{2}\|w\|^2+C\sum_i\xi_i
\]

olur.

Yorum:

- `ξ_i=0`: örnek margin dışında ve doğru sınıfta.
- `0<ξ_i<1`: örnek doğru sınıfta fakat margin içinde.
- `ξ_i≥1`: örnek yanlış sınıflandırılmış olabilir.

`C`, margin genişliği ile eğitim ihlalleri arasındaki dengeyi belirler:

- küçük `C`: daha güçlü regularization, daha geniş margin, daha yüksek bias,
- büyük `C`: ihlallere daha sert ceza, daha dar margin, daha yüksek variance.

## 5. Hinge loss

Tek örnek için hinge loss

\[
L_i=\max(0,1-y_if(x_i))
\]

şeklindedir. Soft-margin primal problem eşdeğer olarak

\[
\min_{w,b}\frac{1}{2}\|w\|^2+C\sum_i\max(0,1-y_i(w^Tx_i+b))
\]

biçiminde yazılabilir.

Hinge loss yalnızca yanlış sınıflandırmaları değil, margin içine giren doğru sınıflandırılmış örnekleri de cezalandırır. Böylece yalnızca accuracy değil, güvenli ayırma mesafesi optimize edilir.

## 6. Lagrangian ve dual problem

Hard-margin primal problem için Lagrangian

\[
\mathcal{L}(w,b,\alpha)=\frac{1}{2}\|w\|^2-\sum_i\alpha_i[y_i(w^Tx_i+b)-1]
\]

şeklindedir ve `α_i≥0` koşulu vardır.

Stationarity koşulları:

\[
\frac{\partial \mathcal{L}}{\partial w}=0 \Rightarrow w=\sum_i\alpha_i y_i x_i
\]

\[
\frac{\partial \mathcal{L}}{\partial b}=0 \Rightarrow \sum_i\alpha_i y_i=0
\]

Bunlar primal değişkenleri dual probleme taşır:

\[
\max_{\alpha}\sum_i\alpha_i-\frac{1}{2}\sum_i\sum_j\alpha_i\alpha_jy_iy_jx_i^Tx_j
\]

kısıtları:

\[
\alpha_i\ge0,\qquad \sum_i\alpha_i y_i=0
\]

Soft margin için ayrıca

\[
0\le\alpha_i\le C
\]

kısıtı gelir.

## 7. KKT koşulları ve support vectors

Karush–Kuhn–Tucker koşullarındaki complementary slackness:

\[
\alpha_i[y_i(w^Tx_i+b)-1]=0
\]

ifadesi şu sonucu verir:

- `α_i=0` ise örnek karar fonksiyonuna doğrudan katkı vermez.
- `α_i>0` ise örnek margin üzerinde veya margin ihlalindedir.

Bu örnekler support vector'dür. Karar fonksiyonu

\[
f(x)=\sum_i\alpha_i y_i x_i^Tx+b
\]

olur ve yalnızca support vector'ler etkili kalır.

Soft-margin yorumunda:

- `0<α_i<C`: örnek genellikle margin üzerindedir.
- `α_i=C`: örnek margin içinde veya yanlış sınıflandırılmış olabilir.
- `α_i=0`: örnek margin dışında ve kolay örnektir.

## 8. Kernel trick

Dual problem veriyi yalnızca iç çarpımlar üzerinden kullanır. Bu nedenle

\[
x_i^Tx_j
\]

yerine

\[
K(x_i,x_j)=\phi(x_i)^T\phi(x_j)
\]

konabilir. Böylece `φ(x)` açıkça hesaplanmadan yüksek boyutlu özellik uzayında doğrusal ayırma yapılır.

Kernel karar fonksiyonu:

\[
f(x)=\sum_i\alpha_i y_iK(x_i,x)+b
\]

## 9. Gram matrix, PSD ve Mercer sezgisi

Eğitim örnekleri için Gram matrix

\[
G_{ij}=K(x_i,x_j)
\]

olarak tanımlanır. Geçerli bir kernel için Gram matrix simetrik ve positive semidefinite olmalıdır:

\[
c^TGc\ge0
\]

her `c` vektörü için sağlanır. Mercer teoremi uygun düzenlilik koşulları altında böyle bir kernel'in bir feature uzayındaki iç çarpıma karşılık geldiğini söyler.

Pratik sonuç: Her benzerlik fonksiyonu kernel değildir. Custom kernel tasarlarken simetri ve PSD özellikleri kontrol edilmelidir.

## 10. Yaygın kernel fonksiyonları

### Linear kernel

\[
K(x,z)=x^Tz
\]

Yüksek boyutlu sparse metin verisinde ve örnek sayısı büyük olduğunda iyi başlangıçtır.

### Polynomial kernel

\[
K(x,z)=(\gamma x^Tz+r)^d
\]

- `degree=d`: etkileşim derecesi,
- `gamma`: iç çarpım ölçeği,
- `coef0=r`: düşük ve yüksek dereceli terimlerin göreli etkisi.

### RBF kernel

\[
K(x,z)=\exp(-\gamma\|x-z\|^2)
\]

RBF, lokal benzerliğe dayalı esnek bir karar sınırı üretir.

- küçük `gamma`: geniş etki alanı, daha düzgün sınır, yüksek bias,
- büyük `gamma`: dar etki alanı, karmaşık sınır, yüksek variance.

## 11. C ve gamma birlikte düşünülmelidir

RBF SVM'de `C` ve `gamma` etkileşir:

| `C` | `gamma` | Tipik sonuç |
|---|---|---|
| küçük | küçük | güçlü underfitting riski |
| büyük | küçük | daha düzgün fakat eğitim hatasına duyarlı sınır |
| küçük | büyük | lokal fakat ihlallere toleranslı model |
| büyük | büyük | güçlü overfitting riski |

Bu nedenle parametreler ayrı ayrı değil, ortak bir arama uzayında seçilmelidir.

## 12. Feature scaling neden kritiktir?

SVM mesafe, norm ve iç çarpıma dayalıdır. Bir feature 0–1, diğeri 0–100000 aralığındaysa büyük ölçekli feature geometrik yapıyı domine eder.

Önerilen yaklaşım:

- dense sayısal veride `StandardScaler`,
- belirli fiziksel sınırlar varsa `MinMaxScaler`,
- sparse matriste merkezleme yapmayan ölçekleyiciler veya `StandardScaler(with_mean=False)`.

Scaling mutlaka cross-validation fold'larının içinde, bir `Pipeline` ile fit edilmelidir. Tüm veri üzerinde scaling yapıp sonra CV çalıştırmak leakage oluşturur.

## 13. LinearSVC, SVC ve SGDClassifier

### LinearSVC

- lineer karar sınırı,
- büyük ve yüksek boyutlu veri için daha ölçeklenebilir,
- doğrudan support vector indeksleri sağlamaz,
- varsayılan olarak probability üretmez.

### SVC(kernel="linear")

- libsvm tabanlıdır,
- support vector bilgisi verir,
- örnek sayısı büyüdükçe pahalılaşır.

### SGDClassifier(loss="hinge")

- online veya mini-batch eğitime uygundur,
- çok büyük veri için daha ölçeklenebilir,
- klasik maksimum margin optimumunu yaklaşık çözer.

## 14. Çok sınıflı SVM

SVM doğal olarak ikili sınıflandırıcıdır.

### One-vs-Rest

`K` sınıf için `K` model kurulur. Her model bir sınıfı diğerlerine karşı ayırır. Eğitim ve tahmin maliyeti daha düşüktür.

### One-vs-One

`K(K-1)/2` ikili model kurulur. Her model iki sınıf çifti üzerinde eğitilir. `SVC` varsayılan olarak OvO kullanır.

`LinearSVC` çoğunlukla OvR yaklaşımıyla kullanılır. Sınıf sayısı büyüdükçe OvO model sayısı hızla artar.

## 15. Class imbalance ve threshold

`class_weight="balanced"`, azınlık sınıfı örneklerinin eğitim kaybındaki ağırlığını artırır. Bu, karar eşiği seçimiyle aynı değildir:

- class weight: modelin öğrendiği sınırı değiştirir,
- threshold: sabit model skorlarının sınıfa çevrilme politikasını değiştirir.

Ranking metrikleri için ROC-AUC ve özellikle dengesiz problemlerde average precision raporlanmalıdır.

## 16. Probability calibration

SVM karar skoru olasılık değildir. Olasılık gerektiğinde:

- sigmoid calibration: Platt scaling, az veriyle daha kararlı,
- isotonic calibration: daha esnek, fakat küçük veriyle overfitting riski yüksek.

Calibration yalnızca training fold'larında öğrenilmelidir. Kalite Brier score, log loss ve calibration curve ile değerlendirilir.

## 17. Hyperparameter optimization

Güvenilir süreç:

1. preprocessing ve scaling'i pipeline içine koy,
2. `C`, kernel ve `gamma` için cross-validation çalıştır,
3. scoring metriğini iş hedefine göre seç,
4. model karşılaştırması için gerekirse nested CV kullan,
5. test kümesini yalnızca son aşamada değerlendir.

Logaritmik aralıklar genellikle daha anlamlıdır:

```python
C = [1e-3, 1e-2, 1e-1, 1, 10, 100]
gamma = [1e-4, 1e-3, 1e-2, 1e-1, 1]
```

## 18. Hesaplama maliyeti

Kernel SVM eğitimi örnek sayısı arttıkça pahalılaşabilir. Bellek maliyeti Gram matrix ve support vector sayısıyla büyür. Büyük veri için şu alternatifler değerlendirilmelidir:

- LinearSVC,
- SGDClassifier,
- Nystroem veya random Fourier features,
- daha küçük temsilci örneklem,
- tree-based veya boosting modelleri.

## 19. Hata analizi

Yalnızca genel metrik yeterli değildir. Şunlar raporlanmalıdır:

- support vector oranı,
- sınıf ve segment bazlı recall,
- skor dağılımları,
- calibration hatası,
- `C`–`gamma` validation yüzeyi,
- scaling öncesi/sonrası performans,
- train–validation farkı,
- tahmin süresi ve model boyutu.

## 20. Üretim kontrol listesi

- preprocessing ve model tek pipeline içinde mi?
- feature sırası ve şeması sürümlendi mi?
- calibration ve threshold ayrı artefaktlar olarak saklandı mı?
- kernel ve hiperparametre seçimi yalnızca training verisinde mi yapıldı?
- support vector sayısı ve tahmin gecikmesi izleniyor mu?
- class distribution ve feature scale drift'i takip ediliyor mu?
- büyük veri için daha ölçeklenebilir alternatiflerle benchmark yapıldı mı?

SVM güçlü bir yöntemdir; ancak seçim yalnızca doğrulukla değil, veri boyutu, feature yapısı, açıklanabilirlik, calibration ihtiyacı ve üretim maliyetiyle birlikte yapılmalıdır.
