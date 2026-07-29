# Alıştırmalar — İstatistiksel Çıkarım, MLE ve Hipotez Testi

## A. Temel kavramlar

1. Population, sample, parameter ve statistic kavramlarını tek bir ürün analitiği örneğiyle açıkla.
2. Estimator ile estimate arasındaki farkı yaz.
3. Sampling distribution neden veri dağılımıyla aynı şey değildir?
4. Unbiased bir estimator neden her zaman en iyi estimator değildir?
5. Bias–variance decomposition formülünü yaz ve yorumla.
6. Consistency kavramını örneklem büyüklüğü üzerinden açıkla.
7. Efficiency karşılaştırması hangi koşullar altında anlamlıdır?
8. Standard deviation ile standard error arasındaki farkı açıkla.
9. Örneklem büyüklüğü 100'den 400'e çıkınca mean standard error yaklaşık nasıl değişir?
10. Random sampling ile convenience sampling arasındaki çıkarım farkını tartış.

## B. Point estimation ve güven aralıkları

11. `[4, 5, 7, 8, 11]` için sample mean hesapla.
12. Aynı veri için population variance ve sample variance hesapla.
13. Sample standard deviation ve mean standard error hesapla.
14. Yüzde 95 normal confidence interval üret.
15. Confidence interval genişliğini azaltmanın üç yolunu yaz.
16. Yüzde 95 confidence interval için doğru frequentist yorumu yaz.
17. “Parametrenin bu aralıkta olma olasılığı yüzde 95” ifadesinin neden sorunlu olduğunu açıkla.
18. Küçük örneklemde normal kritik değer yerine t kritik değeri kullanımını tartış.
19. Outlier içeren veride mean confidence interval davranışını incele.
20. Median için analitik confidence interval yerine bootstrap kullanmanın avantajını açıkla.

## C. Bootstrap

21. Replacement ile sampling neden bootstrap'ın temelidir?
22. 1.000 ve 10.000 bootstrap resample sonuçlarını karşılaştır.
23. Mean için bootstrap standard error hesapla.
24. Median için percentile interval hesapla.
25. Bootstrap interval'ın seed değişimine hassasiyetini incele.
26. Çok küçük örneklemde bootstrap'ın sınırlamalarını yaz.
27. Time-series verisinde iid bootstrap neden yanlış olabilir?
28. Block bootstrap fikrini araştırmadan kendi sözlerinle tanımla.
29. Skewed dağılımda normal interval ile percentile interval'ı karşılaştır.
30. Bootstrap dağılımının bias gösterip göstermediğini ölçen bir fonksiyon yaz.

## D. Likelihood ve MLE

31. Probability ile likelihood arasındaki yön farkını açıkla.
32. Bağımsız Bernoulli gözlemlerinin likelihood fonksiyonunu yaz.
33. Aynı fonksiyonun log-likelihood biçimini türet.
34. `[1, 0, 1, 1, 0]` için Bernoulli MLE hesapla.
35. `p=0.2`, `p=0.6` ve `p=0.9` log-likelihood değerlerini karşılaştır.
36. Log-likelihood kullanımının underflow riskini nasıl azalttığını göster.
37. Gaussian mean MLE değerini türet.
38. Gaussian variance MLE ile unbiased sample variance farkını açıkla.
39. Grid-search MLE ile closed-form MLE sonuçlarını karşılaştır.
40. Likelihood yüzeyinin düz olması parameter uncertainty hakkında ne söyler?

## E. MAP ve regularization

41. MLE ile MAP arasındaki temel farkı yaz.
42. Beta prior ile Bernoulli likelihood neden conjugate çifttir?
43. `Beta(2, 8)` prior altında 3 success ve 2 failure için posterior parametrelerini hesapla.
44. Aynı veri için posterior mean ve MAP değerlerini karşılaştır.
45. Veri miktarı arttıkça prior etkisini simülasyonla göster.
46. Güçlü fakat yanlış prior'ın küçük örneklemde riskini tartış.
47. Gaussian prior ile L2 regularization arasındaki ilişkiyi açıkla.
48. Laplace prior ile L1 regularization bağlantısını açıklamaya çalış.
49. MAP tahmininin tam Bayesian posterior özeti olmadığını açıkla.
50. Posterior predictive düşüncesinin point estimate yaklaşımından farkını yaz.

## F. Hipotez testi

51. Null ve alternative hypothesis'i bir latency deneyi için yaz.
52. p-value tanımını doğru biçimde yaz.
53. p-value'nun null hypothesis'in doğru olma olasılığı olmadığını açıkla.
54. Alpha değerini veriye baktıktan sonra değiştirmenin sakıncasını yaz.
55. One-sided ve two-sided test kullanımını karşılaştır.
56. Type I ve Type II error için ürün örnekleri ver.
57. Statistical power'ı artırmanın dört yolunu yaz.
58. Büyük sample size ile önemsiz farkların anlamlı hale gelmesini açıkla.
59. Failure to reject ile null'u doğrulamak arasındaki farkı yaz.
60. Confidence interval ile hypothesis test kararının ilişkisini açıkla.

## G. Effect size ve A/B testleri

61. Control rate yüzde 10, treatment rate yüzde 11 ise absolute ve relative lift hesapla.
62. Relative lift raporunda baseline neden zorunludur?
63. Cohen's d formülünü yaz.
64. Effect size ile p-value arasındaki farkı açıkla.
65. Minimum practical effect nasıl belirlenebilir?
66. Conversion testi için pooled standard error neden null altında kullanılır?
67. Confidence interval'ın sıfırı kapsaması ne anlama gelir?
68. Sample ratio mismatch için olası üç mühendislik nedeni yaz.
69. Randomization unit ile analysis unit uyuşmazlığına örnek ver.
70. Guardrail metric kullanımını açıkla.

## H. Permutation ve multiple testing

71. Permutation test'in exchangeability varsayımını açıkla.
72. Parametrik test ile permutation test sonuçlarının farklılaşabileceği bir veri yapısı tasarla.
73. Monte Carlo permutation p-value için `+1` düzeltmesinin amacını araştır ve açıkla.
74. Aynı deneyde 20 metric test etmenin false-positive riskini simüle et.
75. Bonferroni threshold'u 10 test ve alpha 0.05 için hesapla.
76. Bonferroni yönteminin neden muhafazakâr olabileceğini açıkla.
77. Benjamini–Hochberg prosedürünü sıralı p-value listesi üzerinde elle uygula.
78. FWER ile FDR arasındaki farkı yaz.
79. Hyperparameter search sonuçlarında multiple testing sorununu tartış.
80. Yalnızca en iyi benchmark skorunu raporlamanın istatistiksel riskini açıkla.

## I. Üretim ve etik

81. Peeking'in false-positive oranını neden artırdığını simüle et.
82. Fixed-horizon test ile sequential test farkını yaz.
83. Missing data mekanizmasının çıkarımı nasıl bozabileceğini açıkla.
84. Veri exclusion kuralını sonuçlara baktıktan sonra belirlemenin riskini yaz.
85. A/A testinin ne amaçla kullanılabileceğini açıkla.
86. Logging değişikliklerinin deney sonuçlarını nasıl sahte biçimde etkileyebileceğini göster.
87. Fairness metriği karşılaştırmasında sample size dengesizliğini tartış.
88. Model latency karşılaştırmasında bağımlı ölçümler için paired design öner.
89. Bir deney raporu için reproducibility checklist hazırla.
90. İstatistiksel anlamlı fakat kullanıcıya zarar veren bir sonuç için karar süreci tasarla.
