# Teori — Problem Tanımı, Baseline ve Deney Tasarımı

## 1. Modelden önce karar problemi gelir

Bir makine öğrenmesi projesinin ilk sorusu “hangi algoritmayı kullanalım?” değildir. Önce desteklenecek karar, tahmin birimi, tahmin zamanı, hedef penceresi ve hata maliyetleri tanımlanır. Bu tanım açık değilse yüksek offline skor üretimde değer sağlamayabilir.

## 2. Tahmin birimi ve grain

Tahmin birimi bir satırın neyi temsil ettiğini belirler: müşteri, sipariş, müşteri–gün veya cihaz–saat. Aynı entity birden fazla satırda bulunuyorsa random satır split'i aynı müşterinin train ve evaluation tarafında görünmesine neden olabilir. Bu durum entity leakage üretir.

## 3. Hedef tanımı

Hedef yalnızca kolon adı değildir. Olay, gözlem penceresi, tahmin ufku, pozitif sınıf, etiketin kesinleştiği zaman ve eksik etiket politikası birlikte tanımlanmalıdır. “Müşteri churn eder mi?” yerine “son 90 günlük davranış kullanılarak müşterinin önümüzdeki 30 gün içinde aboneliğini iptal edip etmeyeceği” daha test edilebilir bir hedeftir.

## 4. Görev türleri

- **Regresyon:** sürekli sayısal hedef tahmini.
- **Binary classification:** iki sınıf; pozitif sınıf açıkça belirtilir.
- **Multiclass classification:** birbirini dışlayan üç veya daha fazla sınıf.

## 5. Özellik kullanılabilirliği ve leakage

Bir kolonun hedefle korelasyonlu olması, tahmin anında kullanılabilir olduğu anlamına gelmez.

Başlıca leakage türleri:

- **Target leakage:** hedefin doğrudan veya türetilmiş kopyası özelliklerde bulunur.
- **Temporal leakage:** gelecekte oluşan bilgi geçmiş tahmininde kullanılır.
- **Entity leakage:** aynı müşteri, cihaz veya belge iki partition'da yer alır.
- **Preprocessing leakage:** imputation, scaling veya encoding tüm veri üzerinde fit edilir.
- **Selection leakage:** evaluation sonuçlarına tekrar tekrar bakılarak model kararı verilir.

## 6. Split stratejileri

### Random split

Bağımsız ve aynı dağılımdan gelen satırlar için uygundur. Sınıflandırmada stratification sınıf oranlarını korur.

### Temporal split

Geçmiş train, gelecek evaluation olur. Forecasting, churn, fraud ve davranışsal verilerde çoğu zaman daha gerçekçidir.

### Entity split

Aynı entity yalnızca tek partition'da bulunur. Hasta, müşteri, cihaz, mağaza veya doküman tabanlı problemlerde gereklidir.

İyi split, üretimde karşılaşılacak genelleme problemini simüle eder.

## 7. Baseline neden zorunludur?

Baseline en basit makul çözümün performansıdır. Yeni model, eklediği karmaşıklık ve operasyon maliyetine değecek kadar iyileşme sağlamalıdır.

Regresyon baseline'ları training mean, median, son gözlem veya segment ortalaması olabilir. Sınıflandırma baseline'ları majority class, class prior, mevcut iş kuralı veya mevcut üretim sistemidir. Baseline aynı zamanda veri ve metrik hattı için bir smoke test'tir.

## 8. Regresyon metrikleri

### MAE

`MAE = mean(abs(y - prediction))`

Doğrudan hedef birimindedir ve büyük hatalara RMSE kadar duyarlı değildir.

### RMSE

`RMSE = sqrt(mean((y - prediction)^2))`

Büyük hataları daha fazla cezalandırır.

### R²

`R² = 1 - residual_sum_of_squares / total_sum_of_squares`

Negatif olabilir. Bu, modelin training mean benzeri basit bir referanstan daha kötü olduğunu gösterir.

## 9. Sınıflandırma metrikleri

- **Accuracy:** tüm doğru tahminlerin oranı.
- **Balanced accuracy:** sınıf başına recall değerlerinin ortalaması.
- **Precision:** pozitif tahminlerin ne kadarı doğru?
- **Recall:** gerçek pozitiflerin ne kadarı bulundu?
- **F1:** precision ve recall'un harmonik ortalaması.
- **ROC-AUC:** sıralama kalitesi.
- **Log loss:** olasılık tahmininin doğruluğu ve aşırı güveni.

Threshold metriği ile probability metriği aynı soruyu cevaplamaz. Model seçimi ve karar eşiği seçimi ayrı aşamalardır.

## 10. Birincil ve guardrail metrikler

Bir deneyde tek bir birincil metrik, birkaç guardrail metrik, kabul edilebilir minimum eşikler ve metric direction önceden tanımlanmalıdır. Örneğin fraud modelinde recall birincil metrik; precision ve günlük inceleme hacmi guardrail olabilir.

## 11. Belirsizlik ve bootstrap

Tek bir skor örneklem değişkenliğini göstermez. Bootstrap evaluation satırlarını replacement ile yeniden örnekler ve metrik dağılımı oluşturur. Paired bootstrap iki modeli aynı örneklenmiş satırlarda karşılaştırarak skor farkının belirsizliğini ölçer.

## 12. Tekrarlanabilir deney kaydı

Her deney en az problem ve dataset sürümü, feature listesi, split stratejisi, random seed, baseline, metrikler, kod sürümü ve karar bilgisini kaydetmelidir. Deney kaydı yoksa model geliştirme bilimsel karşılaştırma yerine hafızaya dayalı deneme-yanılmaya dönüşür.

## 13. Üretim kontrol listesi

1. Prediction unit ve decision time yazılı mı?
2. Hedef ve horizon açık mı?
3. Özelliklerin availability zamanı biliniyor mu?
4. Split üretim senaryosunu taklit ediyor mu?
5. Entity overlap kontrol edildi mi?
6. Baseline çalışıyor mu?
7. Birincil metrik önceden seçildi mi?
8. Başarı eşiği tanımlandı mı?
9. Belirsizlik raporlandı mı?
10. Deney kaydı tekrar üretilebilir mi?
