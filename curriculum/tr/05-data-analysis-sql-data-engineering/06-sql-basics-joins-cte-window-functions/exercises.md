# Alıştırmalar

## A. Temel sorgular

1. Tüm müşterileri `customer_id` sırasıyla listele.
2. Yalnızca `north` bölgesindeki müşterileri getir.
3. Liste fiyatı 200'den yüksek ürünleri azalan fiyatla sırala.
4. Sipariş status değerlerini benzersiz listele.
5. En eski ve en yeni sipariş tarihini hesapla.
6. `paid` sipariş sayısını bul.
7. Her category için ürün sayısını hesapla.
8. `CASE` ile ürünleri low/medium/high fiyat bandına ayır.
9. `COALESCE` kullanımını gösteren bir sorgu yaz.
10. `NULL` karşılaştırmasının neden `=` ile yapılmadığını örnekle.

## B. Aggregation ve grain

11. Sipariş kalemi başına line revenue üret.
12. Sipariş başına toplam gelir hesapla.
13. Müşteri başına sipariş sayısı hesapla.
14. İptal siparişleri gelirden hariç tut.
15. Her ürünün satılan toplam adedini bul.
16. Her category için paid revenue hesapla.
17. Sipariş başına farklı ürün sayısını hesapla.
18. Müşteri başına ortalama paid order value üret.
19. Grain'i sipariş olan ve kalem olan iki sorgunun farkını yaz.
20. JOIN fan-out nedeniyle yanlış sonuç veren bir `COUNT` örneği oluştur.

## C. JOIN

21. Siparişleri müşteri adıyla birleştir.
22. Sipariş kalemlerini ürün adı ve category ile birleştir.
23. Siparişi olmayan müşterileri `LEFT JOIN` ile bul.
24. Aynı sonucu `NOT EXISTS` ile üret.
25. Müşteri kapsamını koruyan gelir sorgusu yaz.
26. `LEFT JOIN` sonrası sağ tablo filtresini `WHERE` içinde yazmanın etkisini göster.
27. Birden çoğa JOIN kardinalitesini açıklayan örnek hazırla.
28. Çoktan çoğa ilişkinin bridge tablosunu belirle.
29. JOIN anahtarında duplicate olduğunda satır sayısının nasıl değiştiğini göster.
30. JOIN sonucunun grain'ini otomatik doğrulayan test yaz.

## D. CTE

31. Sipariş toplamlarını CTE'ye taşı.
32. Bu CTE'den aylık gelir üret.
33. İkinci CTE ile müşteri toplamlarını hesapla.
34. Region bilgisini müşteri toplamlarına ekle.
35. Birden fazla CTE'yi virgülle zincirle.
36. CTE ile subquery sürümünü okunabilirlik açısından karşılaştır.
37. Recursive CTE ile 1–10 sayı dizisi üret.
38. Recursive CTE ile takvim günleri oluştur.
39. CTE'nin grain'ini yorum satırında belgele.
40. Her CTE aşaması için ayrı test sorgusu yaz.

## E. Window function

41. Müşterileri revenue ile `ROW_NUMBER` kullanarak sırala.
42. Aynı işlemi `RANK` ile yap ve farkını açıkla.
43. `DENSE_RANK` ile eşit gelirleri ele al.
44. Her category içindeki en pahalı ürünü bul.
45. Her müşteri için en yeni siparişi seç.
46. Kümülatif müşteri geliri üret.
47. Aylık gelirin üç aylık hareketli toplamını hesapla.
48. `LAG` ile önceki sipariş tarihini getir.
49. `LEAD` ile sonraki sipariş tarihini getir.
50. Sipariş geliri ile müşteri ortalaması arasındaki farkı window AVG ile hesapla.
51. Top-N sorgusunda deterministik tie-breaker ekle.
52. `ROWS` ve `RANGE` frame davranışlarını araştır.
53. Partition olmadan ve partition ile kümülatif toplamı karşılaştır.
54. Window sonucu üzerinde filtre yapmak için CTE kullan.
55. Müşteri revenue percentile yaklaşımı tasarla.

## F. Güvenlik ve kalite

56. Parametreli status filtresi yaz.
57. String birleştirme ile injection riski taşıyan örneği açıkla.
58. Identifier için allowlist doğrulaması geliştir.
59. Read-only SQL doğrulayıcısına yeni mutasyon anahtar kelimeleri ekle.
60. Beklenen kolon kontrolü yaz.
61. Benzersiz grain kontrolü yaz.
62. Negatif revenue kontrolü yaz.
63. Boş sonuç için açık politika belirle.
64. `EXPLAIN QUERY PLAN` çıktısını kaydet.
65. Sorgu sonucunu JSON'a deterministik sırayla yaz.
66. Foreign key ihlalini test et.
67. `CHECK` constraint ihlalini test et.
68. Transaction rollback testi yaz.
69. Query regression testi için sabit beklenen sonuç oluştur.
70. Aynı analizi pandas ile yapıp SQL çıktısıyla karşılaştır.
