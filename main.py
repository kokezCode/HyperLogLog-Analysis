import mmh3
import numpy as np
import matplotlib.pyplot as plt

class HyperLogLog:
    def __init__(self, p):
        """
        HyperLogLog cardinality estimation algorithm.
        :param p: Precision parameter (number of bits for bucket index).
        """
        self.p = p
        self.m = 1 << p
        self.registers = np.zeros(self.m, dtype=int)

    def _hash(self, item):
        # 64-bit unsigned hash üretir
        hash_value = mmh3.hash64(item, signed=False)[0]
        return hash_value

    def _get_bucket_index(self, hash_value):
        # İlk p biti kova indeksi olarak kullanır
        return hash_value >> (64 - self.p)

    def _get_rho(self, hash_value):
        # Geri kalan bitlerdeki ilk 1'in konumunu bulur
        remaining_bits = hash_value & ((1 << (64 - self.p)) - 1)
        binary_str = bin(remaining_bits)[2:].zfill(64 - self.p)
        first_one = binary_str.find('1')
        if first_one == -1:
            return 64 - self.p + 1
        return first_one + 1

    def add(self, item):
        hash_value = self._hash(item)
        bucket_index = self._get_bucket_index(hash_value)
        rho = self._get_rho(hash_value)
        # Sadece daha büyük bir rho değeri gelirse güncelle (Max değer tutma)
        self.registers[bucket_index] = max(self.registers[bucket_index], rho)

    def count(self):
        # Harmonik Ortalama hesaplama
        Z = sum(2.0 ** -reg for reg in self.registers)
        alpha_m = 0.7213 / (1 + 1.079 / self.m)
        raw_estimate = alpha_m * self.m ** 2 / Z

        # Küçük veri seti düzeltmesi (Linear Counting)
        if raw_estimate <= 2.5 * self.m:
            V = np.count_nonzero(self.registers == 0)
            if V > 0:
                return self.m * np.log(self.m / V)
        return raw_estimate

    def merge(self, other):
        if self.p != other.p:
            raise ValueError("HLL nesnelerinin p degerleri eslesmiyor.")
        self.registers = np.maximum(self.registers, other.registers)

def simulate_hll():
    true_cardinality = 100000
    p_values = range(4, 17)
    errors = []
    theoretical_errors = []

    print("\n--- HyperLogLog Simulasyon Analizi Basladi ---")
    print(f"{'p':<5} | {'Kova (m)':<10} | {'Tahmin Edilen':<15} | {'Hata (%)':<10} | {'Teorik Hata (%)':<15}")
    print("-" * 65)

    for p in p_values:
        hll = HyperLogLog(p)
        for i in range(true_cardinality):
            hll.add(str(i))

        estimated_cardinality = hll.count()
        m = 1 << p
        
        actual_error = abs(estimated_cardinality - true_cardinality) / true_cardinality
        theoretical_error = 1.04 / (m ** 0.5)
        
        errors.append(actual_error)
        theoretical_errors.append(theoretical_error)

        print(f"{p:<5} | {m:<10} | {int(estimated_cardinality):<15} | {actual_error*100:>8.2f}% | {theoretical_error*100:>13.2f}%")

    # Grafik Çizimi
    plt.figure(figsize=(10, 6))
    plt.plot([1 << p for p in p_values], errors, 'o-', label='Gercek Hata (Deneysel)')
    plt.plot([1 << p for p in p_values], theoretical_errors, 'x--', label='Teorik Hata (1.04/√m)')
    plt.xscale('log', base=2)
    plt.xlabel('Kova Sayisi (m)')
    plt.ylabel('Hata Orani')
    plt.title('HyperLogLog Hata Analizi: p Degisiminin Etkisi')
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.7)
    
    print("\nAnaliz bitti. Grafigi kapattiginizda program sonlanacaktir.")
    plt.show()

if __name__ == "__main__":
    simulate_hll()