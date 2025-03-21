# MetroSim-lasyonu
Bu proje bir metro ağında iki istasyon arasında **en az aktarmalı** ve **en hızlı** rotayı bulan bir simülasyon uygulamasıdır. Proje Akbank Python ile Yapay Zekaya Giriş Bootcamp kapsamında geliştirilmiştir.

## Kullanılan Teknolojiler ve Kütüphaneler
- Python 3: Projenin ana programlama dili.
- collections.deque**: BFS algoritması için kuyruk yapısı.
- heapq: A* algoritması için öncelik kuyruğu.
- networkx: Metro ağını graf olarak modellemek ve görselleştirmek için.
- matplotlib: Metro ağını ve rotaları görselleştirmek için.

## Algoritmaların Çalışma Mantığı
BFS (En Az Aktarmalı Rota)
- Çalışma Mantığı**: BFS, graf üzerinde en kısa yolu (aktarma sayısına göre) bulur. Bir kuyruk yapısı kullanarak her seviyede tüm komşu istasyonları ziyaret eder.
- Neden Kullanıldı?**: Aktarma sayısı, graf üzerindeki kenar sayısına denk gelir. BFS, bu tür problemlerde en kısa yolu garanti eder.

 A* (En Hızlı Rota)
- Çalışma Mantığı: A*, toplam süreyi (dakika) minimize ederek en hızlı rotayı bulur. Öncelik kuyruğu kullanarak her adımda en düşük maliyetli yolu seçer.
- **Neden Kullanıldı?**: A*, hem gerçek maliyeti hem de tahmini maliyeti dikkate alarak hızlı bir şekilde en iyi rotayı bulur.

## Örnek Kullanım ve Test Sonuçları
Proje, aşağıdaki test senaryolarını başarıyla geçmiştir:
1. ASTI → OSB (en az aktarmalı)**: ASTI → Kizilay → Ulus → Demetevler → OSB (25 dakika)
2. Batıkent → Keçiören (en az aktarmalı)**: Batıkent → Demetevler → Gar → Keçiören (21 dakika)
3. Keçiören → ASTI (en hızlı)**: Keçiören → Gar → Sıhhiye → Kizilay → ASTI (19 dakika)

## Ek Özellikler
- Metro Ağı Görselleştirme**: Metro ağı, renkli hatlarla görselleştirilir.
- Rota Animasyonu**: Bulunan rota, adım adım animasyonla gösterilir.
- Kalabalıklık ve Gecikme**: Merkezi istasyonlarda (örneğin, Kızılay) kalabalıklık nedeniyle ek süreler eklenmiştir.
- Kullanıcı Arayüzü**: Kullanıcı, başlangıç ve bitiş istasyonlarını interaktif olarak girebilir.

## Projeyi Geliştirme Fikirleri
- Gerçek bir şehir metrosu için daha büyük bir ağ eklenebilir.
- Hava durumu veya bakım çalışmaları gibi dinamik faktörler eklenebilir.
- Mobil uygulama arayüzü geliştirilerek daha geniş bir kitleye hitap edebilir.
![image](https://github.com/user-attachments/assets/28d55233-4e4c-422a-ab8e-977dfec7e6a9)
