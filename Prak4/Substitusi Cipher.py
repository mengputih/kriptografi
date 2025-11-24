import tkinter as tk
from tkinter import messagebox

# Fungsi substitusi
def substitusi_cipher(plaintext, aturan):
    ciphertext = ''
    for char in plaintext.upper():
        if char in aturan:
            ciphertext += aturan[char]
        else:
            ciphertext += char
    return ciphertext

aturan_substitusi = {}

def tambah_aturan():
    huruf_asli = entry_asli.get().upper()
    huruf_ganti = entry_ganti.get().upper()

    if len(huruf_asli) != 1 or not huruf_asli.isalpha():
        messagebox.showerror("Error", "Huruf asli harus 1 huruf A-Z!")
        return

    if len(huruf_ganti) != 1 or not huruf_ganti.isalpha():
        messagebox.showerror("Error", "Huruf pengganti harus 1 huruf A-Z!")
        return

    aturan_substitusi[huruf_asli] = huruf_ganti
    listbox.insert(tk.END, f"{huruf_asli} ➝ {huruf_ganti}")
    entry_asli.delete(0, tk.END)
    entry_ganti.delete(0, tk.END)

def enkripsi():
    plaintext = entry_plain.get().upper()

    if plaintext.strip() == "":
        messagebox.showerror("Error", "Plaintext tidak boleh kosong!")
        return

    ciphertext = substitusi_cipher(plaintext, aturan_substitusi)
    label_hasil.config(text=f"Ciphertext:\n{ciphertext}", fg="white")


# ===== UI =====
window = tk.Tk()
window.title("Substitution Cipher")
window.geometry("600x520")
window.configure(bg="#8A2BE2")  # Ungu elegan

judul = tk.Label(window, text="🔐 Substitution Cipher 🔐",
                 font=("Arial", 20, "bold"), bg="#8A2BE2", fg="white")
judul.pack(pady=10)

# Input plaintext
tk.Label(window, text="Masukkan Plaintext:",
         font=("Arial", 12), bg="#8A2BE2", fg="white").pack()
entry_plain = tk.Entry(window, font=("Arial", 14), width=40, justify="center")
entry_plain.pack(pady=5)

# Input aturan
tk.Label(window, text="Aturan Substitusi",
         font=("Arial", 14, "bold"), bg="#8A2BE2", fg="#FFD700").pack(pady=10)

frame = tk.Frame(window, bg="#8A2BE2")
frame.pack()

tk.Label(frame, text="Huruf Asli:", bg="#8A2BE2", fg="white").grid(row=0, column=0)
entry_asli = tk.Entry(frame, width=5, font=("Arial", 14), justify="center")
entry_asli.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Diganti Menjadi:", bg="#8A2BE2", fg="white").grid(row=0, column=2)
entry_ganti = tk.Entry(frame, width=5, font=("Arial", 14), justify="center")
entry_ganti.grid(row=0, column=3, padx=5)

btn_tambah = tk.Button(window, text="Tambah Aturan",
                       bg="#32CD32", fg="white", width=15,
                       font=("Arial", 12, "bold"),
                       activebackground="#228B22", command=tambah_aturan)
btn_tambah.pack(pady=10)

# List aturan
listbox = tk.Listbox(window, width=40, height=8, font=("Courier", 12),
                     bg="#E6E6FA", fg="#4B0082")
listbox.pack()

# Tombol enkripsi
btn_enkripsi = tk.Button(window, text="ENKRIPSI",
                         bg="#FF4500", fg="white", width=15,
                         font=("Arial", 12, "bold"),
                         activebackground="#B22222",
                         command=enkripsi)
btn_enkripsi.pack(pady=15)

# Hasil
label_hasil = tk.Label(window, text="", font=("Arial", 16, "bold"),
                       bg="#8A2BE2", fg="white")
label_hasil.pack(pady=20)

# ====== Label Nama di Bawah ======
label_footer = tk.Label(window, text="ROHANA (41)",
                        font=("Arial", 11, "bold"),
                        bg="#8A2BE2", fg="#FFD700")
label_footer.pack(side="bottom", pady=5)

window.mainloop()
