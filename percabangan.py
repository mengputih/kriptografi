import tkinter as tk
from tkinter import messagebox

def hitung():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        op = operator_var.get()

        if op == '+':
            hasil = a + b
        elif op == '-':
            hasil = a - b
        elif op == '*':
            hasil = a * b
        elif op == '/':
            if b == 0:
                raise ZeroDivisionError
            hasil = a / b
        else:
            messagebox.showerror("Error", "Pilih operator yang valid!")
            return

        label_hasil.config(text=f"Hasil dari {a} {op} {b} = {hasil}")

    except ZeroDivisionError:
        messagebox.showerror("Error", "Pembagian dengan nol tidak diperbolehkan!")
    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid!")

# GUI
root = tk.Tk()
root.title("Latihan 2 - Kalkulator Sederhana")
root.geometry("450x400")
root.configure(bg="#6A0DAD")

tk.Label(root, text="🧮 LATIHAN 2: KALKULATOR ARITMATIKA",
         font=("Arial Rounded MT Bold", 16), bg="#6A0DAD", fg="white").pack(pady=10)

frame = tk.Frame(root, bg="white", relief="ridge", bd=3)
frame.pack(padx=20, pady=10, fill="x")

tk.Label(frame, text="Masukkan Nilai A:", bg="white").pack(pady=5)
entry_a = tk.Entry(frame, font=("Arial", 12), justify="center")
entry_a.pack()

tk.Label(frame, text="Masukkan Nilai B:", bg="white").pack(pady=5)
entry_b = tk.Entry(frame, font=("Arial", 12), justify="center")
entry_b.pack()

tk.Label(frame, text="Pilih Operator (+, -, *, /):", bg="white").pack(pady=5)
operator_var = tk.StringVar()
opsi = ["+", "-", "*", "/"]
menu = tk.OptionMenu(frame, operator_var, *opsi)
menu.config(font=("Arial", 11), bg="#FFD700")
menu.pack()

btn_hitung = tk.Button(frame, text="Hitung", bg="#27AE60", fg="white",
                       font=("Arial", 11, "bold"), width=10, command=hitung)
btn_hitung.pack(pady=10)

label_hasil = tk.Label(root, text="Hasil: -", font=("Arial", 14, "bold"),
                       bg="#6A0DAD", fg="white")
label_hasil.pack(pady=15)

footer = tk.Label(root, text="ROHANA (41)", font=("Arial", 10, "bold"),
                  bg="#6A0DAD", fg="#FFD700", anchor="w")
footer.pack(side="bottom", fill="x", padx=15, pady=5)

root.mainloop()
