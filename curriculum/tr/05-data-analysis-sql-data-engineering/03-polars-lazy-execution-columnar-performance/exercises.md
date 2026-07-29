# Alıştırmalar

## A. Temel kavramlar

1. Kolon tabanlı ve satır tabanlı depolamayı karşılaştır.
2. `DataFrame` ile `LazyFrame` farkını açıkla.
3. Materialization nedir?
4. Expression API neden Python döngüsünden farklıdır?
5. `pl.col` ne üretir?
6. `select` ile `with_columns` farkını örnekle.
7. `filter` içinde üç koşulu birleştir.
8. Null ve NaN farkını Polars bağlamında açıkla.
9. Bir kolonun dtype'ını güvenli cast et.
10. `strict=False` kullanımının riskini açıkla.

## B. Şema ve kalite

11. Zorunlu kolon doğrulama fonksiyonu yaz.
12. Kolon adlarını snake_case yapan fonksiyon geliştir.
13. Normalize sonrası kolon çakışmasını tespit et.
14. Tüm null hücreleri sayan profil fonksiyonu yaz.
15. Negatif fiyatları ayrı karantina tablosuna taşı.
16. Geçersiz tarihleri tespit et.
17. Duplicate siparişlerde son kaydı tut.
18. Composite key tekilliğini doğrula.
19. Bir kolonun beklenen kategori kümesi dışında kalan değerlerini bul.
20. Satır sayısı değişimini pipeline adımları arasında raporla.

## C. Expression API

21. İsim kolonunu trim ve lowercase yap.
22. Fiyatı kuruştan Türk lirasına dönüştüren ifade yaz.
23. `when/then/otherwise` ile değer bandı üret.
24. Liste kolonundaki eleman sayısını hesapla.
25. String kolondan domain çıkar.
26. İki tarih arasındaki gün farkını üret.
27. Birden fazla kolonu aynı dtype'a cast et.
28. Numeric selector kullanarak tüm sayısal kolonları standardize et.
29. Satır bazlı UDF'yi native expression'a çevir.
30. Null değerleri grup medyanıyla doldur.

## D. Lazy execution

31. `read_csv` kodunu `scan_csv` biçimine dönüştür.
32. `collect` çağrısını pipeline sonunda tutacak şekilde refactor yap.
33. Projection pushdown gösterecek bir sorgu yaz.
34. Predicate pushdown gösterecek bir sorgu yaz.
35. Optimize edilmiş ve optimize edilmemiş planı karşılaştır.
36. Aynı kaynaktan iki aggregation üretip `collect_all` kullanımını araştır.
37. Bir sorgunun şemasını veriyi materialize etmeden al.
38. `sink_parquet` kullanan pipeline yaz.
39. Streaming engine ile normal engine sonucunu karşılaştır.
40. Global sort'un streaming üzerindeki etkisini araştır.

## E. GroupBy ve join

41. Müşteri bazlı toplam gelir hesapla.
42. Segment bazlı median sipariş tutarı üret.
43. Her grupta en yüksek üç siparişi seç.
44. `maintain_order=True` maliyetini açıkla.
45. `1:1`, `1:m`, `m:1`, `m:m` örnekleri oluştur.
46. Duplicate boyut tablosunun satır patlaması oluşturduğunu göster.
47. Join öncesi sağ tablo tekilliğini doğrula.
48. Anti join ile boyut tablosunda bulunmayan anahtarları bul.
49. Semi join kullanım senaryosu yaz.
50. Join sonrası toplam gelir invariant'ını test et.

## F. Performans

51. Eager ve lazy sürüm için benchmark fonksiyonu yaz.
52. Isınma çalıştırmasının neden önemli olduğunu açıkla.
53. Medyan ve ortalama süreyi karşılaştır.
54. `estimated_size` ile iki ara sonucu ölç.
55. Gereksiz kolonları kaldırmanın etkisini ölç.
56. Python UDF ile native expression'ı karşılaştır.
57. CSV ve Parquet tarama süresini karşılaştır.
58. Küçük veri sonucunu büyük veriye genellemenin riskini açıkla.
59. CPU, I/O ve bellek darboğazlarını ayırt et.
60. Benchmark sonuçlarını yeniden üretilebilir kıl.

## G. Üretim senaryoları

61. Günlük partition'ları tarayan lazy pipeline tasarla.
62. Şema değişikliği olduğunda fail-fast davranışı ekle.
63. Hatalı kayıtları karantina dosyasına yaz.
64. Çıktı şemasını veri sözleşmesiyle doğrula.
65. Pipeline'a satır sayısı ve null oranı metrikleri ekle.
66. Idempotent çıktı isimlendirmesi tasarla.
67. Müşteri özellik tablosu için freshness metriği üret.
68. Kaynak dosya hash'ini lineage kaydına ekle.
69. Pipeline'ın deterministik olduğunu test et.
70. Eager, lazy ve streaming seçim kararını açıklayan mimari karar kaydı yaz.
