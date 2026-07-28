# Ödev — Tekrar Üretilebilir Deney Repository'si

## Görev

Küçük bir makine öğrenmesi deneyi için Git repository oluştur. Repository en az şu dosyaları içermelidir:

```text
README.md
.gitignore
requirements.txt
src/train.py
src/evaluate.py
configs/baseline.json
tests/test_config.py
```

## Beklenen çalışma akışı

1. Repository'yi başlat ve ilk iskelet commit'ini oluştur.
2. `feature/training-script` branch'inde eğitim kodunu geliştir.
3. `feature/evaluation` branch'inde değerlendirme kodunu geliştir.
4. Değişiklikleri ayrı ve anlamlı commit'lerle kaydet.
5. README üzerinde kasıtlı conflict üret ve çöz.
6. Hatalı bir commit oluşturup `git revert` ile geri al.
7. Son geçmişi `git log --graph --oneline --all` ile raporla.
8. Secret, cache, sanal ortam, ham veri ve model ağırlıklarını izleme dışında bırak.

## Teslim

- Repository bağlantısı veya `git bundle`
- Commit geçmişinin ekran çıktısı
- Conflict çözümünü açıklayan kısa not
- Hangi dosyaların neden `.gitignore` içine alındığını açıklayan bölüm

## Rubrik — 100 puan

- Repository yapısı ve tekrar üretilebilirlik: 20
- Küçük ve anlamlı commit'ler: 20
- Branch çalışma akışı: 15
- Conflict çözümü: 15
- Güvenli geri alma: 10
- `.gitignore` ve secret hijyeni: 10
- Dokümantasyon kalitesi: 10
