# Mülakat Soruları — Veri Mühendisliği Capstone

## 1. ETL ve ELT arasındaki fark nedir?

ETL'de dönüşüm hedefe yüklemeden önce, ELT'de ham veri hedef analitik sisteme yüklendikten sonra yapılır. Seçim; hedef sistem kapasitesi, veri yönetişimi, hassas veri ve yeniden işleme ihtiyacına bağlıdır.

## 2. Bir API istemcisinde neden timeout zorunludur?

Sonsuz beklemeyi, worker tüketimini ve zincirleme gecikmeyi önler. Timeout hatası sınırlı retry ve backoff politikasıyla ele alınabilir.

## 3. Hangi HTTP hataları retry edilmelidir?

Genellikle 429 ve geçici 5xx hataları retry edilir. 400, 401, 403 gibi istemci veya yetki hataları düzeltme olmadan retry edilmemelidir.

## 4. Exponential backoff ve jitter neden kullanılır?

Backoff kaynak sisteme toparlanma süresi verir. Jitter çok sayıda istemcinin aynı anda yeniden istek atmasını engeller.

## 5. Cursor pagination neden offset'ten daha güvenilir olabilir?

Veri eklenip silinirken offset kayabilir; duplicate veya atlanan satırlar oluşabilir. Cursor, sıralama anahtarına veya sunucu durumuna bağlı daha stabil ilerleme sağlayabilir.

## 6. Immutable raw layer neden önemlidir?

Kaynak veriyi yeniden üretme, audit, hata ayıklama, backfill ve yeni dönüşüm mantığını geçmiş girdilere uygulama olanağı sağlar.

## 7. Veri sözleşmesi ile şema arasındaki fark nedir?

Şema çoğunlukla alan adı ve tipini tanımlar. Veri sözleşmesi buna null, aralık, enum, primary key, SLA, sahiplik ve evrim politikalarını ekler.

## 8. Geriye uyumlu şema değişikliğine örnek ver.

Opsiyonel ve nullable yeni bir alan eklemek. Tüketiciler bilinmeyen alanları tolere ediyorsa eski tüketiciler çalışmaya devam eder.

## 9. Kırıcı şema değişikliğine örnek ver.

Alan silmek, tip değiştirmek, opsiyonel alanı zorunlu yapmak veya primary key'i değiştirmek.

## 10. Contract fingerprint neden kullanılır?

Bir veri setinin hangi doğrulama sözleşmesiyle üretildiğini deterministik olarak kaydeder ve sözleşme değişikliklerini dataset version'a bağlar.

## 11. Quarantine ile fail-fast ne zaman kullanılır?

Tekil bozuk kayıtlar quarantine edilebilir. Authentication, warehouse erişimi veya contract parser hatası gibi sistemik sorunlarda fail-fast tercih edilir.

## 12. Idempotent pipeline nedir?

Aynı girişin veya aynı event'in tekrar işlenmesi mantıksal sonucu çoğaltmaz. Primary key, upsert, idempotency key ve run version kullanılır.

## 13. Upsert'te geç gelen eski veri nasıl yönetilir?

Kaynak `updated_at`, sequence veya version alanı karşılaştırılır; yalnızca daha yeni kayıt hedefi günceller. Kaynak saati güvenilir değilse CDC sequence tercih edilebilir.

## 14. Watermark nedir?

Son başarıyla işlenen event time, update time veya artan kimliği temsil eder. Incremental extract sınırını belirler.

## 15. Watermark neden run başında güncellenmemelidir?

Run başarısız olursa veri aralığı atlanabilir. Watermark yalnızca başarılı commit sonrasında ilerletilmelidir.

## 16. Late-arriving data için overlap window nasıl çalışır?

Son watermark'tan biraz daha eski bir başlangıçla veri yeniden okunur. Upsert ve dedup sayesinde tekrarlar güvenli biçimde çözülür.

## 17. Dataset version nasıl oluşturulur?

Input checksum, contract fingerprint, pipeline code/version ve gerekirse parametrelerin canonical gösterimi hash'lenebilir.

## 18. Manifest ne içerir?

Run bilgisi, dataset version, input ve output checksum'ları, satır sayıları, contract sürümleri, lineage ve artefakt yolları.

## 19. Data lineage ne işe yarar?

Bir çıktının hangi kaynak, ara tablo, kod ve run'dan üretildiğini gösterir. Impact analysis, audit ve incident response'u kolaylaştırır.

## 20. Gold tablo grain'i neden açık olmalıdır?

Grain belirsizse JOIN satır çoğalması, duplicate key ve yanlış aggregation oluşur. Her feature'ın hesaplama seviyesi grain ile uyumlu olmalıdır.

## 21. Checksum ile encryption arasındaki fark nedir?

Checksum bütünlük kontrolü sağlar; veriyi gizlemez. Encryption gizlilik sağlar ve anahtar yönetimi gerektirir.

## 22. Pipeline gözlemlenebilirliği için hangi metrikleri izlersin?

Run süresi, extract/valid/rejected satır sayısı, rejection oranı, retry sayısı, watermark lag, artefakt boyutu ve son başarılı run zamanı.

## 23. Backfill ile günlük incremental run çakışırsa ne yaparsın?

Ayrı run namespace, partition kilidi, merge sırası, event version ve idempotent upsert kullanırım. Watermark güncellemelerini workload türüne göre ayırırım.

## 24. SQLite capstone'u üretime nasıl taşırsın?

Kaynak snapshot'larını object storage'a, orchestration'ı Airflow/Dagster benzeri sisteme, warehouse'u PostgreSQL veya cloud warehouse'a taşır; contract registry, secret manager, metric/trace ve CI quality gate eklerim.
