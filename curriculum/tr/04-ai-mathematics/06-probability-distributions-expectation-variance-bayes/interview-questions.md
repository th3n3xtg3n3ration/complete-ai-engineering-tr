# Mülakat Soruları — Olasılık, Dağılımlar ve Bayes

## Temel sorular

1. Koşullu olasılığı sezgisel ve matematiksel olarak açıklar mısın?
2. Bağımsızlık ile birbirini dışlama arasındaki fark nedir?
3. Beklentinin lineerliği neden önemlidir ve bağımsızlık gerektirir mi?
4. Population variance ile sample variance arasındaki fark nedir?
5. Standard deviation ile standard error arasındaki fark nedir?
6. Covariance ve correlation neyi ölçer? Hangi durumlarda yanıltıcı olabilir?
7. Ayrık ve sürekli rassal değişkenlerin olasılık fonksiyonları nasıl farklıdır?
8. Bernoulli, Binomial ve Categorical dağılımlarını hangi problemlerde kullanırsın?
9. Poisson ve Exponential dağılımlarının ilişkisi nedir?
10. Normal dağılım varsayımını nasıl kontrol edersin?

## Orta seviye sorular

11. Law of Large Numbers ile Central Limit Theorem arasındaki fark nedir?
12. CLT, ham verinin normal dağıldığını söyler mi?
13. Bayes teoremindeki prior, likelihood, evidence ve posterior terimlerini açıklar mısın?
14. Base-rate fallacy nedir?
15. MAP ile maximum likelihood arasındaki ilişki nedir?
16. Naive Bayes neden “naive” olarak adlandırılır?
17. Naive Bayes'in bağımsızlık varsayımı yanlış olduğu halde model neden iyi çalışabilir?
18. Gaussian Naive Bayes ile Multinomial Naive Bayes arasındaki fark nedir?
19. Sıfır frekans problemi nedir ve Laplace smoothing nasıl çözer?
20. Gaussian Naive Bayes'te sıfıra yakın varyans hangi sayısal probleme yol açar?

## Uygulama ve üretim soruları

21. Çok küçük olasılıkları çarparken underflow'u nasıl önlersin?
22. Log-sum-exp tekniğini açıklar mısın?
23. Bir olasılık modelinde calibration'ı nasıl ölçersin?
24. Accuracy yüksek ama log-loss kötü olabilir mi? Nasıl?
25. Brier score ile log-loss arasında nasıl seçim yaparsın?
26. Sınıf dengesizliğinde prior seçimi tahminleri nasıl etkiler?
27. Decision threshold neden her zaman `0.5` olmamalıdır?
28. False-negative maliyeti yüksek bir sistemde eşik nasıl seçilir?
29. Calibration için validation ve test verilerini nasıl ayırırsın?
30. Prior probability shift nasıl izlenebilir?
31. Feature distribution shift, Gaussian Naive Bayes'i nasıl etkiler?
32. Out-of-distribution girdilerde yüksek posterior güveni neden oluşabilir?
33. Modelin probability çıktısını kullanıcıya “güven” olarak sunmadan önce hangi kontrolleri yaparsın?
34. Eksik değerleri Gaussian Naive Bayes pipeline'ında nasıl ele alırsın?
35. Model parametrelerini ve random seed'i neden kaydetmek gerekir?

## Derinlemesine sorular

36. Sıfır covariance bağımsızlık anlamına gelmez. Bir karşı örnek verebilir misin?
37. Monte Carlo tahmin hatası neden tipik olarak `1/√N` ölçeğinde azalır?
38. Importance sampling hangi durumda faydalıdır?
39. Posterior predictive distribution nedir?
40. Conjugate prior kavramı ne sağlar?
41. Bernoulli likelihood için Beta prior neden kullanışlıdır?
42. Bayesian credible interval ile frequentist confidence interval arasındaki fark nedir?
43. Evidence veya marginal likelihood model karşılaştırmasında nasıl kullanılır?
44. Naive Bayes karar sınırının kullanılan koşullu dağılıma göre şekli nasıl değişir?
45. Correlated features Naive Bayes'in olasılık kalibrasyonunu neden bozabilir?

## Kodlama soruları

46. Saf Python ile numerically stable `logsumexp` yaz.
47. Bernoulli ve Binomial PMF fonksiyonlarını input validation ile uygula.
48. Online mean ve variance algoritması geliştir.
49. Binary log-loss fonksiyonunu clipping ile yaz.
50. Calibration bin'lerini hesaplayan fonksiyon yaz.
51. Confusion matrix'ten precision, recall ve F1 çıkar.
52. Binary Bayes update fonksiyonunu sıfır evidence kontrolüyle uygula.
53. Gaussian log-likelihood fonksiyonu yaz.
54. `fit/predict_proba` arayüzlü küçük bir Gaussian Naive Bayes sınıfı tasarla.
55. Sabit seed ile tekrarlanabilir train/test split yaz.

## Sistem tasarımı sorusu

Bir fraud detection sistemi tasarlıyorsun. Pozitif sınıf çok nadir, yanlış negatif pahalı ve veri dağılımı zamanla değişiyor. Aşağıdakileri açıkla:

- Prior nasıl tahmin edilir ve izlenir?
- Model olasılıkları nasıl calibrated edilir?
- Eşik nasıl maliyet duyarlı seçilir?
- Hangi metrikler dashboard'da tutulur?
- Drift algılandığında hangi aksiyonlar alınır?
- Test verisi ve online geri bildirim arasında sızıntı nasıl önlenir?
