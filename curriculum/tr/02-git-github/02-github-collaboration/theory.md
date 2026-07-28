# GitHub İş Birliği Teorisi

## 1. GitHub Flow

GitHub Flow kısa ömürlü branch'lere dayanan basit bir iş akışıdır:

1. Bir issue veya görev seç.
2. Açıklayıcı bir branch oluştur.
3. Küçük ve anlamlı commit'ler yap.
4. Erken aşamada draft pull request aç.
5. Otomatik kontrolleri ve code review sürecini tamamla.
6. Onaydan sonra merge et.
7. Branch'i sil ve ilgili issue'yu kapat.

Örnek branch adları:

```text
feat/add-model-endpoint
fix/tokenizer-padding
chore/update-dependencies
```

## 2. İyi bir issue

İyi bir issue; problemi, beklenen sonucu ve kabul kriterlerini açıklar. Çözümü gereğinden fazla dayatmamalıdır.

Önerilen yapı:

- Bağlam
- Problem
- Beklenen davranış
- Kabul kriterleri
- Teknik notlar
- İlgili bağlantılar

## 3. İncelenebilir pull request

İyi bir pull request:

- Tek bir amacı vardır.
- Gereksiz refactor içermez.
- Ne değiştiğini ve neden değiştiğini açıklar.
- Test kanıtı sunar.
- Riskleri ve geri alma planını belirtir.
- İlgili issue'yu bağlar.

Büyük değişiklikleri küçük PR'lara bölmek review kalitesini artırır ve geri alma maliyetini azaltır.

## 4. Code review

Code review yalnızca hata arama işlemi değildir. Bilgi paylaşımı, tasarım doğrulaması ve sürdürülebilirlik kontrolüdür.

Yorum türleri:

- **blocking:** Merge öncesi düzeltilmesi gerekir.
- **suggestion:** İyileştirme önerisidir.
- **question:** Tasarım kararını anlamaya yöneliktir.
- **nit:** Küçük ve zorunlu olmayan düzeltmedir.

İyi yorum örneği:

> `timeout` değeri sabit olduğu için yavaş ortamlarda kararsız test oluşabilir. Bunu fixture üzerinden yapılandırılabilir hale getirmeyi düşünür müsün?

Kişiye değil koda odaklan. Gerekçe ver ve mümkün olduğunda uygulanabilir öneri sun.

## 5. Merge stratejileri

### Merge commit

Branch tarihçesini korur ve ayrı bir merge commit üretir. Uzun ömürlü veya tarihçesi önemli branch'lerde faydalıdır.

### Squash merge

PR içindeki commit'leri tek commit haline getirir. Küçük feature branch'leri ve temiz ana branch tarihçesi için uygundur.

### Rebase merge

Commit'leri hedef branch üzerine doğrusal biçimde taşır. Temiz tarihçe sağlar fakat commit SHA'ları değişir.

Takım, stratejiyi repository seviyesinde standartlaştırmalıdır.

## 6. Branch protection

`main` gibi kritik branch'lerde önerilen kurallar:

- Pull request olmadan doğrudan push'u engelle.
- En az bir onay iste.
- Eski onayları yeni commit geldiğinde geçersiz kıl.
- Zorunlu CI kontrollerini tanımla.
- Conversation'ların çözülmesini zorunlu tut.
- Gerekirse imzalı commit veya linear history iste.

## 7. CODEOWNERS

CODEOWNERS belirli dosya ve dizinler için otomatik reviewer atar.

```text
* @platform-team
/models/ @ml-team
/security/ @security-team
```

CODEOWNERS tek başına yetkilendirme değildir; branch protection ile birlikte kullanılmalıdır.

## 8. Issue, milestone ve project yönetimi

- **Label:** Tür, öncelik veya alan bilgisini gösterir.
- **Milestone:** Bir sürüm veya teslim tarihine bağlı işleri gruplar.
- **Project:** İş akışını görünür hale getirir.

Basit durumlar: Backlog, Ready, In Progress, Review, Done.

## 9. Release ve tag

Semantic Versioning temel biçimi:

```text
MAJOR.MINOR.PATCH
```

- MAJOR: Geriye uyumsuz değişiklik
- MINOR: Geriye uyumlu yeni özellik
- PATCH: Geriye uyumlu hata düzeltmesi

Annotated tag örneği:

```bash
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0
```

Release notları kullanıcı açısından anlamlı değişiklikleri, migration adımlarını ve bilinen sorunları içermelidir.

## 10. Güvenlik

- Secret içeren commit'i yalnızca silmek yeterli değildir; secret'ı iptal edip yenile.
- Fork'lardan gelen workflow'larda yazma yetkilerini sınırla.
- Bağımlılık güncellemelerini otomasyon ve review ile yönet.
- Üçüncü taraf GitHub Action'larını mümkünse commit SHA ile sabitle.
- Hassas ortamlarda gerekli onay mekanizmalarını kullan.