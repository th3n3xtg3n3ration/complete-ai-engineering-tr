# Alıştırmalar

## Kavramsal

1. EDA ile data validation arasındaki farkı açıkla.
2. Gözlem birimi neden ilk belirlenmesi gereken kavramdır?
3. Mean ve median hangi koşullarda farklı hikâyeler anlatır?
4. IQR neden standart sapmaya göre robust kabul edilir?
5. Skewness değeri neyi ölçer?
6. Histogram bin sayısı sonucu nasıl etkiler?
7. Korelasyon neden nedensellik değildir?
8. Simpson paradoksunu bir örnekle açıkla.
9. Küçük segmentlerde oran karşılaştırması neden risklidir?
10. Missingness grafiği hangi soruları yanıtlayamaz?
11. Heatmap hangi koşullarda okunamaz hâle gelir?
12. Log scale ne zaman kullanılmalıdır?
13. Eksenin sıfırdan başlamaması ne zaman yanıltıcıdır?
14. Target distribution zaman içinde neden incelenmelidir?
15. Notebook çıktısı neden tek başına tekrarlanabilir rapor değildir?

## Kodlama

16. `profile_frame` fonksiyonuna unique count özeti ekle.
17. Numeric summary'ye coefficient of variation ekle.
18. Winsorized mean hesaplayan fonksiyon yaz.
19. Spearman ve Pearson farkını raporlayan tablo üret.
20. Kategorik summary'ye cumulative rate ekle.
21. Rare category raporu yaz.
22. Segment bazlı missing rate tablosu üret.
23. Zaman bazlı target rate fonksiyonu yaz.
24. İki segment için ECDF grafiği oluştur.
25. Histogram için Freedman–Diaconis bin kuralını uygula.
26. Scatter plot'a örnekleme sınırı ekle.
27. Correlation heatmap'e hücre değerleri ekle.
28. Duplicate anahtarları ayrı CSV olarak kaydet.
29. EDA config'ini YAML'dan yükle.
30. Üretilen artefaktlar için manifest JSON yaz.
31. Dataset fingerprint üret.
32. Her CSV çıktısı için satır ve kolon sayısını manifest'e ekle.
33. Tarih kolonlarında min/max ve timezone raporla.
34. Çok yüksek kardinaliteli kolonları otomatik işaretle.
35. Boolean kolonları kategorik analizde ele al.
36. Infinity değerlerini profile ekle.
37. Figure dosyalarının boş olmadığını test et.
38. Aynı seed ile aynı demo verinin üretildiğini test et.
39. Config'te bulunmayan kolon için açıklayıcı hata üret.
40. Boş DataFrame davranışını tanımla ve test et.

## Analiz

41. Gelir dağılımında mean/median farkını yorumla.
42. Churn oranını segmentlere göre karşılaştır.
43. Missing gelir satırlarının segment dağılımını incele.
44. Tenure ile churn ilişkisini görselleştir.
45. Yaş ile gelir arasındaki ilişkiyi segmentlere göre incele.
46. Outlier satırları çıkarıldığında korelasyonların değişimini ölç.
47. Global ve segment bazlı ortalamaları karşılaştır.
48. Hedef sınıf dengesizliğinin modelleme etkisini yaz.
49. Zaman içinde veri hacmi düşüşünü nasıl teşhis edeceğini açıkla.
50. Dashboard ile statik EDA raporunun farklarını yaz.

## İleri seviye

51. Population Stability Index uygula.
52. Jensen–Shannon divergence ile kategori drift'i ölç.
53. Bootstrap ile mean güven aralığı üret.
54. Segment farkları için effect size hesapla.
55. Çoklu karşılaştırma riskini EDA bağlamında açıkla.
56. Missingness pattern clustering yaklaşımı tasarla.
57. Pair plot yerine ölçeklenebilir alternatif geliştir.
58. Büyük veri için örnekleme stratejisi tasarla.
59. Parquet metadata üzerinden hızlı profil yaklaşımı öner.
60. EDA raporuna veri sözleşmesi uygunluk bölümü ekle.
