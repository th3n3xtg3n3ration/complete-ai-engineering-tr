# Quiz — Vektörler, Matrisler, Tensörler, Normlar ve Dot Product

Her soru için en uygun seçeneği işaretle.

## Sorular

1. Bir skalerin rank değeri nedir?
   - A) 0
   - B) 1
   - C) 2
   - D) Eleman sayısına bağlıdır

2. `(32, 128)` shape'i çoğunlukla neyi temsil eder?
   - A) 32 özellik ve 128 model
   - B) 32 örnek ve 128 özellik
   - C) 32 kanal ve 128 piksel
   - D) Yalnızca kare matris

3. İki vektörün dot product işlemi için temel koşul nedir?
   - A) Aynı norma sahip olmaları
   - B) Aynı uzunluğa sahip olmaları
   - C) Pozitif olmaları
   - D) Normalize edilmeleri

4. `(m, n)` ile `(n, p)` matrislerinin çarpım sonucu nedir?
   - A) `(n, n)`
   - B) `(m, p)`
   - C) `(m, n, p)`
   - D) `(p, m)`

5. L1 norm nasıl hesaplanır?
   - A) En büyük bileşen alınır
   - B) Kareler toplamının karekökü alınır
   - C) Mutlak değerler toplanır
   - D) Ortalama alınır

6. `[3, 4]` vektörünün L2 normu nedir?
   - A) 4
   - B) 5
   - C) 7
   - D) 25

7. Infinity norm neyi ölçer?
   - A) Eleman sayısını
   - B) En büyük mutlak bileşeni
   - C) Bileşenlerin ortalamasını
   - D) Vektör açısını

8. Cosine similarity temel olarak neyi ölçer?
   - A) Vektörlerin yön benzerliğini
   - B) Vektörlerin eleman sayısını
   - C) Matris determinantını
   - D) Batch büyüklüğünü

9. Sıfır vektörü için cosine similarity neden tanımsızdır?
   - A) Dot product hesaplanamaz
   - B) Norm sıfır olduğu için payda sıfır olur
   - C) Vektör rank-0 olur
   - D) Sonuç her zaman 1 olur

10. L2 normalizasyonundan sonra ne beklenir?
    - A) Tüm elemanlar sıfır olur
    - B) Vektörün L2 normu yaklaşık 1 olur
    - C) Shape değişir
    - D) Rank artar

11. Birim vektörlerde dot product neye eşittir?
    - A) L1 normuna
    - B) Cosine similarity değerine
    - C) Euclidean distance değerine
    - D) Matrix trace değerine

12. Ragged tensor nedir?
    - A) Tüm eksenleri eşit olan tensor
    - B) Alt dizileri uyumsuz shape'lere sahip nested yapı
    - C) Yalnızca negatif sayılardan oluşan tensor
    - D) Normalize edilmiş tensor

13. `(batch, channels, height, width)` hangi yerleşime örnektir?
    - A) Channels-last
    - B) Channels-first
    - C) Sequence-first
    - D) Feature-last olmayan geçersiz yapı

14. Bir dense layer için input `(64, 128)` ve weight `(128, 32)` ise output nedir?
    - A) `(128, 128)`
    - B) `(64, 32)`
    - C) `(32, 64)`
    - D) `(64, 128, 32)`

15. `(64, 32)` matrise `(32,)` bias eklenmesi hangi kavramla açıklanır?
    - A) Recursion
    - B) Broadcasting
    - C) Hashing
    - D) Sorting

16. Cosine similarity 1'e yakınsa genel yorum nedir?
    - A) Vektörler zıt yönlüdür
    - B) Vektörler benzer yönlüdür
    - C) Vektörlerden biri sıfırdır
    - D) Euclidean distance kesinlikle sıfırdır

17. Euclidean distance neye duyarlıdır?
    - A) Yalnızca vektör yönüne
    - B) Mutlak konum ve büyüklük farkına
    - C) Yalnızca rank değerine
    - D) Yalnızca işaret sayısına

18. L1 regularization çoğunlukla hangi davranışla ilişkilidir?
    - A) Sparsity
    - B) Rank artırma
    - C) Veri çoğaltma
    - D) Batch normalization

19. Aşağıdakilerden hangisi shape doğrulamasının yararıdır?
    - A) Mantık hatalarını işlem sınırında yakalamak
    - B) Her işlemi otomatik hızlandırmak
    - C) Tüm floating-point hatalarını yok etmek
    - D) Veriyi şifrelemek

20. `zip` farklı uzunluktaki iki vektörde varsayılan olarak ne yapabilir?
    - A) Hata vermeden kısa olanın sonunda durabilir
    - B) Eksik değerleri sıfırla doldurur
    - C) Uzun vektörü ikiye böler
    - D) Her zaman exception üretir

## Cevap anahtarı

1. A
2. B
3. B
4. B
5. C
6. B
7. B
8. A
9. B
10. B
11. B
12. B
13. B
14. B
15. B
16. B
17. B
18. A
19. A
20. A

## Açık uçlu değerlendirme

1. Cosine similarity ile Euclidean distance arasında seçim yaparken hangi veri özelliklerini incelersin?
2. Shape bilgisinin yalnızca teknik değil semantik bir sözleşme olduğunu bir NLP örneğiyle açıkla.
3. Normalizasyonun faydalı olduğu ve zararlı olabileceği birer senaryo ver.
4. Matrix multiplication hatasını üretime ulaşmadan yakalamak için üç savunma katmanı tasarla.
5. Attention hesaplamasında dot product kullanımını sezgisel olarak açıkla.
