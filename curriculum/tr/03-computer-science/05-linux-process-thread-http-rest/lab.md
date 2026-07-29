# Lab — Linux'tan Test Edilebilir Inference API'ye

Bu laboratuvarda sistem bilgisini küçük bir AI servisinin çalışma yaşam döngüsüne uygulayacaksın.

## Ön koşullar

- Python 3.11+
- Linux, macOS veya WSL
- `curl`
- `pytest`

## Bölüm 1 — Linux ortamını incele

```bash
pwd
whoami
python --version
printf 'PID=%s\n' "$$"
ps -o pid,ppid,stat,command -p "$$"
```

Aşağıdaki soruları cevapla:

1. Shell process'inin PID ve PPID değerleri nedir?
2. Çalışma dizini ile script dosyasının dizini aynı olmak zorunda mıdır?
3. `PATH` değişkeni executable çözümlemesini nasıl etkiler?

Environment variable tanımla:

```bash
export APP_PORT=8080
export MODEL_VERSION=demo-v1
python -c 'import os; print(os.getenv("APP_PORT"), os.getenv("MODEL_VERSION"))'
```

## Bölüm 2 — Güvenli subprocess

`src/system_inspector.py` içindeki `run_command` fonksiyonunu çalıştır:

```bash
python curriculum/tr/03-computer-science/05-linux-process-thread-http-rest/src/system_inspector.py
```

Şunları gözlemle:

- Komut argüman listesi olarak veriliyor.
- `shell=True` kullanılmıyor.
- Timeout uygulanıyor.
- Exit code, stdout ve stderr kontrollü biçimde dönüyor.

Başarısız komut deneyi:

```python
from pathlib import Path
import importlib.util

path = Path("curriculum/tr/03-computer-science/05-linux-process-thread-http-rest/src/system_inspector.py")
spec = importlib.util.spec_from_file_location("system_inspector", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(module.run_command(["python", "-c", "raise SystemExit(3)"]))
```

## Bölüm 3 — Sınırlı thread pool

`parallel_map` fonksiyonunu I/O beklemesini taklit eden görevlerle dene:

```python
import time
from pathlib import Path
import importlib.util

path = Path("curriculum/tr/03-computer-science/05-linux-process-thread-http-rest/src/system_inspector.py")
spec = importlib.util.spec_from_file_location("system_inspector", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def work(value: int) -> int:
    time.sleep(0.1)
    return value * value

print(module.parallel_map(work, range(8), max_workers=4))
```

`max_workers=1`, `2` ve `4` değerlerini karşılaştır. Thread sayısını sınırsız artırmanın neden doğru olmadığını yaz.

## Bölüm 4 — HTTP API'yi başlat

```bash
export APP_PORT=8080
export MODEL_VERSION=demo-v1
python curriculum/tr/03-computer-science/05-linux-process-thread-http-rest/src/http_api.py
```

Başka terminalde:

```bash
curl -i http://127.0.0.1:8080/health
```

Beklenen gövde:

```json
{"status":"ok","model_version":"demo-v1"}
```

Tahmin isteği:

```bash
curl -i -X POST http://127.0.0.1:8080/v1/predictions \
  -H 'Content-Type: application/json' \
  -H 'X-Request-ID: lab-001' \
  -d '{"features":[0.2,0.7,0.1]}'
```

API, sayıların ortalamasını skor olarak kullanır ve `0.5` eşiğine göre label üretir. Bu basit modelin amacı ML kalitesi değil, servis sözleşmesini incelemektir.

## Bölüm 5 — Hata senaryoları

Yanlış media type:

```bash
curl -i -X POST http://127.0.0.1:8080/v1/predictions \
  -H 'Content-Type: text/plain' \
  -d 'hello'
```

Bozuk JSON:

```bash
curl -i -X POST http://127.0.0.1:8080/v1/predictions \
  -H 'Content-Type: application/json' \
  -d '{broken}'
```

Geçersiz özellikler:

```bash
curl -i -X POST http://127.0.0.1:8080/v1/predictions \
  -H 'Content-Type: application/json' \
  -d '{"features":[]}'
```

Her cevap için şunları kaydet:

- HTTP durum kodu
- `Content-Type`
- `X-Request-ID`
- Hata `code` alanı
- İstemcinin bu hatayı retry edip etmemesi gerektiği

## Bölüm 6 — Concurrency deneyi

Aşağıdaki script ile aynı anda istek gönder:

```python
from concurrent.futures import ThreadPoolExecutor
from json import dumps
from urllib.request import Request, urlopen


def predict(index: int) -> tuple[int, str]:
    request = Request(
        "http://127.0.0.1:8080/v1/predictions",
        data=dumps({"features": [index / 10, 0.5]}).encode(),
        headers={
            "Content-Type": "application/json",
            "X-Request-ID": f"batch-{index}",
        },
        method="POST",
    )
    with urlopen(request, timeout=2) as response:
        return response.status, response.read().decode()


with ThreadPoolExecutor(max_workers=4) as pool:
    print(list(pool.map(predict, range(12))))
```

Servisin thread-per-request yaklaşımının avantaj ve risklerini yaz. Üretimde concurrency sınırının yalnızca istemci tarafında değil, servis veya reverse proxy katmanında da uygulanması gerektiğini tartış.

## Bölüm 7 — Graceful shutdown

Servis terminalinde `Ctrl+C` kullan. Process'in traceback dökmeden kapanmasını doğrula. Ardından:

```bash
ss -ltn | grep 8080 || true
```

Portun serbest bırakıldığını kontrol et.

## Bölüm 8 — Testler

```bash
pytest curriculum/tr/03-computer-science/05-linux-process-thread-http-rest/tests -q
```

Testlerin dış network'e bağlanmadan core doğrulama ve response üretim fonksiyonlarını sınadığını incele.

## Teslim çıktıları

- Linux komut gözlemleri
- Process/thread karşılaştırması
- Başarılı ve başarısız HTTP örnekleri
- Concurrency deneyi sonucu
- Graceful shutdown doğrulaması
- En az üç yeni pytest testi
