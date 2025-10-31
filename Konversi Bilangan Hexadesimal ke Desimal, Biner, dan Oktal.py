# Program Konversi Bilangan Hexadesimal ke Desimal, Biner, dan Oktal

# Input bilangan hexadesimal
heksa = input("Masukkan bilangan hexadesimal: ")

# Konversi ke desimal
desimal = int(heksa, 16)

# Konversi ke biner
biner = bin(desimal)

# Konversi ke oktal
oktal = oct(desimal)

# Tampilkan hasil
print("Bilangan Hexadesimal:", heksa.upper())
print("Konversi ke Desimal  :", desimal)
print("Konversi ke Biner    :", biner[2:])  # hapus awalan '0b'
print("Konversi ke Oktal    :", oktal[2:])  # hapus awalan '0o'
