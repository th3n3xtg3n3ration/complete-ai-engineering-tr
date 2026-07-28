# İleri Python Quiz

Her soru 1 puandır.

1. Generator ile normal fonksiyon arasındaki temel fark nedir?
2. `yield` kullanıldığında fonksiyonun dönüş değeri hangi tür davranışı kazanır?
3. `functools.wraps` neden kullanılır?
4. Context manager hangi iki yaşam döngüsü aşamasını yönetir?
5. `dataclass(frozen=True)` ne sağlar?
6. Type hint'ler Python tarafından çalışma zamanında zorunlu tutulur mu?
7. Özel exception sınıfı tanımlamanın yararı nedir?
8. Comprehension hangi durumda okunabilirliği azaltabilir?
9. Saf fonksiyonun iki temel özelliğini yaz.
10. `Iterable` ile `Iterator` arasındaki fark nedir?

## Cevap anahtarı

1. Generator sonuçları tembel ve sırayla üretir; normal fonksiyon genellikle sonucu tek seferde döndürür.
2. Fonksiyon bir generator nesnesi üretir ve yürütme durumu çağrılar arasında korunur.
3. Sarılan fonksiyonun adı ve docstring gibi metadata'sını korur.
4. Kaynağın edinilmesi ve güvenli biçimde serbest bırakılması.
5. Alanların oluşturma sonrasında değiştirilmesini engeller.
6. Hayır; statik analiz ve araç desteği sağlar.
7. Hata türünü ve çözüm bağlamını açık hale getirir.
8. İç içe koşul ve dönüşümler fazla olduğunda.
9. Aynı girdiye aynı çıktıyı verir ve gözlenebilir yan etki üretmez.
10. Iterable üzerinde dolaşılabilir; iterator ayrıca sıradaki elemanı `__next__` ile üretir.
