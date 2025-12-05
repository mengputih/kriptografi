"""
AES Key Generation GUI (tkinter)
- Masukkan Plaintext dan Cipherkey (akan dip-pad/truncate ke 16 bytes jika perlu)
- Klik "Generate" untuk melihat langkah-langkah dan K0..K10
- Klik "Save" untuk menyimpan keluaran ke file teks
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText

# ---- SBOX & RCON (diambil dari pratikum) ----
SBOX = [
    0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76,
    0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0,
    0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15,
    0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75,
    0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84,
    0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF,
    0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8,
    0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2,
    0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73,
    0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB,
    0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79,
    0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08,
    0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A,
    0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E,
    0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF,
    0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16
]

RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]


# ---- AES helper functions ----
def text_to_hex(text: str):
    return [format(ord(c), '02X') for c in text]

def to_matrix_4x4(hex_list):
    matrix = [[None]*4 for _ in range(4)]
    # Fill column-wise
    for i in range(16):
        row = i % 4
        col = i // 4
        matrix[row][col] = hex_list[i]
    return matrix

def xor_matrices(m1, m2):
    result = [[None]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            v1 = int(m1[r][c], 16)
            v2 = int(m2[r][c], 16)
            result[r][c] = format(v1 ^ v2, '02X')
    return result

def rot_word(word):
    return word[1:] + word[:1]

def sub_word(word):
    return [SBOX[b] for b in word]

def key_expansion(key_matrix_hex):
    # convert matrix hex (string) to ints matrix
    key_matrix = [[int(x,16) for x in row] for row in key_matrix_hex]
    key_words = []
    for col in range(4):
        key_words.append([key_matrix[row][col] for row in range(4)])
    for i in range(4, 44):
        temp = key_words[i-1].copy()
        if i % 4 == 0:
            temp = rot_word(temp)
            temp = sub_word(temp)
            temp[0] ^= RCON[(i//4)-1]
        new_word = [temp[j] ^ key_words[i-4][j] for j in range(4)]
        key_words.append(new_word)
    return key_words  # list of 44 words (each word is list of 4 ints)

def words_to_matrix(words):
    # words: 4 words (each word is 4 bytes ints) -> 4x4 matrix row-major
    matrix = [[0]*4 for _ in range(4)]
    for col in range(4):
        for row in range(4):
            matrix[row][col] = words[col][row]
    return matrix

def hex_matrix_to_str(mat):
    return "\n".join(" ".join(f"{x:02X}" if isinstance(x,int) else x for x in row) for row in mat)

# ---- GUI app ----
class AESKeyGenApp:
    def __init__(self, root):
        self.root = root
        root.title("AES Key Generation - GUI (Pratikum 8)")
        root.geometry("900x640")

        frm = ttk.Frame(root, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)

        # Inputs
        inp_frame = ttk.LabelFrame(frm, text="Input", padding=8)
        inp_frame.pack(fill=tk.X)
        ttk.Label(inp_frame, text="Plaintext (ASCII, will be padded/truncated to 16 chars):").grid(row=0, column=0, sticky=tk.W)
        self.plain_entry = ttk.Entry(inp_frame, width=70)
        self.plain_entry.grid(row=0, column=1, padx=6, pady=4)
        ttk.Label(inp_frame, text="Cipher Key (ASCII, will be padded/truncated to 16 chars):").grid(row=1, column=0, sticky=tk.W)
        self.key_entry = ttk.Entry(inp_frame, width=70)
        self.key_entry.grid(row=1, column=1, padx=6, pady=4)

        btn_frame = ttk.Frame(inp_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(6,0))
        gen_btn = ttk.Button(btn_frame, text="Generate", command=self.generate)
        gen_btn.pack(side=tk.LEFT, padx=6)
        clear_btn = ttk.Button(btn_frame, text="Clear Output", command=self.clear_output)
        clear_btn.pack(side=tk.LEFT, padx=6)
        save_btn = ttk.Button(btn_frame, text="Save Output...", command=self.save_output)
        save_btn.pack(side=tk.LEFT, padx=6)

        # Output area
        out_frame = ttk.LabelFrame(frm, text="Output / Step-by-step", padding=8)
        out_frame.pack(fill=tk.BOTH, expand=True, pady=(8,0))
        self.output = ScrolledText(out_frame, wrap=tk.WORD, font=("Consolas", 10))
        self.output.pack(fill=tk.BOTH, expand=True)

        # sample demo values
        self.plain_entry.insert(0, "PRATIKUMKRIPTOGA")
        self.key_entry.insert(0, "UNIKASANTOTHOMAS")

    def clear_output(self):
        self.output.delete("1.0", tk.END)

    def save_output(self):
        content = self.output.get("1.0", tk.END).strip()
        if not content:
            messagebox.showinfo("Save", "Tidak ada output untuk disimpan.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt"),("All files","*.*")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Save", f"Output tersimpan ke:\n{path}")

    def generate(self):
        self.clear_output()
        pt = self.plain_entry.get()
        key = self.key_entry.get()

        # Normalize to 16 chars (pad with spaces or truncate)
        def norm16(s):
            if len(s) < 16:
                return s + " "*(16-len(s))
            return s[:16]
        pt16 = norm16(pt)
        key16 = norm16(key)

        self.output.insert(tk.END, f"Plaintext input: '{pt}'\nPlaintext (padded/truncated to 16): '{pt16}'\n\n")
        self.output.insert(tk.END, f"CipherKey input: '{key}'\nCipherKey (padded/truncated to 16): '{key16}'\n\n")

        # 1) Konversi ke HEX
        hex_plain = text_to_hex(pt16)
        hex_key = text_to_hex(key16)
        self.output.insert(tk.END, "1) Konversi ke HEX (per byte):\n")
        self.output.insert(tk.END, "Plaintext HEX: " + " ".join(hex_plain) + "\n")
        self.output.insert(tk.END, "CipherKey HEX: " + " ".join(hex_key) + "\n\n")

        # matriks 4x4 (kolom per kolom)
        matrix_plain = to_matrix_4x4(hex_plain)
        matrix_key = to_matrix_4x4(hex_key)
        self.output.insert(tk.END, "Matriks Plaintext (4x4, kolom-major):\n")
        self.output.insert(tk.END, hex_matrix_to_str(matrix_plain) + "\n\n")
        self.output.insert(tk.END, "Matriks CipherKey (4x4, kolom-major):\n")
        self.output.insert(tk.END, hex_matrix_to_str(matrix_key) + "\n\n")

        # 2) XOR AddRoundKey
        matrix_xor = xor_matrices(matrix_plain, matrix_key)
        self.output.insert(tk.END, "2) XOR (AddRoundKey) Plaintext ^ CipherKey:\n")
        self.output.insert(tk.END, hex_matrix_to_str(matrix_xor) + "\n\n")

        # 3) Key expansion
        self.output.insert(tk.END, "3) Key Expansion (men-generate K0..K10) - langkah internal:\n")
        # convert key_matrix to ints for expansion; but our key_expansion expects hex strings->ints inside
        key_matrix_hex = [[x for x in row] for row in matrix_key]  # still hex strings
        all_words = key_expansion(key_matrix_hex)  # returns list of 44 words (ints)
        # print K0..K10
        for r in range(11):
            start = r*4
            end = start + 4
            words = all_words[start:end]
            km = words_to_matrix(words)
            self.output.insert(tk.END, f"=== K{r} ===\n")
            # format as hex two-digit
            for row in km:
                self.output.insert(tk.END, " ".join(f"{b:02X}" for b in row) + "\n")
            self.output.insert(tk.END, "\n")

        # optionally show some internal words for debugging/learning
        self.output.insert(tk.END, "Catatan: Algoritma RotWord, SubWord (SBOX) dan RCON digunakan saat i%4==0.\n")
        self.output.insert(tk.END, "Selesai. Anda dapat menyimpan hasil dengan tombol Save.\n")

        # Scroll to top
        self.output.see("1.0")


def main():
    root = tk.Tk()
    app = AESKeyGenApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
