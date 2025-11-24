import tkinter as tk
from tkinter import ttk, messagebox

# ===================== TABLES DES =====================

IP = [
    58,50,42,34,26,18,10,2,
    60,52,44,36,28,20,12,4,
    62,54,46,38,30,22,14,6,
    64,56,48,40,32,24,16,8,
    57,49,41,33,25,17,9,1,
    59,51,43,35,27,19,11,3,
    61,53,45,37,29,21,13,5,
    63,55,47,39,31,23,15,7
]

IP_INV = [
    40,8,48,16,56,24,64,32,
    39,7,47,15,55,23,63,31,
    38,6,46,14,54,22,62,30,
    37,5,45,13,53,21,61,29,
    36,4,44,12,52,20,60,28,
    35,3,43,11,51,19,59,27,
    34,2,42,10,50,18,58,26,
    33,1,41,9,49,17,57,25
]

PC1 = [57,49,41,33,25,17,9,
       1,58,50,42,34,26,18,
       10,2,59,51,43,35,27,
       19,11,3,60,52,44,36,
       63,55,47,39,31,23,15,
       7,62,54,46,38,30,22,
       14,6,61,53,45,37,29,
       21,13,5,28,20,12,4]

PC2 = [14,17,11,24,1,5,3,28,
       15,6,21,10,23,19,12,4,
       26,8,16,7,27,20,13,2,
       41,52,31,37,47,55,30,40,
       51,45,33,48,44,49,39,56,
       34,53,46,42,50,36,29,32]

SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

E = [
    32,1,2,3,4,5,
    4,5,6,7,8,9,
    8,9,10,11,12,13,
    12,13,14,15,16,17,
    16,17,18,19,20,21,
    20,21,22,23,24,25,
    24,25,26,27,28,29,
    28,29,30,31,32,1
]

P = [
    16,7,20,21,29,12,28,17,
    1,15,23,26,5,18,31,10,
    2,8,24,14,32,27,3,9,
    19,13,30,6,22,11,4,25
]

S_BOXES = [
    [
        14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7,
        0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,
        4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,
        15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13
    ],
    [
        15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,
        3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,
        0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,
        13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9
    ],
    [
        10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,
        13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,
        13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,
        1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12
    ],
    [
        7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,
        13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,
        10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,
        3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14
    ],
    [
        2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,
        14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,
        4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,
        11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3
    ],
    [
        12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,
        10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,
        9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,
        4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13
    ],
    [
        4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,
        13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,
        1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,
        6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12
    ],
    [
        13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,
        1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,
        7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,
        2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11
    ]
]

# ===================== HELPER FUNCTIONS =====================

def perm(bits, table):
    return "".join(bits[i-1] for i in table)

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def sbox_sub(bits48):
    out = ""
    for i in range(8):
        b = bits48[i*6:(i+1)*6]
        r = int(b[0] + b[5], 2)
        c = int(b[1:5], 2)
        out += f"{S_BOXES[i][r*16 + c]:04b}"
    return out

def f(R, K):
    ER = perm(R, E)
    x = f"{int(ER,2) ^ int(K,2):048b}"
    s = sbox_sub(x)
    return perm(s, P)

def gen_subkeys(key64):
    k56 = perm(key64, PC1)
    C, D = k56[:28], k56[28:]
    keys = []
    for i in range(16):
        C = left_shift(C, SHIFT[i])
        D = left_shift(D, SHIFT[i])
        keys.append(perm(C+D, PC2))
    return keys

def text_to_bits(txt):
    return "".join(f"{ord(c):08b}" for c in txt)

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return "".join(chr(int(c,2)) for c in chars)

# ===================== DES CORE =====================

def des_encrypt_block(block64, subkeys):
    b = perm(block64, IP)
    L, R = b[:32], b[32:]
    for i in range(16):
        L, R = R, f"{int(L,2) ^ int(f(R,subkeys[i]),2):032b}"
    fin = perm(R+L, IP_INV)
    return fin

def des_decrypt_block(block64, subkeys):
    b = perm(block64, IP)
    L, R = b[:32], b[32:]
    for i in range(15, -1, -1):
        L, R = R, f"{int(L,2) ^ int(f(R,subkeys[i]),2):032b}"
    fin = perm(R+L, IP_INV)
    return fin

def pad64(bits):
    x = len(bits) % 64
    return bits if x == 0 else bits + "0"*(64-x)

# ===================== GUI =====================

class DESUI:
    def __init__(self, root):
        root.title("DES Encrypt & Decrypt – ROHANA (41)")
        root.geometry("900x720")
        root.configure(bg="#1E1E1E")

        tk.Label(root, text="ROHANA (41)",
                 font=("Segoe UI", 18, "bold"),
                 bg="#1E1E1E", fg="white").pack(anchor="w", padx=10, pady=10)

        frame = tk.Frame(root, bg="#1E1E1E")
        frame.pack(pady=5)

        tk.Label(frame, text="Plaintext:", fg="white", bg="#1E1E1E",
                 font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w")
        self.plain = tk.Text(frame, width=70, height=4,
                             bg="#252526", fg="white", insertbackground="white")
        self.plain.grid(row=1, column=0, columnspan=3, pady=5)

        tk.Label(frame, text="Key (max 8 chars):", fg="white",
                 bg="#1E1E1E", font=("Segoe UI", 12)).grid(row=2, column=0, sticky="w")
        self.key = tk.Entry(frame, width=30, bg="#2D2D30", fg="white",
                            insertbackground="white")
        self.key.grid(row=3, column=0, pady=5)

        btn_frame = tk.Frame(frame, bg="#1E1E1E")
        btn_frame.grid(row=3, column=1, padx=10)

        tk.Button(btn_frame, text="ENCRYPT", bg="#0E639C",
                  fg="white", command=self.encrypt).pack(side="left", padx=5)
        tk.Button(btn_frame, text="DECRYPT", bg="#0E639C",
                  fg="white", command=self.decrypt).pack(side="left", padx=5)
        tk.Button(btn_frame, text="CLEAR", bg="#444",
                  fg="white", command=self.clear).pack(side="left", padx=5)

        # Subkey List
        sk_frame = tk.LabelFrame(root, text="16 Subkeys",
                                 fg="white", bg="#1E1E1E", width=420, height=420)
        sk_frame.place(x=10, y=240)

        self.tree = ttk.Treeview(sk_frame, columns=("r", "k"), show="headings")
        self.tree.heading("r", text="Round")
        self.tree.heading("k", text="Key (48-bit)")
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

        # Ciphertext
        out_frame = tk.LabelFrame(root, text="Output",
                                  fg="white", bg="#1E1E1E")
        out_frame.place(x=450, y=240, width=430, height=420)

        tk.Label(out_frame, text="Binary:", bg="#1E1E1E", fg="white").pack(anchor="w")
        self.out_bin = tk.Text(out_frame, height=10, bg="#252526", fg="white")
        self.out_bin.pack(fill="both", padx=6, pady=3)

        tk.Label(out_frame, text="Hex:", bg="#1E1E1E", fg="white").pack(anchor="w")
        self.out_hex = tk.Text(out_frame, height=6, bg="#252526", fg="white")
        self.out_hex.pack(fill="both", padx=6, pady=3)

        # Styling
        s = ttk.Style()
        s.configure("Treeview", background="#252526",
                    foreground="white", fieldbackground="#252526")

    # ================= ACTIONS =================

    def update_subkeys(self, keys):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for i, k in enumerate(keys, 1):
            self.tree.insert("", "end", values=(i, k))

    def encrypt(self):
        txt = self.plain.get("1.0", tk.END).strip()
        key = self.key.get()
        if key == "" or txt == "":
            messagebox.showwarning("Warning", "Isi plaintext dan key!")
            return
        if len(key) > 8:
            messagebox.showwarning("Warning", "Key max 8 karakter!")
            return

        key = key.ljust(8, "\x00")
        key_bits = text_to_bits(key)
        keys = gen_subkeys(key_bits)

        self.update_subkeys(keys)

        bits = pad64(text_to_bits(txt))

        out = ""
        for i in range(0, len(bits), 64):
            block = bits[i:i+64]
            out += des_encrypt_block(block, keys)

        self.out_bin.delete("1.0", tk.END)
        self.out_hex.delete("1.0", tk.END)
        self.out_bin.insert(tk.END, out)
        self.out_hex.insert(tk.END, hex(int(out, 2))[2:].upper())

    def decrypt(self):
        cipher_hex = self.out_hex.get("1.0", tk.END).strip()

        if cipher_hex == "":
            messagebox.showwarning("Warning", "Tidak ada ciphertext.")
            return

        try:
            bits = f"{int(cipher_hex, 16):b}"
        except:
            messagebox.showerror("Error", "Hex tidak valid!")
            return

        bits = pad64(bits)

        key = self.key.get().ljust(8, "\x00")
        key_bits = text_to_bits(key)
        keys = gen_subkeys(key_bits)

        out = ""
        for i in range(0, len(bits), 64):
            block = bits[i:i+64]
            out += des_decrypt_block(block, keys)

        plain = bits_to_text(out)

        messagebox.showinfo("Dekripsi Berhasil", f"Plaintext:\n{plain}")

    def clear(self):
        self.plain.delete("1.0", tk.END)
        self.key.delete(0, tk.END)
        self.out_bin.delete("1.0", tk.END)
        self.out_hex.delete("1.0", tk.END)
        for r in self.tree.get_children():
            self.tree.delete(r)

# ===================== RUN =====================

root = tk.Tk()
app = DESUI(root)
root.mainloop()
