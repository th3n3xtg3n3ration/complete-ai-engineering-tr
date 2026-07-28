# Quiz

1. GitHub Flow'un temel amacı nedir?
2. Draft pull request ne zaman açılmalıdır?
3. İyi bir pull request neden tek bir amaca odaklanmalıdır?
4. Blocking review yorumu ne anlama gelir?
5. Squash merge hangi durumda avantajlıdır?
6. Rebase merge'in önemli yan etkisi nedir?
7. Branch protection neden kullanılır?
8. CODEOWNERS tek başına erişim kontrolü sağlar mı?
9. `Closes #42` ifadesi ne işe yarar?
10. Bir secret commit edildiyse yalnızca commit'i silmek neden yeterli değildir?

## Cevap anahtarı

1. Kısa ömürlü branch ve PR tabanlı güvenli, sürekli iş birliği sağlamaktır.
2. Değişiklik yönü görünür olduğunda, tamamlanmasını beklemeden açılabilir.
3. Review yükünü, risk alanını ve geri alma maliyetini azaltır.
4. Merge öncesinde çözülmesi gereken bir sorun olduğunu belirtir.
5. Feature branch'teki ara commit'lerin ana branch tarihçesine taşınması istenmediğinde.
6. Commit SHA'larını değiştirir.
7. Kritik branch'lere doğrudan veya doğrulanmamış değişiklik girişini engellemek için.
8. Hayır; branch protection ve repository izinleriyle birlikte kullanılmalıdır.
9. PR merge edildiğinde ilgili issue'nun otomatik kapanmasını sağlar.
10. Secret Git tarihçesinde veya loglarda kalmış olabilir; iptal edilip yenilenmelidir.