# Alıştırmalar

1. `ModelService` için model sürümünün boş olmasını engelleyen doğrulama ekle ve testini yaz.
2. Başarısız tahminde `request_id` alanının log kaydında bulunduğunu `caplog` ile doğrula.
3. Aynı predictor'ı 100, 1.000 ve 10.000 çağrıda `timeit` ile ölç.
4. Bir liste içinde tekrar eden üyelik araması yapan yavaş fonksiyonu set kullanarak optimize et; önce ve sonra ölçüm yap.
5. Dependency injection kullanılmayan bir HTTP istemci örneğini test edilebilir hale getir.
6. Exception chaining kullanılmayan kodu `raise ... from exc` ile düzelt.
7. Hassas veri içeren örnek logları güvenli alanlarla yeniden tasarla.
8. Unit ve integration testlerinin ayrımını gösteren iki pytest dosyası hazırla.
