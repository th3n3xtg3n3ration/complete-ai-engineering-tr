# Quiz — Logistic Regression, Threshold ve Calibration

1. Logistic regression'ın doğrusal olarak modellediği büyüklük nedir?
2. Sigmoid fonksiyonunun çıktı aralığı nedir?
3. Log loss aşırı güvenli yanlış tahminleri neden güçlü cezalandırır?
4. Maximum likelihood ile cross-entropy arasındaki ilişki nedir?
5. L2 regularization katsayılara nasıl etki eder?
6. scikit-learn logistic regression'da küçük `C` ne anlama gelir?
7. Accuracy dengesiz sınıflarda neden yanıltıcıdır?
8. Precision hangi soruyu yanıtlar?
9. Recall hangi soruyu yanıtlar?
10. Balanced accuracy nasıl hesaplanır?
11. ROC-AUC threshold seçer mi?
12. Average precision hangi durumda daha bilgilendiricidir?
13. Varsayılan 0.5 threshold neden her iş problemi için uygun değildir?
14. Yanlış negatif maliyeti yükselirse optimum threshold genellikle hangi yönde hareket eder?
15. Calibration ile discrimination arasındaki fark nedir?
16. Brier score neyi ölçer?
17. Reliability diagram nasıl yorumlanır?
18. Platt scaling hangi tür dönüşüm öğrenir?
19. Isotonic regression'ın temel riski nedir?
20. Calibration neden cross-validation veya ayrı bir calibration setiyle yapılmalıdır?

## Cevap anahtarı

1. Log-odds.
2. Sıfır ile bir arası.
3. Logaritmik ceza probability sıfıra yaklaştıkça büyür.
4. Negatif log-likelihood binary cross-entropy loss'a eşdeğerdir.
5. Katsayıları sıfıra doğru küçültür.
6. Daha güçlü regularization.
7. Çoğunluk sınıfı tahmini yüksek accuracy verebilir.
8. Pozitif tahminlerin ne kadarı doğru?
9. Gerçek pozitiflerin ne kadarı yakalandı?
10. Sınıf başına recall değerlerinin ortalaması.
11. Hayır, ranking kalitesini özetler.
12. Pozitif sınıf seyrekken.
13. İş maliyetleri ve prevalence simetrik olmayabilir.
14. Düşer.
15. Discrimination sıralamayı, calibration olasılık doğruluğunu ölçer.
16. Olasılıkların karesel tahmin hatasını.
17. Ortalama tahmin olasılığı gözlenen event rate ile karşılaştırılır.
18. Logistic/sigmoid dönüşüm.
19. Küçük veride overfit.
20. Aynı veriye fit edilen calibration iyimser sonuç üretir.
