# Kurulum

## Gereksinimler

- Git
- Python 3.11 veya üzeri
- VS Code veya benzeri bir editör
- En az 8 GB RAM önerilir

GPU başlangıç için zorunlu değildir. Derin öğrenme ve LLM modüllerinde Google Colab veya bulut GPU kullanılabilir.

## Yerel kurulum

```bash
git clone <REPOSITORY_URL>
cd complete-ai-engineering-tr
python -m venv .venv
```

Aktivasyon:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.venv\\Scripts\\Activate.ps1
```

Bağımlılıklar ve test:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
make check
```
