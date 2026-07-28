# Quiz — OOP ve Tasarım İlkeleri

1. Encapsulation'ın temel amacı nedir?
2. Composition ile inheritance arasındaki temel fark nedir?
3. `@dataclass(frozen=True)` ne sağlar?
4. `Protocol` hangi tür polymorphism'i kolaylaştırır?
5. Single Responsibility Principle ne söyler?
6. Dependency injection test edilebilirliği neden artırır?
7. Liskov Substitution Principle hangi problemi önler?
8. Open/Closed Principle nasıl uygulanabilir?
9. Büyük arayüzlerin bölünmesini öneren ilke hangisidir?
10. Domain kuralını CLI katmanına yazmak neden sakıncalıdır?

## Cevap anahtarı

1. İç durumu kontrollü bir arayüz arkasında korumak.
2. Inheritance bir `is-a`, composition bir `has-a` ilişkisi kurar.
3. Alan atamasını engelleyerek immutable'a yakın bir değer nesnesi üretir.
4. Yapısal polymorphism.
5. Bir sınıfın tek değişim nedeni olması gerektiğini.
6. Sahte bağımlılıkların kolayca verilebilmesini sağlar.
7. Alt türlerin üst türün davranış sözleşmesini bozmasını.
8. Soyutlama ve yeni gerçekleştirimler ekleyerek.
9. Interface Segregation Principle.
10. Katmanları sıkı bağlar ve birim testi zorlaştırır.
