import tkinter as tk
from tkinter import messagebox

# Permutation tables
PC1 = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
PC2 = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

def permute(block, table):
    return [block[x-1] for x in table]

def left_shift(block, n):
    return block[n:] + block[:n]

def process_des():
    key_input = entry.get().strip()

    # basic validation
    if len(key_input) != 64 or any(c not in "01" for c in key_input):
        messagebox.showerror("Error", "Kunci harus 64-bit biner (0/1)")
        return

    key = [int(b) for b in key_input]
    output.delete("1.0", tk.END)

    # PC-1
    k_plus = permute(key, PC1)
    output.insert(tk.END, "PC-1:\n" + str(k_plus) + "\n\n")

    # C0 D0
    C = k_plus[:28]
    D = k_plus[28:]
    output.insert(tk.END, "C0: " + str(C) + "\nD0: " + str(D) + "\n\n")

    # Subkey rounds
    for r in range(16):
        C = left_shift(C, SHIFT[r])
        D = left_shift(D, SHIFT[r])
        output.insert(tk.END, f"C{r+1}: {C}\nD{r+1}: {D}\n")
        CD = C + D
        Ki = permute(CD, PC2)
        output.insert(tk.END, f"K{r+1}: {Ki}\n\n")

# ================= UI DESIGN ================
root = tk.Tk()
root.configure(bg="#82C5AF")
root.title("DES Key Generator UI")
root.geometry("700x650")

title = tk.Label(root, text="ROHANA (41)", fg="white", bg="#3A4738", font=("Segoe UI", 18, "bold"))
title.pack(anchor="w", padx=20, pady=10)

label = tk.Label(root, text="Masukkan Kunci 64-bit:", fg="white", bg="#A3A49B", font=("Segoe UI", 12))
label.pack(pady=5)

entry = tk.Entry(root, width=80, bg="#7F936D", fg="white", insertbackground="white", font=("Consolas", 11))
entry.pack(pady=5)

btn = tk.Button(root, text="Generate Kunci DES", command=process_des,
                bg="#0E639C", fg="white", activebackground="#1177BB",
                font=("Segoe UI", 11, "bold"), relief="flat", padx=12, pady=6)
btn.pack(pady=10)

output = tk.Text(root, height=28, width=85, bg="#445167", fg="white",
                 insertbackground="white", font=("Consolas", 10))
output.pack(padx=10, pady=10)

root.mainloop()
