# Teori — Clustering, Anomali Tespiti ve Boyut İndirgeme

## 1. Etiketsiz öğrenme nedir?

Etiketsiz öğrenmede gözlemler vardır fakat doğrudan bir hedef değişken bulunmaz. Amaç; veri içindeki benzerlikleri, yoğunluk bölgelerini, düşük boyutlu yapıyı veya olağan dışı örnekleri keşfetmektir. Sonuçlar keşifseldir; küme numaraları gerçek sınıf etiketi değildir.

## 2. K-Means

K-Means, her gözlemi en yakın merkeze atayarak küme içi kareler toplamını küçültür:

`J = sum_k sum_{x_i in C_k} ||x_i - mu_k||^2`

Algoritma iki adımı tekrarlar:

1. Atama: Her örneği en yakın merkeze ata.
2. Güncelleme: Her merkezin konumunu o kümeye atanmış örneklerin ortalaması yap.

K-Means küresel optimum garantisi vermez. Başlangıç merkezleri sonucu etkileyebilir; bu yüzden K-Means++ ve birden fazla başlangıç kullanılır.

### Varsayımlar ve sınırlamalar

- Öklid uzaklığı anlamlı olmalıdır.
- Özellik ölçekleri karşılaştırılabilir olmalıdır.
- Küremsi, benzer varyanslı kümelerde daha iyi çalışır.
- Aykırı değerlerden etkilenir.
- `k` önceden seçilmelidir.

## 3. Küme sayısının seçimi

### Inertia

Küme içi kareler toplamıdır. `k` arttıkça daima azalır; bu nedenle tek başına yeterli değildir.

### Silhouette

Bir örnek için:

`s = (b-a) / max(a,b)`

Burada `a`, örneğin kendi kümesine ortalama uzaklığı; `b`, en yakın diğer kümeye ortalama uzaklığıdır. Değer 1'e yaklaştıkça ayrışma güçlenir.

### Davies–Bouldin

Küme içi saçılım ile kümeler arası ayrımı karşılaştırır. Daha düşük değer genellikle daha iyidir.

Metrikler iş anlamının yerine geçmez. Stabil olmayan veya açıklanamayan bir segmentasyon, yüksek silhouette değerine rağmen kullanışsız olabilir.

## 4. Hiyerarşik kümeleme

Agglomerative yaklaşım her örneği ayrı küme olarak başlatır ve kümeleri aşamalı birleştirir.

Yaygın linkage seçenekleri:

- single: en yakın iki nokta,
- complete: en uzak iki nokta,
- average: ortalama çift uzaklığı,
- Ward: birleşme sonrası varyans artışı.

Dendrogram, birleşmelerin hangi uzaklıkta gerçekleştiğini gösterir. Büyük veri setlerinde hesaplama maliyeti hızla büyür.

## 5. DBSCAN

DBSCAN iki temel parametre kullanır:

- `eps`: komşuluk yarıçapı,
- `min_samples`: yoğun bölge için gereken minimum örnek sayısı.

Çekirdek noktalar yeterli komşuya sahiptir. Sınır noktaları bir çekirdek noktanın komşuluğundadır. Hiçbir kümeye bağlanmayan noktalar `-1` etiketiyle gürültü kabul edilir.

DBSCAN düzensiz şekilli kümeleri bulabilir ve küme sayısını önceden istemez. Fakat değişken yoğunlukta, yüksek boyutlu veya kötü ölçeklenmiş veride zorlanır.

## 6. Anomali tespiti

Anomali, çoğunluğun üretim mekanizmasından farklı görünen örnektir. İstatistiksel sıra dışılık ile iş açısından risk aynı şey değildir.

### Isolation Forest

Rastgele özellik ve kesme noktalarıyla örnekleri izole eder. Daha az bölmeyle izole edilen örnekler daha anomalidir. Yüksek boyutlu ve orta-büyük veri setlerinde güçlü bir başlangıç modelidir.

### Local Outlier Factor

Bir örneğin yerel yoğunluğunu komşularının yoğunluğuyla karşılaştırır. Yerel anomalileri yakalayabilir; komşuluk sayısına ve ölçeklemeye duyarlıdır.

### One-Class SVM

Normal örnekleri feature space içinde çevreleyen bir sınır öğrenir. Kernel ve `nu` seçimine duyarlıdır; büyük veri setlerinde pahalı olabilir.

### Threshold seçimi

Model skoru karar değildir. Eşik; etiketli doğrulama verisi, uzman kapasitesi veya beklenen maliyetle seçilmelidir. Örneğin yanlış alarm incelemesi 40 TL, kaçırılan gerçek olay 1.000 TL ise toplam beklenen maliyet:

`maliyet = 40 * FP + 1000 * FN`

olarak değerlendirilebilir.

## 7. PCA

PCA, verideki varyansı ardışık olarak en fazla açıklayan ortogonal yönleri bulur. Merkezlenmiş veri matrisi `X` için kovaryans matrisi:

`Sigma = X^T X / (n-1)`

Özvektörler ana bileşen yönlerini, özdeğerler açıklanan varyansı verir. Uygulamada SVD daha kararlı olabilir:

`X = U S V^T`

Ana bileşenler `V` satırlarıyla ilişkilidir; tekil değerlerin kareleri açıklanan varyansı belirler.

### Explained variance ratio

Her bileşenin toplam varyansın ne kadarını açıkladığını gösterir. Yüzde 95 gibi sabit bir eşik otomatik kalite garantisi değildir; görev performansı ve hesaplama maliyeti birlikte değerlendirilmelidir.

### PCA öncesi scaling

Özellik birimleri farklıysa yüksek varyanslı ölçü birimi bileşenleri domine eder. StandardScaler çoğu genel amaçlı senaryoda uygun başlangıçtır. Scaling ve PCA yalnızca train verisinde fit edilmelidir.

## 8. t-SNE ve UMAP

t-SNE ve UMAP daha çok görselleştirme ve yerel komşuluk keşfi için kullanılır. İki boyutlu grafikte görülen adacıklar otomatik olarak gerçek kümeler değildir. Farklı random seed ve hiperparametrelerle görünüm değişebilir.

## 9. Üretim ilkeleri

- Ön işleme, model ve dönüşümler tek pipeline içinde tutulmalıdır.
- Kategorik değişkenler için uzaklık geometrisi dikkatle tasarlanmalıdır.
- Fit yalnızca eğitim verisinde yapılmalıdır.
- Küme profilleri zaman içinde izlenmelidir.
- Anomali oranındaki değişim veri drift'i veya sistem arızası olabilir.
- Küme kimlikleri yeniden eğitimler arasında yer değiştirebilir; merkez eşleştirme gerekir.
- Model sürümü, feature şeması, eşik ve eğitim veri aralığı kaydedilmelidir.
