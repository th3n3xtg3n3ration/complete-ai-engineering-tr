# Alıştırmalar

## Temel

1. B-tree indeksin arama ve yazma maliyetini açıkla.
2. Primary key ile unique indeks arasındaki ilişkiyi yaz.
3. Full table scan her zaman neden kötü değildir?
4. `EXPLAIN QUERY PLAN` ile gerçek yürütme süresi arasındaki farkı açıkla.
5. `DEFERRED`, `IMMEDIATE` ve `EXCLUSIVE` transaction modlarını karşılaştır.
6. Atomicity ihlaline bir para transferi örneği ver.
7. Savepoint ile transaction arasındaki farkı yaz.
8. Idempotency key neden gereklidir?
9. Optimistic locking hangi sorunu çözer?
10. `busy_timeout` neyi değiştirir?
11. WAL modunun temel avantajını açıkla.
12. `foreign_key_check` ile `integrity_check` arasındaki farkı araştır.
13. Backup dosyasını restore testine sokmanın önemini yaz.
14. Query-only bağlantının kullanım alanını açıkla.
15. Exponential backoff neden sabit beklemeden daha uygundur?

## Uygulama

16. Hesap tablosuna `currency_code` constraint'i ekle.
17. Negatif bakiye girişini veritabanı seviyesinde reddet.
18. Transfer işlemine açıklama alanı ekle.
19. Aynı idempotency key'in farklı operasyon adıyla kullanımını engelle.
20. Transfer öncesi ve sonrası toplam bakiyenin değişmediğini test et.
21. Savepoint içinde üç alt adım kur ve ikincisini rollback et.
22. Optimistic locking çatışmasını iki bağlantıyla canlandır.
23. Dosya tabanlı veritabanında WAL modunu doğrula.
24. `accounts(owner_name)` indeksinin plan etkisini ölç.
25. Kullanılmayan bir indeks oluşturup yazma maliyetini tartış.
26. Birleşik indeks kolon sırasını değiştirerek planı karşılaştır.
27. Covering index oluştur ve plan çıktısını incele.
28. Partial index ile yalnızca yüksek tutarlı transferleri indeksle.
29. Unique indeks ihlalini test et.
30. `ORDER BY` için geçici B-tree kullanımını gösteren sorgu yaz.
31. Lock hatasını yalnızca belirli mesajlarda retry eden test yaz.
32. Retry bütçesi dolduğunda son hatanın yükseldiğini doğrula.
33. Backup sonrası yeni transferin backup dosyasında olmadığını göster.
34. Read-only bağlantıda yazma girişimini reddet.
35. `PRAGMA quick_check` ile `integrity_check` farkını araştır.

## İleri

36. Hesap hareketlerinden materialized balance yaklaşımı tasarla.
37. Double-entry ledger şeması kur.
38. Transfer toplamını sıfır toplam prensibiyle doğrula.
39. Büyük transfer tablosu üretip indeks öncesi/sonrası benchmark yap.
40. Selectivity düşük kolonun indekslenmesini değerlendir.
41. Composite index left-most prefix davranışını otomatik test et.
42. Query-plan regression testi yaz.
43. Index migration için ileri/geri migration dosyaları tasarla.
44. Online index oluşturma risklerini PostgreSQL bağlamında araştır.
45. Isolation anomaly örneklerini dirty read, non-repeatable read ve phantom read olarak karşılaştır.
46. SQLite'ın snapshot davranışını WAL altında gözlemle.
47. Uzun süren read transaction'ın WAL büyümesine etkisini araştır.
48. Connection pool kullanıldığında transaction sınırlarının riskini yaz.
49. Retry edilen işlemin idempotent olmaması durumunu analiz et.
50. Outbox pattern şeması tasarla.
51. Exactly-once iddiasının neden zor olduğunu açıkla.
52. Database migration sırasında backward compatibility planı yaz.
53. Backup retention ve encryption politikası tasarla.
54. Point-in-time recovery kavramını araştır.
55. Lock contention metriği için izleme tasarımı yap.
56. Slow query log eşiklerini nasıl belirleyeceğini açıkla.
57. Query timeout stratejisi oluştur.
58. Connection leak riskini test eden fixture yaz.
59. Foreign key cascade kullanımının avantaj ve risklerini tartış.
60. Capstone için veritabanı güvenilirlik kontrol listesi hazırla.
