# Quiz

1. Bir tablonun grain'i neyi tanımlar?
2. Primary key ile foreign key arasındaki fark nedir?
3. `COUNT(*)` ile `COUNT(column)` arasındaki fark nedir?
4. `NULL = NULL` neden true değildir?
5. `WHERE` ile `HAVING` arasındaki fark nedir?
6. INNER JOIN hangi kayıtları korur?
7. LEFT JOIN hangi durumda tercih edilir?
8. JOIN fan-out nedir?
9. `NOT EXISTS`, `NOT IN` karşısında neden daha güvenli olabilir?
10. CTE'nin temel mühendislik faydası nedir?
11. Window function ile GROUP BY arasındaki ana fark nedir?
12. `ROW_NUMBER` ve `DENSE_RANK` nasıl ayrılır?
13. `LAG` hangi tür analizlerde kullanılır?
14. Kümülatif toplam için hangi window aggregate kullanılır?
15. `PARTITION BY` ne yapar?
16. Window sorgusunda deterministik `ORDER BY` neden önemlidir?
17. Parametreli sorgu hangi riski azaltır?
18. Tablo adı neden normal query parametresi olamaz?
19. `EXPLAIN QUERY PLAN` ne sağlar?
20. Analitik sorgunun doğru olduğunu kanıtlamak için hangi üç çıktı kontrolü uygulanabilir?

## Cevap anahtarı

1. Tek satırın temsil ettiği varlık veya olay seviyesini.
2. Primary key satırı tanımlar; foreign key başka tablonun anahtarına referans verir.
3. İlki tüm satırları, ikincisi NULL olmayan kolon değerlerini sayar.
4. NULL bilinmeyendir ve karşılaştırma unknown üretir.
5. WHERE aggregation öncesi, HAVING aggregation sonrası filtreler.
6. İki tarafta eşleşenleri.
7. Sol tablonun tüm kapsamı korunmak istendiğinde.
8. Birden çoğa veya çoktan çoğa JOIN nedeniyle satırların çoğalmasıdır.
9. NOT IN listesindeki NULL tüm sonucu belirsiz hâle getirebilir.
10. Sorguyu isimlendirilmiş, okunabilir ve test edilebilir aşamalara ayırmasıdır.
11. GROUP BY satır sayısını azaltır; window function mevcut satırları korur.
12. ROW_NUMBER her satıra farklı sıra verir; DENSE_RANK eşit değerlere aynı sıra verir.
13. Önceki satır karşılaştırması, değişim ve zaman aralığı analizlerinde.
14. `SUM(...) OVER (...)`.
15. Window hesaplamasını bağımsız gruplara böler.
16. Eşit değerlerde sonucun tekrarlanabilir olması için.
17. SQL injection riskini.
18. Parametre mekanizması değer literal'ları içindir; identifier değildir.
19. Tarama, arama ve JOIN planı hakkında özet bilgi verir.
20. Kolon şeması, benzersiz grain ve iş kuralı/metrik kontrolleri.
