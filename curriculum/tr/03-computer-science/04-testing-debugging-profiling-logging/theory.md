# Teori — Test, Debugging, Profiling ve Logging

## 1. Kaliteyi dört ayrı problem olarak düşün

- **Testing:** Davranışın beklendiği gibi olduğunu kanıtlar.
- **Debugging:** Beklenmeyen davranışın nedenini bulur.
- **Profiling:** Zaman ve bellek maliyetinin nerede oluştuğunu ölçer.
- **Logging:** Çalışan sistemin geçmişi hakkında teşhis verisi üretir.

Bu araçlar birbirinin alternatifi değildir. Üretim kalitesindeki bir AI servisi dördünü birlikte kullanır.

## 2. Test piramidi

Unit testler küçük ve hızlıdır. Integration testler bileşenlerin birlikte çalışmasını doğrular. Uçtan uca testler gerçek kullanıcı akışına yaklaşır fakat daha yavaş ve kırılgandır. Çoğu projede taban geniş, üst katmanlar daha dar tutulur.

### Arrange, Act, Assert

1. Girdileri ve bağımlılıkları hazırla.
2. Test edilen davranışı çalıştır.
3. Sonucu ve yan etkileri doğrula.

Testler implementasyon detayına değil, gözlemlenebilir davranışa bağlanmalıdır.

## 3. Fixture ve parametrization

Fixture tekrar eden kurulumu merkezileştirir. Parametrization aynı davranışı farklı girdilerle doğrular. Edge case'ler, boş girdiler, sınır değerleri ve hatalı tipler tablo halinde test edilebilir.

## 4. Mock ve dependency injection

Ağ, veritabanı, saat ve rastgelelik gibi bağımlılıklar testleri yavaş veya nondeterministic yapabilir. Dependency injection bağımlılığı fonksiyona dışarıdan verir. Mock ise gerçek bağımlılığın kontrollü bir temsilini sağlar.

Mock yalnızca sınır noktalarında kullanılmalıdır. Her iç fonksiyonu mock'lamak testleri implementasyona aşırı bağlar.

## 5. Sistematik debugging

1. Sorunu tekrarlanabilir hale getir.
2. Beklenen ve gerçek davranışı yaz.
3. Arama alanını küçült.
4. Hipotez oluştur.
5. Tek değişkeni değiştirerek hipotezi test et.
6. Kök nedeni düzelt.
7. Regression testi ekle.

`print` geçici olabilir; breakpoint, stack trace, exception chaining ve minimal reproducible example daha güvenilir yöntemlerdir.

## 6. Profiling

Ölçmeden optimizasyon yapma. Önce gerçek iş yükünü seç, sonra baseline ölç. `timeit` küçük kod parçaları, `cProfile` çağrı bazlı CPU profili, `pstats` ise sonuçların sıralanması için uygundur.

Profiling soruları:

- Toplam sürenin çoğu hangi fonksiyonda?
- Fonksiyon kaç kez çağrılıyor?
- Sorun algoritmik karmaşıklık mı, I/O mu, tekrar hesaplama mı?
- Optimizasyon okunabilirliği veya doğruluğu bozuyor mu?

## 7. Logging

Seviyeler:

- `DEBUG`: ayrıntılı geliştirme bilgisi
- `INFO`: normal iş akışı
- `WARNING`: sistem çalışıyor fakat dikkat gereken durum
- `ERROR`: işlem başarısız
- `CRITICAL`: servis bütünlüğünü tehdit eden hata

Log kayıtlarında zaman, seviye, olay adı, request ID, model sürümü, latency ve hata türü bulunabilir. Parola, token, kişisel veri veya ham kullanıcı prompt'u kontrolsüz biçimde loglanmamalıdır.

## 8. AI mühendisliği bağlamı

Model çıktısı doğru görünse bile servis hatalı olabilir. Şema doğrulama, timeout, retry, model versiyonu, input boyutu, latency ve fallback kararı test ve loglarla izlenmelidir. Testler deterministic parçaları sıkı doğrularken probabilistic model davranışı tolerans, property veya evaluation metrikleriyle ele alınmalıdır.
