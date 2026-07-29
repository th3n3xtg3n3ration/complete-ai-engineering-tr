# Mülakat Soruları — İstatistiksel Çıkarım, MLE ve Hipotez Testi

## Temel sorular

1. Population, sample, parameter ve statistic arasındaki fark nedir?
2. Estimator ile estimate arasındaki farkı nasıl açıklarsın?
3. Sampling distribution nedir ve neden önemlidir?
4. Bias ve variance arasındaki dengeyi anlat.
5. Consistent estimator ne demektir?
6. Standard deviation ile standard error arasındaki fark nedir?
7. Sample size arttığında standard error nasıl değişir?
8. Confidence interval nasıl doğru yorumlanır?
9. Bootstrap hangi durumlarda faydalıdır?
10. Basit bootstrap hangi durumlarda yanıltıcı olabilir?

## Likelihood ve tahmin

11. Probability ile likelihood arasındaki fark nedir?
12. Neden likelihood yerine log-likelihood optimize edilir?
13. Bernoulli parametresinin MLE değerini nasıl türetirsin?
14. Gaussian mean ve variance MLE değerleri nelerdir?
15. Gaussian variance MLE neden unbiased sample variance ile aynı değildir?
16. MLE hangi koşullarda kötü davranabilir?
17. MLE ile MAP arasındaki fark nedir?
18. Prior veri arttıkça MAP tahminini nasıl etkiler?
19. Regularization neden MAP perspektifiyle yorumlanabilir?
20. Flat likelihood surface ne anlama gelir?

## Hipotez testi

21. p-value nedir?
22. p-value ne değildir?
23. Alpha ne zaman belirlenmelidir?
24. Type I ve Type II error arasındaki fark nedir?
25. Statistical power nasıl artırılabilir?
26. Failure to reject neden null hypothesis'i kanıtlamaz?
27. One-sided test ne zaman kullanılmalıdır?
28. Confidence interval ile two-sided test kararı arasındaki ilişki nedir?
29. Statistical significance ile practical significance arasındaki fark nedir?
30. Effect size neden p-value ile birlikte raporlanmalıdır?

## A/B test ve üretim

31. Bir A/B testinde randomization unit neden önemlidir?
32. Sample ratio mismatch nedir ve nasıl teşhis edilir?
33. Peeking neden false-positive oranını artırır?
34. Fixed-horizon ile sequential testing arasındaki fark nedir?
35. Primary metric ve guardrail metric nasıl seçilir?
36. Multiple testing problemi nedir?
37. Bonferroni ve Benjamini–Hochberg arasındaki fark nedir?
38. Permutation test hangi varsayıma dayanır?
39. Dönüşüm oranı testinde absolute lift ile relative lift neden birlikte verilmelidir?
40. Çok büyük örneklemde neden anlamsız derecede küçük farklar significant olabilir?
41. A/A test ne işe yarar?
42. Experiment logging hataları sonucu nasıl bozabilir?
43. Kullanıcı düzeyinde randomization yapılmışken session düzeyinde analiz neden risklidir?
44. Bir model benchmark farkı için confidence interval nasıl üretirsin?
45. Hyperparameter search'te multiple testing riskini nasıl yönetirsin?
46. Bir retrieval değişikliğinin kalite, latency ve maliyet etkilerini nasıl birlikte test edersin?
47. Missing data deney sonucunu nasıl yanlı hale getirebilir?
48. Outlier exclusion kuralı ne zaman belirlenmelidir?
49. Bir sonuç significant fakat guardrail kötüleşmişse nasıl karar verirsin?
50. İyi bir deney raporunda hangi bilgiler zorunlu olmalıdır?

## Kodlama soruları

51. Saf Python ile sample variance fonksiyonu yaz.
52. Seed kontrollü bootstrap mean interval fonksiyonu yaz.
53. Bernoulli log-likelihood fonksiyonu yaz.
54. Gaussian MLE hesaplayan fonksiyon yaz.
55. Two-sided normal p-value fonksiyonu yaz.
56. İki bağımsız ortalama için unequal-variance standard error hesapla.
57. İki conversion rate için pooled z test uygula.
58. Seed kontrollü permutation test yaz.
59. Bonferroni adjusted p-value fonksiyonu yaz.
60. Benjamini–Hochberg adjusted p-value algoritması yaz.

## Güçlü cevapta beklenenler

Güçlü bir aday:

- Formülleri yalnızca ezberden değil, varsayımlarıyla açıklar.
- p-value'yu posterior probability gibi yorumlamaz.
- Point estimate, confidence interval ve effect size'ı birlikte düşünür.
- Randomization unit, leakage, peeking ve sample ratio mismatch risklerini bilir.
- Parametrik testlerin küçük örneklem ve dağılım varsayımlarını belirtir.
- Bootstrap ve permutation test'in de varsayımsız olmadığını vurgular.
- Multiple testing düzeltmesini deney planının parçası olarak görür.
- Statistical significance ile ürün kararını birbirinden ayırır.
- Reproducibility için seed, veri aralığı, kod sürümü ve exclusion kurallarını kaydeder.
