# Alıştırmalar — Fonksiyonlar, Logaritmalar ve Grafikler

## Seviye 1 — Temel kavramlar

1. `f(x) = 3x - 7` için:
   - eğimi ve y ekseni kesişimini yaz,
   - `f(-2)`, `f(0)` ve `f(5)` değerlerini hesapla,
   - `f(x) = 8` denklemini çöz.

2. `g(x) = x² - 4x + 3` fonksiyonunun:
   - sıfır noktalarını,
   - `g(0)` değerini,
   - simetri eksenini bul.

3. Aşağıdaki ifadeleri hesapla:
   - `log₂(64)`
   - `log₁₀(0.001)`
   - `ln(e⁵)`
   - `2^(log₂(7))`

4. Logaritma kurallarını kullanarak sadeleştir:
   - `log(xy)`
   - `log(x³ / y)`
   - `2log(a) + log(b)`

5. Aşağıdaki fonksiyonların domain'ini yaz:
   - `1 / (x - 2)`
   - `log(x + 4)`
   - `sqrt(3 - x)`
   - `log(1 - x²)`

## Seviye 2 — Kodlama

6. `quadratic(x, a, b, c)` fonksiyonunu yaz. Tüm girdilerin sonlu gerçek sayı olduğunu doğrula.

7. Bir fonksiyonu `[start, stop]` aralığında örnekleyen `sample_points` fonksiyonunu yaz. `step <= 0` ve ters aralık durumlarında açık exception üret.

8. `safe_log_probability(p, epsilon=1e-12)` fonksiyonunu yaz. Olasılığı güvenli aralığa kırp ve `-log(p)` döndür.

9. Naive sigmoid ile kararlı sigmoid implementasyonlarını `[-1000, -100, 0, 100, 1000]` girdilerinde karşılaştır.

10. `temperature_softmax(logits, temperature)` fonksiyonunu geliştir. Aşağıdaki özellikleri test et:
    - toplam 1 olmalı,
    - tüm değerler pozitif olmalı,
    - düşük sıcaklık daha keskin dağılım üretmeli,
    - `temperature <= 0` reddedilmeli.

11. Merkezi fark ve ileri fark ile sayısal türev yaz. `x²`, `sin(x)` ve `exp(x)` üzerinde hata oranlarını karşılaştır.

12. Bir doğrunun iki noktadan eğimini hesaplayan fonksiyon yaz. Dikey doğru durumunda özel exception üret.

## Seviye 3 — AI bağlantıları

13. Sigmoid için `x = -8` ile `x = 8` arasında çıktı ve sayısal eğim tablosu üret. En büyük eğimin hangi noktada olduğunu programatik olarak bul.

14. ReLU, leaky ReLU ve softplus fonksiyonlarını aynı aralıkta örnekle. Negatif bölgede çıktı ve eğim farklarını raporla.

15. Aşağıdaki ikili sınıflandırma modellerini BCE ile karşılaştır:

```text
Targets:          [1, 0, 1, 1, 0]
Model A:          [0.9, 0.2, 0.8, 0.7, 0.1]
Model B:          [0.6, 0.4, 0.55, 0.51, 0.45]
Model C:          [0.1, 0.9, 0.2, 0.3, 0.8]
```

Her model için doğruluk da hesapla. Aynı doğruluğa sahip modellerin loss değerleri neden farklı olabilir?

16. Üç sınıflı bir problem için logits değerlerini softmax'a dönüştür. Tüm logits değerlerine aynı sabiti ekleyerek sonucun değişmediğini testle.

17. One-hot hedef ve softmax olasılıkları için categorical cross-entropy hesapla. Doğru sınıf olasılığını kademeli olarak artır ve loss eğrisini üret.

18. `f(x) = sigmoid(2x - 1)` bileşkesini kodla. `x = 0.5` noktasındaki sayısal türevi bul ve bileşke davranışını yorumla.

## Seviye 4 — Tasarım ve analiz

19. Fonksiyon kütüphanesindeki tüm public fonksiyonlar için şu sözleşmeyi yaz:
    - kabul edilen girdiler,
    - çıktı tipi,
    - domain kısıtları,
    - üretilebilecek exception'lar,
    - sayısal kararlılık notları.

20. `NaN`, `inf`, boş vektör, uzunluk uyuşmazlığı ve geçersiz olasılık girdileri için parametrized pytest tablosu hazırla.

21. Binary cross-entropy'yi doğrudan olasılıktan hesaplamak yerine logit üzerinden kararlı biçimde hesaplayan `binary_cross_entropy_with_logits` fonksiyonunu araştır ve uygula. Formülü teknik notla açıkla.

22. Log-sum-exp fonksiyonunu kararlı biçimde uygula:

```text
log(sum(exp(values)))
```

Naive sürümle aşırı girdilerde karşılaştır.

23. Fonksiyon örnekleme aracına JSON Lines çıktı formatı ekle. CSV ve JSONL writer'ları aynı veri üretim katmanını paylaşmalı.

24. Deney aracına şu kalite kontrollerini ekle:
    - çıktı dosyasını atomik yazma,
    - mevcut dosyayı yanlışlıkla ezmeme seçeneği,
    - parametreleri rapora kaydetme,
    - satır sayısını doğrulama.

## Challenge

25. Tek değişkenli bir fonksiyon grafiğini harici paket kullanmadan ASCII olarak çizen küçük bir araç geliştir. Araç:

- x ve y aralıklarını kabul etmeli,
- eksenleri göstermeli,
- sigmoid, tanh ve ReLU için çalışmalı,
- terminal genişliğine göre ölçeklenmeli,
- domain hatalarını açıklayıcı mesajla raporlamalı.
