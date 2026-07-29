# Mülakat Soruları — Clustering, Anomali Tespiti ve Boyut İndirgeme

## Clustering

1. Supervised ve unsupervised öğrenme arasındaki temel fark nedir?
2. K-Means objective fonksiyonunu yaz ve geometrik olarak yorumla.
3. K-Means neden global optimum garantisi vermez?
4. K-Means++ neyi iyileştirir?
5. `n_init` parametresi neden önemlidir?
6. Scaling yapılmadığında K-Means sonucu nasıl bozulabilir?
7. K-Means hangi küme geometrilerinde başarısız olur?
8. Inertia neden `k` arttıkça sürekli azalır?
9. Elbow method neden öznel olabilir?
10. Silhouette skorunun bileşenleri nelerdir?
11. Negatif silhouette değeri ne anlatır?
12. Davies–Bouldin skorunu nasıl yorumlarsın?
13. Internal ve external clustering metrikleri arasındaki fark nedir?
14. Ground truth yokken küme sayısını nasıl seçersin?
15. Bootstrap ile küme stabilitesi nasıl ölçülür?
16. Küme etiketleri yeniden eğitimde neden yer değiştirebilir?
17. İki modelin kümelerini nasıl eşleştirirsin?
18. Çok küçük bir kümenin anomali mi segment mi olduğunu nasıl araştırırsın?
19. Kategorik feature'larla uzaklık tabanlı clustering nasıl ele alınır?
20. MiniBatchKMeans ne zaman tercih edilir?

## Hiyerarşik yöntemler ve DBSCAN

21. Agglomerative ve divisive clustering farkı nedir?
22. Single, complete, average ve Ward linkage'ı karşılaştır.
23. Chaining effect nedir?
24. Dendrogram nasıl okunur?
25. Hiyerarşik clustering'in zaman ve bellek maliyeti nedir?
26. DBSCAN'de core, border ve noise point nedir?
27. `eps` ve `min_samples` nasıl seçilir?
28. DBSCAN'in K-Means'e göre avantajları nelerdir?
29. DBSCAN değişken yoğunluklu veride neden zorlanır?
30. Yüksek boyutta distance concentration DBSCAN'i nasıl etkiler?
31. HDBSCAN'in temel avantajı nedir?
32. OPTICS ne tür bir problemi çözmeye çalışır?

## Anomali tespiti

33. Point, contextual ve collective anomaly farkı nedir?
34. Isolation Forest'ın çalışma sezgisini açıkla.
35. Isolation Forest'ta contamination neyi etkiler?
36. LOF neden yerel anomalilerde güçlüdür?
37. LOF novelty mode ne zaman gerekir?
38. One-Class SVM'de `nu` parametresini yorumla.
39. Kernel seçimi One-Class SVM'i nasıl etkiler?
40. Anomali skor yönünü neden açıkça belgelemek gerekir?
41. Ground truth az olduğunda anomali modeli nasıl değerlendirilir?
42. Precision–recall eğrisi neden ROC eğrisinden daha yararlı olabilir?
43. Manuel inceleme kapasitesi threshold seçimini nasıl etkiler?
44. Yanlış pozitif ve yanlış negatif maliyetlerini threshold'a nasıl dahil edersin?
45. Segment bazında ayrı threshold kullanmanın avantajı ve riski nedir?
46. Anomali skor dağılımı drift'i nasıl izlenir?
47. Feedback loop ve selective labels problemi nedir?
48. Fraud modeli neden kendi kararlarıyla gelecekteki etiketleri bozabilir?

## PCA ve boyut indirgeme

49. Curse of dimensionality nedir?
50. PCA hangi objective'i optimize eder?
51. Kovaryans matrisi ve PCA ilişkisi nedir?
52. Özdeğer ve özvektörlerin PCA'daki anlamı nedir?
53. SVD ile PCA nasıl hesaplanır?
54. PCA öncesi centering neden gerekir?
55. PCA öncesi scaling ne zaman zorunluya yakındır?
56. Explained variance ratio neyi ölçer?
57. Kaç bileşen seçileceğine nasıl karar verirsin?
58. PCA neden feature selection değil feature extraction yöntemidir?
59. PCA loading'leri nasıl yorumlanır?
60. Whitening ne yapar ve hangi bilgiyi değiştirebilir?
61. IncrementalPCA ne zaman kullanılır?
62. SparsePCA'nın motivasyonu nedir?
63. Kernel PCA hangi tür yapıları yakalayabilir?
64. PCA reconstruction error ne için kullanılabilir?
65. PCA'nın kategorik one-hot feature'larda kullanım riskleri nelerdir?
66. PCA'yı split öncesi fit etmek neden leakage yaratır?

## Görselleştirme ve üretim

67. t-SNE lokal ve global yapıyı nasıl korur?
68. Perplexity t-SNE sonucunu nasıl etkiler?
69. UMAP ve t-SNE arasındaki pratik farklar nelerdir?
70. İki boyutlu embedding'deki adacıkları neden doğrudan sınıf kabul etmemeliyiz?
71. Unsupervised model için train/test ayrımı neden hâlâ anlamlıdır?
72. Clustering pipeline'ında hangi artefact'lar sürümlenmelidir?
73. Küme merkez kaymasını üretimde nasıl izlersin?
74. Segment büyüklüğündeki ani değişim ne anlatabilir?
75. Yeni kategori ve eksik kolon sorunlarını nasıl yönetirsin?
76. Yeniden eğitim sonrası iş kurallarının yanlış kümeye bağlanmasını nasıl önlersin?
77. Batch ve online scoring tasarımlarını karşılaştır.
78. Modelin başarısını kullanıcı davranışını değiştirdikten sonra nasıl ölçersin?
79. Unsupervised model için shadow deployment nasıl yapılır?
80. Bir segmentasyon projesinin başarısız olduğunu hangi sinyallerden anlarsın?
