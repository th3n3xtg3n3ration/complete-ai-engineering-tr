# Kavram Haritası

## 1. Yapay zekâ en geniş şemsiyedir

**Yapay zekâ (artificial intelligence)**; algılama, tahmin, karar verme, planlama veya içerik üretme gibi görevleri gerçekleştiren sistemlerin genel alanıdır.

## 2. Makine öğrenmesi, AI'ın bir alt alanıdır

**Makine öğrenmesi (machine learning)**, bütün karar kurallarını geliştiricinin yazması yerine modelin örüntüleri veriden öğrenmesini sağlar.

```text
Girdi verisi + doğru örnekler → eğitim algoritması → model
Model + yeni girdi → tahmin
```

## 3. Derin öğrenme, makine öğrenmesinin bir yaklaşımıdır

**Derin öğrenme (deep learning)**, çok katmanlı yapay sinir ağlarını kullanır. Görüntü, ses ve metin gibi yüksek boyutlu verilerde güçlüdür.

## 4. Attention ve Transformer

**Attention**, modelin bir dizinin farklı parçaları arasındaki ilişkiye değişken önem vermesini sağlar.

**Transformer**, attention mekanizmasını merkezine alan bir sinir ağı mimarisidir. BERT, GPT ve T5 gibi model aileleri Transformer tabanlıdır.

## 5. Büyük dil modelleri

**Büyük dil modeli (large language model, LLM)**, büyük metin koleksiyonlarında token dizilerini öğrenir. Temel eğitim hedefi çoğu zaman sıradaki tokenı tahmin etmektir. Bu basit hedef, yeterli veri ve ölçekle özetleme, soru-cevap, kodlama ve metin üretme gibi davranışlar sağlayabilir.

## 6. Üretken yapay zekâ

**Üretken yapay zekâ (generative AI)** yeni metin, görsel, ses, video veya kod üreten sistemlerin genel adıdır. Her üretken model LLM değildir; görsel diffusion modelleri buna örnektir.

## 7. RAG

**Retrieval-augmented generation (RAG)**, kullanıcının sorusuyla ilgili belgeleri getirir ve bu bilgileri üretim sırasında modele bağlam olarak verir.

```text
Soru
 → arama sorgusu
 → ilgili parçaların getirilmesi
 → LLM'e soru + kaynaklar
 → kaynaklara dayalı cevap
```

RAG, modelin parametrelerini değiştirmez. Bilgiyi dış kaynaktan çalışma anında getirir.

## 8. Agentic AI

**Agentic AI**, bir hedefe ulaşmak için yalnızca cevap üretmeyen; durum izleyen, karar veren, araç kullanan ve çok adımlı iş yürüten sistemleri ifade eder.

```text
Hedef
 → durumu incele
 → sonraki eylemi seç
 → araç kullan
 → sonucu gözlemle
 → gerekirse planı güncelle
 → tamamla veya insan onayı iste
```

Güvenilir bir ajan yalnızca “zeki prompt” değildir. Şema doğrulama, yetkilendirme, timeout, retry, adım sınırı, maliyet bütçesi, loglama, evaluation ve insan onayı gibi klasik yazılım bileşenlerine ihtiyaç duyar.

## 9. Birlikte nasıl kullanılırlar?

Örnek bir şirket asistanı:

- Klasik yazılım: kullanıcı girişi ve yetkilendirme
- RAG: şirket belgelerini arama
- LLM: soruyu anlama ve cevap yazma
- Agent workflow: SQL aracı veya rapor aracını seçme
- Güvenlik: hassas veriyi filtreleme ve onay isteme
- Evaluation: cevabın doğru kaynaklara dayanıp dayanmadığını ölçme
