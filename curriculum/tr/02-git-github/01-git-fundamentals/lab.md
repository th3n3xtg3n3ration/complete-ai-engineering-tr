# Laboratuvar — Branch Tabanlı Git Akışı

## Senaryo

Bir sınıflandırma projesine veri doğrulama özelliği ekleyeceksin.

## 1. Repository oluştur

```bash
mkdir git-lab
cd git-lab
git init
git branch -M main
```

## 2. İlk dosyaları ekle

```bash
mkdir -p src tests
printf "def validate(rows):\n    return bool(rows)\n" > src/validation.py
printf "# Git Lab\n" > README.md
printf ".venv/\n__pycache__/\n.env\n" > .gitignore

git add README.md .gitignore src/validation.py
git commit -m "feat: initialize validation project"
```

## 3. Feature branch aç

```bash
git switch -c feature/strict-validation
```

`src/validation.py` dosyasını şu hale getir:

```python
from collections.abc import Sequence


def validate(rows: Sequence[dict[str, object]]) -> bool:
    return bool(rows) and all("label" in row for row in rows)
```

```bash
git add src/validation.py
git commit -m "feat(validation): require label field"
```

## 4. Conflict üret

Feature branch'teyken README'ye kurulum açıklaması ekle ve commit et. Ardından `main` branch'ine dönüp aynı satırı farklı biçimde değiştir.

```bash
git switch main
# README.md dosyasını farklı biçimde düzenle
git add README.md
git commit -m "docs: update project description"
git merge feature/strict-validation
```

Conflict oluşursa işaretleri temizle, iki değişikliği anlamlı biçimde birleştir ve çözümü tamamla:

```bash
git add README.md
git commit -m "merge: resolve README conflict"
```

## 5. Geçmişi incele

```bash
git log --oneline --graph --decorate --all
git show --stat HEAD
git diff HEAD~1..HEAD
```

## 6. Güvenli geri alma

Yeni bir commit oluştur, ardından onu `revert` ile tersine çevir:

```bash
git revert <commit-sha>
```

Son durumda geçmiş korunmalı ve tersine çevirme ayrı bir commit olarak görünmelidir.

## Başarı ölçütleri

- `main` ve feature branch geçmişi anlaşılır olmalı.
- En az dört anlamlı commit bulunmalı.
- Conflict işaretleri hiçbir dosyada kalmamalı.
- `.env`, sanal ortam ve cache dosyaları izlenmemeli.
- `git status` temiz sonuç vermeli.
