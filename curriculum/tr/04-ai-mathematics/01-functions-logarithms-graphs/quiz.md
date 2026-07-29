# Quiz — Fonksiyonlar, Logaritmalar ve Grafikler

Her soru 5 puandır. Toplam 100 puan.

## Sorular

1. Bir fonksiyonun domain'i neyi ifade eder?

   A. Fonksiyonun gerçekten ürettiği çıktıları  
   B. Fonksiyonun kabul ettiği girdileri  
   C. Fonksiyonun yalnızca sıfır noktalarını  
   D. Fonksiyonun parametre sayısını

2. `f(x) = 4x - 3` fonksiyonunun eğimi nedir?

   A. `-3`  
   B. `1`  
   C. `3`  
   D. `4`

3. `log₂(32)` kaçtır?

   A. `4`  
   B. `5`  
   C. `8`  
   D. `16`

4. Aşağıdakilerden hangisi doğrudur?

   A. `log(xy) = log(x)log(y)`  
   B. `log(x/y) = log(x) + log(y)`  
   C. `log(x^k) = k log(x)`  
   D. `log(0) = 0`

5. `(f ∘ g)(x)` ne anlama gelir?

   A. `f(x) + g(x)`  
   B. `f(g(x))`  
   C. `g(f(x))` ile her zaman aynı sonuç  
   D. `f(x) / g(x)`

6. Bir doğrusal fonksiyonun benzersiz tersinin olmaması hangi durumda gerçekleşir?

   A. Eğim negatif olduğunda  
   B. Kesişim sıfır olduğunda  
   C. Eğim sıfır olduğunda  
   D. Domain tüm gerçek sayılar olduğunda

7. Sigmoid fonksiyonunun çıktı aralığı hangisidir?

   A. `(-∞, ∞)`  
   B. `[-1, 1]`  
   C. `(0, 1)`  
   D. `[0, ∞)`

8. Tanh fonksiyonunun önemli özelliklerinden biri hangisidir?

   A. Çıktısı daima pozitiftir  
   B. Sıfır merkezlidir  
   C. Yalnızca tam sayılarda tanımlıdır  
   D. Olasılıkların toplamını 1 yapar

9. ReLU'nun negatif girdilerdeki çıktısı nedir?

   A. Girdinin karesi  
   B. `-1`  
   C. `0`  
   D. Sigmoid çıktısı

10. Softmax öncesi tüm logit değerlerinden maksimum logit neden çıkarılır?

    A. Sınıf sayısını azaltmak için  
    B. Sonucu değiştirmeden sayısal taşmayı azaltmak için  
    C. Olasılıkları negatif yapmak için  
    D. Gradient'i tamamen sıfırlamak için

11. Softmax çıktıları için hangisi doğrudur?

    A. Toplamları 0'dır  
    B. Her biri tam sayıdır  
    C. Toplamları 1'dir  
    D. Mutlaka eşittirler

12. `-log(p)` ifadesinde `p` sıfıra yaklaştıkça ne olur?

    A. Loss sıfıra yaklaşır  
    B. Loss hızla büyür  
    C. Loss daima 1 olur  
    D. Loss negatif olur

13. Binary cross-entropy için hedef değerler tipik olarak hangileridir?

    A. Yalnızca `-1` ve `1`  
    B. Yalnızca `0` ve `1`  
    C. Her zaman doğal sayılar  
    D. Yalnızca logits

14. MSE büyük hataları neden daha güçlü cezalandırır?

    A. Hatanın logaritmasını aldığı için  
    B. Hatanın mutlak değerini aldığı için  
    C. Hatayı karesini aldığı için  
    D. Hatayı tamamen yok saydığı için

15. Merkezi fark ile sayısal türev yaklaşımı hangisidir?

    A. `(f(x+h) - f(x-h)) / (2h)`  
    B. `f(x) / h`  
    C. `f(x+h) + f(x-h)`  
    D. `h / f(x)`

16. Sigmoid ve tanh büyük mutlak girdilerde hangi davranışı gösterebilir?

    A. Doygunluk ve küçük eğim  
    B. Sonsuz sınıf üretme  
    C. Kesinlikle doğrusal büyüme  
    D. Domain dışına çıkma

17. `log(0)` problemine karşı loss implementasyonunda yaygın çözüm nedir?

    A. Tüm loss değerlerini silmek  
    B. Olasılıkları küçük epsilon ile güvenli aralığa kırpmak  
    C. Logaritma yerine rastgele sayı kullanmak  
    D. Hedefleri ters çevirmek

18. Bir deep neural network matematiksel olarak nasıl düşünülebilir?

    A. Tek bir sabit sayı  
    B. Fonksiyonların bileşkesi  
    C. Yalnızca bir tablo  
    D. Sıralanmamış bir küme

19. Softmax logits değerlerinin tümüne aynı sabit eklenirse ne olur?

    A. Olasılık dağılımı değişmez  
    B. Tüm olasılıklar sıfır olur  
    C. Sınıf sayısı artar  
    D. Sonuç artık normalize olmaz

20. Sayısal kararlılık neden önemlidir?

    A. Yalnızca kodu daha kısa yapmak için  
    B. Matematiksel olarak doğru formüllerin floating-point ortamında overflow, underflow veya tanımsız değer üretmesini önlemek için  
    C. Test yazmayı gereksiz yapmak için  
    D. Modelin veri ihtiyacını sıfırlamak için

## Cevap anahtarı

1. B
2. D
3. B
4. C
5. B
6. C
7. C
8. B
9. C
10. B
11. C
12. B
13. B
14. C
15. A
16. A
17. B
18. B
19. A
20. B

## Değerlendirme

- **90–100:** Kavramlar güçlü; sonraki lineer cebir dersine hazırsın.
- **75–89:** İyi düzey; sayısal kararlılık ve loss yorumunu tekrar et.
- **60–74:** Temel var; logaritma, bileşke ve aktivasyon grafiklerini yeniden çalış.
- **0–59:** Teori ve laboratuvarı tekrar tamamla, ardından quizi yeniden çöz.
