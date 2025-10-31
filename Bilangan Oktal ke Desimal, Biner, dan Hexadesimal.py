# Program Konversi Bilangan Oktal ke Desimal, Biner, dan Hexadesimal

# Input bilangan oktal
oktal = input("Masukkan bilangan oktal: ")

# Konversi ke desimal
desimal = int(oktal, 8)

# Konversi ke biner
biner = bin(desimal)

# Konversi ke hexadesimal
hexadesimal = hex(desimal)

# Tampilkan hasil
print("Bilangan Oktal      :", oktal)
print("Konversi ke Desimal :", desimal)
print("Konversi ke Biner   :", biner[2:])  # hapus awalan '0b'
print("Konversi ke Hexa    :", hexadesimal[2:].upper())  # hapus awalan '0x'
