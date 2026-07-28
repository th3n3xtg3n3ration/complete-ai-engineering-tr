# Teori — Dosya, Paket ve Bağımlılık Yönetimi

## 1. Dosya sistemiyle güvenli çalışma

Python'da dosya yolları için karakter dizisi birleştirmek yerine `pathlib.Path` kullanılır. Böylece Windows, Linux ve macOS arasındaki ayraç farkları uygulama koduna sızmaz.

```python
from pathlib import Path

base_dir = Path("data")
input_path = base_dir / "raw" / "records.json"
```

Bir dosya açıldığında kaynak mutlaka kapatılmalıdır. `with` bloğu bu yaşam döngüsünü otomatik yönetir.

```python
with input_path.open("r", encoding="utf-8") as stream:
    content = stream.read()
```

## 2. Metin, JSON ve CSV

Metin dosyalarında encoding açıkça belirtilmelidir. Türkçe karakterler için `utf-8` varsayımı kod içinde görünür olmalıdır.

JSON, Python sözlük ve listeleriyle doğal biçimde eşleşir. Buna rağmen dışarıdan gelen veri her zaman doğrulanmalıdır. Bir alanın bulunması, türünün doğru olduğu anlamına gelmez.

CSV tablo verisi için uygundur ancak tür bilgisi taşımaz. Okunan her hücre başlangıçta metindir; sayı ve tarih dönüşümleri bilinçli yapılmalıdır.

## 3. Atomik yazma

Bir süreç dosyayı doğrudan hedef konuma yazarken yarıda kesilirse bozuk veya eksik dosya bırakabilir. Daha güvenli yaklaşım:

1. Aynı dizinde geçici dosya oluştur.
2. İçeriği tamamen yaz.
3. Gerekirse diske aktarımı tamamla.
4. Geçici dosyayı hedef dosyayla değiştir.

`Path.replace` aynı dosya sistemi içinde bu son adımı güvenli biçimde gerçekleştirir.

## 4. Modül ve paket

Bir `.py` dosyası modüldür. Birden fazla modülün anlamlı dizin altında toplanması paketi oluşturur. Paket sınırları teknik değil, kavramsal sorumluluklara göre çizilmelidir.

Örnek:

```text
data_toolkit/
├── __init__.py
├── models.py
├── storage.py
└── service.py
```

- `models.py`: veri modeli ve doğrulama
- `storage.py`: dosya erişimi
- `service.py`: iş akışı

Bu ayrım, tek sorumluluk ilkesini ve test edilebilirliği destekler.

## 5. Mutlak ve göreli import

Uygulama paketlerinde açık mutlak importlar genellikle daha okunabilirdir:

```python
from data_toolkit.models import Record
```

Göreli importlar aynı paket içindeki yakın modüllerde kullanılabilir, ancak derin `../../` benzeri yapılar tasarım kokusudur.

## 6. `pyproject.toml`

Modern Python projelerinde yapılandırmanın merkezi `pyproject.toml` dosyasıdır. Bu dosya şunları tanımlayabilir:

- build sistemi
- proje adı ve sürümü
- desteklenen Python sürümü
- çalışma zamanı bağımlılıkları
- geliştirme bağımlılıkları
- test, lint ve type-check ayarları

Bağımlılıklar doğrudan ve dolaylı olarak ayrılır. Kodun doğrudan import ettiği paket proje bağımlılığıdır; onun kendi bağımlılıklarını ayrıca elle listelemek gerekmez.

## 7. Sanal ortam

Sanal ortam, projeye ait Python yorumlayıcısı ve paket kurulum alanı sağlar. Projeler arası sürüm çakışmasını azaltır.

```bash
python -m venv .venv
python -m pip install -e .[dev]
```

`python -m pip` kullanımı, çağrılan `pip` komutunun etkin Python yorumlayıcısıyla eşleşmesini sağlar.

## 8. Sürüm aralıkları ve kilit dosyaları

Geniş sürüm aralıkları esneklik, tam sürüm sabitleme yeniden üretilebilirlik sağlar. Kütüphane geliştirirken uyumlu aralıklar; uygulama dağıtırken kilit dosyası tercih edilir.

Semantik sürümleme genel olarak `MAJOR.MINOR.PATCH` biçimindedir:

- MAJOR: geriye uyumsuz değişiklik
- MINOR: geriye uyumlu özellik
- PATCH: geriye uyumlu hata düzeltmesi

## 9. Yapılandırma ve sırlar

API anahtarları kaynak koda veya repoya yazılmaz. Ortam değişkenleri ya da secret manager kullanılır. `.env` dosyası yerel geliştirmede yardımcı olabilir, fakat `.gitignore` içinde tutulmalıdır.

## 10. Test stratejisi

Dosya testleri gerçek kullanıcı dizinlerine yazmamalıdır. `pytest` içindeki `tmp_path` fixture'ı her test için izole geçici dizin sağlar.

Test edilmesi gereken durumlar:

- dosya bulunamadığında davranış
- bozuk JSON
- yanlış alan türleri
- Unicode içerik
- üst dizinin otomatik oluşturulması
- yazma sonrası okuma eşitliği
- özet hesaplaması

## Kontrol listesi

- Yollar `Path` ile mi oluşturuluyor?
- Encoding açıkça belirtilmiş mi?
- Dış veri doğrulanıyor mu?
- Yazma işlemi yarıda kesilirse hedef korunuyor mu?
- İş mantığı dosya erişiminden ayrılmış mı?
- Bağımlılıklar `pyproject.toml` içinde tanımlı mı?
- Sırlar repodan uzak tutuluyor mu?
- Testler geçici dizin kullanıyor mu?