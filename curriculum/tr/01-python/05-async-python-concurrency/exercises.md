# Alıştırmalar

1. Bir saniye bekleyip değer döndüren coroutine yaz.
2. Üç coroutine'i `gather` ile birlikte çalıştır ve süreyi ölç.
3. `create_task` ile görev oluşturup sonucunu güvenli biçimde bekle.
4. Belirli sürede bitmeyen görevi timeout ile durdur.
5. Bir görevi dışarıdan iptal et ve temizliği `finally` içinde yap.
6. En fazla üç işin birlikte çalıştığı Semaphore örneği yaz.
7. `asyncio.Queue` ile bir producer ve iki consumer oluştur.
8. Queue'ya `maxsize` ekleyerek backpressure davranışını gözlemle.
9. Geçici `ConnectionError` için üç denemeli exponential backoff uygula.
10. Başarılı ve başarısız sonuçları dataclass ile modelle.
11. Bloklayan bir fonksiyonu `asyncio.to_thread` ile çalıştır.
12. Paylaşılan sayacı Lock olmadan ve Lock ile güncelleyerek farkı incele.
13. Crawler'a URL tekrarlarını kaldırma özelliği ekle.
14. Sonuçları JSON dosyasına yazan ayrı bir fonksiyon geliştir.
15. Crawler'a toplam başarı oranı ve ortalama gecikme özeti ekle.

Her alıştırmada type hint, açıklayıcı isimler ve en az bir otomatik test kullan.
