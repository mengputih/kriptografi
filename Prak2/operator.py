import tkinter as tk
from tkinter import messagebox

def hitung():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        op = entry_op.get().strip()

        if op == "+":
            hasil = a + b
        elif op == "-":
            hasil = a - b
        elif op == "*":
            hasil = a * b
        elif op == "/":
            if b == 0:
                messagebox.showerror("Error", "Pembagian dengan nol tidak diperbolehkan!")
                return
            hasil = a / b
        else:
            messagebox.showerror("Error", "Operator tidak valid! Gunakan +, -, *, atau /")
            return

        # Tampilkan hasil
        label_hasil.config(
            text=f"Hasil dari {a} {op} {b} = {hasil}", fg="white"
        )

    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid untuk nilai A dan B!")

root = tk.Tk()
root.title("🧮 Kalkulator Sederhana - ROHANA (41)")
root.geometry("500x420")
root.configure(bg="#6A0DAD")  


judul = tk.Label(
    root,
    text="💫 KALKULATOR ARITMATIKA SEDERHANA 💫",
    font=("Arial Rounded MT Bold", 16),
    bg="#6A0DAD",
    fg="white",
)
judul.pack(pady=10)

subjudul = tk.Label(
    root,
    text="Latihan: Gunakan IF untuk memilih operator",
    font=("Arial", 11, "italic"),
    bg="#6A0DAD",
    fg="#FFD700",
)
subjudul.pack()


frame = tk.Frame(root, bg="white", relief="ridge", bd=4)
frame.pack(pady=15, padx=20, fill="x")


tk.Label(frame, text="Masukkan Nilai A:", bg="white", font=("Arial", 11, "bold")).pack(pady=5)
entry_a = tk.Entry(frame, width=20, font=("Arial", 12), justify="center")
entry_a.pack(pady=5)


tk.Label(frame, text="Masukkan Nilai B:", bg="white", font=("Arial", 11, "bold")).pack(pady=5)
entry_b = tk.Entry(frame, width=20, font=("Arial", 12), justify="center")
entry_b.pack(pady=5)


tk.Label(frame, text="Masukkan Operator (+, -, *, /):", bg="white", font=("Arial", 11, "bold")).pack(pady=5)
entry_op = tk.Entry(frame, width=10, font=("Arial", 12), justify="center")
entry_op.pack(pady=5)


btn_hitung = tk.Button(
    frame,
    text="Hitung",
    bg="#27AE60",
    fg="white",
    font=("Arial", 12, "bold"),
    width=12,
    command=hitung,
)
btn_hitung.pack(pady=10)


label_hasil = tk.Label(root, text="Hasil: -", font=("Arial", 14, "bold"), bg="#6A0DAD", fg="white")
label_hasil.pack(pady=20)


footer = tk.Label(
    root,
    text="ROHANA (41)",
    font=("Arial", 10, "bold"),
    bg="#6A0DAD",
    fg="#FFD700",
    anchor="w"
)
footer.pack(side="bottom", fill="x", padx=15, pady=5)

root.mainloop()
