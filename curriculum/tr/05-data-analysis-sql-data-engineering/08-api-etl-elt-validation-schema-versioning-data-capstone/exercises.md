# Alıştırmalar — Veri Pipeline Capstone

## API extraction ve dayanıklılık

1. Timeout bulunmayan bir API istemcisinin iki üretim riskini yaz.
2. 429 yanıtında Retry-After değerinin neden backoff hesabından önce gelmesi gerektiğini açıkla.
3. Exponential backoff için ilk dört gecikmeyi base=0.5 saniye ile hesapla.
4. Jitter kullanılmayan retry sisteminde oluşabilecek thundering herd problemini açıkla.
5. Cursor pagination ile offset pagination arasındaki farkı örnekle açıkla.
6. Cursor döngüsünü tespit eden bir algoritma yaz.
7. Maksimum sayfa sayısı sınırının neden güvenlik kontrolü olduğunu açıkla.
8. API response body UTF-8 değilse uygulanacak hata politikasını tasarla.
9. 401 ve 503 yanıtlarının retry politikası neden farklı olmalıdır?
10. Transport bağımlılığını enjekte etmenin test edilebilirlik faydasını açıkla.

## Raw katman ve checksum

11. Canonical JSON ile normal JSON serialization arasındaki hash farkını göster.
12. SHA-256 checksum'ın erişim kontrolü olmadığını açıkla.
13. Aynı veri farklı fetched_at ile kaydedildiğinde snapshot sürümleme kararını tartış.
14. Atomic file replacement için temp dosya yaklaşımını uygula.
15. Bronze snapshot envelope'ında bulunması gereken beş metadata alanını yaz.
16. Content-addressed path tasarımı oluştur.
17. Bozuk snapshot dosyasını manifest checksum ile tespit eden fonksiyon yaz.
18. Raw verinin neden yerinde güncellenmemesi gerektiğini açıkla.
19. Sıkıştırılmış raw snapshot kullanmanın artı ve eksilerini yaz.
20. Retention policy ile reproducibility arasındaki gerilimi tartış.

## Veri sözleşmeleri

21. Customer için alan tipi, null ve enum kuralları içeren sözleşme yaz.
22. Required ile nullable kavramlarının farkını örnekle açıkla.
23. Unknown field politikasını strict ve permissive modlarda karşılaştır.
24. Primary-key duplicate kaydını record-level hata olarak raporla.
25. Timezone içermeyen datetime değerini reddeden doğrulama yaz.
26. NaN ve infinity değerlerini number alanında reddet.
27. Regex pattern ile kimlik formatı doğrula.
28. Opsiyonel alan eklemenin neden genellikle geriye uyumlu olduğunu açıkla.
29. Enum değerinin kaldırılmasını kırıcı değişiklik olarak raporla.
30. Sözleşme fingerprint'inin kullanım alanlarını yaz.

## ETL, ELT ve katmanlar

31. ETL ve ELT için birer uygun sistem örneği ver.
32. Bronze, silver ve gold katmanlarının sorumluluklarını tablo halinde karşılaştır.
33. PII maskelemenin hangi katmanda yapılması gerektiğini iki senaryoyla tartış.
34. Silver katmanda duplicate çözümleme stratejisi tasarla.
35. Gold tablo grain'ini yanlış tanımlamanın sonuçlarını açıkla.
36. Bir müşteri özellik tablosu için beş özellik öner.
37. Transform-before-load kararının maliyetini tartış.
38. ELT sisteminde ham veriye erişim yetkisini nasıl sınırlandıracağını yaz.
39. Katmanlar arasında schema drift kontrolü tasarla.
40. Bir gold veri ürününün tüketici sözleşmesini yaz.

## Idempotency ve incremental load

41. Idempotent upsert için primary key ve updated_at kullanımını açıkla.
42. Aynı dataset version'ın iki kez yüklenmesini önleyen SQL tasarla.
43. Geç gelen eski kaydın yeni kaydı ezmesini engelle.
44. Watermark'ın yalnızca başarılı run sonunda ilerletilmesi gerektiğini açıkla.
45. Overlap window kullanan incremental extract tasarla.
46. Source delete olaylarını yakalamak için tombstone yaklaşımını açıkla.
47. Full refresh ile incremental load maliyetini karşılaştır.
48. Backfill çalıştırmasının online incremental run ile çakışmasını önle.
49. Dataset version formülüne hangi bileşenlerin girmesi gerektiğini savun.
50. Pipeline code version değiştiğinde aynı input için yeni dataset version üret.

## Lineage, kalite ve operasyon

51. Bir manifest JSON şeması tasarla.
52. Input, valid, rejected ve output satır sayıları arasında invariant yaz.
53. Reddedilen kayıt oranı için warning ve failure eşikleri öner.
54. Artefakt checksum doğrulama fonksiyonu yaz.
55. Bir gold tabloyu bronze snapshot'a bağlayan lineage kaydı oluştur.
56. Run status için running, succeeded ve failed durum geçişlerini tasarla.
57. Pipeline metriği ve log arasındaki farkı örnekle açıkla.
58. Secret değerlerinin loglara sızmasını önleyen redaction yaklaşımı yaz.
59. Quarantine kayıtları için yeniden işleme workflow'u tasarla.
60. SQLite capstone'u cloud object storage ve warehouse mimarisine taşıma planı yaz.
