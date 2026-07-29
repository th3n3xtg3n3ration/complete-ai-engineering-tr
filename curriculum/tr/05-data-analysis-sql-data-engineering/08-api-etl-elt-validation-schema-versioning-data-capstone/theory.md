# Teori — Güvenilir API Kaynağından Sürümlü Veri Ürününe

## 1. Veri hattının gerçek amacı

Bir veri hattı yalnızca veriyi A noktasından B noktasına taşımaz. Üretim kalitesinde bir pipeline şu sorulara cevap vermelidir:

- Veri nereden geldi?
- Hangi anda ve hangi kurallarla işlendi?
- Hangi kayıtlar reddedildi, neden reddedildi?
- Aynı girdi yeniden işlendiğinde aynı çıktı üretilebilir mi?
- Bir çıktı bozulduğunda hangi girdilerden türediği bulunabilir mi?
- Şema değiştiğinde tüketiciler etkilenir mi?

Bu nedenle capstone'un merkezinde **tekrarlanabilirlik, gözlemlenebilirlik, idempotency ve veri sözleşmesi** vardır.

## 2. API extraction güvenilirliği

### 2.1 Timeout

Timeout bulunmayan bir istek sonsuza kadar bekleyebilir. Bağlantı ve okuma süreleri iş yüküne göre sınırlandırılmalıdır. Timeout hatası genellikle retry edilebilir; ancak retry sayısı sınırsız olmamalıdır.

### 2.2 Retry ve exponential backoff

`429`, `500`, `502`, `503` ve `504` gibi geçici durumlarda tekrar deneme anlamlıdır. Her denemeyi aynı anda yapmak kaynak sistemi daha fazla zorlar. Exponential backoff gecikmeyi yaklaşık olarak şöyle büyütür:

```text
base_delay × 2^(attempt - 1)
```

Dağıtık sistemlerde aynı anda retry yapan istemcilerin senkronize olmasını azaltmak için jitter eklenebilir. Sunucu `Retry-After` veriyorsa istemci bu değeri tercih etmelidir.

### 2.3 Pagination

API'ler tek yanıtta bütün veriyi döndürmez. Yaygın modeller:

- Offset/limit
- Sayfa numarası
- Cursor
- `next` URL

Cursor pagination değişen veri setlerinde offset'e göre daha kararlı olabilir. İstemci cursor döngülerini ve maksimum sayfa sayısını kontrol etmelidir.

### 2.4 Idempotent extraction

Aynı kaynağın aynı anlık görüntüsü tekrar alındığında gereksiz kopya üretmemek için içerik checksum'ı kullanılabilir. Ham veri asla sessizce güncellenmemeli; yeni snapshot ayrı bir artefakt olarak saklanmalıdır.

## 3. ETL ve ELT

### ETL

1. Extract
2. Transform
3. Load

Dönüşüm hedef sisteme yüklemeden önce yapılır. Hedef sistemin kapasitesi sınırlıysa veya hassas verinin yüklenmeden önce maskelenmesi gerekiyorsa avantajlıdır.

### ELT

1. Extract
2. Load
3. Transform

Ham veri önce warehouse veya lake'e yüklenir, dönüşüm hedef sistemde yapılır. Büyük ölçekli analitik platformlarda yeniden işleme ve farklı tüketiciler için esneklik sağlar.

Gerçek sistemler hibrit olabilir. Bu derste ham snapshot'lar bronze katmanına yüklenir; temel doğrulama ve normalizasyon silver katmanını, SQL analitiği ise gold katmanını oluşturur.

## 4. Bronze, silver ve gold katmanları

### Bronze

- Kaynak yanıtına en yakın biçim
- Değiştirilemez snapshot
- Fetch zamanı, kaynak adı ve şema sürümü
- SHA-256 checksum

### Silver

- Tipleri normalleştirilmiş kayıtlar
- Veri sözleşmesini geçen satırlar
- Tekil primary key
- UTC tarih-saat biçimi
- Bilinen kategori değerleri

### Gold

- İş veya modelleme için hazır veri ürünü
- Açık grain
- SQL ile üretilmiş özellikler
- Tüketiciye yönelik stabil şema

Katmanlar teknik isimlerden fazlasıdır; sorumluluk sınırı oluşturur.

## 5. Veri sözleşmesi

Bir veri sözleşmesi üretici ile tüketici arasındaki makine tarafından kontrol edilebilir anlaşmadır. Tipik kurallar:

- Alan adı ve tipi
- Zorunlu veya opsiyonel olma
- Null kabulü
- Minimum ve maksimum değer
- Enum değerleri
- Regex pattern
- Primary key
- Unknown field politikası
- Sözleşme sürümü

Şema yalnızca kolon listesinden ibaret değildir. `amount >= 0`, `status ∈ {paid, cancelled, refunded}` ve `customer_id` tekilliği de sözleşmenin parçasıdır.

## 6. Şema evrimi ve uyumluluk

Uyumlu değişiklik örnekleri:

- Opsiyonel ve nullable yeni alan eklemek
- Enum'a yeni değer eklemek, tüketicinin unknown değerleri desteklemesi koşuluyla
- Açıklama ve metadata güncellemek

Kırıcı değişiklik örnekleri:

- Alan silmek
- Tip değiştirmek
- Opsiyonel alanı zorunlu yapmak
- Nullable alanı non-nullable yapmak
- Primary key değiştirmek
- Enum değerini kaldırmak

Semantic versioning yaklaşımında:

- Patch: doğrulama davranışını değiştirmeyen düzeltme
- Minor: geriye uyumlu ekleme
- Major: kırıcı değişiklik

Her sözleşmenin canonical JSON gösteriminden fingerprint üretmek, pipeline çalıştırmalarını doğru sözleşmeyle ilişkilendirir.

## 7. Doğrulama ve quarantine

İki temel hata politikası vardır:

### Fail-fast

Kritik sistemik hata varsa pipeline durur. Örnek: kaynak kimlik doğrulaması başarısız, warehouse erişilemiyor, sözleşme dosyası okunamıyor.

### Record-level quarantine

Tekil bozuk kayıtlar ayrılır; geçerli kayıtlar işlemeye devam eder. Quarantine kaydı şunları içermelidir:

- Dataset version
- Entity adı
- Kaynak kayıt indeksi veya kimliği
- Ham kayıt
- Alan, hata kodu ve mesaj

Quarantine sessiz veri kaybı değildir. Reddedilen oran için alarm ve düzeltme süreci gerekir.

## 8. Idempotent load ve upsert

Pipeline tekrar çalıştırıldığında aynı iş sonucunu iki kez üretmemelidir. Idempotency için:

- Deterministik dataset version
- Primary key
- `INSERT ... ON CONFLICT DO UPDATE`
- Güncelleme zamanı karşılaştırması
- Tekil run kaydı
- Content-addressed artefakt yolları

`updated_at` kontrolü, geç gelen eski verinin daha yeni kaydı ezmesini engeller. Bununla birlikte kaynak zaman damgasına güvenilip güvenilemeyeceği ayrıca değerlendirilmelidir.

## 9. Incremental load ve watermark

Büyük tabloların tamamını her seferinde okumak pahalıdır. Watermark son başarıyla işlenen zamanı veya artan kimliği tutar. Yeni çalıştırma:

```text
updated_at > previous_watermark
```

koşuluyla veri alabilir. Dikkat edilmesi gerekenler:

- Geç gelen kayıtlar
- Saat farkı ve UTC normalizasyonu
- Kaynak güncelleme zamanının değişebilirliği
- Watermark'ın yalnızca başarılı run sonunda ilerletilmesi
- Küçük overlap penceresiyle yeniden okuma

Bu dersteki upsert mantığı incremental tasarımın temelini gösterir.

## 10. Lineage, manifest ve dataset version

### Lineage

Bir gold tablonun hangi silver ve bronze artefaktlarından üretildiğini gösterir.

### Manifest

Bir çalıştırmanın makine tarafından okunabilir özetidir:

- Dataset version
- Run zamanı
- Pipeline version
- Input checksum
- Contract fingerprint
- Satır sayıları
- Reddedilen kayıt sayısı
- Artefakt yolları, boyutları ve checksum'ları
- Katmanlar arası lineage

### Dataset version

Bu derste sürüm şu bileşenlerden türetilir:

```text
hash(input checksum + contract fingerprint + pipeline version)
```

Böylece veri, sözleşme veya kod sürümü değiştiğinde yeni bir dataset version üretilir.

## 11. Artefakt bütünlüğü

SHA-256 checksum, dosyanın daha sonra değişip değişmediğini denetler. Manifest doğrulaması:

1. Dosya mevcut mu?
2. Boyut beklenenle uyumlu mu?
3. Yeniden hesaplanan checksum manifestteki değere eşit mi?

Checksum erişim kontrolünün yerini tutmaz; bütünlük kontrolü sağlar.

## 12. Warehouse ve veri ürünü grain'i

Capstone warehouse'unda:

- `customers`: müşteri başına bir satır
- `orders`: sipariş başına bir satır
- `customer_features`: müşteri başına bir satır
- `rejected_records`: run, entity ve kayıt indeksi başına bir satır
- `pipeline_runs`: dataset version başına bir satır

Her tablo için grain açık değilse JOIN çoğalması ve yanlış aggregation riski yükselir.

## 13. Gözlemlenebilirlik

Üretim pipeline'ında en az şu metrikler izlenmelidir:

- Run süresi
- API sayfa ve retry sayısı
- Extract edilen kayıt sayısı
- Geçerli ve reddedilen kayıt sayısı
- Reddedilme oranı ve hata kodları
- Upsert edilen satır sayısı
- Gold çıktı satır sayısı
- Watermark gecikmesi
- Artefakt boyutu
- Son başarılı run zamanı

Log, metric ve lineage birlikte kullanıldığında hata ayıklama kolaylaşır.

## 14. Güvenlik

- API anahtarını kaynak koda yazma.
- Secret manager veya ortam değişkeni kullan.
- Loglarda token ve kişisel veri gösterme.
- TLS doğrulamasını kapatma.
- Ham katmana erişimi sınırla.
- Hassas alanları maskele veya şifrele.
- Minimum yetki prensibini uygula.
- Veri saklama ve silme politikasını tanımla.

## 15. Capstone mimarisi

```text
API / JSON
   │
   ▼
ApiClient: timeout + retry + pagination
   │
   ▼
Bronze: immutable JSON snapshot + checksum
   │
   ▼
DataContract: type + rule + PK validation
   ├── invalid ──► quarantine
   │
   ▼
Silver: normalized JSONL
   │
   ▼
SQLite warehouse: idempotent upsert
   │
   ▼
SQL feature transformation
   │
   ▼
Gold: customer_features.csv
   │
   ▼
Manifest: version + lineage + checksums + counts
```

Bu mimari küçük ölçekte SQLite ile uygulanır; aynı ilkeler object storage, orchestrator, lakehouse ve dağıtık warehouse sistemlerine taşınabilir.
