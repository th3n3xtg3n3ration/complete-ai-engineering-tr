# Alıştırmalar — NumPy Dizileri, Vektörleştirme ve Broadcasting

## A. Temel kavramlar

1. Python listesi ile `ndarray` arasındaki üç farkı yaz.
2. `(4, 3, 2)` shape'li dizinin `ndim`, `size` ve eksen uzunluklarını bul.
3. `float32` ve `float64` bellek maliyetini 10 milyon eleman için hesapla.
4. `strides` kavramını kendi cümlelerinle açıkla.
5. C-contiguous ve Fortran-contiguous düzenleri karşılaştır.
6. `np.arange` ile `np.linspace` farkını örnekle.
7. `reshape` işleminin hangi durumda copy üretebileceğini araştır.
8. `ravel` ve `flatten` farkını göster.
9. `astype` kullanımında olası hassasiyet kaybına örnek ver.
10. `np.asarray` ve `np.array` farkını deneyle.

## B. İndeksleme ve shape

11. 5×6 matrisin son iki sütununu seç.
12. Tek indeksli satırları boolean mask ile seç.
13. Negatif değerleri sıfırla.
14. Her satırın en büyük eleman indeksini bul.
15. Fancy indexing'in copy ürettiğini göster.
16. Basic slicing'in view üretmesini `np.shares_memory` ile doğrula.
17. `(10,)` diziyi `(10, 1)` ve `(1, 10)` biçimine getir.
18. Üç matrisi yeni bir batch ekseninde birleştir.
19. `concatenate`, `stack`, `vstack` ve `hstack` farklarını örnekle.
20. Bir matrisi satır ve sütun bloklarına ayır.

## C. Axis ve aggregation

21. Her sütunun ortalamasını hesapla.
22. Her satırın standart sapmasını hesapla.
23. `keepdims=True` olmadan ve kullanarak merkezleme yap.
24. NaN içeren veride `mean` ve `nanmean` sonuçlarını karşılaştır.
25. Her sütundaki sonlu olmayan değer sayısını bul.
26. `argmax` sonucunun axis'e göre nasıl değiştiğini göster.
27. 3-D tensörde her örnek için özellik ortalaması hesapla.
28. Weighted mean fonksiyonu yaz.
29. Kümülatif toplam ile günlük satıştan toplam satış serisi üret.
30. Quantile ve percentile eşdeğerliğini göster.

## D. Broadcasting

31. `(32, 128)` matrise `(128,)` bias ekle.
32. `(32, 128)` matrisi `(32, 1)` scale ile çarp.
33. `(32, 128)` ile `(32,)` neden uyumsuzdur?
34. İki nokta kümesi için broadcast ile pairwise fark üret.
35. Bu fark dizisinin bellek maliyetini hesapla.
36. Aynı mesafeyi matris özdeşliğiyle daha az bellekle hesapla.
37. RGB görüntünün her kanalına farklı katsayı uygula.
38. Batch normalization'ın yalnızca forward standardization kısmını yaz.
39. `(batch, time, feature)` tensörüne feature bias ekle.
40. Broadcasting hatası veren üç shape çifti tasarla.

## E. Vektörleştirme

41. Döngüyle kare alma kodunu vektörleştir.
42. Koşullu fiyat indirimi kodunu `np.where` ile yaz.
43. One-hot encoding işlemini NumPy ile uygula.
44. Confusion matrix'i `np.add.at` ile üret.
45. Moving average hesapla.
46. Cosine similarity matrisini uygula.
47. Top-k seçiminde full sort ve `argpartition` karşılaştır.
48. Z-score outlier maskesi oluştur.
49. Min–max scaling'i sabit sütunları güvenli ele alarak yaz.
50. Loop ve vectorized sürümü `perf_counter` ile ölç.

## F. Veri kalitesi ve pipeline

51. Tamamı eksik sütunları tespit et.
52. Median imputation uygula.
53. IQR tabanlı clipping sınırları hesapla.
54. Eğitim ve test için ayrı fit yapmanın neden hatalı olduğunu göster.
55. Feature sayısı değiştiğinde hata veren transformer yaz.
56. Fit edilmeden transform çağrısını engelle.
57. State'i immutable dataclass ile sakla.
58. Pipeline'ın input'u mutate etmediğini test et.
59. NaN ve inf politikalarını karşılaştır.
60. Sabit sütunları raporlayan bir fonksiyon yaz.

## G. İleri görevler

61. Welford algoritmasıyla online mean/variance uygula.
62. Büyük matrislerde chunked standardization tasarla.
63. Memory-mapped array kullanım senaryosu yaz.
64. `einsum` ile batch dot product uygula.
65. `np.lib.stride_tricks.sliding_window_view` ile pencereleme yap.
66. Stable softmax uygula ve naive sürümle karşılaştır.
67. PCA öncesi centering adımını doğrula.
68. Sparse veri için dense NumPy yaklaşımının riskini açıkla.
69. Benchmark sonuçlarının güvenilirliği için deney protokolü yaz.
70. Mini projen için veri sözleşmesi ve test matrisi hazırla.
