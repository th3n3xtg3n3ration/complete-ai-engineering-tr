# Teori — Algoritmik Düşünme, Big-O ve Temel Veri Yapıları

## 1. Algoritmik düşünme

Bir problemi kodlamadan önce dört parçaya ayır:

1. Girdi nedir?
2. Beklenen çıktı nedir?
3. Kısıtlar nelerdir?
4. Hangi kenar durumları vardır?

Örneğin bir tahmin API'sine gelen istekleri sıraya almak istiyorsan maksimum kuyruk uzunluğu, işlem sırası, taşma davranışı ve iptal senaryoları önceden tanımlanmalıdır.

## 2. Zaman ve alan karmaşıklığı

Big-O, girdi boyutu büyürken algoritmanın maliyetinin nasıl arttığını ifade eder. Sabit katsayıları ve düşük dereceli terimleri göz ardı ederek büyüme hızına odaklanır.

- `O(1)`: dictionary anahtar erişimi gibi sabit zamanlı işlemler
- `O(log n)`: her adımda arama uzayını küçülten binary search
- `O(n)`: bütün kayıtları bir kez dolaşma
- `O(n log n)`: verimli karşılaştırmalı sıralama algoritmaları
- `O(n²)`: iç içe iki tam tarama

Big-O tek başına gerçek çalışma süresini söylemez. Veri boyutu, sabit maliyetler, bellek erişimi ve kullanılan dil de önemlidir.

## 3. Amortized analysis

Python listesine `append` çoğu zaman `O(1)` maliyetlidir. Kapasite dolduğunda daha büyük bir alan ayrılır ve elemanlar taşınır; bu tek işlem pahalı olsa da çok sayıda ekleme boyunca ortalama maliyet `O(1)` kabul edilir.

## 4. Temel veri yapıları

### Dynamic array / Python list

- Index erişimi: `O(1)`
- Sona ekleme: amortized `O(1)`
- Baştan ekleme veya silme: `O(n)`
- Üyelik araması: `O(n)`

### Stack

LIFO davranışı gösterir. Geri alma, expression evaluation, DFS ve çağrı yığını senaryolarında kullanılır.

### Queue

FIFO davranışı gösterir. İş kuyruğu, mesaj işleme ve breadth-first search için uygundur. Python'da baştan silme yapan list yerine `collections.deque` kullanılmalıdır.

### Hash table

Python `dict` ve `set`, ortalama durumda ekleme, silme ve arama için `O(1)` sağlar. Collision yönetimi ve hash fonksiyonunun kalitesi performansı etkiler.

### Linked list

Düğümler değer ve sonraki düğüm referansını tutar. Baştan ekleme `O(1)` olsa da index erişimi `O(n)` maliyetlidir. Python uygulamalarında çoğu zaman list veya deque daha pratiktir; linked list temel pointer mantığını öğrenmek için değerlidir.

## 5. Time-space trade-off

Daha fazla bellek kullanarak zamanı azaltabilirsin. Örneğin tekrar eden kullanıcı kimliklerini her sorguda listede aramak yerine bir `set` içinde saklamak aramayı ortalama `O(1)` seviyesine indirir, fakat ek bellek tüketir.

## 6. AI mühendisliği bağlantıları

- Batch oluşturma: queue/deque
- Token veya embedding cache: hash table
- Beam search ve graph traversal: queue/priority queue
- Agent geri alma geçmişi: stack
- Streaming pencereleri: deque
- Büyük veri üzerinde kötü bir `O(n²)` çözümden kaçınma: karmaşıklık analizi

Doğru veri yapısı seçimi yalnızca kod kalitesini değil, model servisinin gecikmesini ve altyapı maliyetini de doğrudan etkiler.
