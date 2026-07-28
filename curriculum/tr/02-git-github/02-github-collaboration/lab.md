# Uygulama Laboratuvarı

## Senaryo

Bir AI tahmin servisinde `/health` endpoint'i için dokümantasyon ve test ekleyeceksin.

## 1. Issue hazırla

Başlık:

```text
feat: add health endpoint documentation and test
```

Kabul kriterleri:

- Endpoint davranışı README'de açıklanmalı.
- Başarılı yanıt testi eklenmeli.
- CI kontrolleri geçmeli.

## 2. Branch oluştur

```bash
git switch main
git pull --ff-only
git switch -c feat/health-endpoint-docs
```

## 3. Değişiklikleri ayrı commit'lere böl

```bash
git add README.md
git commit -m "docs: explain health endpoint"

git add tests/test_health.py
git commit -m "test: cover health endpoint"
```

## 4. Push et

```bash
git push -u origin feat/health-endpoint-docs
```

## 5. Draft pull request aç

PR açıklamasına şunları ekle:

- Değişikliğin amacı
- Uygulanan çözüm
- Test komutu ve sonucu
- Riskler
- İlgili issue: `Closes #<numara>`

## 6. Self-review yap

```bash
git diff origin/main...HEAD
git log --oneline origin/main..HEAD
```

Kontrol et:

- Debug çıktısı kaldı mı?
- Secret veya büyük dosya eklendi mi?
- Kapsam dışı değişiklik var mı?
- Testler değişikliği gerçekten doğruluyor mu?

## 7. Review geri bildirimini işle

Reviewer timeout davranışı için yeni test isterse değişikliği uygula:

```bash
git add tests/test_health.py
git commit -m "test: cover health timeout behavior"
git push
```

Geri bildirime kısa biçimde yanıt ver ve conversation'ı yalnızca çözüm gerçekten uygulandığında kapat.

## 8. Merge stratejisini seç

Bu küçük feature branch için squash merge kullan. Squash commit mesajı:

```text
feat: document and test health endpoint (#<PR>)
```

## 9. Temizlik

```bash
git switch main
git pull --ff-only
git branch -d feat/health-endpoint-docs
git fetch --prune
```

## 10. Release provası

Son değişiklik geriye uyumlu bir özellikse bir sonraki minor sürümü planla ve örnek release notu yaz:

```markdown
## Added
- Health endpoint documentation and automated coverage.
```