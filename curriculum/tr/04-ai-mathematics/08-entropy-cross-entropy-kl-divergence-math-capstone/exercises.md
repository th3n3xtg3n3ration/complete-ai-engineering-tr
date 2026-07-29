# Alıştırmalar — Entropi, Cross-Entropy, KL Divergence ve Matematik Capstone

## A. Kavramsal sorular

1. Surprisal ile olasılık arasındaki ilişkiyi açıklayın.
2. Logaritma tabanının bilgi birimine etkisini yazın.
3. Entropi neden beklenen surprisal olarak tanımlanır?
4. Deterministik dağılımın entropisi neden sıfırdır?
5. Eşit dağılım neden maksimum entropiye sahiptir?
6. Binary entropy eğrisinin `p = 0.5` çevresindeki davranışını açıklayın.
7. Cross-entropy ile entropy arasındaki farkı yazın.
8. Cross-entropy neden gerçek dağılımdan daha küçük olamaz?
9. KL divergence neden simetrik değildir?
10. KL divergence neden uzaklık metriği değildir?
11. Jensen–Shannon divergence'ın KL'ye göre iki avantajını yazın.
12. Mutual information bağımsızlık hakkında ne söyler?
13. Conditional entropy neyi ölçer?
14. Softmax neden sınıf skorlarını olasılığa dönüştürür?
15. Softmax'a sabit bir sayı eklemek sonucu neden değiştirmez?
16. Log-sum-exp hilesi neden gereklidir?
17. Negative log-likelihood ile cross-entropy ilişkisini açıklayın.
18. Label smoothing hangi sorunu azaltmayı hedefler?
19. Focal loss hangi örneklerin etkisini azaltır?
20. Perplexity neden yalnızca aynı tokenization altında karşılaştırılmalıdır?
21. Accuracy ile calibration arasındaki farkı açıklayın.
22. Brier score ile cross-entropy'nin ceza davranışını karşılaştırın.
23. Class weighting ile label smoothing arasındaki farkı yazın.
24. Distribution shift sırasında predictive entropy nasıl kullanılabilir?
25. Düşük loss neden tek başına güvenilir model anlamına gelmez?

## B. El ile hesaplama

26. `(0.5, 0.5)` dağılımının entropisini bit cinsinden hesaplayın.
27. `(1, 0, 0, 0)` dağılımının entropisini hesaplayın.
28. `(0.25, 0.25, 0.25, 0.25)` dağılımının entropisini hesaplayın.
29. `P=(0.8,0.2)` ve `Q=(0.6,0.4)` için cross-entropy hesaplayın.
30. Aynı dağılımlar için `KL(P || Q)` hesaplayın.
31. `KL(Q || P)` hesaplayıp 30. soruyla karşılaştırın.
32. `H(P,Q)=H(P)+KL(P||Q)` eşitliğini sayısal olarak doğrulayın.
33. `(2, 1, 0)` logits için softmax değerlerini yaklaşık hesaplayın.
34. Aynı logits'e `100` ekleyerek sonucun değişmediğini gösterin.
35. Doğru sınıf olasılığı `0.9` olan örneğin NLL değerini hesaplayın.
36. Doğru sınıf olasılığı `0.01` olan örneğin NLL değerini hesaplayın.
37. Binary hedef `1`, logit `0` için BCE hesaplayın.
38. Binary hedef `0`, logit `2` için BCE hesaplayın.
39. Üç sınıfta smoothing `0.1` için hedef dağılımı oluşturun.
40. Ortalama NLL `ln(20)` ise perplexity değerini bulun.

## C. Kodlama görevleri

41. `surprisal` fonksiyonunu sıfırdan yazın.
42. `entropy` fonksiyonuna giriş doğrulama ekleyin.
43. `binary_entropy` fonksiyonunu yalnızca `entropy` kullanarak yazın.
44. `cross_entropy` fonksiyonunda destek uyuşmazlığını ele alın.
45. `kl_divergence` fonksiyonunu farklı log tabanlarını destekleyecek biçimde yazın.
46. Jensen–Shannon divergence uygulayın.
47. Normalize edilmemiş ağırlıkları dağılıma çeviren fonksiyon yazın.
48. Sayısal kararlı `log_sum_exp` uygulayın.
49. Sayısal kararlı `softmax` uygulayın.
50. `log_softmax` uygulayın.
51. Logits tabanlı binary cross-entropy uygulayın.
52. Categorical cross-entropy from logits uygulayın.
53. Label-smoothed cross-entropy uygulayın.
54. Binary focal loss uygulayın.
55. Multiclass Brier score uygulayın.
56. Top-label expected calibration error uygulayın.
57. Joint table'dan mutual information hesaplayın.
58. Confusion matrix üreten fonksiyon yazın.
59. Accuracy ve macro recall hesaplayın.
60. Probability vector girişleri için property-style testler yazın.

## D. Deney ve analiz

61. İki sınıflı dağılımda `p` değerini `0.01` adımlarla değiştirip binary entropy tablosu üretin.
62. Dört sınıflı eşit dağılım ile dengesiz dağılımı karşılaştırın.
63. `Q` dağılımını `P`'den uzaklaştırdıkça cross-entropy değişimini ölçün.
64. KL'nin yönünü üç farklı dağılım çiftiyle gösterin.
65. JS divergence ile KL divergence'ı destek uyuşmazlığında karşılaştırın.
66. Büyük pozitif ve negatif logits üzerinde softmax kararlılığını test edin.
67. Önce softmax sonra log ile doğrudan log-softmax sonuçlarını karşılaştırın.
68. Label smoothing değerini `0.0`, `0.05`, `0.1`, `0.2` olarak deneyin.
69. Focal loss için `gamma` değerini değiştirip kolay/zor örnek oranını ölçün.
70. Class imbalance oluşturup accuracy ile macro recall farkını gösterin.
71. Aynı accuracy'ye sahip iki modelin Brier score değerlerini karşılaştırın.
72. Confidence değerlerini yapay olarak büyütüp ECE değişimini ölçün.
73. Temperature scaling benzeri biçimde logits'i farklı sıcaklıklara bölün.
74. Predictive entropy ile hatalı tahminler arasındaki ilişkiyi inceleyin.
75. Distribution shift sonrası entropy, accuracy ve ECE değişimini raporlayın.

## E. Capstone görevleri

76. Softmax regression ağırlık ve bias boyutlarını açıklayın.
77. Tek örnek için logit gradient'ini türetin.
78. Ağırlık gradient'ini dış çarpım olarak gösterin.
79. L2 regularization gradient'ini ekleyin.
80. Model initialization için iki farklı ölçek deneyin.
81. Learning rate grid'i oluşturup yakınsamayı karşılaştırın.
82. Loss history içinde divergence algılayan kural yazın.
83. Early stopping ekleyin.
84. Train/validation bölmesi ekleyin.
85. Mini-batch eğitim ekleyin.
86. Gradient clipping ekleyin.
87. Class weights desteği ekleyin.
88. Per-class precision ve recall raporlayın.
89. Calibration histogramı için veri tablosu üretin.
90. Model çıktıları için ortalama entropy hesaplayın.
91. İki modelin tahmin dağılımları arasında ortalama JS divergence hesaplayın.
92. Label smoothing'in ağırlık normuna etkisini inceleyin.
93. L2 regularization'ın confidence üzerindeki etkisini ölçün.
94. Shifted test setinde karar sınırı davranışını yorumlayın.
95. Seed değişiminin sonuç varyansını raporlayın.
96. En iyi modeli yalnızca accuracy yerine çoklu metriklerle seçin.
97. Model kartı biçiminde sınırlılıkları yazın.
98. Deney konfigürasyonunu JSON olarak kaydeden yardımcı yazın.
99. Sonuçları Markdown tabloya dönüştüren raporlayıcı yazın.
100. Tüm modül kavramlarını kullanan teknik bir capstone raporu hazırlayın.
