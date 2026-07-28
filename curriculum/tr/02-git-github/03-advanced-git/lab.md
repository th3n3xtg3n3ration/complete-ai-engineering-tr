# Uygulama Laboratuvarı

## Hazırlık

```bash
mkdir advanced-git-lab
cd advanced-git-lab
git init
git config user.name "AI Engineer"
git config user.email "ai@example.com"
```

## Görev 1 — Dağınık geçmiş oluştur

Bir `train.py` dosyası oluştur ve art arda küçük değişiklikler yap:

```bash
git add train.py
git commit -m "feat: add training entrypoint"
# typo düzelt
git commit -am "fix typo"
# log ekle
git commit -am "temp"
```

Ardından geçmişi düzenle:

```bash
git rebase -i HEAD~3
```

Commit mesajlarını anlamlı hale getir ve düzeltme commit'lerini squash et.

## Görev 2 — Cherry-pick

```bash
git switch -c hotfix/metric
# metric düzeltmesini yap
git add .
git commit -m "fix: correct F1 metric calculation"
HOTFIX_SHA=$(git rev-parse HEAD)
git switch main
git cherry-pick "$HOTFIX_SHA"
```

## Görev 3 — Reflog ile kurtarma

```bash
git switch -c experiment/recovery
# iki commit oluştur
git reset --hard HEAD~2
git reflog
```

Reflog'daki kayıp commit SHA'sından kurtarma branch'i oluştur:

```bash
git branch recovery/experiment <sha>
```

## Görev 4 — Bisect

En az sekiz commit oluştur. İlk commit'lerde `score()` doğru sonuç versin; ortadaki bir commit'te regresyon ekle. İyi ve kötü commit'leri belirleyip:

```bash
git bisect start
git bisect bad <bad-sha>
git bisect good <good-sha>
git bisect run python scripts/bisect_demo.py
git bisect reset
```

## Görev 5 — Güvenli force push analizi

Aşağıdaki iki komutun ekip ortamındaki farkını açıklayan kısa bir not yaz:

```bash
git push --force
git push --force-with-lease
```

## Teslim kontrolü

```bash
git log --graph --oneline --decorate --all
git status
```

Repository temiz olmalı; kurtarma branch'i ve bisect sonucu raporda belgelenmelidir.
