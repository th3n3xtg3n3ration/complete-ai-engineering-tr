# Quiz — Olasılık, Dağılımlar, Beklenti, Varyans ve Bayes

Her soru için en doğru seçeneği işaretle. Cevap anahtarı sayfanın sonundadır.

## Sorular

1. `P(A|B)` hangi ifadeye eşittir?
   - A) `P(A)/P(B)`
   - B) `P(A∩B)/P(B)`
   - C) `P(A∪B)/P(B)`
   - D) `P(B|A)`

2. Bağımsız `A` ve `B` olayları için hangisi doğrudur?
   - A) `P(A∩B)=0`
   - B) `P(A∪B)=1`
   - C) `P(A∩B)=P(A)P(B)`
   - D) `P(A)=P(B)`

3. Beklentinin lineerliği için bağımsızlık gerekir mi?
   - A) Her zaman gerekir
   - B) Yalnızca sürekli değişkenlerde gerekir
   - C) Hayır
   - D) Yalnızca covariance sıfırsa gerekmez

4. Bernoulli dağılımının varyansı hangisidir?
   - A) `p²`
   - B) `p(1-p)`
   - C) `1-p`
   - D) `np`

5. Poisson dağılımında mean ve variance ilişkisi nedir?
   - A) İkisi de `λ`
   - B) Mean `λ²`, variance `λ`
   - C) Mean `0`, variance `1`
   - D) Her zaman farklıdır

6. Sürekli bir rassal değişken için tek bir noktanın olasılığı genellikle nedir?
   - A) PDF değerine eşittir
   - B) Birdir
   - C) Sıfırdır
   - D) Hesaplanamaz

7. Sample variance hesaplanırken neden çoğu zaman `n-1` kullanılır?
   - A) Hesabı hızlandırmak için
   - B) Mean'i sıfırlamak için
   - C) Population variance için unbiased tahmin elde etmek için
   - D) Sonucu normalize etmemek için

8. Correlation değeri `0` ise kesin olarak ne söylenebilir?
   - A) Değişkenler bağımsızdır
   - B) Doğrusal ilişki ölçümü sıfırdır
   - C) Değişkenler aynıdır
   - D) Nedensel ilişki yoktur

9. Central Limit Theorem temel olarak neyin dağılımını açıklar?
   - A) Her ham veri kümesinin
   - B) Normalize edilmiş toplam veya örnek ortalamasının
   - C) Yalnızca Bernoulli değişkenlerin
   - D) Model parametrelerinin

10. Bayes formülünde `P(D|H)` nedir?
    - A) Prior
    - B) Posterior
    - C) Likelihood
    - D) Evidence

11. Prior çok düşük olduğunda güçlü fakat kusurlu bir pozitif test sonucu için ne olabilir?
    - A) Posterior zorunlu olarak bire eşit olur
    - B) Base rate posterior'u önemli ölçüde sınırlayabilir
    - C) Likelihood önemsiz hale gelir
    - D) Evidence sıfır olur

12. Naive Bayes'in temel varsayımı nedir?
    - A) Tüm sınıflar eşit sıklıktadır
    - B) Özellikler tamamen bağımsızdır
    - C) Özellikler sınıf koşullu bağımsızdır
    - D) Her özellik uniform dağılır

13. Çok küçük olasılıkların çarpımı hangi probleme yol açabilir?
    - A) Overfitting
    - B) Underflow
    - C) Data leakage
    - D) Label shift

14. Naive Bayes'te underflow için yaygın çözüm nedir?
    - A) Olasılıkları karesini almak
    - B) Log-olasılıkları toplamak
    - C) Veriyi sıralamak
    - D) Sınıf sayısını azaltmak

15. Gaussian Naive Bayes'te variance smoothing neden kullanılır?
    - A) Sınıf sayısını artırmak için
    - B) Sıfıra yakın varyans nedeniyle oluşan sayısal sorunları önlemek için
    - C) Mean değerlerini eşitlemek için
    - D) Test verisini normalize etmek için

16. Monte Carlo tahmininde standart hata tipik olarak nasıl ölçeklenir?
    - A) `N`
    - B) `1/N`
    - C) `1/√N`
    - D) `log(N)`

17. Calibration hangi davranışı ölçer?
    - A) Tahmin süresini
    - B) Tahmin olasılıkları ile gözlenen frekansların uyumunu
    - C) Yalnızca accuracy değerini
    - D) Feature sayısını

18. Yanlış negatif maliyeti yüksekse hangi yaklaşım uygundur?
    - A) Karar eşiğini maliyet analiziyle seçmek
    - B) Eşiği her zaman `0.5` tutmak
    - C) Prior'ı sıfırlamak
    - D) Log-loss kullanmamak

19. Veri sızıntısı hangi durumda oluşur?
    - A) Eğitim istatistikleri yalnızca eğitim verisinden hesaplandığında
    - B) Test verisi model seçimi veya eğitim istatistiklerine dahil edildiğinde
    - C) Random seed sabitlendiğinde
    - D) Log-uzayı kullanıldığında

20. Accuracy yüksek fakat log-loss kötü ise olası açıklama nedir?
    - A) Model doğru sınıfları seçse de yanlış veya aşırı güvenli olasılıklar üretiyor olabilir
    - B) Model kesinlikle iyi calibrated'dır
    - C) Veride hiçbir belirsizlik yoktur
    - D) Accuracy yanlış hesaplanmıştır

## Cevap anahtarı

1. B
2. C
3. C
4. B
5. A
6. C
7. C
8. B
9. B
10. C
11. B
12. C
13. B
14. B
15. B
16. C
17. B
18. A
19. B
20. A

## Başarı ölçütü

- 18–20 doğru: Konuya hâkimsin.
- 15–17 doğru: Uygulamaya geçebilirsin; yanlışlarını teoriyle tekrar et.
- 11–14 doğru: Lab çalışmalarını tamamlayıp quizi yeniden çöz.
- 0–10 doğru: Koşullu olasılık, dağılımlar ve Bayes bölümlerini baştan çalış.
