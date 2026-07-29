# Alıştırmalar

## Kavramsal

1. Lineer dönüşümün iki temel koşulunu yaz.
2. Rotation dönüşümünün neden norm koruduğunu açıkla.
3. Scaling ile shear arasındaki geometrik farkı anlat.
4. Projection matrisinin neden simetrik olduğunu araştır.
5. Rank ile bilgi kaybı arasındaki ilişkiyi açıkla.
6. Null space'in model feature'ları açısından anlamını yorumla.
7. Eigenvector'ün neden yalnızca yön belirttiğini açıkla.
8. Negatif eigenvalue geometrik olarak ne ifade eder?
9. Power iteration hangi durumda başarısız olabilir?
10. SVD ile eigendecomposition arasındaki temel farkı yaz.
11. PCA neden veriyi merkezler?
12. PCA neden ölçek farklarına duyarlıdır?
13. Explained variance tek başına neden yeterli olmayabilir?
14. Reconstruction error neyi ölçer?
15. Train/test leakage PCA'da nasıl oluşur?

## Hesaplama

16. `(2, 3)` vektörünü x yönünde 3, y yönünde 2 kat ölçekle.
17. `(1, 0)` vektörünü 90 derece döndür.
18. `(2, 1)` vektörüne `k=2` shear uygula.
19. `(3, 4)` vektörünü x eksenine project et.
20. `(3, 4)` vektörünü `(1, 1)` yönüne project et.
21. Projection residual'ının yönle ortogonal olduğunu doğrula.
22. `[[2, 0], [0, 1]]` matrisinin eigenpair'lerini bul.
23. `[[0, -1], [1, 0]]` rotation matrisinin reel eigenvector durumunu tartış.
24. İki feature'lı küçük bir veri kümesinin covariance matrisini elle hesapla.
25. Covariance diagonal elemanlarını yorumla.
26. Bir component ile projection sonucunu hesapla.
27. Reconstructed verinin hata değerini bul.

## Kodlama

28. `reflection_matrix_x()` fonksiyonu yaz.
29. `reflection_matrix_y()` fonksiyonu yaz.
30. Genel boyutlu diagonal scaling matrisi oluştur.
31. Matrisin yaklaşık simetrik olup olmadığını kontrol et.
32. Orthogonality kontrol fonksiyonu yaz.
33. Gram-Schmidt algoritmasını uygula.
34. Matrix rank için Gaussian elimination yaklaşımı geliştir.
35. Null space için küçük bir çözücü tasarla.
36. Power iteration convergence geçmişini kaydet.
37. Rayleigh quotient değişimini CSV'ye yaz.
38. Deflation ile ilk iki eigenpair'i bul.
39. PCA modelini JSON uyumlu sözlüğe dönüştür.
40. Kaydedilmiş PCA modelini tekrar yükle.
41. Standardization seçeneği ekle.
42. Explained variance threshold ile component sayısı seç.
43. PCA transform sırasında feature sayısını doğrula.
44. Reconstruction error için MAE seçeneği ekle.
45. Orijinal ve düşürülmüş embedding komşuluklarını karşılaştır.

## İleri seviye

46. Yakın eigenvalue'ların power iteration hızına etkisini deneyle.
47. Başlangıç vektörünün convergence üzerindeki etkisini ölç.
48. Gürültü eklenmiş veride PCA'nın denoising etkisini incele.
49. Farklı feature ölçeklerinde PCA sonuçlarını karşılaştır.
50. PCA öncesi standardization gereksinimini teknik raporla değerlendir.
