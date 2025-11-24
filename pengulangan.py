import tkinter as tk
from tkinter import messagebox

def hitung():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        hasil = a + b
        label_hasil.config(text=f"Hasil dari {a} + {b} = {hasil}")
        btn_ulang.config(state="normal")
    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid!")

def ulang():
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)
    label_hasil.config(text="Hasil: -")
    btn_ulang.config(state="disabled")

# GUI
win = tk.Tk()
win.title("Latihan 1 - Pengulangan (Y/T)")
win.geometry("400x350")
win.configure(bg="#6A0DAD")

tk.Label(win, text="🔁 LATIHAN 1: PERHITUNGAN BERULANG (Y/T)",
         font=("Arial", 12, "bold"), bg="#6A0DAD", fg="white", wraplength=380).pack(pady=15)

frame = tk.Frame(win, bg="white", relief="ridge", bd=3)
frame.pack(padx=15, pady=10, fill="x")

tk.Label(frame, text="Masukkan Nilai A:", bg="white").pack(pady=5)
entry_a = tk.Entry(frame, font=("Arial", 12), justify="center")
entry_a.pack()

tk.Label(frame, text="Masukkan Nilai B:", bg="white").pack(pady=5)
entry_b = tk.Entry(frame, font=("Arial", 12), justify="center")
entry_b.pack()

btn_hitung = tk.Button(frame, text="Hitung", bg="#27AE60", fg="white",
                       font=("Arial", 11, "bold"), width=10, command=hitung)
btn_hitung.pack(pady=8)

btn_ulang = tk.Button(frame, text="Ulang (Y/T)", bg="#E67E22", fg="white",
                      font=("Arial", 11, "bold"), width=10, command=ulang, state="disabled")
btn_ulang.pack()

label_hasil = tk.Label(win, text="Hasil: -", font=("Arial", 14, "bold"),
                       bg="#6A0DAD", fg="white")
label_hasil.pack(pady=15)

footer = tk.Label(win, text="ROHANA (41)", font=("Arial", 10, "bold"),
                  bg="#6A0DAD", fg="#FFD700", anchor="w")
footer.pack(side="bottom", fill="x", padx=15, pady=5)

win.mainloop()
