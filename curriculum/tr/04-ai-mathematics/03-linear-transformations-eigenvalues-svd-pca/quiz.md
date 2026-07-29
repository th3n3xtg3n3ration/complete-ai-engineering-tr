# Quiz — Lineer Dönüşümler, Özdeğer, SVD ve PCA

## Sorular

1. Bir dönüşümün lineer olması için hangi iki koşulu sağlaması gerekir?
2. Rotation matrisi bir vektörün hangi özelliğini korur?
3. `Ax = 0` denklemini sağlayan vektörler hangi uzayı oluşturur?
4. Rank neyi ölçer?
5. `Av = λv` denkleminde `v` ve `λ` neyi temsil eder?
6. Power iteration hangi eigenvalue'a karşılık gelen yönü bulmayı hedefler?
7. Rayleigh quotient ne için kullanılır?
8. SVD açılımı nedir?
9. Singular value'lar hangi matriste bulunur?
10. PCA'dan önce veri neden merkezlenir?
11. Covariance matrisinin diagonal elemanları neyi gösterir?
12. PCA component'leri neden birbirine ortogonaldir?
13. Explained variance ratio nasıl yorumlanır?
14. Reconstruction error yüksekse ne anlaşılır?
15. PCA neden feature scaling'e duyarlıdır?
16. PCA modelinin test verisine ayrı fit edilmesi neden yanlıştır?
17. Projection residual'ı projection yönüne göre nasıldır?
18. Düşük rank approximation hangi amaçlarla kullanılabilir?
19. Embedding compression sonrası hangi downstream ölçüm yapılmalıdır?
20. Yakın eigenvalue'lar power iteration yakınsamasını nasıl etkiler?

## Cevap anahtarı

1. Toplamı ve skaler çarpmayı korumalıdır.
2. L2 normunu ve açıları korur.
3. Null space.
4. Bağımsız çıktı yönlerinin boyutunu.
5. Eigenvector ve eigenvalue.
6. Mutlak değerce baskın eigenvalue yönünü.
7. Bir vektöre karşılık gelen eigenvalue yaklaşımını hesaplamak için.
8. `A = UΣVᵀ`.
9. `Σ` diagonal matrisinde.
10. Varyans yönlerini veri ortalamasından bağımsız ölçmek için.
11. Feature varyanslarını.
12. Simetrik covariance matrisinin eigenvector'leri ortogonal seçilebilir.
13. Component'in toplam varyansın ne kadarını koruduğunu gösterir.
14. Boyut indirgeme sırasında önemli bilgi kaybı vardır.
15. Büyük ölçekli feature'lar covariance değerlerini domine eder.
16. Veri sızıntısı oluşturur ve gerçek genelleme ölçümünü bozar.
17. Ortogonaldir.
18. Sıkıştırma, denoising ve boyut indirgeme.
19. Retrieval kalitesi, komşuluk korunumu veya görev metriği ölçülmelidir.
20. Yakınsamayı yavaşlatır.
