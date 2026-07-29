# Quiz — İstatistiksel Çıkarım, MLE ve Hipotez Testi

Her soru için en uygun seçeneği işaretle.

## Sorular

1. Aşağıdakilerden hangisi parametredir?
   - A) Bir örneklemin ortalaması
   - B) Evrendeki gerçek dönüşüm oranı
   - C) Bootstrap ortalamalarının listesi
   - D) Bir testin p-value değeri

2. Standard error neyi ölçer?
   - A) Tekil gözlemlerin hatasını
   - B) Bir tahmin edicinin örneklemler arası değişkenliğini
   - C) Modelin eğitim loss'unu
   - D) Veri giriş hatalarının sayısını

3. Sample size dört katına çıkarsa mean standard error yaklaşık nasıl değişir?
   - A) Dört katına çıkar
   - B) İki katına çıkar
   - C) Yarıya iner
   - D) Değişmez

4. Yüzde 95 confidence interval'ın doğru frequentist yorumu hangisidir?
   - A) Parametrenin bu aralıkta olma olasılığı kesin olarak yüzde 95'tir
   - B) Verinin yüzde 95'i aralıktadır
   - C) Aynı prosedür tekrarlandığında aralıkların yaklaşık yüzde 95'i gerçek parametreyi kapsar
   - D) Null hypothesis yüzde 95 olasılıkla doğrudur

5. Bootstrap örnekleri nasıl üretilir?
   - A) Replacement olmadan daha küçük örnekler çekerek
   - B) Gözlenen örneklemden replacement ile aynı büyüklükte örnekler çekerek
   - C) Yalnızca normal dağılımdan veri üreterek
   - D) Parametreleri rastgele değiştirerek

6. Likelihood hangi bakış açısını kullanır?
   - A) Parametre sabit, veri değişken
   - B) Veri sabit, parametre adayları karşılaştırılıyor
   - C) Hem veri hem parametre sabit
   - D) Yalnızca prior dağılımı inceleniyor

7. Log-likelihood neden tercih edilir?
   - A) Her zaman pozitif olduğu için
   - B) Çarpımları toplama dönüştürüp sayısal kararlılığı artırdığı için
   - C) Prior ihtiyacını ortadan kaldırdığı için
   - D) Bias değerini sıfırladığı için

8. Bernoulli parametresinin MLE değeri nedir?
   - A) Sample median
   - B) Sample variance
   - C) Success oranı
   - D) Standard error

9. Gaussian variance MLE hangi paydayı kullanır?
   - A) `n`
   - B) `n - 1`
   - C) `sqrt(n)`
   - D) `n + 1`

10. MAP tahmini MLE'den hangi bilgiyle ayrılır?
    - A) Bootstrap dağılımı
    - B) Prior dağılımı
    - C) Test statistic
    - D) Confidence level

11. p-value aşağıdakilerden hangisidir?
    - A) Null hypothesis'in doğru olma olasılığı
    - B) Alternative hypothesis'in doğru olma olasılığı
    - C) Null doğru kabul edildiğinde gözlenen kadar veya daha uç sonuç olasılığı
    - D) Effect size'ın normalize edilmiş hali

12. Type I error nedir?
    - A) Gerçek etkiyi kaçırmak
    - B) Etki yokken null'u reddetmek
    - C) Confidence interval'ı geniş hesaplamak
    - D) Sample size'ı küçük seçmek

13. Statistical power nedir?
    - A) Gerçek bir etkiyi yakalama olasılığı
    - B) Null'un doğru olma olasılığı
    - C) Test statistic'in mutlak değeri
    - D) Standard deviation'ın karesi

14. Büyük örneklemde çok küçük bir farkın anlamlı çıkması neyi gösterir?
    - A) Fark mutlaka iş açısından önemlidir
    - B) Statistical significance ile practical significance ayrılmalıdır
    - C) p-value yanlış hesaplanmıştır
    - D) Bootstrap kullanılamaz

15. Permutation test'in temel varsayımı hangisidir?
    - A) Tüm veriler Gaussian olmalıdır
    - B) Null altında grup etiketleri exchangeable olmalıdır
    - C) Variance sıfır olmalıdır
    - D) Sample size'lar eşit olmalıdır

16. Bonferroni düzeltmesi esas olarak neyi kontrol eder?
    - A) False discovery rate
    - B) Family-wise error rate
    - C) Statistical power'ı maksimum yapmayı
    - D) Effect size'ı

17. Benjamini–Hochberg yöntemi neyi kontrol etmeyi hedefler?
    - A) False discovery rate
    - B) Standard error
    - C) Sample ratio mismatch
    - D) Bias

18. Peeking neden sorunludur?
    - A) Sample mean'i her zaman küçültür
    - B) Nominal false-positive oranını bozabilir
    - C) Effect size'ı sıfırlar
    - D) Randomization'ı otomatik düzeltir

19. Sample ratio mismatch neye işaret edebilir?
    - A) Yalnızca model overfitting'ine
    - B) Assignment, logging veya eligibility hatasına
    - C) Confidence interval'ın doğru olduğuna
    - D) Prior'ın güçlü olduğuna

20. En iyi deney raporu hangilerini birlikte sunar?
    - A) Yalnızca p-value
    - B) Yalnızca point estimate
    - C) Estimate, confidence interval, effect size, assumptions ve practical significance
    - D) Yalnızca sample size

## Cevap anahtarı

1. B
2. B
3. C
4. C
5. B
6. B
7. B
8. C
9. A
10. B
11. C
12. B
13. A
14. B
15. B
16. B
17. A
18. B
19. B
20. C
