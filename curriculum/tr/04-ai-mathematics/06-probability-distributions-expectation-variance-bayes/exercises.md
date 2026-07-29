# Alıştırmalar — Olasılık, Dağılımlar, Beklenti, Varyans ve Bayes

Alıştırmaları kod, matematiksel gerekçe ve kısa teknik yorumla tamamla. Kod cevapları İngilizce olmalıdır.

## A. Temel olaylar ve aksiyomlar

1. İki zar deneyinin örnek uzay büyüklüğünü hesapla.
2. İki zar toplamının 7 olma olasılığını bul.
3. Bir kart destesinden kırmızı veya as çekme olasılığını birleşim kuralıyla hesapla.
4. `P(A)=0.6`, `P(B)=0.5`, `P(A∩B)=0.3` için `P(A∪B)` değerini bul.
5. Bir olay ile tümleyeninin bağımsız olabileceği koşulu incele.
6. Bir olasılık tablosundaki aksiyom ihlalini tespit eden fonksiyon yaz.
7. Ayrık ve birbirini dışlayan olaylar arasındaki farkı örnekle açıkla.
8. Inclusion-exclusion kuralını üç olay için yaz.
9. En az bir başarının olasılığını tümleyen üzerinden hesapla.
10. Birthday paradox problemini küçük grup boyutları için simüle et.

## B. Koşullu olasılık ve bağımsızlık

11. Bir torbadan geri koymadan top çekme deneyinde koşullu olasılık hesapla.
12. Aynı deneyi geri koyarak tekrarla ve bağımsızlığı yorumla.
13. `P(A|B)` ile `P(B|A)` karışıklığını gösteren bir örnek kur.
14. İki olayın bağımsızlığını sayısal toleransla test eden fonksiyon yaz.
15. Pairwise independence ile mutual independence farkını araştır.
16. Simpson paradoksunu küçük bir tabloyla göster.
17. Toplam olasılık kuralını üç sınıflı bir veri kaynağına uygula.
18. Selection bias'ın koşullu olasılıkları nasıl bozduğunu açıkla.
19. Confusion matrix'ten sensitivity ve specificity hesapla.
20. Base rate düşükken pozitif predictive value davranışını çizelgele.

## C. Rassal değişkenler ve dağılımlar

21. Bernoulli PMF değerlerinin toplamını doğrula.
22. Binomial dağılımın mean ve variance formüllerini simülasyonla test et.
23. Categorical örnekleyici yaz.
24. Geometric dağılımı Bernoulli denemeleriyle simüle et.
25. Poisson PMF toplamını sonlu bir üst sınıra kadar yaklaşıkla.
26. Poisson dağılımında `λ` arttıkça şeklin nasıl değiştiğini raporla.
27. Exponential örneklerinin memoryless özelliğini deneysel olarak test et.
28. Uniform dağılımın teorik mean ve variance değerlerini türet.
29. Normal PDF'nin sayısal integralini yaklaşık bir olarak doğrula.
30. Standard normal için z-score dönüşümü uygula.
31. Heavy-tailed bir dağılım ile normal dağılımı aykırı değer açısından karşılaştır.
32. Mixture distribution üret ve tek Gaussian varsayımının neden yetersiz kaldığını göster.
33. Empirical CDF fonksiyonu geliştir.
34. Quantile tahmini için lineer interpolation uygula.
35. Random seed kullanılmayan deneylerin yeniden üretilebilirliğini incele.

## D. Beklenti, varyans ve ilişki

36. Beklentinin lineerliğini bağımlı değişkenlerle göster.
37. `Var(aX+b)` formülünü türet ve test et.
38. `Var(X+Y)` formülünde covariance teriminin rolünü açıkla.
39. Online mean algoritması yaz.
40. Welford algoritmasıyla online variance hesapla.
41. Population ve sample variance farkını küçük veri üzerinde göster.
42. Covariance matrisini saf Python ile hesapla.
43. Sıfır covariance fakat bağımlı değişken örneği üret.
44. Pearson correlation'ın aykırı değerlere duyarlılığını ölç.
45. Correlation ile nedensellik arasındaki farkı gerçekçi bir senaryoyla açıkla.
46. Weighted expectation hesaplayan güvenli bir fonksiyon yaz.
47. Bias-variance ayrımını bir tahmin edici üzerinden tartış.
48. Standard error ile standard deviation farkını örnekle açıkla.
49. Bootstrap ile mean için güven aralığı tahmin et.
50. Monte Carlo tahmin hatasını örnek sayısına göre ölç.

## E. LLN, CLT ve örnekleme

51. Bir Bernoulli süreci için running mean üret.
52. Tek bir koşuda running mean'in neden monoton olmadığını göster.
53. Farklı sample size değerleri için örnek ortalaması varyansını ölç.
54. Exponential veriden örnek ortalamaları üreterek CLT'yi gözlemle.
55. Çok ağır kuyruklu bir dağılımda CLT yakınsamasını tartış.
56. IID varsayımının bozulduğu zaman serisinde örnek ortalamasını incele.
57. Sampling with replacement ve without replacement farkını ölç.
58. Stratified sampling tasarla.
59. Importance sampling fikrini basit integral üzerinde uygula.
60. Rejection sampling ile hedef dağılımdan örnek üret.

## F. Bayes ve sınıflandırma

61. Binary Bayes posterior formülünü toplam olasılıktan türet.
62. Farklı prior değerlerinin posterior üzerindeki etkisini tabloyla göster.
63. Ardışık iki bağımsız gözlem sonrası posterior güncellemesi yap.
64. Likelihood ile probability of parameters ayrımını açıkla.
65. MAP ve maximum likelihood tahminlerini karşılaştır.
66. Laplace smoothing'in categorical Naive Bayes üzerindeki etkisini göster.
67. Gaussian Naive Bayes'i iki boyutlu veri üzerinde eğit.
68. Sıfır varyanslı özellik için smoothing olmadan oluşan sorunu göster.
69. Probability multiplication ile oluşan underflow'u log-uzayıyla düzelt.
70. Log-sum-exp fonksiyonunu test et.
71. Eğitim verisinden öğrenilen prior ile uniform prior'ı karşılaştır.
72. Feature independence varsayımının ihlal edildiği veri üret.
73. Correlated feature'ların Naive Bayes posterior güvenine etkisini ölç.
74. Class imbalance altında accuracy'nin yetersizliğini göster.
75. Decision threshold taraması yap.
76. False-negative maliyeti yüksek bir senaryoda optimum eşik bul.
77. Binary log-loss hesapla.
78. Brier score uygula.
79. Reliability diagram verilerini üret.
80. Expected calibration error hesapla.

## G. Üretim ve yorumlama

81. Veri sızıntısı içeren hatalı bir pipeline yaz ve düzelt.
82. Missing value bulunan veride açık hata politikası tasarla.
83. Out-of-distribution örneklerde posterior güvenini incele.
84. Model çıktısının calibration olmadan neden güven skoru sayılamayacağını açıkla.
85. Prior drift izleme metriği tasarla.
86. Class-conditional dağılım değişimini algılayan basit kontrol yaz.
87. NaN ve infinity girişleri için testler ekle.
88. Model parametrelerini JSON uyumlu biçimde serileştirme tasarımı yap.
89. Random seed ve deney yapılandırmasını rapora kaydet.
90. Accuracy, log-loss ve calibration arasında karar verirken kullanılacak değerlendirme kontrol listesi hazırla.
