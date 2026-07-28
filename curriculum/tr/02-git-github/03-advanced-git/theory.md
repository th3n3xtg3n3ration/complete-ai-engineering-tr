# İleri Git Teorisi

## 1. Commit graph

Git geçmişi doğrusal bir liste değil, commit düğümlerinden oluşan yönlendirilmiş çevrimsiz bir grafiktir. Her commit bir veya daha fazla parent commit'e işaret eder. Branch ise yalnızca belirli bir commit'i gösteren hareketli referanstır.

```bash
git log --graph --oneline --decorate --all
```

## 2. Rebase

Rebase, bir commit dizisinin tabanını değiştirir. Feature branch'i güncel `main` üzerine taşımak için:

```bash
git switch feature/model-evaluation
git fetch origin
git rebase origin/main
```

Rebase paylaşılan geçmişi yeniden yazar. Başkalarının kullandığı branch'lerde dikkatli olunmalıdır.

Çakışma durumunda:

```bash
git status
# dosyayı düzelt
git add <dosya>
git rebase --continue
```

Vazgeçmek için:

```bash
git rebase --abort
```

## 3. Interactive rebase

Son commit'leri yeniden sıralamak, birleştirmek veya mesajlarını düzeltmek için:

```bash
git rebase -i HEAD~5
```

Yaygın komutlar:

- `pick`: commit'i korur.
- `reword`: commit mesajını değiştirir.
- `squash`: commit'i önceki commit ile birleştirir.
- `fixup`: mesajı atmadan önceki commit ile birleştirir.
- `drop`: commit'i geçmişten çıkarır.

## 4. Cherry-pick

Başka bir branch'teki belirli commit'i mevcut branch'e uygular:

```bash
git cherry-pick <commit-sha>
```

Bir aralık için:

```bash
git cherry-pick A^..B
```

Cherry-pick commit'i taşımak yerine aynı değişiklikleri içeren yeni bir commit üretir.

## 5. Reflog

Reflog, `HEAD` ve branch referanslarının yerel hareket geçmişini tutar:

```bash
git reflog
```

Yanlış reset sonrası kurtarma:

```bash
git reset --hard HEAD~2
git reflog
git branch recovery/<name> <kayip-commit-sha>
```

Kurtarma branch'i oluşturmak, doğrudan reset atmaktan daha güvenli bir ilk adımdır.

## 6. Bisect

`git bisect`, hatayı oluşturan ilk commit'i ikili arama ile bulur:

```bash
git bisect start
git bisect bad
git bisect good <bilinen-iyi-sha>
```

Her adımda test çalıştırılır:

```bash
git bisect good
# veya
git bisect bad
```

Otomatik kullanım:

```bash
git bisect run python scripts/bisect_demo.py
```

İşlem sonunda:

```bash
git bisect reset
```

## 7. Force push güvenliği

Rebase sonrası uzak branch güncellenirken sıradan `--force` başkasının değişikliğini silebilir. Daha güvenli seçenek:

```bash
git push --force-with-lease
```

Bu komut, uzak branch beklenmedik biçimde değişmişse push'u reddeder.

## 8. Reset türleri

```bash
git reset --soft HEAD~1
git reset --mixed HEAD~1
git reset --hard HEAD~1
```

- `--soft`: commit'i geri alır; değişiklikler staged kalır.
- `--mixed`: commit ve staging'i geri alır; dosyalar working tree'de kalır.
- `--hard`: commit, staging ve working tree değişikliklerini siler.

Paylaşılan geçmişte `revert`, yerel ve yayımlanmamış geçmişte kontrollü `reset` tercih edilir.

## 9. AI projelerinde pratik yaklaşım

Kod, yapılandırma ve değerlendirme mantığı Git ile izlenebilir. Büyük veri kümeleri ve model ağırlıkları doğrudan normal Git geçmişine eklenmemelidir. Bunlar object storage, artifact registry, DVC veya Git LFS gibi çözümlerle yönetilmeli; commit içinde sürüm veya checksum referansı tutulmalıdır.
