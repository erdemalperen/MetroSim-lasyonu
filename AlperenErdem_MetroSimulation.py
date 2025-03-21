import heapq
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional

class Istasyon:
    def __init__(self, ad: str):
        self.ad = ad
        self.komsular: List[Tuple[str, int]] = []  # (komşu istasyon, süre)

    def komsu_ekle(self, komsu: str, sure: int):
        self.komsular.append((komsu, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        # Kalabalık istasyonlar ve gecikme süreleri (dakika cinsinden)
        self.kalabalik_istasyonlar = {"Kizilay": 2, "Gar": 1}
        # Metro hatları ve renkleri
        self.hatlar = {
            "Kizilay-Ulus": "red",
            "Batıkent-Demetevler": "blue",
            "Gar-Keçiören": "green",
            "Sıhhiye-Kizilay": "purple"
        }

    def istasyon_ekle(self, ad: str):
        if ad not in self.istasyonlar:
            self.istasyonlar[ad] = Istasyon(ad)

    def baglanti_ekle(self, istasyon1: str, istasyon2: str, sure: int):
        self.istasyon_ekle(istasyon1)
        self.istasyon_ekle(istasyon2)
        self.istasyonlar[istasyon1].komsu_ekle(istasyon2, sure)
        self.istasyonlar[istasyon2].komsu_ekle(istasyon1, sure)

    def rota_suresi_hesapla(self, rota: List[str]) -> int:
        if not rota:
            return 0
        toplam_sure = 0
        for i in range(len(rota) - 1):
            istasyon1, istasyon2 = rota[i], rota[i + 1]
            for komsu, sure in self.istasyonlar[istasyon1].komsular:
                if komsu == istasyon2:
                    toplam_sure += sure
                    # Kalabalıklık kontrolü: Merkezi istasyonlarda ek süre
                    if istasyon1 in self.kalabalik_istasyonlar:
                        toplam_sure += self.kalabalik_istasyonlar[istasyon1]
                    break
        return toplam_sure

    def en_az_aktarma_bul(self, baslangic: str, bitis: str) -> Tuple[Optional[List[str]], Optional[int]]:
        if baslangic not in self.istasyonlar or bitis not in self.istasyonlar:
            return None, None

        ziyaret_edildi = set()
        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi.add(baslangic)

        while kuyruk:
            mevcut_istasyon, rota = kuyruk.popleft()
            if mevcut_istasyon == bitis:
                toplam_sure = self.rota_suresi_hesapla(rota)
                return rota, toplam_sure

            for komsu, _ in self.istasyonlar[mevcut_istasyon].komsular:
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu)
                    yeni_rota = rota + [komsu]
                    kuyruk.append((komsu, yeni_rota))

        return None, None

    def en_hizli_rota_bul(self, baslangic: str, bitis: str) -> Tuple[Optional[List[str]], Optional[int]]:
        if baslangic not in self.istasyonlar or bitis not in self.istasyonlar:
            return None, None

        kuyruk = [(0, baslangic, [baslangic])]
        maliyetler = {baslangic: 0}
        rotalar = {baslangic: [baslangic]}

        while kuyruk:
            toplam_sure, mevcut_istasyon, rota = heapq.heappop(kuyruk)
            if mevcut_istasyon == bitis:
                return rota, toplam_sure

            for komsu, sure in self.istasyonlar[mevcut_istasyon].komsular:
                yeni_sure = maliyetler[mevcut_istasyon] + sure
                if komsu not in maliyetler or yeni_sure < maliyetler[komsu]:
                    maliyetler[komsu] = yeni_sure
                    yeni_rota = rota + [komsu]
                    rotalar[komsu] = yeni_rota
                    heapq.heappush(kuyruk, (yeni_sure, komsu, yeni_rota))

        return None, None

    def metro_agi_gorsellestir(self):
        G = nx.Graph()
        renkler = []

        # Graf'a istasyonları ve bağlantıları ekleyelim
        for istasyon in self.istasyonlar:
            G.add_node(istasyon)
            for komsu, sure in self.istasyonlar[istasyon].komsular:
                G.add_edge(istasyon, komsu, weight=sure)

        # Renkleri belirleyelim
        for u, v in G.edges():
            renk = "black"
            for hat, renk_adi in self.hatlar.items():
                ist1, ist2 = hat.split("-")
                if (u == ist1 and v == ist2) or (u == ist2 and v == ist1):
                    renk = renk_adi
                    break
            renkler.append(renk)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10, edge_color=renkler)
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.title("Metro Ağı Haritası")
        plt.show()

    def rota_animasyonu(self, rota: List[str]):
        if not rota:
            print("Rota bulunamadı!")
            return

        G = nx.Graph()
        for istasyon in self.istasyonlar:
            G.add_node(istasyon)
            for komsu, sure in self.istasyonlar[istasyon].komsular:
                G.add_edge(istasyon, komsu)

        pos = nx.spring_layout(G)
        plt.ion()  # İnteraktif mod

        for i in range(len(rota)):
            plt.clf()
            nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10)
            path = rota[:i+1]
            path_edges = list(zip(path[:-1], path[1:]))
            nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="orange")
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="orange", width=2)
            plt.title(f"Rota: {' -> '.join(path)}")
            plt.pause(1)

        plt.ioff()
        plt.show()

    def kullanici_arayuzu(self):
        self.metro_agi_gorsellestir()
        while True:
            print("\nMetro Simülasyonu")
            print("1. En az aktarmalı rota bul")
            print("2. En hızlı rota bul")
            print("3. Çıkış")
            secim = input("Seçiminiz (1-3): ")

            if secim == "3":
                break

            baslangic = input("Başlangıç istasyonu: ")
            bitis = input("Bitiş istasyonu: ")

            if secim == "1":
                rota, sure = self.en_az_aktarma_bul(baslangic, bitis)
            elif secim == "2":
                rota, sure = self.en_hizli_rota_bul(baslangic, bitis)
            else:
                print("Geçersiz seçim!")
                continue

            if rota:
                print(f"Rota: {' -> '.join(rota)}")
                print(f"Toplam süre: {sure} dakika")
                self.rota_animasyonu(rota)
            else:
                print("Rota bulunamadı!")

def test_senaryolari():
    metro = MetroAgi()

    # Metro ağını oluştur
    metro.baglanti_ekle("ASTI", "Kizilay", 5)
    metro.baglanti_ekle("Kizilay", "Ulus", 4)
    metro.baglanti_ekle("Ulus", "Demetevler", 6)
    metro.baglanti_ekle("Demetevler", "OSB", 5)
    metro.baglanti_ekle("Batıkent", "Demetevler", 7)
    metro.baglanti_ekle("Demetevler", "Gar", 4)
    metro.baglanti_ekle("Gar", "Keçiören", 6)
    metro.baglanti_ekle("Gar", "Sıhhiye", 3)
    metro.baglanti_ekle("Sıhhiye", "Kizilay", 2)

    # Test senaryoları
    print("--- Test Senaryoları ---")
    print("1. ASTI'den OSB'ye (en az aktarmalı):")
    rota, sure = metro.en_az_aktarma_bul("ASTI", "OSB")
    print(f"En az aktarmalı rota: {' -> '.join(rota)}")
    print(f"Toplam süre: {sure} dakika")

    print("\n2. Batıkent'ten Keçiören'e (en az aktarmalı):")
    rota, sure = metro.en_az_aktarma_bul("Batıkent", "Keçiören")
    print(f"En az aktarmalı rota: {' -> '.join(rota)}")
    print(f"Toplam süre: {sure} dakika")

    print("\n3. Keçiören'den ASTI'ye (en hızlı):")
    rota, sure = metro.en_hizli_rota_bul("Keçiören", "ASTI")
    print(f"En hızlı rota: {' -> '.join(rota)}")
    print(f"Toplam süre: {sure} dakika")

    # Kullanıcı arayüzünü başlat
    metro.kullanici_arayuzu()

if __name__ == "__main__":
    test_senaryolari()