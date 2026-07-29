# Alıştırmalar — pandas Series, DataFrame, İndeksleme ve GroupBy

## A. Series ve Index

1. Özel index kullanan bir `Series` oluştur ve etiket seçimi yap.
2. Farklı index'lere sahip iki Series'i topla; oluşan eksik değerleri açıkla.
3. `reindex` ile yeni bir sıralama üret.
4. Duplicate index taşıyan bir Series'in seçim davranışını incele.
5. `RangeIndex`, `DatetimeIndex` ve kategorik index örnekleri oluştur.
6. Index adını değiştir ve `reset_index` uygula.
7. Bir index'in benzersiz ve monoton olup olmadığını kontrol et.
8. Etiket hizalamasını atlayıp NumPy değerleriyle toplama yap; riskini yaz.

## B. DataFrame oluşturma ve tipler

9. Dictionary, kayıt listesi ve Series sözlüğünden üç DataFrame oluştur.
10. `info`, `dtypes`, `shape`, `memory_usage` çıktılarını yorumla.
11. `object` kolonu `string` dtype'a dönüştür.
12. Eksik değer taşıyan tamsayı kolonunu `Int64` yap.
13. Boolean kolonu nullable `boolean` dtype'a dönüştür.
14. Düşük kardinaliteli bir string kolonu `category` yap ve bellek farkını ölç.
15. Sayısal görünümlü hatalı değerleri `to_numeric` ile temizle.
16. Tarih kolonunu UTC datetime'a dönüştür ve geçersiz kayıtları raporla.

## C. İndeksleme ve seçim

17. `loc` ile etiket tabanlı satır ve kolon seç.
18. `iloc` ile ilk beş satırın son iki kolonunu seç.
19. Birden fazla koşulu parantez kullanarak boolean mask ile birleştir.
20. `isin`, `between`, `str.contains` ve `isna` kullanan dört filtre yaz.
21. `query` ile eşdeğer bir filtre oluştur.
22. Filtrelenmiş alt kümeye güvenli biçimde yeni kolon ata.
23. Chained assignment üreten hatalı kodu `loc` ile düzelt.
24. Mask index'inin DataFrame index'iyle uyuşmadığı bir hata örneği üret.
25. `at` ve `iat` ile tek hücre erişimini karşılaştır.
26. `copy(deep=False)` ve normal `copy()` davranışını incele.

## D. Kolon üretimi ve dönüşüm

27. Adet ve fiyat kolonlarından gelir kolonu üret.
28. `assign` ile zincirlenebilir iki yeni özellik oluştur.
29. `where` ve `mask` ile negatif değerleri düzelt.
30. `clip` ile alt ve üst sınır uygula.
31. `map` ile kodları açıklama metnine çevir.
32. `replace` ile birden fazla hatalı etiketi düzelt.
33. `cut` ile yaş grupları üret.
34. `qcut` ile gelir dilimleri oluştur.
35. `explode` ile liste taşıyan bir kolonu satırlara aç.
36. Uzun ve geniş format arasında `melt` ve `pivot` uygula.

## E. Eksik ve duplicate veri

37. Kolon bazında eksik oranı hesapla.
38. Grup median'ı ile eksik değer doldur.
39. İleri ve geri doldurma işlemlerinin zaman serisindeki risklerini yaz.
40. Tam satır duplicate ve anahtar duplicate ayrımını göster.
41. Zaman damgasına göre en yeni duplicate kaydı tut.
42. Duplicate çözümleme öncesi ve sonrası satır sayısını raporla.
43. Tüm değerleri eksik olan bir kolonu tespit et.
44. Eksik değer doldurma istatistiğini yalnızca eğitim setinde öğren.

## F. GroupBy

45. Segment bazında müşteri sayısı, toplam ve ortalama gelir hesapla.
46. İki kolonla gruplayıp düz kolon isimli çıktı üret.
47. `agg` içinde named aggregation kullan.
48. `transform` ile grup ortalamasından sapma üret.
49. Her grubun toplamındaki satır payını hesapla.
50. `filter` ile en az beş kayıt taşıyan grupları tut.
51. Grup içi sıralama ve yüzde sıra üret.
52. Her gruptaki en yüksek üç kaydı seç.
53. Eksik grup anahtarlarını `dropna=False` ile koru.
54. Kategorik grup kolonunda `observed=True` etkisini ölç.

## G. Birleştirme

55. `left`, `inner`, `right` ve `outer` merge sonuçlarını karşılaştır.
56. `one_to_one`, `one_to_many` ve `many_to_one` kardinalitelerine örnek oluştur.
57. Hatalı kardinaliteyi `validate` ile yakala.
58. Merge sonrası beklenmeyen satır çoğalmasını teşhis et.
59. Farklı kolon adlarına sahip anahtarlarla merge yap.
60. Aynı şemalı aylık dosyaları `concat` ile birleştir.
61. Concat öncesi kolon sırası ve dtype doğrulaması yaz.
62. Kaynak tabloyu belirten bir provenance kolonu ekleyerek concat yap.

## H. Pipeline ve üretim

63. Gerekli kolonları doğrulayan fonksiyon yaz.
64. Kolon isimlerini snake_case'e dönüştür ve çakışmaları reddet.
65. DataFrame kalite profili üret.
66. Eğitim median'ı ve kategori sözlüğü öğrenen sınıf geliştir.
67. Bilinmeyen kategoriyi `__unknown__` seviyesine yönlendir.
68. Deterministik one-hot encoding üret.
69. Pipeline'ın girdiyi değiştirmediğini test et.
70. Pipeline çıktısının kolon sırasını test et.
71. Duplicate dimension key bulunan merge için test yaz.
72. Geçersiz tarih, negatif fiyat ve eksik anahtar için hata testleri yaz.

## I. Analiz soruları

73. `apply(axis=1)` neden çoğu zaman yavaştır?
74. `iterrows` hangi tip kayıplarına yol açabilir?
75. Index alignment hangi durumda yararlı, hangi durumda tehlikelidir?
76. `groupby().agg()` ile SQL `GROUP BY` arasındaki benzerlikleri yaz.
77. `transform` neden feature engineering için önemlidir?
78. Kategorik dtype model pipeline'ında nasıl sabitlenmelidir?
79. Merge kardinalitesi neden veri kalitesi kontratıdır?
80. Bir notebook analizini üretim pipeline'ına dönüştürmek için on maddelik plan yaz.