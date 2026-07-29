# Quiz — SVM, Margin, Kernel ve Ölçekleme

Her soruda tek doğru seçenek vardır.

## Sorular

1. Maximum-margin SVM'in temel amacı nedir?
   - A) Eğitim doğruluğunu her durumda %100 yapmak
   - B) En yakın örneklere olan geometrik uzaklığı maksimize etmek
   - C) Özellik sayısını azaltmak
   - D) Tahminleri doğrudan olasılığa çevirmek

2. Canonical ölçekte toplam margin genişliği hangisidir?
   - A) `||w||`
   - B) `1/||w||²`
   - C) `2/||w||`
   - D) `C/||w||`

3. Soft-margin SVM'de slack değişkenlerinin görevi nedir?
   - A) Kernel matrisini normalize etmek
   - B) Margin ihlallerini ve bazı hataları kabul etmek
   - C) Çok sınıflı problemi ikili probleme çevirmek
   - D) Olasılık calibration yapmak

4. `C` değeri büyüdüğünde genel eğilim nedir?
   - A) Margin ihlalleri daha az cezalandırılır
   - B) Model her zaman lineer olur
   - C) Margin ihlalleri daha sert cezalandırılır
   - D) Gamma otomatik olarak küçülür

5. Bir örneğin hinge loss'u ne zaman sıfırdır?
   - A) `y f(x) <= 0`
   - B) `y f(x) >= 1`
   - C) `f(x)=0`
   - D) Olasılık 0.5 olduğunda

6. Karar sınırını doğrudan belirleyen eğitim örneklerine ne ad verilir?
   - A) Centroid
   - B) Support vector
   - C) Bootstrap örneği
   - D) Calibration point

7. Kernel trick ne sağlar?
   - A) Yüksek boyutlu feature mapping'i açıkça oluşturmadan iç çarpım hesaplamayı
   - B) Eksik değerleri doldurmayı
   - C) Her modeli olasılıksal yapmayı
   - D) Cross-validation ihtiyacını kaldırmayı

8. RBF kernel formülü hangisidir?
   - A) `xᵀz`
   - B) `(γxᵀz+c)^d`
   - C) `exp(-γ||x-z||²)`
   - D) `max(0,1-yf(x))`

9. RBF SVM'de çok büyük `gamma` genellikle neye yol açabilir?
   - A) Aşırı düzgün karar sınırına
   - B) Daha lokal ve karmaşık karar bölgelerine
   - C) Modelin tamamen lineer olmasına
   - D) Olasılıkların otomatik kalibre olmasına

10. SVM'de scaling neden önemlidir?
    - A) Yalnızca grafiklerin güzel görünmesi için
    - B) Mesafe ve iç çarpım hesaplarında büyük ölçekli feature'ların baskın olmasını önlemek için
    - C) Etiketleri dengelemek için
    - D) Test verisini büyütmek için

11. Preprocessing hangi şekilde uygulanmalıdır?
    - A) Split öncesinde tüm veri üzerinde
    - B) Sadece test verisinde
    - C) Pipeline içinde, her training fold üzerinde fit edilerek
    - D) Model eğitiminden sonra

12. `class_weight="balanced"` neyi değiştirir?
    - A) Eğitim sırasında sınıfların hata katkısını
    - B) Tahmin threshold'unu doğrudan 0.3 yapar
    - C) Kernel'i RBF'e çevirir
    - D) Özellikleri standardize eder

13. Threshold tuning ile class weighting arasındaki doğru fark hangisidir?
    - A) İkisi tamamen aynıdır
    - B) Class weighting eğitim hedefini, threshold tuning karar politikasını değiştirir
    - C) Threshold tuning yalnızca regresyonda kullanılır
    - D) Class weighting sadece scaling yapar

14. SVC'nin `decision_function` çıktısı varsayılan olarak nedir?
    - A) Kesin kalibre edilmiş olasılık
    - B) Karar skoru
    - C) Hinge loss ortalaması
    - D) Support vector indeksi

15. Probability calibration için hangisi kullanılabilir?
    - A) Platt/sigmoid scaling
    - B) PCA
    - C) Bootstrap aggregating
    - D) Mean imputation

16. Isotonic calibration'ın sigmoid calibration'a göre önemli riski nedir?
    - A) Yalnızca lineer veriyle çalışması
    - B) Az veriyle overfit olabilmesi
    - C) Olasılık üretememesi
    - D) Sadece çok sınıflı veri kabul etmesi

17. `SVC` çok sınıflı problemi varsayılan olarak hangi stratejiyle eğitir?
    - A) One-vs-one
    - B) K-means
    - C) Bagging
    - D) Stacking

18. Yüksek boyutlu sparse metin verisi için çoğunlukla hangi seçenek daha uygundur?
    - A) RBF SVC ve yoğun matrise dönüşüm
    - B) LinearSVC veya SGD tabanlı lineer sınıflandırıcı
    - C) Polynomial SVC degree 10
    - D) Scaling olmadan precomputed RBF

19. Hyperparameter seçimi için test kümesinin kullanılması ne oluşturur?
    - A) Regularization
    - B) Test leakage ve iyimser performans tahmini
    - C) Calibration
    - D) Support vector pruning

20. Nested cross-validation'ın temel amacı nedir?
    - A) Feature scaling'i kaldırmak
    - B) Model seçimi yapılırken genelleme performansını daha tarafsız tahmin etmek
    - C) Olasılık üretmek
    - D) Kernel matrisini küçültmek

## Cevap anahtarı

| Soru | Cevap | Kısa gerekçe |
|---:|:---:|---|
| 1 | B | SVM en yakın örneklere olan geometrik margin'i büyütür. |
| 2 | C | Canonical iki destek düzlemi arasındaki mesafe `2/||w||` değeridir. |
| 3 | B | Slack değişkenleri soft-margin ihlallerini temsil eder. |
| 4 | C | Büyük `C`, ihlalleri daha yüksek maliyetle cezalandırır. |
| 5 | B | `y f(x) >= 1` olduğunda örnek margin dışında ve doğru taraftadır. |
| 6 | B | Sıfırdan farklı dual coefficient alan örnekler support vector olur. |
| 7 | A | Kernel, feature uzayındaki iç çarpımı dolaylı hesaplar. |
| 8 | C | RBF uzaklığa dayalı üstel benzerliktir. |
| 9 | B | Büyük gamma, örnek etkisini daraltarak karmaşıklığı artırabilir. |
| 10 | B | Ölçek farkı, geometriyi ve kernel uzaklıklarını bozabilir. |
| 11 | C | Pipeline yaklaşımı validation/test bilgisinin fit işlemine sızmasını önler. |
| 12 | A | Sınıf ağırlıkları loss içindeki örnek maliyetlerini değiştirir. |
| 13 | B | Biri modeli, diğeri karar eşiğini değiştirir. |
| 14 | B | Decision function bir skor üretir; doğrudan olasılık değildir. |
| 15 | A | Sigmoid/Platt ve isotonic yaygın calibration yöntemleridir. |
| 16 | B | Esnek monoton eşleme az veride yüksek varyans gösterebilir. |
| 17 | A | `SVC` eğitimi one-vs-one temellidir. |
| 18 | B | Lineer yöntemler sparse ve yüksek boyutlu veride daha ölçeklenebilirdir. |
| 19 | B | Teste göre seçim yapmak bağımsız son değerlendirmeyi bozar. |
| 20 | B | İç döngü seçim, dış döngü tarafsız değerlendirme içindir. |
