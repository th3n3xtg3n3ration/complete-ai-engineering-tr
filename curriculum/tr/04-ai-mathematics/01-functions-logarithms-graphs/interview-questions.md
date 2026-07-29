# Mülakat Soruları — Fonksiyonlar, Logaritmalar ve Grafikler

## Temel sorular

### 1. Domain, codomain ve range arasındaki fark nedir?

**Beklenen cevap:** Domain kabul edilen girdiler kümesidir. Codomain çıktıların ait olması hedeflenen kümedir. Range ise fonksiyonun gerçekten ürettiği çıktıların kümesidir. Range codomain'in alt kümesi olabilir.

### 2. Doğrusal ve afin dönüşüm arasındaki fark nedir?

**Beklenen cevap:** Katı matematiksel kullanımda doğrusal dönüşüm orijini korur ve `f(x)=Wx` biçimindedir. Bias içeren `f(x)=Wx+b` dönüşümü afin dönüşümdür. ML dünyasında linear layer adı çoğu zaman bias içeren afin dönüşüm için kullanılır.

### 3. Logaritma neden yalnızca pozitif girdilerde tanımlıdır?

**Beklenen cevap:** Gerçek sayılar bağlamında pozitif bir tabanın herhangi bir gerçek kuvveti pozitiftir. Bu nedenle `b^y = x` eşitliğinde `x <= 0` için gerçek bir `y` bulunmaz.

### 4. Logaritmalar makine öğrenmesinde neden sık kullanılır?

**Beklenen cevap:** Çarpımları toplamlara dönüştürür, çok küçük olasılıklarla çalışmayı kolaylaştırır, geniş değer aralıklarını sıkıştırır ve maximum likelihood hedeflerini optimize edilebilir toplam loss biçimine dönüştürür.

### 5. Fonksiyon bileşkesi sinir ağlarıyla nasıl ilişkilidir?

**Beklenen cevap:** Her katman girdiyi başka bir temsile dönüştüren fonksiyondur. Ağın bütünü bu katman fonksiyonlarının bileşkesidir. Backpropagation da bileşke üzerindeki zincir kuralına dayanır.

## Aktivasyon soruları

### 6. Sinir ağlarında neden doğrusal olmayan aktivasyon gerekir?

**Beklenen cevap:** Yalnızca doğrusal/afin katmanların bileşkesi yine tek bir afin dönüşüme indirgenir. Doğrusal olmayan aktivasyonlar ağın karmaşık karar sınırlarını ve doğrusal olmayan ilişkileri temsil etmesini sağlar.

### 7. Sigmoid fonksiyonunun avantajları ve sınırlamaları nelerdir?

**Beklenen cevap:** `(0,1)` aralığında düzgün çıktı üretir ve ikili sınıflandırma olasılığı için uygundur. Büyük mutlak girdilerde doygunlaşır, gradient küçülür ve gizli katmanlarda vanishing gradient sorununu ağırlaştırabilir.

### 8. Tanh sigmoid'den hangi açıdan farklıdır?

**Beklenen cevap:** Tanh çıktısı `(-1,1)` aralığındadır ve sıfır merkezlidir. Ancak o da doygunlaşabilir. Sigmoid ile `tanh(x)=2*sigmoid(2x)-1` ilişkisi vardır.

### 9. ReLU neden yaygın kullanılır?

**Beklenen cevap:** Basit ve ucuzdur, pozitif bölgede gradient'i sabittir ve sigmoid/tanh'a göre pozitif bölgede doygunluk yaşamaz. Negatif bölgede sıfır gradient nedeniyle dead neuron problemi oluşturabilir.

### 10. Softplus hangi durumda ReLU'ya alternatif olabilir?

**Beklenen cevap:** Düzgün ve her noktada türevlenebilir bir yaklaşım gerektiğinde kullanılabilir. ReLU'nun yumuşak yaklaşımıdır; ancak hesaplama maliyeti daha yüksektir ve tam sparsity üretmez.

### 11. Softmax ile sigmoid arasındaki temel fark nedir?

**Beklenen cevap:** Sigmoid her skoru bağımsız olarak `(0,1)` aralığına taşır. Softmax sınıflar arasında rekabet oluşturarak tüm çıktıların toplamını 1 yapar. Tek etiketli çok sınıflı problemler için softmax, bağımsız çok etiketli problemler için sigmoid daha doğaldır.

### 12. Temperature softmax neyi değiştirir?

**Beklenen cevap:** Logits değerleri softmax öncesi sıcaklığa bölünür. Düşük sıcaklık dağılımı keskinleştirir, yüksek sıcaklık düzleştirir. Sınıf sırası değişmez, güven dağılımı değişir.

## Loss ve olasılık soruları

### 13. Cross-entropy neyi ölçer?

**Beklenen cevap:** Hedef dağılım altında tahmin dağılımına ait negatif log olasılığın beklenen değeridir. Tahmin hedefe yaklaştıkça düşer. One-hot hedefte doğru sınıfa verilen olasılığın negatif logaritmasına indirgenir.

### 14. Neden `log(0)` doğrudan hesaplanmamalıdır?

**Beklenen cevap:** Tanımsızdır ve floating-point hesapta domain error veya sonsuz değer üretir. Olasılık kırpma ya da logit tabanlı kararlı formüller kullanılmalıdır.

### 15. MSE ile cross-entropy sınıflandırmada nasıl farklı davranır?

**Beklenen cevap:** MSE olasılık hatasını karesel uzaklıkla ölçer. Cross-entropy doğru sınıfa verilen olasılığı logaritmik biçimde değerlendirir ve kendinden emin yanlış tahminleri daha güçlü cezalandırır. Olasılıksal sınıflandırma hedefiyle daha doğrudan ilişkilidir.

### 16. Negative log-likelihood ile cross-entropy arasındaki ilişki nedir?

**Beklenen cevap:** One-hot veya gözlenen sınıf hedefleri altında categorical cross-entropy, doğru sınıfın negative log-likelihood değerine eşittir. Dataset genelinde bu değerlerin toplamı veya ortalaması optimize edilir.

## Sayısal kararlılık soruları

### 17. Naive sigmoid neden büyük negatif girdide overflow üretebilir?

**Beklenen cevap:** `exp(-x)` ifadesinde `x` büyük negatif olduğunda `-x` büyük pozitif olur ve üstel değer floating-point aralığını aşabilir. İşarete göre dallanan eşdeğer form kullanılabilir.

### 18. Softmax'ta maksimum logit neden çıkarılır?

**Beklenen cevap:** Softmax sabit kaydırmaya invariant'tır. Maksimumu çıkarmak en büyük üstel girdiyi sıfıra taşır; böylece en büyük `exp` değeri 1 olur ve overflow riski azalır.

### 19. Log-sum-exp trick nedir?

**Beklenen cevap:** `log(sum(exp(x_i)))`, `m + log(sum(exp(x_i-m)))` biçiminde hesaplanır; burada `m=max(x)`. Bu dönüşüm matematiksel sonucu korurken üstel taşmayı azaltır.

### 20. Probability clipping'in dezavantajı nedir?

**Beklenen cevap:** Sonsuz loss'u önler ve pratik kararlılık sağlar; fakat gerçek matematiksel değeri küçük miktarda değiştirir ve seçilen epsilon'a bağımlılık oluşturur. Mümkünse logits üzerinden kararlı loss daha iyi olabilir.

## Grafik ve türev soruları

### 21. Bir learning curve'de plato ne anlatabilir?

**Beklenen cevap:** Öğrenme oranının düşük olması, kapasite sınırı, gradient küçülmesi, optimizasyon darboğazı veya veri/özellik sınırı gibi nedenlerle iyileşmenin yavaşladığını gösterebilir. Tek başına neden belirlemez; diğer metriklerle incelenmelidir.

### 22. Train loss düşerken validation loss yükseliyorsa olası yorum nedir?

**Beklenen cevap:** Overfitting göstergesi olabilir. Model eğitim verisine uyum sağlamaya devam ederken genelleme performansı kötüleşmektedir. Veri sızıntısı, dağılım farkı veya değerlendirme hataları da kontrol edilmelidir.

### 23. Merkezi fark neden ileri farka göre çoğu zaman daha doğrudur?

**Beklenen cevap:** Merkezi fark iki taraftaki bilgiyi kullanır ve truncation error genellikle ikinci derecedendir; ileri farkın hatası çoğunlukla birinci derecedendir. Ancak iki fonksiyon değerlendirmesi gerektirir.

### 24. Sayısal türevde step çok küçük seçilirse ne olur?

**Beklenen cevap:** Teorik yaklaşım hatası azalırken floating-point çıkarma iptali ve yuvarlama hatası büyüyebilir. Çok büyük step ise yerel eğimi kötü yaklaşıklar. Uygun ölçek seçilmelidir.

## Tasarım soruları

### 25. Matematik fonksiyonu API'sinde hangi doğrulamaları yaparsın?

**Beklenen cevap:** Tip, finite değer, domain kısıtı, boş koleksiyon, shape/uzunluk uyumu, olasılık aralığı, dağılım toplamı ve hiperparametre sınırları. Hata mesajları hangi argümanın neden geçersiz olduğunu söylemelidir.

### 26. Aktivasyon laboratuvarını production-quality hâle nasıl getirirsin?

**Beklenen cevap:** Paket yapısı, type hints, testler, CLI sözleşmesi, deterministik deney, atomik çıktı, structured errors, CI, lint/type check, benchmark, dokümantasyon, sürümleme ve gerekiyorsa NumPy backend eklenir.

### 27. Bir adaydan softmax implementasyonu isterken hangi edge case'lere bakarsın?

**Beklenen cevap:** Boş girdi, tek eleman, büyük logits, çok negatif logits, eşit logits, shift invariance, toplamın 1 olması, NaN/inf, input mutation ve sayısal kararlılık.

### 28. Framework fonksiyonları varken neden bunları sıfırdan yazmayı öğrenmeliyiz?

**Beklenen cevap:** Amaç production'da framework yerine elle kod yazmak değildir. Formül, domain, gradient ve kararlılık davranışını anlamak; hataları teşhis etmek; doğru API ve loss seçimini yapmak için temel implementasyon faydalıdır.
