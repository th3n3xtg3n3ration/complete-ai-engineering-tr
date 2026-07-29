# Mülakat Soruları — Linux, Process, Thread, HTTP ve REST

## Linux ve process

### 1. Process ile program arasındaki fark nedir?

Program disk üzerindeki executable ve kaynakların bütünüdür. Process ise programın çalışan örneğidir; PID, adres alanı, açık dosyalar, environment ve çalışma durumu gibi runtime özelliklere sahiptir.

### 2. PID ve PPID nedir?

PID process kimliğidir. PPID, process'i başlatan parent process'in kimliğidir. Servis yöneticisi veya shell çoğu zaman uygulama process'inin parent'ıdır.

### 3. Zombie process nasıl oluşur?

Child process sonlanır fakat parent exit durumunu `wait` ailesiyle toplamazsa process tablosunda zombie kayıt kalabilir. Zombie CPU çalıştırmaz; ancak process tablosu kaynağı tüketir.

### 4. `SIGTERM` ile `SIGKILL` arasındaki fark nedir?

`SIGTERM` uygulamaya kontrollü kapanma fırsatı verir ve yakalanabilir. `SIGKILL` kernel tarafından zorla uygulatılır, yakalanamaz ve cleanup garantisi vermez.

### 5. Neden servisleri root olarak çalıştırmamak gerekir?

Bir güvenlik açığının etkisini sınırlandırmak için least privilege uygulanır. Servisin yalnızca gerekli dosya, port ve kaynaklara erişmesi gerekir.

### 6. Environment variable ile secret yönetmenin sınırlamaları nelerdir?

Kaynak koda gömmekten daha iyidir; ancak process inspection, crash dump veya yanlış loglama yoluyla sızabilir. Üretimde secret manager, kısa ömürlü credential ve erişim kontrolü gerekir.

### 7. `shell=True` neden risklidir?

Kullanıcı kontrollü input shell metakarakterleriyle yorumlanabilir ve command injection oluşabilir. Argüman listesi, allowlist, path doğrulama ve shell'i devre dışı bırakma daha güvenlidir.

## Thread ve concurrency

### 8. Concurrency ile parallelism arasındaki fark nedir?

Concurrency birden fazla işin ilerlemesini koordine etmektir. Parallelism işlerin fiziksel olarak aynı anda, çoğunlukla birden fazla çekirdekte yürütülmesidir.

### 9. Python GIL thread kullanımını nasıl etkiler?

CPython'da aynı process içindeki yalnızca bir thread aynı anda Python bytecode çalıştırır. Bu nedenle CPU-bound saf Python kodu thread ile beklenen ölçüde hızlanmayabilir; I/O-bound görevler ise bekleme sırasında fayda görebilir.

### 10. Race condition nedir?

Sonucun thread veya process zamanlamasına bağlı olduğu, paylaşılan mutable state üzerindeki koordinasyonsuz erişim problemidir. Lock, queue, immutable veri ve sahiplik tasarımıyla azaltılabilir.

### 11. Deadlock için gerekli koşullar nelerdir?

Klasik koşullar: mutual exclusion, hold and wait, no preemption ve circular wait. Bunlardan en az birini tasarımla bozmak deadlock'u önleyebilir.

### 12. Lock kapsamı neden küçük tutulmalıdır?

Geniş kritik bölge contention'ı artırır, throughput'u düşürür ve deadlock riskini büyütebilir. Yalnızca paylaşılan state değişikliği lock altında tutulmalıdır.

### 13. Thread pool neden sınırlanmalıdır?

Her thread stack belleği ve scheduler maliyeti taşır. Sınırsız concurrency downstream servisi, bağlantı havuzunu ve CPU'yu aşırı yükleyebilir; açık sınır backpressure sağlar.

### 14. CPU-bound inference preprocessing için thread mi process mi seçersin?

Saf Python CPU-bound işte process pool GIL'i aşabilir; ancak serialization ve bellek maliyeti vardır. NumPy/PyTorch gibi GIL'i bırakan native kodlarda thread yaklaşımı da uygun olabilir. Ölçüm yapılmalıdır.

## HTTP

### 15. HTTP request'in temel parçaları nelerdir?

Method, target/path, protocol version, header'lar ve opsiyonel body. Response ise status line, header'lar ve opsiyonel body içerir.

### 16. `400` ile `422` arasındaki pratik fark nedir?

`400`, malformed request veya genel istemci hatası için kullanılabilir. `422`, JSON parse edilebildiği halde domain doğrulamasının başarısız olduğu durumları daha açık ifade eder.

### 17. `401` ile `403` arasındaki fark nedir?

`401`, kimlik doğrulama eksik veya geçersiz olduğunda kullanılır. `403`, kimlik bilinse bile ilgili işlemi yapma yetkisi olmadığını belirtir.

### 18. `503` ne zaman kullanılmalıdır?

Servis geçici olarak hazır değilse, bakımda ise veya kapasite dolduysa kullanılır. Retry mümkünse istemciye `Retry-After` gibi bilgi sağlanabilir.

### 19. Idempotency nedir?

Aynı isteğin tekrar uygulanmasının sistem durumunu ilk başarılı uygulamadan daha fazla değiştirmemesidir. Retry güvenliği için özellikle ödeme, job creation ve uzun süren işlemlerde önemlidir.

### 20. Timeout türlerini nasıl ayırırsın?

Connection timeout bağlantı kurulmasını, read timeout cevap beklemeyi, application/model timeout iş mantığını sınırlar. İstemci, proxy ve servis timeout'ları uyumlu tasarlanmalıdır.

### 21. HTTP retry hangi hatalarda güvenlidir?

Tek başına durum kodu yeterli değildir. İşlemin idempotent olması, retry budget, jittered exponential backoff ve `Retry-After` dikkate alınmalıdır. `429`, `502`, `503`, `504` çoğu zaman adaydır; non-idempotent POST dikkat ister.

## REST ve API tasarımı

### 22. REST endpoint isimlerinde fiil yerine kaynak kullanmanın avantajı nedir?

HTTP metotları eylemi, URL ise kaynağı ifade eder. Böylece sözleşme daha tutarlı, tahmin edilebilir ve genişletilebilir olur.

### 23. Offset ve cursor pagination farkı nedir?

Offset basit ve rastgele sayfa erişimine uygundur; fakat sık değişen veride kayıt atlama veya tekrarı yaşanabilir. Cursor, kararlı sıralama anahtarıyla değişen büyük koleksiyonlarda daha tutarlıdır.

### 24. API version ile model version neden ayrıdır?

API version istemci sözleşmesini, model version ise tahmin üreten artifact'i ifade eder. Model ağırlığı değişebilir fakat request/response şeması aynı kalabilir.

### 25. Sağlık kontrolü ile readiness kontrolü neden ayrılmalıdır?

Process canlı olabilir fakat model yüklenmemiş veya bağımlılık erişilemez olabilir. Liveness restart kararına, readiness ise trafik yönlendirmesine hizmet eder.

### 26. Tutarlı hata sözleşmesi neden önemlidir?

İstemci tarafının retry, kullanıcı mesajı, telemetry ve hata sınıflandırmasını deterministik yapmasını sağlar. İnsan mesajından ayrı, kararlı makine kodu bulunmalıdır.

### 27. Request ID ne işe yarar?

Bir isteğin gateway, servis ve downstream bileşenler arasındaki izini korele eder. İstemciden gelen güvenli bir ID korunabilir veya servis tarafından üretilebilir.

### 28. Inference API'de neden body boyutu sınırı gerekir?

Bellek tüketimini, parse süresini ve denial-of-service riskini kontrol eder. Modelin kabul ettiği input boyutuyla API limiti uyumlu olmalıdır.

### 29. Backpressure nedir?

Sistem kapasitesi dolduğunda daha fazla işi sınırsız kabul etmek yerine kuyruğu sınırlama, reddetme veya yavaşlatma mekanizmasıdır. Latency çöküşünü ve kaynak tükenmesini önler.

### 30. Standart kütüphane HTTP sunucusunu production'da neden doğrudan kullanmazsın?

Eğitim ve küçük internal araçlar için uygundur; ancak production'da gelişmiş timeout, worker yönetimi, TLS termination, observability, güvenlik hardening ve ekosistem desteği için olgun bir application server ve reverse proxy tercih edilir.

## Sistem tasarım sorusu

Bir GPU inference API tasarla. Şunları tartış:

- Request doğrulama ve maksimum batch boyutu
- Sync ve async endpoint ayrımı
- Dynamic batching
- GPU concurrency ve queue sınırı
- Timeout ve cancellation
- Model version rollout
- Health/readiness
- Metrics ve tracing
- Idempotency
- Rate limiting
- Graceful shutdown sırasında queue davranışı
- Overload durumunda `429` ile `503` seçimi
