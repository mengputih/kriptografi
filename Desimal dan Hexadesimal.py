# Program Konversi Bilangan Biner ke Desimal dan Hexadesimal

# Input bilangan biner dari pengguna
biner = input("Masukkan bilangan biner: ")

# Konversi ke desimal
desimal = int(biner, 2)

# Konversi ke hexadesimal
hexadesimal = hex(desimal)

# Tampilkan hasil
print("Bilangan Biner     :", biner)
print("Konversi ke Desimal:", desimal)
print("Konversi ke Hexa    :", hexadesimal.upper())
