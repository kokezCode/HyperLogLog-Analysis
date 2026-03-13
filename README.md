# HyperLogLog (HLL) Kardinalite Tahmini ve Performans Analizi

Bu proje, büyük veri setlerinde eşsiz öğe sayısını (kardinalite) tahmin etmek için kullanılan **HyperLogLog** algoritmasının Python implementasyonunu ve teknik analizini içermektedir. 

##  Genel Bakış
HyperLogLog, bellek verimliliği odaklı olasılıksal bir veri yapısıdır. [cite_start]Geleneksel yöntemler (HashSet vb.) eşsiz öğeleri saymak için $O(N)$ bellek gerektirirken, HLL algoritması $O(\log \log N)$ bellek karmaşıklığı ile çalışır[cite: 36, 37]. [cite_start]Bu sayede milyarlarca benzersiz veriyi sadece birkaç kilobayt bellek kullanarak yaklaşık %1-2 hata payı ile tahmin edebilir[cite: 41, 42].

##  Teknik Bileşenler
Algoritmanın başarısını sağlayan temel bileşenler şunlardır:

* [cite_start]**Hashing:** Verilerin 64-bitlik bir uzaya düzgün dağılımı (uniform distribution) için **MurmurHash3 (mmh3)** kullanılmıştır[cite: 45, 49].
* [cite_start]**Kovalama (Bucketing):** Hash değerinin ilk $p$ biti kullanılarak veri $m = 2^p$ alt kümeye bölünür, bu da hata varyansını azaltır[cite: 53, 54].
* [cite_start]**Harmonik Ortalama:** Uç değerlerin (outliers) tahmini bozmasını engellemek amacıyla register değerlerinin harmonik ortalaması alınır[cite: 69].
* [cite_start]**Linear Counting:** Küçük veri setlerindeki ($2.5 \times m$) yanlılığı gidermek için düşük kardinalite düzeltmesi uygulanır[cite: 78, 80].
* [cite_start]**Merge Özelliği:** Dağıtık sistemlerde kullanılabilmesi için iki farklı HLL yapısının kayıpsız birleştirilmesini destekler[cite: 89, 91].

##  Analiz ve Simülasyon Sonuçları
Proje kapsamında, 100.000 eşsiz öğe içeren bir veri seti üzerinden farklı hassasiyet ($p$) değerleri test edilmiştir. [cite_start]Sonuçlar, teorik hata sınırı olan $1.04/\sqrt{m}$ formülü ile kıyaslanmıştır[cite: 96, 132].

### Performans Tablosu
| Hassasiyet (p) | Kova Sayısı (m) | Tahmin Edilen | Gerçek Hata (%) | Teorik Hata (%) |
| :--- | :--- | :--- | :--- | :--- |
| 4 | 16 | 102.119 | %2.12 | %26.00 |
| 8 | 256 | 98.616 | %1.38 | %6.50 |
| 12 | 4.096 | 102.208 | %2.21 | %1.62 |
| 16 | 65.536 | 100.802 | %0.80 | %0.41 |

### Hata Analizi Grafiği
Aşağıdaki grafikte, kova sayısı arttıkça deneysel hatanın teorik limitlere nasıl yakınsadığı görülmektedir:

![Hata Analizi Grafiği](hata.analizi.png)


-------------------------------------

