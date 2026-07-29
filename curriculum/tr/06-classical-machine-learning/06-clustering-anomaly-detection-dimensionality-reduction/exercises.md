# Alıştırmalar — Clustering, Anomali Tespiti ve Boyut İndirgeme

Her çözümde varsayımlarını, değerlendirme yöntemini ve leakage riskini belirt.

## K-Means ve geometri

1. İki boyutlu üç kümeli veri üret ve K-Means merkezlerini görselleştir.
2. Aynı veri üzerinde `n_init=1` ve `n_init=30` sonuçlarını karşılaştır.
3. Özelliklerden birini 1.000 ile çarp; scaling öncesi ve sonrası kümeleri karşılaştır.
4. `k=1..10` için inertia eğrisini oluştur ve elbow seçimini gerekçelendir.
5. `k=2..8` için silhouette skorlarını hesapla.
6. En iyi silhouette değerinin iş açısından anlamsız segmentler ürettiği bir örnek tasarla.
7. Küme merkezlerini orijinal feature ölçeğine geri dönüştür.
8. Aykırı değer eklemeden önce ve sonra merkezlerin hareketini ölç.
9. K-Means'in iç içe halkalar verisinde neden başarısız olduğunu göster.
10. Küme büyüklüklerinin aşırı dengesiz olduğu veri üret ve sonucu analiz et.

## Hiyerarşik kümeleme ve DBSCAN

11. Single, complete, average ve Ward linkage sonuçlarını karşılaştır.
12. Küçük bir veri için dendrogram oluştur ve iki farklı kesme yüksekliği seç.
13. Single linkage chaining etkisini gösteren veri üret.
14. DBSCAN için `eps` ve `min_samples` grid'i oluştur.
15. Her DBSCAN denemesinde küme sayısı ve gürültü oranını raporla.
16. K-distance grafiğiyle `eps` adayı belirle.
17. Değişken yoğunluklu iki kümede DBSCAN'in sınırlamasını göster.
18. Yüksek boyutta DBSCAN performansını PCA öncesi ve sonrası karşılaştır.
19. Gürültü noktalarını ayrı küme gibi değerlendirmenin neden hatalı olabileceğini açıkla.
20. Aynı veri üzerinde K-Means, Agglomerative ve DBSCAN sonuçlarını karşılaştır.

## Küme değerlendirme

21. Silhouette skorunu küçük bir örnek için elle hesapla.
22. Davies–Bouldin skorunun düşük olmasının ne anlama geldiğini açıkla.
23. Adjusted Rand Index kullanmak için hangi ek bilgiye ihtiyaç olduğunu belirt.
24. Bootstrap örnekleriyle küme stabilitesi ölçümü tasarla.
25. İki yeniden eğitim arasında küme etiketlerini merkez uzaklığıyla eşleştir.
26. Segment profil tablosu oluşturan fonksiyon yaz.
27. Her küme için sayısal ve kategorik feature özetleri üret.
28. Küme sayısı seçimini metrik, stabilite ve iş kuralını birlikte kullanarak yap.
29. Çok küçük bir kümenin değerli niş segment mi yoksa gürültü mü olduğunu araştır.
30. Train'de öğrenilen merkezlerle test verisinin uzaklık dağılımını incele.

## Anomali tespiti

31. Isolation Forest ile sentetik anomalileri tespit et.
32. `contamination` parametresinin tahmin oranına etkisini ölç.
33. LOF için `n_neighbors` değerlerini karşılaştır.
34. LOF novelty modunun kullanım amacını açıkla.
35. One-Class SVM'de `nu` ve `gamma` grid'i dene.
36. Global ve yerel anomali arasındaki farkı veriyle göster.
37. Anomali skorlarını percentile'e dönüştür.
38. Manuel inceleme kapasitesi günlük 100 kayıt ise threshold seç.
39. Yanlış alarm maliyeti 30 TL, kaçırma maliyeti 1.500 TL iken en düşük maliyetli eşiği bul.
40. Etiketlerin yalnızca küçük bir alt kümede bulunduğu değerlendirme planı tasarla.
41. Segment bazında anomali oranlarını karşılaştır.
42. Veri drift'i sonrası skor dağılımındaki değişimi ölç.
43. Yeni bir kategori geldiğinde pipeline davranışını test et.
44. Anomali modelinin kimlik kolonunu kullanmasının riskini göster.
45. Uzman geri bildirimini threshold güncellemesine dahil eden süreç tasarla.

## PCA ve temsil öğrenme

46. PCA'yı scaling olmadan ve scaling ile uygula.
47. Kümülatif explained variance grafiği oluştur.
48. Yüzde 90, 95 ve 99 varyans eşikleri için bileşen sayılarını karşılaştır.
49. PCA reconstruction error hesapla.
50. En yüksek loading'e sahip feature'ları her bileşen için raporla.
51. Korelasyonlu feature'lardan oluşan veri üzerinde PCA uygula.
52. PCA sonrası bileşenlerin korelasyon matrisini incele.
53. Whitening'in varyanslara etkisini göster.
54. IncrementalPCA ile standart PCA'yı karşılaştır.
55. Kernel PCA'yı doğrusal olmayan veri üzerinde dene.
56. t-SNE görselinin random seed ile nasıl değiştiğini göster.
57. t-SNE grafiğindeki adacıkları otomatik gerçek küme kabul etmenin riskini açıkla.
58. PCA fit'ini tüm veri üzerinde yaparak leakage oluştur ve doğru pipeline ile karşılaştır.
59. PCA sonrası sınıflandırma başarımını bileşen sayısına göre ölç.
60. Clustering, anomaly detection ve PCA'yı tek üretim tasarımında birleştir.
