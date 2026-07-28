# Quiz — Dosya, Paket ve Bağımlılık Yönetimi

1. `pathlib.Path` kullanmanın temel avantajı nedir?
2. Dosya açarken neden `with` bloğu tercih edilir?
3. JSON ile CSV arasındaki tür bilgisi farkı nedir?
4. Atomik yazma hangi bozulma riskini azaltır?
5. Python modülü ile paket arasındaki fark nedir?
6. `pyproject.toml` hangi sorumlulukları üstlenebilir?
7. Sanal ortam neden kullanılır?
8. Doğrudan ve dolaylı bağımlılık arasındaki fark nedir?
9. API anahtarları neden kaynak koda yazılmamalıdır?
10. Dosya testlerinde `tmp_path` ne sağlar?

## Cevap anahtarı

1. İşletim sistemleri arasında taşınabilir ve okunabilir yol işlemleri sağlar.
2. Dosyanın hata olsa bile kapatılmasını garanti eder.
3. JSON temel türleri korur; CSV hücreleri başlangıçta metindir.
4. Yarım veya bozuk hedef dosya bırakma riskini azaltır.
5. Modül tek Python dosyasıdır; paket ilişkili modülleri bir ad alanında toplar.
6. Build sistemi, metadata, bağımlılıklar ve araç ayarlarını tanımlar.
7. Proje bağımlılıklarını diğer projelerden izole eder.
8. Doğrudan bağımlılığı proje kullanır; dolaylı bağımlılığı kullanılan paket getirir.
9. Sırların git geçmişine ve yetkisiz kişilere sızmasını önlemek için.
10. Her test için izole, geçici bir dosya sistemi alanı sağlar.