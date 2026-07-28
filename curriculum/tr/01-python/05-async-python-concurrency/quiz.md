# Quiz

1. Coroutine nedir ve normal fonksiyondan farkı nedir?
2. `await` çalıştığında kontrol nereye geçer?
3. `create_task` ile doğrudan `await` arasındaki fark nedir?
4. `gather` hangi problem için kullanılır?
5. Semaphore neden gereklidir?
6. Queue'da backpressure nasıl oluşturulur?
7. Cancellation neden yutulmamalıdır?
8. Async yaklaşım neden CPU-bound işlerde tek başına hız sağlamaz?
9. Retry hangi hata türlerinde uygulanmalıdır?
10. Thread ve process hangi durumlarda tercih edilir?

## Cevap anahtarı

1. Event loop tarafından yürütülebilen, askıya alınabilir fonksiyon akışıdır.
2. Event loop başka hazır görevleri ilerletir.
3. `await` mevcut akışı bekletir; task işi planlayarak eşzamanlı ilerlemeye izin verir.
4. Birden fazla awaitable sonucunu birlikte beklemek için.
5. Sınırsız eşzamanlılığın kaynakları tüketmesini engellemek için.
6. `Queue(maxsize=n)` ile üretici kuyruk dolduğunda bekletilir.
7. Üst katmanın durdurma isteğinin doğru yayılması gerekir.
8. Event loop gerçek CPU paralelliği sağlamaz; CPU-bound iş event loop'u bloke eder.
9. Timeout ve geçici bağlantı hataları gibi geçici sorunlarda.
10. Thread bloklayan I/O için, process CPU-bound paralellik için tercih edilir.
