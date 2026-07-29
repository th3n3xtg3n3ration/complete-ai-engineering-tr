# Teori — Veri Temizleme, Encoding ve Veri Sızıntısı

## 1. Temiz veri ne demektir?

Temiz veri, yalnızca `NaN` içermeyen veri değildir. Bir veri ürününün güvenilirliği en az şu boyutlarla değerlendirilir:

- **Completeness:** Gerekli alanlar dolu mu?
- **Validity:** Değerler izin verilen aralık ve formatta mı?
- **Consistency:** Aynı kavram farklı kaynaklarda aynı biçimde mi temsil ediliyor?
- **Uniqueness:** İş anahtarları beklenen kardinaliteyi koruyor mu?
- **Timeliness:** Veri karar anında erişilebilir ve güncel mi?
- **Lineage:** Değerin hangi kaynaktan ve hangi dönüşümlerden geldiği biliniyor mu?

Bu boyutlardan biri bozulduğunda model performansı kadar raporlama, izlenebilirlik ve operasyonel kararlar da etkilenir.

## 2. Eksik değer mekanizmaları

### MCAR

Eksiklik başka hiçbir gözlenen veya gözlenmeyen değişkenle ilişkili değildir. Gerçek sistemlerde güçlü bir varsayımdır.

### MAR

Eksiklik, gözlenen başka değişkenlerle açıklanabilir. Örneğin gelir bilgisinin eksikliği yaş grubuna göre değişebilir.

### MNAR

Eksiklik, eksik olan değerin kendisiyle veya gözlenmeyen süreçlerle ilişkilidir. Yüksek gelirlilerin gelir bilgisini paylaşmaması klasik örnektir.

İmputation yöntemi seçmeden önce eksiklik mekanizması, iş süreci ve karar maliyeti birlikte değerlendirilmelidir.

## 3. Eksik değer stratejileri

- Satır veya kolon silme
- Sabit değer ile doldurma
- Mean/median/mode imputation
- Grup bazlı imputation
- Model tabanlı imputation
- Eksiklik göstergesi üretme
- Eksikliği ayrı bir kategori olarak koruma

Median, çarpık sayısal dağılımlarda mean'e göre daha dayanıklıdır. Ancak hiçbir imputation yöntemi kayıp bilgiyi geri getirmez; yalnızca açık bir varsayım altında kullanılabilir bir temsil üretir.

## 4. Aykırı değer

Aykırı değer üç farklı anlam taşıyabilir:

1. Ölçüm veya giriş hatası
2. Geçerli fakat nadir gözlem
3. Veri üretim sürecindeki değişim

Her aykırı değer silinmemelidir. Kredi dolandırıcılığı, arıza ve güvenlik problemlerinde nadir gözlemler sinyalin kendisi olabilir.

### IQR yöntemi

`IQR = Q3 - Q1`

Alt ve üst sınırlar:

`Q1 - k × IQR`, `Q3 + k × IQR`

Yaygın `k` değeri 1.5'tir. Bu eşik dağılımın iş anlamını tek başına temsil etmez.

### Robust z-score

Median ve median absolute deviation kullanır. Mean ve standart sapmaya göre uç değerlerden daha az etkilenir.

## 5. Aykırı değer müdahaleleri

- İş kuralına göre reddetme
- Kaynak sistemde düzeltme
- Clipping veya winsorization
- Log/Box-Cox benzeri dönüşüm
- Robust scaler
- Ayrı özellik veya segment üretme
- Hiç müdahale etmeyip robust model kullanma

Müdahale kararı sadece istatistiksel eşiğe değil, veri üretim sürecine dayanmalıdır.

## 6. Kategorik encoding

### One-hot encoding

Nominal kategoriler için yorumlanabilir bir temsildir. Yüksek kardinalitede geniş ve seyrek matris üretir.

### Ordinal encoding

Yalnızca kategoriler arasında gerçek bir sıralama varsa kullanılmalıdır. Rastgele sayısal kodlar modele yapay mesafe dayatabilir.

### Rare-category grouping

Az görülen kategorileri `__OTHER__` altında toplamak boyutu ve varyansı azaltır. Eşik yalnızca eğitim verisinde belirlenmelidir.

### Bilinmeyen kategori

Üretimde eğitimde görülmeyen değerler normaldir. Pipeline açık bir `__OTHER__` politikası uygulamalı, hata veya sessiz kolon kayması üretmemelidir.

## 7. Fit ve transform ayrımı

Aşağıdakiler eğitim verisinde öğrenilir:

- Median ve mean
- Quantile ve IQR sınırları
- Kategori sözlüğü
- Scaling parametreleri
- Feature selection kararları

Validation ve test verisi bu istatistikleri değiştirmeden yalnızca `transform` edilir. Aksi durumda evaluation bilgisi eğitim sürecine sızar.

## 8. Veri sızıntısı türleri

### Target leakage

Feature, hedefin doğrudan veya dolaylı kopyasıdır. Örneğin kredi temerrüdünü tahmin ederken tahsilat sonucu feature olarak kullanmak.

### Temporal leakage

Tahmin anından sonra oluşan bilgi modele verilir. Rastgele split, zaman bağımlı problemlerde geleceği geçmişe taşıyabilir.

### Entity leakage

Aynı müşteri, hasta, cihaz veya dokümanın çok benzer kayıtları train ve validation'a dağılır. Model genelleme yerine kimlik ezberler.

### Preprocessing leakage

İmputation, scaling, encoding veya feature selection tüm veri üzerinde fit edilir.

### Aggregation leakage

Bir satır için oluşturulan geçmiş özet, yanlışlıkla o satırın geleceğini veya hedefini de içerir.

## 9. Leakage denetim kontrol listesi

- Feature tahmin anında gerçekten mevcut mu?
- Feature adı hedef veya sonuca ilişkin şüpheli bir anlam taşıyor mu?
- Aynı row ID iki split'te bulunuyor mu?
- Aynı entity farklı split'lerde bulunmalı mı?
- Zaman kesiminden sonra oluşan kayıt train'e girmiş mi?
- Fit edilen tüm preprocessing nesneleri yalnızca train verisini gördü mü?
- Aggregation penceresi tahmin zamanında kapanıyor mu?
- Validation metrikleri olağandışı derecede yüksek mi?

## 10. Üretim ilkeleri

Temizleme pipeline'ı:

- Deterministik olmalı
- Girdiyi yerinde değiştirmemeli
- Öğrenilen istatistikleri saklamalı
- Bilinmeyen kategoriyi açıkça yönetmeli
- Şema ve aralık hatalarında anlaşılır mesaj vermeli
- Train/evaluation ayrımını testlerle korumalı
- Veri kalitesi ve leakage raporu üretmeli
