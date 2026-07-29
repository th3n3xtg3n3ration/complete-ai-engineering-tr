# Quiz — Linux, Process, Thread, HTTP ve REST

Her soru için en doğru seçeneği işaretle.

## Sorular

### 1. Linux'ta çalışan bir program örneğini en doğru tanımlayan kavram hangisidir?

A. Header  
B. Process  
C. Socket path  
D. Environment key

### 2. `subprocess.run` için güvenli varsayılan yaklaşım hangisidir?

A. Kullanıcı girdisini string'e ekleyip `shell=True` kullanmak  
B. Komutu argüman listesiyle vermek ve timeout belirlemek  
C. Exit code'u görmezden gelmek  
D. stdout'u sınırsız bellekte tutmak

### 3. I/O-bound görevler için thread kullanımının temel avantajı nedir?

A. Her zaman CPU çekirdeği sayısı kadar hızlanır  
B. GIL'i tamamen kaldırır  
C. Bir görev beklerken diğer görevlerin ilerlemesini sağlar  
D. Process izolasyonu sağlar

### 4. Race condition ne zaman oluşur?

A. Tek thread immutable veri okuduğunda  
B. Birden fazla yürütme akışı paylaşılan mutable state'i koordinasyonsuz değiştirdiğinde  
C. HTTP cevabı `404` döndüğünde  
D. Process `SIGTERM` aldığında

### 5. `SIGKILL` hakkında hangisi doğrudur?

A. Uygulama tarafından yakalanıp cleanup yapılabilir  
B. Yalnızca thread'lere gönderilir  
C. Process'i zorla sonlandırır ve cleanup garantisi vermez  
D. HTTP bağlantısını keep-alive yapar

### 6. Semantik olarak idempotent olması beklenen metot hangisidir?

A. POST  
B. PUT  
C. CONNECT  
D. TRACE

### 7. Geçerli JSON içeren ancak `features` alanı boş olan inference isteği için en uygun kod hangisidir?

A. 201  
B. 301  
C. 422  
D. 502

### 8. Servis geçici olarak kapasitesini doldurduğunda en uygun cevap hangisidir?

A. 204  
B. 401  
C. 404  
D. 503

### 9. `/health` ile `/ready` ayrımının temel nedeni nedir?

A. Biri yalnızca POST kabul eder  
B. Process yaşıyor olabilir fakat model trafik almaya hazır olmayabilir  
C. İkisi her zaman aynı cevabı vermelidir  
D. Readiness yalnızca istemci tarafında kullanılır

### 10. REST kaynak adı için daha uygun örnek hangisidir?

A. `/v1/createPredictionNow`  
B. `/run-model`  
C. `/v1/predictions`  
D. `/doInferenceAction`

### 11. `429 Too Many Requests` cevabında istemci davranışına yardımcı olan header hangisidir?

A. Location  
B. Retry-After  
C. ETag  
D. Origin

### 12. API loglarında hangisi varsayılan olarak tutulmamalıdır?

A. Request ID  
B. HTTP durum kodu  
C. Ham authorization token  
D. Latency

### 13. Thread pool boyutunu sınırlamanın önemli nedeni nedir?

A. JSON parse işlemini devre dışı bırakmak  
B. Kaynak tüketimini ve scheduler baskısını kontrol etmek  
C. HTTP'yi stateful hale getirmek  
D. Process ID'yi sabitlemek

### 14. Cursor pagination hangi durumda offset pagination'a göre daha avantajlı olabilir?

A. Veri hiç değişmiyorsa ve yalnızca iki kayıt varsa  
B. Koleksiyon sık değişiyor ve sayfalar arasında tutarlılık isteniyorsa  
C. API yalnızca tek obje döndürüyorsa  
D. Request body XML ise

### 15. API sürümü ile model sürümünün ayrı izlenmesinin nedeni nedir?

A. Her model değişikliği mutlaka breaking API change değildir  
B. HTTP header kullanılamaz  
C. Model sürümü yalnızca Linux kernel tarafından bilinir  
D. API sürümü loglanamaz

## Kısa cevap

1. Concurrency ile parallelism arasındaki farkı iki cümleyle açıkla.
2. Deadlock riskini azaltmak için üç yöntem yaz.
3. `POST /v1/prediction-jobs` için idempotency key neden yararlı olabilir?
4. Graceful shutdown sırasında yapılması gereken dört işlemi sırala.
5. Bir inference endpoint'inde payload boyutu neden sınırlandırılmalıdır?

## Cevap anahtarı

1. B
2. B
3. C
4. B
5. C
6. B
7. C
8. D
9. B
10. C
11. B
12. C
13. B
14. B
15. A
