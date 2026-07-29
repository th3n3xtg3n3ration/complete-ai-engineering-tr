# Quiz — Clustering, Anomali Tespiti ve Boyut İndirgeme

Her soruda tek doğru seçenek vardır.

1. K-Means hangi amacı küçültür?
   - A) Küme içi kareler toplamı
   - B) Sınıflandırma log-loss'u
   - C) Test hatası
   - D) Özellik sayısı
2. K-Means öncesi scaling neden önemlidir?
   - A) Küme sayısını otomatik seçer
   - B) Büyük ölçekli özelliklerin uzaklığı domine etmesini önler
   - C) Aykırı değerleri siler
   - D) Etiket üretir
3. Silhouette skoru 1'e yaklaştığında genel yorum nedir?
   - A) Kümeler daha iyi ayrışır
   - B) Model kesin overfit olmuştur
   - C) Tüm noktalar anomalidir
   - D) PCA gereksizdir
4. DBSCAN'de `-1` etiketi neyi gösterir?
   - A) En büyük küme
   - B) Gürültü noktası
   - C) İlk merkez
   - D) Eksik değer
5. Ward linkage neyi sınırlamaya çalışır?
   - A) Birleşme sonrası varyans artışını
   - B) Test seti boyutunu
   - C) Anomali oranını
   - D) Feature sayısını
6. Isolation Forest'ın temel sezgisi nedir?
   - A) Anomaliler daha az bölmeyle izole edilir
   - B) Her anomali en yakın merkezdedir
   - C) Tüm noktalar aynı yoğunluktadır
   - D) Etiketler rastgele üretilir
7. LOF özellikle neyi karşılaştırır?
   - A) Yerel yoğunlukları
   - B) Sınıf olasılıklarını
   - C) Özdeğerleri
   - D) Küme merkezlerini
8. One-Class SVM hangi senaryoya uygundur?
   - A) Normal davranış örneklerinden sınır öğrenmeye
   - B) Çok sınıflı etiket tahminine yalnızca
   - C) SQL sorgusu üretmeye
   - D) Eksik değer doldurmaya
9. PCA'nın ilk bileşeni neyi maksimize eder?
   - A) Yansıtılmış varyansı
   - B) Küme sayısını
   - C) Anomali sayısını
   - D) Test satırı sayısını
10. PCA bileşenleri genel olarak nasıldır?
   - A) Birbirine ortogonal
   - B) Tamamen kategorik
   - C) Etiketle aynı
   - D) Daima iki adet
11. Explained variance ratio toplamı neyi ifade eder?
   - A) Seçilen bileşenlerin açıkladığı varyans payını
   - B) Accuracy değerini
   - C) Contamination oranını
   - D) Learning rate'i
12. Unsupervised pipeline'da leakage nasıl oluşabilir?
   - A) Scaler ve PCA tüm veride fit edilirse
   - B) Random seed verilirse
   - C) Küme profili çıkarılırsa
   - D) Test verisi yalnızca transform edilirse
13. K-Means'in iç içe halkalarda zorlanmasının nedeni nedir?
   - A) Öklid uzaklığına dayalı küremsi bölmeler üretmesi
   - B) Hiç merkez kullanmaması
   - C) Etiket gerektirmesi
   - D) Sadece metinle çalışması
14. DBSCAN'in avantajı hangisidir?
   - A) Küme sayısını önceden istememesi
   - B) Her veri setinde tek parametreyle kusursuz olması
   - C) Scaling'e duyarsız olması
   - D) Her zaman tüm noktaları kümeye ataması
15. t-SNE grafiği için doğru yorum hangisidir?
   - A) Görsel adacıklar tek başına gerçek sınıf kanıtı değildir
   - B) Global uzaklıkları kusursuz korur
   - C) Üretimde doğrudan tahmin etiketi verir
   - D) Parametresizdir
16. `contamination` neyi etkiler?
   - A) Beklenen anomali oranı veya karar sınırı
   - B) PCA özvektör sayısını doğrudan
   - C) K-Means merkez sayısını
   - D) Dendrogram yüksekliğini
17. Anomali threshold'u en iyi nasıl seçilir?
   - A) Maliyet, kapasite ve doğrulama verisiyle
   - B) Her zaman 0 olarak
   - C) Yalnız train accuracy ile
   - D) Rastgele
18. Küme numaraları yeniden eğitimde neden değişebilir?
   - A) Etiketler anlamsal kimlik değil, algoritmik indekslerdir
   - B) PCA yasaktır
   - C) Veri satırları kaybolur
   - D) Silhouette negatif olamaz
19. High-dimensional veride uzaklıkların ayırt ediciliği neden azalabilir?
   - A) Curse of dimensionality
   - B) Label smoothing
   - C) Early stopping
   - D) Bootstrap bias
20. Üretimde hangi bilgi mutlaka sürümlenmelidir?
   - A) Feature şeması, preprocessing, model ve threshold
   - B) Yalnız notebook ekran görüntüsü
   - C) Sadece küme isimleri
   - D) Yalnız eğitim süresi

## Cevap anahtarı

1-A, 2-B, 3-A, 4-B, 5-A, 6-A, 7-A, 8-A, 9-A, 10-A, 11-A, 12-A, 13-A, 14-A, 15-A, 16-A, 17-A, 18-A, 19-A, 20-A
