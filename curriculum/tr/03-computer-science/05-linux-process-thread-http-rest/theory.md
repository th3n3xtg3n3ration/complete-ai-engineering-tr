# Teori — Linux, Process, Thread, HTTP ve REST

## 1. AI mühendisliği neden sistem bilgisi gerektirir?

Bir model yalnızca Python fonksiyonundan ibaret değildir. Üretimde model; bir process içinde çalışır, dosya ve environment variable okur, ağ üzerinden istek alır, aynı anda birden fazla işi yönetir, kaynak sınırlarına uyar ve kontrollü biçimde kapanır. Bu nedenle sistem davranışını anlamadan güvenilir AI servisi geliştirmek zordur.

## 2. Linux çalışma ortamı

### 2.1 Dosya sistemi

Linux'ta kök dizin `/` ile başlar. Sık kullanılan dizinler:

- `/home`: kullanıcı dosyaları
- `/etc`: sistem ve servis yapılandırmaları
- `/var`: log, cache ve değişken çalışma verileri
- `/tmp`: geçici dosyalar
- `/proc`: process ve kernel bilgilerini sunan sanal dosya sistemi

Mutlak yol `/opt/models/model.bin`, göreli yol ise çalışma dizinine göre `models/model.bin` biçimindedir. Üretim kodunda çalışma dizininin sabit olduğunu varsaymak yerine `pathlib.Path` kullanmak daha güvenlidir.

### 2.2 İzinler

`r`, `w` ve `x`; okuma, yazma ve çalıştırma izinleridir. İzinler owner, group ve others için ayrı tutulur.

```bash
ls -l
chmod 640 config.env
```

Bir inference servisi mümkün olan en düşük yetkiyle çalışmalıdır. Model dosyasına okuma izni gerekebilir; ancak tüm dosya sistemine yazma izni çoğu zaman gereksizdir.

### 2.3 Environment variable

Secret, port ve çalışma modu gibi deploy-time değerler kaynak koda gömülmemelidir.

```bash
export APP_PORT=8080
export MODEL_VERSION=v1.4.0
```

Python tarafında:

```python
import os

port = int(os.getenv("APP_PORT", "8080"))
```

Environment variable eksik veya hatalıysa servis erken ve anlaşılır bir hata ile durmalıdır.

### 2.4 Temel araçlar

- `pwd`, `ls`, `cd`: konum ve dosyalar
- `cat`, `less`, `head`, `tail`: dosya okuma
- `grep`, `find`: arama
- `ps`, `top`: process gözlemleme
- `kill`: sinyal gönderme
- `curl`: HTTP istemcisi
- `ss`: dinlenen portları inceleme

Shell pipeline örneği:

```bash
ps aux | grep python
```

Her komutun exit code'u vardır. `0` genellikle başarıyı, sıfır dışındaki değerler hatayı gösterir.

## 3. Process

Process, çalışan bir program örneğidir. Kendi sanal adres alanına, PID değerine, açık dosya tanımlayıcılarına ve environment değerlerine sahiptir.

Bir child process başlatmak için Python'da `subprocess.run` tercih edilebilir:

```python
from subprocess import run

result = run(
    ["python", "--version"],
    capture_output=True,
    text=True,
    check=True,
    timeout=5,
)
```

Güvenli kullanım ilkeleri:

1. Komutu string yerine argüman listesi olarak ver.
2. Kullanıcı girdisini shell komutuna doğrudan ekleme.
3. Timeout belirle.
4. Exit code'u kontrol et.
5. stdout ve stderr boyutlarının sınırsız büyümesine izin verme.

`shell=True`, shell injection riskini artırabilir ve yalnızca bilinçli olarak kullanılmalıdır.

## 4. Thread, concurrency ve parallelism

- **Concurrency:** Birden fazla işin ilerlemesini koordine etmek.
- **Parallelism:** Birden fazla işi fiziksel olarak aynı anda yürütmek.
- **Thread:** Aynı process içindeki yürütme akışı; belleği diğer thread'lerle paylaşır.
- **Process:** Bellek izolasyonu daha güçlüdür; veri paylaşımı daha pahalıdır.

Python'daki GIL nedeniyle CPU-bound saf Python işleri thread ile doğrusal biçimde hızlanmaz. Thread'ler çoğunlukla ağ, disk ve bekleme ağırlıklı I/O-bound işler için uygundur. CPU-bound işlerde process pool veya native kütüphaneler değerlendirilebilir.

### 4.1 Race condition

Birden fazla thread paylaşılan veriyi eşzamanlı değiştirirse sonuç zamanlamaya bağlı hale gelebilir.

```python
from threading import Lock

lock = Lock()

with lock:
    shared_counter += 1
```

Lock kritik bölgeyi korur; fakat gereğinden geniş lock alanı throughput'u düşürür.

### 4.2 Deadlock

İki iş birbirinin tuttuğu kaynağı beklerse sistem ilerleyemez. Önleme yaklaşımları:

- Lock'ları tutarlı sırada almak
- Lock kapsamını küçültmek
- Timeout kullanmak
- Paylaşılan mutable state'i azaltmak
- Queue tabanlı mesajlaşmayı tercih etmek

### 4.3 Thread pool

Sınırsız thread üretmek bellek ve scheduler maliyetini artırır. `ThreadPoolExecutor`, concurrency sınırını açıkça belirler.

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(fetch_item, item_ids))
```

## 5. Process yaşam döngüsü ve sinyaller

Linux servisleri genellikle `SIGTERM` ile kontrollü kapanma isteği alır. Graceful shutdown sırasında:

1. Yeni istek kabulü durdurulur.
2. Devam eden işler sınırlı süre tamamlanır.
3. Buffer ve loglar flush edilir.
4. Ağ bağlantıları ve dosyalar kapatılır.
5. Process anlamlı exit code ile çıkar.

Ani `SIGKILL` yakalanamaz; temizlik kodu çalışmaz.

## 6. HTTP temelleri

HTTP bir request/response protokolüdür.

Örnek request:

```http
POST /v1/predictions HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer ...

{"features": [0.2, 0.7, 0.1]}
```

Örnek response:

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Request-ID: 5f6...

{"label": 1, "score": 0.73}
```

### 6.1 Metotlar

- `GET`: kaynak oku
- `POST`: işlem başlat veya yeni kaynak oluştur
- `PUT`: kaynağı bütünüyle değiştir
- `PATCH`: kısmi güncelle
- `DELETE`: kaynağı sil

`GET`, `PUT` ve `DELETE` semantik olarak idempotent tasarlanır: aynı isteğin tekrarı sistem durumunu ilk başarılı çağrıdan daha fazla değiştirmemelidir. `POST` varsayılan olarak idempotent değildir; ödeme veya uzun süren inference job'larında idempotency key kullanılabilir.

### 6.2 Durum kodları

- `200 OK`: başarılı cevap
- `201 Created`: kaynak oluşturuldu
- `202 Accepted`: async iş kabul edildi
- `204 No Content`: içeriksiz başarı
- `400 Bad Request`: biçim veya genel istemci hatası
- `401 Unauthorized`: kimlik doğrulama gerekli/geçersiz
- `403 Forbidden`: yetki yok
- `404 Not Found`: kaynak yok
- `409 Conflict`: durum çakışması
- `422 Unprocessable Content`: semantik doğrulama hatası
- `429 Too Many Requests`: rate limit
- `500 Internal Server Error`: beklenmeyen sunucu hatası
- `503 Service Unavailable`: servis geçici olarak hazır değil

### 6.3 Header'lar

- `Content-Type`: gövdenin medya türü
- `Accept`: istemcinin kabul ettiği medya türü
- `Authorization`: kimlik bilgisi
- `Cache-Control`: cache davranışı
- `Retry-After`: yeniden deneme zamanı
- `X-Request-ID` veya standart tracing header'ları: istek korelasyonu

Secret ve kişisel veri header/log içinde kontrolsüz tutulmamalıdır.

## 7. REST tasarımı

REST bir kütüphane değil, kaynak odaklı tasarım yaklaşımıdır.

İyi kaynak isimleri:

```text
GET  /v1/models
GET  /v1/models/{model_id}
POST /v1/predictions
GET  /v1/predictions/{prediction_id}
```

Eylem fiillerini URL'ye taşımak yerine HTTP metodunu ve kaynak modelini kullanmak genellikle daha tutarlıdır.

### 7.1 Hata sözleşmesi

Tutarlı hata gövdesi istemcilerin güvenilir davranmasını sağlar:

```json
{
  "error": {
    "code": "INVALID_FEATURES",
    "message": "features must be a non-empty numeric list",
    "request_id": "..."
  }
}
```

Stack trace ve secret değerler istemciye gönderilmemelidir.

### 7.2 Pagination

Büyük koleksiyonlar tek cevapta döndürülmemelidir. Offset pagination basittir; cursor pagination değişen veri kümelerinde daha kararlı olabilir.

```text
GET /v1/jobs?limit=50&cursor=abc123
```

Sunucu maksimum `limit` değerini sınırlandırmalıdır.

### 7.3 Versioning

Breaking change'ler için açık sürümleme gerekir. URL tabanlı `/v1/...` yaklaşımı anlaşılırdır. Sürüm değişikliği, yalnızca model ağırlığı değişiminden farklıdır: API sözleşmesi sürümü ile model sürümü ayrı alanlarda izlenmelidir.

## 8. AI inference API tasarım notları

Bir prediction endpoint'i şu riskleri yönetmelidir:

- Girdi boyutu ve tip doğrulaması
- Payload boyutu sınırı
- Model timeout'u
- Concurrency sınırı ve backpressure
- Request ID ve model version
- PII içermeyen loglar
- Health ve readiness ayrımı
- Deterministik hata sözleşmesi

`/health` process'in yaşadığını gösterebilir. `/ready` ise modelin yüklendiğini ve trafiğe hazır olduğunu doğrular. Bu iki sinyali karıştırmak, deploy sırasında hatalı trafik yönlendirmesine neden olabilir.

## 9. Güvenilir servis kontrol listesi

- En düşük Linux yetkisi
- Açık timeout'lar
- Sınırlı concurrency
- Güvenli subprocess kullanımı
- Kontrollü shutdown
- Şeması belirli JSON cevapları
- Doğru HTTP durum kodları
- Idempotency stratejisi
- Payload ve pagination sınırları
- Secret/PII redaction
- Unit ve integration testleri
