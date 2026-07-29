# Alıştırmalar

## Temel

1. Completeness ve validity arasındaki farkı iki örnekle açıkla.
2. MCAR, MAR ve MNAR için birer iş senaryosu yaz.
3. Mean ve median imputation sonuçlarını çarpık bir seri üzerinde karşılaştır.
4. Bir kolonda eksik oranını ve sayısını hesapla.
5. İş anahtarına göre duplicate kayıtları raporla.
6. IQR sınırlarını elle hesapla.
7. Sabit bir seride robust z-score davranışını açıkla.
8. Sayısal string kolonunu nullable float'a dönüştür.
9. Negatif yaş değerlerini iş kuralıyla reddet.
10. Girdiyi mutasyona uğratmayan bir clipping fonksiyonu yaz.

## Orta

11. Missing indicator eklemenin yararlı olduğu bir senaryo tasarla.
12. Rare-category eşiğini yalnızca train verisinde öğren.
13. Bilinmeyen kategoriyi `__OTHER__` ile kodla.
14. Eksik kategoriyi `__MISSING__` olarak koru.
15. One-hot kolon sırasını deterministik yap.
16. Train medianının evaluation medianından farklı olduğu bir test yaz.
17. IQR clipping sınırlarının evaluation verisinde yeniden fit edilmediğini kanıtla.
18. Aynı `row_id` değerinin iki split'te bulunmasını engelle.
19. Zaman kesimine göre train ve evaluation üret.
20. Geçersiz timestamp için açık hata mesajı üret.

## İleri

21. Target ile aynı olan feature'ı otomatik bul.
22. Hedefle mutlak korelasyonu 0.999'dan büyük numeric proxy'leri raporla.
23. Post-outcome feature adlarını isim tabanlı heuristic ile işaretle.
24. Aynı müşterinin iki split'te bulunmasının problem olmadığı ve olduğu iki senaryoyu karşılaştır.
25. Group-based split tasarla.
26. Time-aware aggregation için yalnızca geçmiş kayıtları kullan.
27. Leakage üreten ve üretmeyen rolling feature örnekleri yaz.
28. Missingness drift raporu oluştur.
29. Training ve production kategori dağılımlarını karşılaştır.
30. Pipeline'ın öğrenilen durumunu JSON uyumlu bir sözlüğe dönüştür.

## Uygulama

31. 100 bin satırlık sentetik veri üret.
32. Eksiklik oranlarını kolon bazında raporla.
33. Çok yüksek kardinaliteli kategorileri tespit et.
34. Duplicate çözümleme için `keep-last` iş kuralı uygula.
35. Domain aralığı dışındaki değerleri quarantine tablosuna taşı.
36. Sayısal kolonlar için quantile profili üret.
37. Kategorik kolonlar için top-K ve coverage raporu üret.
38. Train/test preprocessing çıktılarının aynı kolonlara sahip olduğunu test et.
39. Evaluation'da görülmeyen kategoriler ekle.
40. Outlier clipping öncesi ve sonrası dağılım özetini karşılaştır.
41. Feature-target audit raporunu DataFrame'e çevir.
42. Leakage finding severity seviyelerine göre pipeline'ı durdur.
43. Satır çakışmasını hash tabanlı denetle.
44. Entity overlap oranını hesapla.
45. Zaman split'inde cutoff çevresindeki boundary testlerini yaz.
46. Pipeline'ı scikit-learn benzeri `fit/transform` arayüzüyle paketle.
47. Girdinin yerinde değiştirilmediğini test et.
48. Eksik required column durumunu test et.
49. Tamamı eksik numeric training kolonunu reddet.
50. Tamamı rare olan categorical kolonun davranışını test et.

## Tasarım ve tartışma

51. Aykırı değer silmenin fraud detection'a etkisini tartış.
52. Median imputation'ın variance üzerindeki etkisini açıkla.
53. Target encoding'in leakage riskini açıkla.
54. Cross-validation içinde preprocessing'in nerede fit edilmesi gerektiğini göster.
55. Random split'in churn probleminde ne zaman hatalı olabileceğini tartış.
56. Healthcare verisinde entity split gereksinimini açıkla.
57. Gelecek bilgisi kullanan üç feature örneği yaz.
58. Data contract ile cleaning pipeline ilişkisini açıkla.
59. Quarantine ve hard-fail politikalarını karşılaştır.
60. Veri kalite metriğini SLO olarak tanımla.
