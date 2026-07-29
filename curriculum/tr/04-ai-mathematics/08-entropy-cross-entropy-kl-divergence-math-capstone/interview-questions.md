# Mülakat Soruları — Bilgi Teorisi ve AI Matematik Capstone

## Temel seviye

1. Surprisal nedir ve neden negatif logaritmayla tanımlanır?
2. Entropi neyi ölçer?
3. Deterministik dağılımın entropisi neden sıfırdır?
4. Binary entropy hangi noktada maksimumdur?
5. Cross-entropy ile entropy arasındaki fark nedir?
6. One-hot hedefte cross-entropy nasıl sadeleşir?
7. KL divergence neden simetrik değildir?
8. Jensen–Shannon divergence ne avantaj sağlar?
9. Mutual information neyi ölçer?
10. Perplexity nasıl yorumlanır?

## Orta seviye

11. `H(P,Q)=H(P)+KL(P||Q)` eşitliğinin model eğitimindeki anlamı nedir?
12. `P` pozitif kütle verirken `Q` sıfır verirse ne olur?
13. Softmax overflow problemi nasıl önlenir?
14. Log-softmax neden önce softmax sonra log almaktan daha güvenlidir?
15. BCE'yi logits üzerinden kararlı biçimde nasıl hesaplarsınız?
16. Label smoothing gradient davranışını nasıl değiştirir?
17. Focal loss hangi problemlerde yararlıdır?
18. Class weighting ile focal loss arasındaki fark nedir?
19. Accuracy yüksekken calibration neden kötü olabilir?
20. Brier score ile negative log-likelihood'i karşılaştırın.
21. ECE nasıl hesaplanır ve hangi sınırlılıklara sahiptir?
22. Predictive entropy ile aleatoric/epistemic belirsizlik aynı şey midir?
23. KL divergence'ın yönü model davranışını nasıl etkileyebilir?
24. Mutual information feature selection'da nasıl kullanılabilir?
25. Perplexity karşılaştırmalarında tokenization neden önemlidir?

## İleri seviye

26. Softmax regression için `dL/dlogits = p - y` sonucunu türetin.
27. Softmax Jacobian'ını açıklayın.
28. Cross-entropy ile softmax birlikte kullanıldığında gradient neden sadeleşir?
29. Label smoothing'in calibration ve accuracy üzerindeki olası etkilerini tartışın.
30. L2 regularization confidence değerlerini nasıl etkileyebilir?
31. Distribution shift sırasında entropy ve JS divergence nasıl izlenebilir?
32. Model çıktılarında sıfır olasılıkların üretim riskleri nelerdir?
33. `sum` ve `mean` reduction optimizer davranışını nasıl değiştirir?
34. Temperature scaling nasıl çalışır?
35. Reliability diagram hangi bilgiyi verir?
36. ECE bin sayısına neden duyarlıdır?
37. Multiclass calibration için top-label ECE'nin sınırlılıkları nelerdir?
38. KL yerine JS divergence tercih edeceğiniz bir örnek verin.
39. Entropy regularization hangi amaçlarla kullanılabilir?
40. Knowledge distillation'da temperature ve KL divergence nasıl kullanılır?

## Sistem tasarımı ve hata analizi

41. Üretimde model confidence drift'ini nasıl izlersiniz?
42. Accuracy sabitken cross-entropy artıyorsa ne düşünürsünüz?
43. Validation loss azalırken ECE artıyorsa hangi adımları atarsınız?
44. Class imbalance olan sistemde hangi loss ve metrikleri seçersiniz?
45. Çok büyük logits gözlemlendiğinde hangi sayısal kontrolleri yaparsınız?
46. Bir loss kütüphanesinin API tasarımında hangi reduction seçeneklerini sunarsınız?
47. Olasılık girdilerini sessizce normalize etmek neden risklidir?
48. Eğitim ve serving softmax implementasyonlarının farklı olması ne tür hata üretir?
49. Seed tekrarlanabilirliği için hangi bileşenleri kontrol edersiniz?
50. Saf Python capstone'u üretim kalitesine taşımak için hangi mimari değişiklikleri yaparsınız?

## Beklenen cevap özellikleri

Güçlü bir aday:

- formülleri yalnızca ezberden söylemez, sezgisel anlamlarını açıklar,
- sayısal kararlılık ve sınır durumlarını dikkate alır,
- accuracy ile probability quality arasındaki farkı bilir,
- loss, gradient ve optimizasyon ilişkisini kurar,
- üretim izleme ve distribution shift risklerini tartışır,
- deneylerin tekrarlanabilirliğini önemser.
