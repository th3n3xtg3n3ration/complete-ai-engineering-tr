# Katkıda Bulunma Rehberi

Katkılar; yazım düzeltmesi, hata raporu, yeni alıştırma, test, ders, proje, çeviri veya pedagojik inceleme biçiminde olabilir.

## Başlamadan önce

1. Mevcut issue ve pull request'leri kontrol edin.
2. Büyük bir ders veya mimari değişiklik için önce issue açın.
3. Bir dersin ön koşullarını ve hedef seviyesini belirleyin.
4. Telif hakkı bulunan içeriği izinsiz kopyalamayın.
5. Haricî kod, görsel ve veri setlerinin lisansını açıkça belirtin.

## Geliştirme ortamı

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -r requirements-dev.txt
ruff check .
pytest
python tools/curriculum-validator/validate_metadata.py
```

## Branch ve commit biçimi

```text
feat/python-variables-lesson
fix/broken-quiz-answer
content/transformer-analogy
chore/update-ci
```

Commit örnekleri:

```text
feat: add Python variables lesson
fix: correct attention matrix dimensions
content: improve Turkish gradient explanation
```

## Ders kalite kontrol listesi

Bir dersin `stable` olabilmesi için:

- [ ] Ön koşullar belirtilmiş
- [ ] Ölçülebilir öğrenme hedefleri yazılmış
- [ ] Sezgisel ve teknik anlatım mevcut
- [ ] Kod örnekleri çalışıyor
- [ ] En az bir alıştırma mevcut
- [ ] Ödev ve rubrik mevcut
- [ ] Ön/son quiz geçerli JSON
- [ ] Yaygın hatalar açıklanmış
- [ ] Kaynaklar ve lisanslar belirtilmiş
- [ ] Metadata doğrulamasından geçmiş
- [ ] Teknik inceleme yapılmış
- [ ] Hedef seviyeden bir öğrenciyle denenmiş

## Dil standardı

- Ana anlatım Türkçe
- İlk kullanımda Türkçe terim ve İngilizce karşılığı
- Kod değişkenleri, fonksiyonları ve sınıfları İngilizce
- Açıklayıcı ama gereksiz uzun olmayan yorumlar
- Cinsiyetçi, dışlayıcı veya küçümseyici dil kullanılmaz

## Kod standardı

- Python 3.11+
- Type hint kullanımı
- Küçük ve tek sorumluluklu fonksiyonlar
- Öğretici kodlarda açık isimler
- Kritik davranışlar için test
- Gizli anahtar veya kişisel veri commit edilmez

## Pull request içeriği

PR açıklaması şunları içermelidir:

- Ne değişti?
- Neden gerekliydi?
- Öğrenci veya katkıcıya etkisi nedir?
- Hangi kontroller çalıştırıldı?
- Görsel değişiklik varsa ekran görüntüsü
- Yeni ders varsa hedef seviye ve ön koşullar
