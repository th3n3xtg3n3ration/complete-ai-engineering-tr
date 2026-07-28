# İlk GitHub Yayını

Bu paket yerel git deposu olarak hazırlanmıştır. GitHub'da `complete-ai-engineering-tr` adlı boş bir public repository oluşturduktan sonra:

```bash
git remote add origin https://github.com/<KULLANICI_ADI>/complete-ai-engineering-tr.git
git push -u origin main
```

SSH kullanıyorsanız:

```bash
git remote add origin git@github.com:<KULLANICI_ADI>/complete-ai-engineering-tr.git
git push -u origin main
```

Yayımdan sonra yapılacaklar:

1. Repository açıklamasını ekleyin.
2. Topics alanına `artificial-intelligence`, `machine-learning`, `deep-learning`, `llm`, `rag`, `agentic-ai`, `turkish`, `education` ekleyin.
3. GitHub Actions'ın çalıştığını doğrulayın.
4. Issue ve Discussions özelliklerini etkinleştirin.
5. `.github/ISSUE_TEMPLATE/config.yml` içindeki `OWNER` değerini kullanıcı adınızla değiştirin.
6. Private vulnerability reporting özelliğini etkinleştirin.
