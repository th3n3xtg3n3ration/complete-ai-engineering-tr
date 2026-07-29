# Ödev — Mini Autodiff ve Gradient Doğrulama

## Görev

Saf Python ile reverse-mode otomatik türev motoru geliştir. Motor en az `+`, `-`, `*`, `/`, power, `exp`, `log`, `tanh` ve ReLU operasyonlarını desteklemeli.

## Gereksinimler

- Hesaplama graph'ı ve topological backward geçiş
- Paylaşılan düğümlerde doğru gradient birikimi
- Gradient sıfırlama politikası
- Domain doğrulaması ve anlaşılır hatalar
- Scalar linear regression loss örneği
- En az bir mini nöron örneği
- Merkezi fark tabanlı gradient checker
- Jacobian ve Hessian için sayısal yardımcılar
- En az 20 pytest testi
- Step-size ve relative error analizi
- Vanishing veya exploding gradient deneyi

## Teknik rapor

Rapor şu başlıkları içermeli:

1. Graph ve backward mimarisi
2. Zincir kuralının uygulanışı
3. Gradient birikimi
4. Sayısal türevde step-size seçimi
5. Gradient check sonuçları
6. Hessian ve eğrilik yorumu
7. Bilinen sınırlamalar

## Rubrik — 100 puan

- Matematiksel doğruluk: 25
- Autodiff motoru: 25
- Sayısal diferansiyasyon: 15
- Test kapsamı: 15
- Deney ve analiz: 10
- Kod kalitesi ve dokümantasyon: 10

## Başarı ölçütü

Gradient checker'ın tüm desteklenen operasyonlarda belirlenen tolerans içinde geçmesi ve testlerin tekrar üretilebilir olması gerekir.
