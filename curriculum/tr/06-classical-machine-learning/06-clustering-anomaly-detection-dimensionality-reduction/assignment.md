# Ödev — Müşteri Segmentasyonu ve Anomali İzleme Sistemi

## Senaryo

Bir e-ticaret şirketi, müşterileri davranışlarına göre segmentlere ayırmak ve olağan dışı hesap hareketlerini manuel inceleme ekibine yönlendirmek istiyor. Veri; sipariş sıklığı, sepet tutarı, iade oranı, oturum süresi, kanal, bölge ve üyelik yaşı alanlarını içeriyor.

Yanlış alarm incelemesinin maliyeti **35 TL**, kaçırılan gerçek riskli olayın beklenen maliyeti **1.200 TL** olarak kabul edilecektir.

## Zorunlu teslimatlar

### 1. Problem ve veri sözleşmesi

- Gözlem birimini ve skor üretim zamanını tanımla.
- Kimlik, post-outcome ve leakage yaratabilecek feature'ları dışla.
- Sayısal ve kategorik alanların veri tiplerini doğrula.
- Eksik değer, aykırı değer ve yeni kategori politikasını yaz.

### 2. Veri bölme

- Zaman etkisi varsa temporal holdout kullan.
- Aynı müşterinin geçmiş ve gelecek kayıtlarının split'ler arasında nasıl yönetildiğini açıkla.
- Preprocessing adımlarını yalnızca train üzerinde fit et.

### 3. Segmentasyon

En az şu modelleri karşılaştır:

1. StandardScaler + K-Means,
2. PCA + K-Means,
3. Agglomerative Clustering,
4. DBSCAN.

`k`, linkage, `eps` ve `min_samples` seçimlerini gerekçelendir. Inertia, silhouette, Davies–Bouldin, küme büyüklüğü ve bootstrap stabilitesi raporla.

### 4. Segment profili

Her segment için:

- büyüklük,
- temel feature ortalama ve medyanları,
- kanal ve bölge dağılımları,
- gelir veya operasyon açısından olası yorum,
- yanlış yorumlama riskleri

sunulmalıdır. Küme numaralarına doğrudan iş ismi vermeden önce profil kanıtı göster.

### 5. Anomali tespiti

Isolation Forest, LOF ve One-Class SVM modellerinden en az ikisini karşılaştır. Skor yönünü açıkça tanımla. Threshold'u:

`toplam maliyet = 35 * FP + 1200 * FN`

formülü, manuel inceleme kapasitesi ve doğrulama örnekleriyle seç.

### 6. PCA analizi

- Explained variance tablosu ve kümülatif grafik üret.
- En önemli loading'leri yorumla.
- Yüzde 90, 95 ve 99 varyans eşiklerinin model ve çalışma zamanı etkisini karşılaştır.
- PCA'sız ve PCA'lı segmentasyon sonuçlarını karşılaştır.

### 7. Üretim tasarımı

- Preprocessing ve modeli pipeline içinde paketle.
- Model, scaler/PCA, feature şeması, threshold ve eğitim tarihini sürümle.
- Küme oranı, merkez kayması, anomali skor dağılımı ve veri kalite metriklerini izle.
- Yeniden eğitim sonrası küme kimliklerini eşleştirme stratejisi öner.
- Geri alma ve sessiz dağıtım planı yaz.

## Test beklentileri

- Eksik kolonlarda açıklayıcı hata
- NaN ve sonsuz değer kontrolü
- Sabit random seed ile yeniden üretilebilirlik
- Pipeline'ın test verisinde yeniden fit olmaması
- Beklenen çıktı boyutları
- Anomali skor yönünün doğrulanması
- Küme sayısı ve threshold sınır kontrolleri

## Rubrik

| Alan | Puan |
|---|---:|
| Problem tanımı ve leakage kontrolü | 15 |
| Segmentasyon deneyleri | 20 |
| Değerlendirme ve stabilite | 15 |
| Anomali modeli ve maliyet duyarlı eşik | 20 |
| PCA analizi | 10 |
| Üretim tasarımı | 10 |
| Kod kalitesi ve testler | 10 |
| **Toplam** | **100** |
