# Quiz

1. Unit test ile integration test arasındaki temel fark nedir?
2. Fixture hangi problemi çözer?
3. Parametrization ne zaman tercih edilir?
4. Mock kullanımında aşırıya kaçmak neden zararlıdır?
5. Regression testi nedir?
6. `cProfile` ile `timeit` hangi farklı sorulara cevap verir?
7. Cumulative time neyi gösterir?
8. `WARNING` ve `ERROR` seviyeleri nasıl ayrılır?
9. Loglarda neden ham kullanıcı verisi tutulmamalıdır?
10. Bir production hatası düzeltildikten sonra hangi test eklenmelidir?

## Cevap anahtarı

1. Unit test tek birimi izole eder; integration test bileşenlerin birlikte çalışmasını doğrular.
2. Tekrarlanan test kurulumunu ve temizliğini merkezileştirir.
3. Aynı davranış çok sayıda girdiyle sınanırken.
4. Testleri iç implementasyona bağlar ve refactor sırasında gereksiz kırılma üretir.
5. Daha önce görülen bir hatanın geri dönmediğini doğrulayan testtir.
6. `timeit` küçük süre ölçümleri, `cProfile` çağrı bazlı darboğaz analizi yapar.
7. Fonksiyonun kendi süresiyle alt çağrılarının toplam süresini.
8. Warning riskli fakat devam eden; error başarısız işlemdir.
9. Gizlilik, güvenlik ve mevzuat riskleri nedeniyle.
10. Hatanın senaryosunu yeniden üreten regression testi.
