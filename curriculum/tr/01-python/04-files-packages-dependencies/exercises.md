# Alıştırmalar

1. `Path` kullanarak `data/raw/events.json` yolunu oluştur.
2. UTF-8 metin dosyasındaki boş satırları atlayan bir fonksiyon yaz.
3. CSV satırlarını sözlüklere dönüştür ve sayısal alanları doğru tipe çevir.
4. JSON kökü liste değilse açıklayıcı hata üreten bir okuyucu geliştir.
5. Eksik üst dizinleri oluşturarak dosya yazan bir fonksiyon yaz.
6. Bir dosyanın SHA-256 özetini hesapla.
7. `Record` modeline isteğe bağlı `created_at` alanı ekle ve ISO-8601 doğrulaması yap.
8. `save_records` fonksiyonuna sıralama seçeneği ekle.
9. JSON yerine JSON Lines biçimini destekleyen ayrı depolama sınıfı geliştir.
10. Ortam değişkeninden veri dizini okuyan, yoksa güvenli varsayılan kullanan yapılandırma fonksiyonu yaz.
11. Pakete komut satırı giriş noktası ekleyerek bir JSON dosyasının özetini yazdır.
12. Geçici dosyanın yazma hatasında temizlendiğini doğrulayan test oluştur.

## Başarı ölçütü

Çözümler tür ipuçları içermeli, kullanıcı dizinine sabit yol yazmamalı, encoding belirtmeli ve hata durumlarını test etmelidir.