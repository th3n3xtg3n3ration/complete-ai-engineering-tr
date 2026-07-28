# Teori — Git Temelleri

## 1. Git neyi çözer?

Git, dosyaların zaman içindeki değişimini kaydeden dağıtık bir sürüm kontrol sistemidir. Her geliştirici repository geçmişinin yerel bir kopyasına sahiptir. Bu sayede çevrimdışı commit oluşturulabilir, branch açılabilir ve geçmiş incelenebilir.

## 2. Dört temel alan

- **Working tree:** Üzerinde çalıştığın dosyalar.
- **Staging area:** Bir sonraki commit'e girecek seçilmiş değişiklikler.
- **Local repository:** Commit geçmişinin yerel kopyası.
- **Remote repository:** Takımla paylaşılan uzak repository.

Temel akış:

```bash
git status
git add src/model.py
git commit -m "feat(model): add baseline classifier"
git push origin feature/baseline-model
```

## 3. İyi commit tasarımı

İyi bir commit tek bir mantıksal değişikliği temsil eder. Kod, ilgisiz biçimlendirme ve dokümantasyon değişikliklerini aynı commit'e doldurmak incelemeyi zorlaştırır.

Örnek mesajlar:

```text
feat(data): add CSV validation
fix(train): prevent division by zero
refactor(eval): extract metric calculation
docs(readme): document local setup
```

Commit mesajı yapılan değişikliği ve amacını açıkça anlatmalıdır.

## 4. Branch kullanımı

Branch, bağımsız bir çalışma hattıdır.

```bash
git switch -c feature/data-validation
```

Değişiklik tamamlandığında hedef branch ile birleştirilir:

```bash
git switch main
git merge feature/data-validation
```

## 5. Merge conflict

Aynı satırlar farklı branch'lerde değiştirildiğinde Git otomatik karar veremez. Dosyada conflict işaretleri oluşur:

```text
<<<<<<< HEAD
current branch content
=======
incoming branch content
>>>>>>> feature/example
```

Doğru içerik elle seçilir, işaretler silinir ve çözüm commit edilir.

```bash
git add conflicted_file.py
git commit
```

## 6. Remote çalışma akışı

```bash
git remote -v
git fetch origin
git pull --ff-only origin main
git push -u origin feature/data-validation
```

`fetch`, uzaktaki değişiklikleri indirir fakat çalışma branch'ini değiştirmez. `pull`, indirme ve birleştirme işlemlerini birlikte yürütür. Ekiplerde beklenmeyen merge commit'lerini önlemek için `--ff-only` yararlıdır.

## 7. Değişiklikleri geri alma

### Çalışma alanındaki değişikliği bırakmak

```bash
git restore path/to/file.py
```

### Stage alanından çıkarmak

```bash
git restore --staged path/to/file.py
```

### Paylaşılmış commit'i güvenli biçimde tersine çevirmek

```bash
git revert <commit-sha>
```

### Yerel geçmişi taşımak

```bash
git reset --soft HEAD~1
```

`reset`, paylaşılmış branch'lerde dikkatli kullanılmalıdır. `--hard` seçeneği çalışma alanını da değiştirdiği için veri kaybına yol açabilir.

## 8. `.gitignore` ve güvenlik

Aşağıdakiler genellikle commit edilmemelidir:

```gitignore
.venv/
__pycache__/
*.pyc
.env
.ipynb_checkpoints/
data/raw/
models/*.bin
```

API anahtarı veya parola commit edildiyse yalnızca dosyayı silmek yeterli değildir. Secret derhal iptal edilmeli, yenisi oluşturulmalı ve gerekirse geçmiş temizlenmelidir.

## 9. AI projelerinde repository hijyeni

- Büyük veri ve model dosyalarını doğrudan Git'e koyma.
- Deney çıktıları için izleme sistemi veya artifact storage kullan.
- Kod, yapılandırma ve dokümantasyonu sürümle.
- Rastgelelik kaynaklarını ve bağımlılık sürümlerini kaydet.
- Her deney için tekrar üretilebilir komutlar sağla.
