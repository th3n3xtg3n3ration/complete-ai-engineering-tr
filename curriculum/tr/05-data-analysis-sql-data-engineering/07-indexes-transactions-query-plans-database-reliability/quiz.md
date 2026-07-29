# Quiz

1. Bir indeksin temel amacı nedir?
   - A) Transaction sayısını artırmak
   - B) Belirli sorgularda okunan veri miktarını azaltmak
   - C) Her yazmayı hızlandırmak
   - D) Foreign key'i kaldırmak

2. `(a, b)` birleşik indeksi en doğal olarak hangi filtreyi destekler?
   - A) Yalnızca `b`
   - B) `a` veya `a` ve `b`
   - C) Hiçbirini
   - D) Yalnızca sıralamayı

3. `SCAN accounts` ifadesi neyi düşündürür?
   - A) Tüm tablo taraması
   - B) Unique index kullanımı
   - C) Transaction rollback
   - D) Backup

4. Atomicity neyi garanti eder?
   - A) İşlem parçalarının kısmen kalmasını
   - B) İşlemin tamamen uygulanmasını veya hiç uygulanmamasını
   - C) Her sorgunun indeks kullanmasını
   - D) Sonsuz retry yapılmasını

5. Yazma işlemi kaçınılmazsa kilidi erken almak için hangi SQLite modu uygundur?
   - A) `BEGIN IMMEDIATE`
   - B) `SELECT DISTINCT`
   - C) `PRAGMA query_only`
   - D) `VACUUM`

6. Savepoint ne sağlar?
   - A) Tüm veritabanını siler
   - B) Transaction içinde kısmi rollback sınırı
   - C) İndeks oluşturur
   - D) Query planını değiştirir

7. Idempotency key'in amacı nedir?
   - A) Aynı mantıksal isteğin ikinci kez uygulanmasını önlemek
   - B) İndeksi kaldırmak
   - C) Foreign key'i devre dışı bırakmak
   - D) Sıralamayı ters çevirmek

8. Optimistic locking genellikle hangi alanı kullanır?
   - A) `version`
   - B) `password`
   - C) `index_name`
   - D) `backup_path`

9. WAL neyin kısaltmasıdır?
   - A) Write-Ahead Logging
   - B) Wide Access Layer
   - C) Window Aggregate Logic
   - D) Write After Lock

10. `busy_timeout` neyi yönetmeye yardımcı olur?
    - A) Geçici lock bekleme süresini
    - B) Kolon adlarını
    - C) Grafik boyutunu
    - D) Index uniqueness'i

11. Retry hangi hata türünde en uygundur?
    - A) Kalıcı şema hatası
    - B) Geçici lock çatışması
    - C) Yanlış kolon adı
    - D) Constraint tasarım hatası

12. Covering index ne sağlar?
    - A) Sorgunun ihtiyaç duyduğu verinin indeks üzerinden karşılanabilmesini
    - B) Transaction'ı kaldırmayı
    - C) Backup şifrelemeyi
    - D) Foreign key'i gizlemeyi

13. `PRAGMA integrity_check` ne için kullanılır?
    - A) Veritabanı yapısal bütünlüğünü kontrol etmek
    - B) Model accuracy ölçmek
    - C) CSV üretmek
    - D) HTTP isteği atmak

14. Query-only bağlantı ne yapar?
    - A) Yazmaları reddeder
    - B) Tüm indeksleri kaldırır
    - C) WAL'ı siler
    - D) Transaction'ı otomatik retry eder

15. Backup güvenilirliğinin en iyi kanıtı nedir?
    - A) Dosyanın var olması
    - B) Restore edilip kritik sorguların çalışması
    - C) Dosya adının doğru olması
    - D) Boyutunun sıfırdan büyük olması

16. Çok fazla indeksin temel riski nedir?
    - A) Yazma ve disk maliyetini artırması
    - B) Constraint'leri güçlendirmesi
    - C) Query planını her zaman iyileştirmesi
    - D) Transaction'ı atomik yapması

17. Exponential backoff ne yapar?
    - A) Her retry'da bekleme süresini artırır
    - B) İndeksi küçültür
    - C) Backup'ı siler
    - D) Version değerini sıfırlar

18. Optimistic update sıfır satır etkilediyse en olası durum nedir?
    - A) Version çatışması
    - B) WAL etkinleşmesi
    - C) İndeksin covering olması
    - D) Backup tamamlanması

19. Transaction içinde idempotency kaydı neden aynı atomik sınırda tutulmalıdır?
    - A) İşlem ile tekrar korumasının ayrışmasını önlemek için
    - B) İndeks sayısını azaltmak için
    - C) Query-only modu açmak için
    - D) CSV üretmek için

20. İndeks kararını doğrulamak için en iyi yaklaşım hangisidir?
    - A) Sadece sezgi
    - B) Query planı ve ölçüm
    - C) Tüm kolonları indekslemek
    - D) Constraint'leri kaldırmak

## Cevap anahtarı

1-B, 2-B, 3-A, 4-B, 5-A, 6-B, 7-A, 8-A, 9-A, 10-A, 11-B, 12-A, 13-A, 14-A, 15-B, 16-A, 17-A, 18-A, 19-A, 20-B
