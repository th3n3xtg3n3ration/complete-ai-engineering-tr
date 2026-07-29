# Quiz — Türev ve Otomatik Türev

1. Türevin geometrik anlamı nedir?
2. Merkezi fark neden ileri farktan genellikle daha doğrudur?
3. Çok küçük `h` neden sayısal hata oluşturabilir?
4. Gradient hangi yönü gösterir?
5. Directional derivative nasıl hesaplanır?
6. Zincir kuralı backpropagation ile nasıl ilişkilidir?
7. Aynı düğüm iki farklı yoldan kullanılırsa gradient neden toplanır?
8. Jacobian'ın boyutu nasıl belirlenir?
9. Hessian hangi bilgiyi taşır?
10. Pozitif definite Hessian neyi düşündürür?
11. Saddle point nasıl tanınabilir?
12. Gradient checking ne zaman kullanılır?
13. Relative error neden absolute error'dan daha güvenilir olabilir?
14. Reverse-mode autodiff hangi problem tipinde avantajlıdır?
15. Forward-mode autodiff hangi problem tipinde avantajlıdır?
16. ReLU'nun türevi negatif bölgede kaçtır?
17. Vanishing gradient ne demektir?
18. Exploding gradient nasıl teşhis edilir?
19. Tam Jacobian neden büyük modellerde pahalıdır?
20. Autodiff neden yalnızca sayısal türev değildir?

## Cevap anahtarı

1. Teğet eğimi/anlık değişim oranı.
2. Hata derecesi daha iyidir ve iki taraflı örnek kullanır.
3. Floating-point iptali ve yuvarlama nedeniyle.
4. En hızlı artış yönünü.
5. `gradient · unit_direction`.
6. Yerel türevlerin graph boyunca zincirlenmesidir.
7. Toplam türev tüm yolların katkısını içerir.
8. Çıktı boyutu × girdi boyutu.
9. İkinci türevleri ve yerel eğriliği.
10. Yerel minimum olasılığını.
11. Hessian özdeğerlerinin karışık işaretli olmasıyla.
12. Backward implementasyonunu doğrularken.
13. Değer ölçeğini dikkate alır.
14. Az çıktı, çok parametre olduğunda.
15. Az girdi, çok çıktı olduğunda.
16. `0`.
17. Gradient'ların çok küçülmesi.
18. Gradient normlarını izleyerek.
19. Boyutu ve bellek maliyeti çok büyür.
20. Operasyon graph'ında analitik türev kurallarını uygular.
