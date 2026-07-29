# Quiz — API, ETL/ELT ve Veri Ürünü Güvenilirliği

Her soru için en doğru seçeneği işaretle.

1. `503 Service Unavailable` yanıtında en uygun ilk davranış hangisidir?
   - A) Sonsuz retry
   - B) Sınırlı retry ve backoff
   - C) Veriyi silmek
   - D) Şema sürümünü artırmak

2. `Retry-After` header'ı neyi belirtir?
   - A) Response boyutunu
   - B) İstemcinin yeniden denemeden önce beklemesi gereken süreyi
   - C) Token süresini
   - D) Sayfa sayısını

3. Cursor pagination'ın önemli bir avantajı nedir?
   - A) Her zaman daha küçük JSON üretir
   - B) Değişen veri setlerinde offset kaymasına karşı daha kararlı olabilir
   - C) Authentication gerektirmez
   - D) Duplicate veriyi otomatik siler

4. Bronze katmanın temel özelliği hangisidir?
   - A) Model tahmini içerir
   - B) Kaynağa yakın ve değiştirilemez ham snapshot saklar
   - C) Yalnızca aggregate veri içerir
   - D) Primary key içermez

5. ETL sıralaması hangisidir?
   - A) Extract, Transform, Load
   - B) Extract, Load, Transform
   - C) Transform, Extract, Load
   - D) Load, Transform, Extract

6. ELT hangi durumda özellikle avantajlıdır?
   - A) Hedef analitik platform güçlü dönüşüm kapasitesine sahipse
   - B) Hiç ham veri saklanmayacaksa
   - C) Veritabanı yoksa
   - D) Şema kontrolü gerekmiyorsa

7. Veri sözleşmesinde hangisi bulunabilir?
   - A) Alan tipi
   - B) Null politikası
   - C) Primary key
   - D) Hepsi

8. Opsiyonel nullable alan eklemek genellikle nasıl sınıflandırılır?
   - A) Geriye uyumlu değişiklik
   - B) Her zaman major kırılma
   - C) Veri kaybı
   - D) Transaction hatası

9. Aşağıdakilerden hangisi kırıcı şema değişikliğidir?
   - A) Açıklama eklemek
   - B) Opsiyonel alan eklemek
   - C) Mevcut alanın tipini değiştirmek
   - D) Metadata sırasını değiştirmek

10. Quarantine katmanının amacı nedir?
    - A) Geçersiz kayıtları nedenleriyle ayrı tutmak
    - B) Bütün pipeline loglarını silmek
    - C) API token saklamak
    - D) İndeks oluşturmak

11. Idempotent pipeline ne sağlar?
    - A) Her retry'da farklı sonuç
    - B) Aynı girdinin tekrarlı işlenmesinde aynı mantıksal sonuç
    - C) Daha büyük dosya
    - D) Şemasız veri

12. `updated_at` kontrollü upsert'in faydası nedir?
    - A) Eski kaydın yeni kaydı ezmesini azaltır
    - B) Primary key'i kaldırır
    - C) API rate limit'i artırır
    - D) Hash algoritmasını değiştirir

13. Watermark ne için kullanılır?
    - A) Son işlenen sınırı takip ederek incremental extract yapmak
    - B) JSON'u sıkıştırmak
    - C) Secret şifrelemek
    - D) Grafik üretmek

14. Watermark ne zaman ilerletilmelidir?
    - A) Extract başlamadan önce
    - B) Başarılı run tamamlandıktan sonra
    - C) Her reddedilen kayıtta
    - D) API timeout olduğunda

15. Dataset version hangi bileşenlerden türetilebilir?
    - A) Input checksum
    - B) Contract fingerprint
    - C) Pipeline version
    - D) Hepsi

16. Manifestin amacı nedir?
    - A) Artefakt, lineage, sürüm ve kalite bilgisini kaydetmek
    - B) Yalnızca kullanıcı parolası saklamak
    - C) API endpoint değiştirmek
    - D) SQL transaction başlatmak

17. SHA-256 checksum neyi denetlemeye yardım eder?
    - A) Artefakt bütünlüğünü
    - B) Kullanıcı yetkisini
    - C) SQL isolation seviyesini
    - D) API kotasını

18. Gold tablo için en kritik tasarım bilgisi hangisidir?
    - A) Dosya adının uzunluğu
    - B) Tablo grain'i
    - C) Terminal teması
    - D) JSON indentation

19. API secret için doğru yaklaşım hangisidir?
    - A) Kaynak koda yazmak
    - B) Loglarda göstermek
    - C) Secret manager veya ortam değişkeni kullanmak
    - D) Manifestte açık metin saklamak

20. Pipeline gözlemlenebilirliğinde hangisi yararlıdır?
    - A) Reddedilme oranı
    - B) Son başarılı run zamanı
    - C) Retry sayısı
    - D) Hepsi

## Cevap anahtarı

1-B, 2-B, 3-B, 4-B, 5-A, 6-A, 7-D, 8-A, 9-C, 10-A, 11-B, 12-A, 13-A, 14-B, 15-D, 16-A, 17-A, 18-B, 19-C, 20-D
