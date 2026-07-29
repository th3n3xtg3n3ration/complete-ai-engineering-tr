# Teori — İndeksler, Transaction, Query Plan ve Güvenilirlik

## 1. İndeks neden vardır?

İndeks, tablodaki satırlara daha az veri okuyarak ulaşmayı sağlayan ek bir veri yapısıdır. SQLite çoğunlukla B-tree tabanlı indeksler kullanır. İndeks sorguyu hızlandırabilir; fakat her `INSERT`, `UPDATE` ve `DELETE` işleminde indeksin de güncellenmesi gerekir. Bu nedenle "her kolona indeks" yaklaşımı üretim sistemlerinde genellikle yanlıştır.

İndeks kararı şu üç soruyla başlamalıdır:

1. Hangi sorgular sık çalışıyor?
2. Hangi kolonlar filtreleme, join ve sıralama için kullanılıyor?
3. Okuma kazancı yazma ve disk maliyetini haklı çıkarıyor mu?

## 2. İndeks türleri

- **Tek kolonlu indeks:** Tek bir filtre veya join anahtarını destekler.
- **Birleşik indeks:** Birden fazla kolonu belirli sırayla içerir.
- **Unique indeks:** Arama hızına ek olarak benzersizlik kuralı uygular.
- **Covering indeks:** Sorgunun ihtiyaç duyduğu kolonları indeks üzerinden karşılayabilir.
- **Partial indeks:** Yalnızca belirli koşulu sağlayan satırları indeksler.

## 3. Left-most prefix kuralı

`(customer_id, created_at)` indeksinin ilk kolonu `customer_id` olduğu için şu sorgular iyi adaydır:

- `WHERE customer_id = ?`
- `WHERE customer_id = ? AND created_at >= ?`
- `WHERE customer_id = ? ORDER BY created_at DESC`

Yalnızca `created_at` ile filtrelenen sorgu bu indeksin sol başını kullanmadığı için aynı faydayı görmeyebilir. Kolon sırası iş yüküne göre belirlenmelidir.

## 4. Query plan okumak

`EXPLAIN QUERY PLAN` sorgunun nasıl yürütüleceğine dair özet verir.

- `SCAN table`: Genellikle tüm tablo taraması.
- `SEARCH table USING INDEX ...`: İndeksli arama.
- `USING COVERING INDEX`: Tabloya dönmeden indeks üzerinden sonuç üretme olasılığı.
- `USE TEMP B-TREE FOR ORDER BY`: Sıralama için geçici yapı kullanımı.

Küçük tabloda full scan bazen daha ucuz olabilir. Planı tek başına değil veri büyüklüğü, seçicilik ve gerçek süreyle birlikte yorumlamak gerekir.

## 5. ACID

- **Atomicity:** İşlem ya tamamen gerçekleşir ya hiç gerçekleşmez.
- **Consistency:** Constraint ve iş kuralları korunur.
- **Isolation:** Eş zamanlı işlemler birbirinin ara durumlarını kontrolsüz biçimde görmez.
- **Durability:** Commit edilen veri kalıcı depolamaya aktarılır.

Para transferinde kaynaktan düşme başarılı, hedefe ekleme başarısız olursa atomicity ihlal edilir. Bu iki değişiklik aynı transaction içinde olmalıdır.

## 6. Transaction modları

SQLite'ta:

- `BEGIN DEFERRED`: Kilit ihtiyacı ilk erişime kadar ertelenir.
- `BEGIN IMMEDIATE`: Yazma niyetini baştan bildirir ve uygun kilidi erken alır.
- `BEGIN EXCLUSIVE`: Daha güçlü bir kilit talep eder; özel durumlar dışında dikkatli kullanılmalıdır.

Yazma işleminin kaçınılmaz olduğu kritik bir transfer akışında `IMMEDIATE`, çatışmayı işlemin ortasında değil başında görünür kılar.

## 7. Savepoint

Savepoint, uzun bir transaction içinde alt rollback sınırı oluşturur. Bir alt adım başarısız olduğunda tüm transaction yerine yalnızca ilgili bölüm geri alınabilir. Savepoint, ayrı bir transaction değildir; dış transaction commit edilmeden kalıcı hâle gelmez.

## 8. Idempotency

Ağ hatası nedeniyle istemci aynı transfer isteğini tekrar gönderebilir. Idempotency key, aynı mantıksal işlemin ikinci kez uygulanmasını engeller. Anahtar ile işlem sonucu birlikte transaction içinde kaydedilmelidir; aksi hâlde para hareketi gerçekleşip anahtar kaydı başarısız olabilir.

## 9. Optimistic locking

Optimistic locking satırdaki `version` değerini kullanır:

```sql
UPDATE accounts
SET balance = ?, version = version + 1
WHERE account_id = ? AND version = ?;
```

Güncellenen satır sayısı sıfırsa başka bir işlem arada değişiklik yapmıştır. Sistem eski veriyi sessizce ezmek yerine çatışmayı bildirir.

## 10. WAL ve concurrency

Write-Ahead Logging modunda değişiklikler önce WAL dosyasına yazılır. Bu yaklaşım birçok okuma-yazma senaryosunda concurrency'yi iyileştirebilir. Yine de SQLite tek bir anda sınırlı yazma concurrency'sine sahiptir. `busy_timeout` ve kontrollü exponential backoff geçici kilit çatışmalarını yönetmeye yardımcı olur.

## 11. Güvenilirlik araçları

- `PRAGMA foreign_keys = ON`
- `PRAGMA integrity_check`
- `PRAGMA foreign_key_check`
- `PRAGMA query_only = ON`
- SQLite backup API
- Düzenli restore testi
- Constraint, transaction ve rollback testleri

Backup dosyasının var olması yeterli değildir. Gerçek güvence, backup'ın açılıp kritik sorguların başarılı çalıştığının test edilmesidir.

## 12. Üretim kontrol listesi

- Transaction sınırı iş operasyonuyla aynı mı?
- Retry yalnızca gerçekten geçici hatalarda mı uygulanıyor?
- İşlem idempotent mi?
- Constraint'ler veritabanı seviyesinde de var mı?
- Sorgu grain'i açık mı?
- İndeks kararı query plan ve ölçümle doğrulandı mı?
- Backup restore testi var mı?
- İzleme metrikleri lock süresi, hata oranı ve yavaş sorguları kapsıyor mu?
