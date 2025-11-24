import tkinter as tk
from tkinter import messagebox, scrolledtext

# === Fungsi Cipher ===
def substitusi_cipher(plaintext):
    hasil = ""
    tabel = "Huruf Asli | +3 | Hasil\n------------------------\n"
    for char in plaintext:
        if char.isalpha():
            kode = ord(char.upper())
            kode_baru = ((kode - 65 + 3) % 26) + 65
            hasil_huruf = chr(kode_baru)
            tabel += f"{char.upper()} | +3 | {hasil_huruf}\n"
            hasil += hasil_huruf
        else:
            tabel += f"{char} |    | {char}\n"
            hasil += char
    return hasil, tabel

def transposisi_cipher(plaintext):
    while len(plaintext) % 4 != 0:
        plaintext += " "
    
    part_length = len(plaintext) // 4
    parts = [plaintext[i:i + part_length] for i in range(0, len(plaintext), part_length)]

    proses = "\nProses Transposisi:\n"
    for i, part in enumerate(parts, start=1):
        proses += f"Bagian {i}: {part}\n"

    ciphertext = ""
    for col in range(part_length):
        for part in parts:
            if col < len(part):
                ciphertext += part[col]

    return ciphertext.strip(), proses


# === Fungsi Tombol ===
def enkripsi():
    plaintext = entry_plain.get().upper().strip()
    if plaintext == "":
        messagebox.showerror("Error", "Masukkan plaintext terlebih dahulu!")
        return

    hasil_sub, tabel = substitusi_cipher(plaintext)
    hasil_trans, proses = transposisi_cipher(hasil_sub)

    output.delete(1.0, tk.END)
    output.insert(tk.END, f"Plaintext: {plaintext}\n\n")
    output.insert(tk.END, tabel + "\n")
    output.insert(tk.END, f"Hasil Substitusi: {hasil_sub}\n\n")
    output.insert(tk.END, proses + "\n")
    output.insert(tk.END, f"Transposisi Cipher (4 blok): {hasil_trans}\n")
    output.insert(tk.END, "==============================\n")
    output.insert(tk.END, "Enkripsi selesai ✅")


# === UI ===
window = tk.Tk()
window.title("Kriptografi Klasik: Substitusi + Transposisi Cipher")
window.geometry("720x600")
window.configure(bg="#6A0DAD")

# Judul
judul = tk.Label(window, text="🔐 KRIPTOGRAFI KLASIK 🔐",
                 font=("Arial", 20, "bold"), bg="#6A0DAD", fg="white")
judul.pack(pady=10)

subjudul = tk.Label(window, text="Substitusi Cipher (+3) + Transposisi Cipher (4 Blok)",
                    font=("Arial", 13), bg="#6A0DAD", fg="#FFD700")
subjudul.pack()

# Input plaintext
frame_input = tk.Frame(window, bg="#6A0DAD")
frame_input.pack(pady=15)
tk.Label(frame_input, text="Masukkan Plaintext:",
         font=("Arial", 12), bg="#6A0DAD", fg="white").grid(row=0, column=0, padx=5)
entry_plain = tk.Entry(frame_input, font=("Arial", 14), width=40, justify="center")
entry_plain.grid(row=0, column=1, padx=5)

# Tombol Enkripsi
btn_enkripsi = tk.Button(window, text="ENKRIPSI",
                         bg="#FF4500", fg="white", width=15,
                         font=("Arial", 12, "bold"),
                         activebackground="#B22222",
                         command=enkripsi)
btn_enkripsi.pack(pady=10)

# Hasil Output
output = scrolledtext.ScrolledText(window, width=80, height=20,
                                   font=("Courier", 11), bg="#E6E6FA", fg="#4B0082")
output.pack(pady=10)

# Footer Nama
label_footer = tk.Label(window, text="ROHANA (41)",
                        font=("Arial", 11, "bold"),
                        bg="#6A0DAD", fg="#FFD700", anchor="w")
label_footer.pack(side="bottom", fill="x", padx=15, pady=5)

window.mainloop()
