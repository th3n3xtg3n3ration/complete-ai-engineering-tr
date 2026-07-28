# Ayrıntılı Teori

## Klasik programlama ile makine öğrenmesi arasındaki fark

Klasik programlamada geliştirici kuralları doğrudan yazar:

```text
Kurallar + veri → sonuç
```

Makine öğrenmesinde eğitim süreci örneklerden kurallara benzeyen parametreleri çıkarır:

```text
Veri + beklenen sonuçlar → öğrenme algoritması → model
Model + yeni veri → tahmin
```

Kurallar açık, kararlı ve denetlenebilir olduğunda klasik yazılım çoğu zaman daha iyi seçimdir. Örneğin iki sayının vergi oranıyla çarpılması için makine öğrenmesine gerek yoktur.

## Makine öğrenmesi türleri

### Denetimli öğrenme

Girdilerle birlikte doğru hedefler bulunur. Ev fiyatı tahmini ve spam sınıflandırma örnek verilebilir.

### Denetimsiz öğrenme

Doğru cevap etiketi verilmez. Model grupları, sıkışık temsilleri veya olağan dışı örnekleri bulmaya çalışır.

### Pekiştirmeli öğrenme

Ajan bir ortamda eylem yapar ve ödül sinyaliyle uzun vadeli davranış öğrenir.

## Derin öğrenme neden ortaya çıktı?

Klasik ML yöntemlerinde özellikleri çoğu zaman insan tasarlar. Derin ağlar, yeterli veri ve hesaplama olduğunda ham veya daha az işlenmiş girdilerden katmanlı temsiller öğrenebilir.

Örneğin görüntü sınıflandırmada ilk katmanlar kenarları, orta katmanlar dokuları ve daha ileri katmanlar nesne parçalarını temsil edebilir. Bu açıklama sezgiseldir; gerçek ağ temsilleri her zaman bu kadar temiz ayrılmaz.

## Transformer'ın temel fikri

Bir cümledeki her token, diğer tokenlarla ilişkisini attention üzerinden değerlendirebilir. Böylece model, yalnızca yakın komşulara veya sırayla işlenen gizli duruma bağımlı kalmadan bağlamsal ilişkiler kurabilir.

Transformer bloğunda genel olarak:

- Token embedding
- Positional information
- Multi-head self-attention
- Residual connection
- Normalization
- Feed-forward network bulunur.

## LLM neyi bilir?

Bir LLM'nin bilgisi üç kaynaktan gelebilir:

1. Ön eğitim sırasında parametrelerine sıkışan örüntüler
2. Kullanıcı ve sistem mesajlarındaki bağlam
3. RAG veya araçlar yoluyla çalışma anında getirilen bilgi

Modelin akıcı konuşması, söylediğinin doğru olduğunu garanti etmez. Bu nedenle kaynaklandırma, retrieval, doğrulama ve evaluation gereklidir.

## RAG mı fine-tuning mi?

RAG genellikle güncel, sık değişen veya kullanıcıya özel bilginin dış kaynaktan getirilmesi için kullanılır. Fine-tuning ise davranış, biçim, görev kalıbı veya alan uyarlaması için yararlı olabilir.

Basit karar ilkesi:

- “Model hangi bilgiyi kullanmalı?” → önce RAG düşün.
- “Model nasıl davranmalı veya hangi biçimde cevap vermeli?” → fine-tuning değerlendir.

Bu ayrım mutlak değildir; gelişmiş sistemlerde ikisi birlikte kullanılabilir.

## Ajan ne zaman gereksizdir?

Tek bir API çağrısı, sabit adımlı workflow veya basit retrieval işlemi problemi çözüyorsa serbest karar veren bir ajan eklemek gereksiz karmaşıklık yaratabilir.

Ajan, özellikle şu durumlarda anlamlıdır:

- Hangi aracın kullanılacağı girdiye göre değişiyorsa
- Görev birden fazla gözlem ve eylem gerektiriyorsa
- Ara sonuçlara göre plan güncelleniyorsa
- Başarısızlıkta alternatif yol denenmesi gerekiyorsa

Ancak yüksek riskli işlemlerde deterministik workflow ve insan onayı çoğu zaman daha güvenlidir.

## Sistem düşüncesi

Gerçek AI ürününün yalnızca küçük bir bölümü modeldir. Geri kalan sistem:

- Veri hattı
- API
- Veritabanı
- Kimlik doğrulama
- Yetkilendirme
- İzleme
- Güvenlik
- Test
- Maliyet kontrolü
- İnsan deneyiminden oluşur.

Bu eğitim, modeli sistemden ayrı değil, bu bileşenlerle birlikte öğretir.
