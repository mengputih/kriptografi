import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText

# ---------------- SBOX & RCON ----------------
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

def generate(self):
    self.clear_output()
    pt = self.plain_entry.get()
    key = self.key_entry.get()

    nama = "PUTRI ANGEL LIPIPIAN"
    npm = "230840163"

    identitas_text = (
        f"Nama : {nama}\n"
        f"NPM  : {npm}\n"
        f"==============================\n\n"
    )

    self.summary_text.insert(tk.END, identitas_text)
    self.detail_text.insert(tk.END, identitas_text)

def ascii_to_bytes_hex(s: str):
    """Return list of 16 hex strings (2-char uppercase) for ASCII input (padded/truncated)."""
    b = [format(ord(c), '02X') for c in s]
    return b

def to_matrix_col_major(hex_list):
    """Return 4x4 matrix (rows) filled column-major from hex string list length 16."""
    mat = [[None]*4 for _ in range(4)]
    for i in range(16):
        r = i % 4
        c = i // 4
        mat[r][c] = hex_list[i]
    return mat

def bytes_hex_to_int_matrix(hex_mat):
    return [[int(x,16) for x in row] for row in hex_mat]

def int_matrix_to_hex_str(mat):
    return "\n".join(" ".join(f"{x:02X}" for x in row) for row in mat)

def words_to_matrix(words):
    """words: list of 4 words (each word is list of 4 ints) -> 4x4 matrix (row major but columns are words)"""
    mat = [[0]*4 for _ in range(4)]
    for col in range(4):
        for row in range(4):
            mat[row][col] = words[col][row]
    return mat

def rot_word(word):
    """word: list of 4 ints -> rotated"""
    return word[1:] + word[:1]

def sub_word(word):
    """apply SBOX (word: list ints) -> list ints"""
    return [SBOX[b] for b in word]

def xor_word(a, b):
    return [a[i] ^ b[i] for i in range(4)]

def format_word_hex(word):
    return " ".join(f"{b:02X}" for b in word)

# ---------------- Key expansion verbose ----------------
def key_expansion_verbose(key_hex_matrix):
    """
    key_hex_matrix: 4x4 matrix of hex strings (row-major where cols are words)
    Returns: dict { 'words': list of 44 words (ints), 'rounds': list of round-info for K1..K10 }
    Each round-info contains detailed steps for W[i].
    """
    
    key_mat_int = [[int(x,16) for x in row] for row in key_hex_matrix]
    words = []
    for c in range(4):
        w = [key_mat_int[r][c] for r in range(4)]
        words.append(w)  # W0..W3

    steps = {}  
    for i in range(4):
        steps[i] = {
            "generated_from": None,
            "word": words[i].copy(),
            "notes": ["Initial key word (W{})".format(i)]
        }


    for i in range(4, 44):
        info = {"generated_from": [], "notes": [], "word_before_ops": None}
        prev = words[i-1].copy()
        info["word_before_ops"] = prev.copy()
        if i % 4 == 0:
            # RotWord
            rot = rot_word(prev)
            info["generated_from"].append(("RotWord", prev.copy(), rot.copy()))
            # SubWord
            sub = sub_word(rot)
            info["generated_from"].append(("SubWord", rot.copy(), sub.copy()))
            # XOR with RCON on first byte
            rcon_val = RCON[(i//4)-1]
            sub_rcon = sub.copy()
            sub_rcon[0] ^= rcon_val
            info["generated_from"].append(("RCON XOR", sub.copy(), sub_rcon.copy(), rcon_val))
            temp = sub_rcon
        else:
            temp = prev

        w_im4 = words[i-4]
        new_w = xor_word(temp, w_im4)
        info["word"] = new_w.copy()
        info["generated_from"].append(("XOR with W{}".format(i-4), temp.copy(), w_im4.copy(), new_w.copy()))
        steps[i] = info
        words.append(new_w)

    # build rounds K1..K10 using words
    rounds = []
    for r in range(1, 11):
        start = r*4
        wlist = words[start:start+4]  # each is list of 4 ints
        round_info = {
            "round": r,
            "words_index": (start, start+1, start+2, start+3),
            "words": [w.copy() for w in wlist],
            "steps_for_words": { idx: steps[idx] for idx in range(start, start+4) }
        }
        rounds.append(round_info)

    return {"words": words, "rounds": rounds, "steps": steps}

# ---------------- GUI ----------------
class AESKeyExpGUI:
    def __init__(self, root):
        self.root = root
        root.title("AES Key Expansion - Verbose (K1..K10)")
        root.geometry("1000x700")

        frame = ttk.Frame(root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Input frame
        in_frame = ttk.LabelFrame(frame, text="Input", padding=8)
        in_frame.pack(fill=tk.X)
        ttk.Label(in_frame, text="Plaintext (ASCII) [only shown for completeness]:").grid(row=0, column=0, sticky=tk.W)
        self.plain_entry = ttk.Entry(in_frame, width=80)
        self.plain_entry.grid(row=0, column=1, padx=6, pady=4)
        ttk.Label(in_frame, text="CipherKey (ASCII, will be padded/truncated to 16 chars):").grid(row=1, column=0, sticky=tk.W)
        self.key_entry = ttk.Entry(in_frame, width=80)
        self.key_entry.grid(row=1, column=1, padx=6, pady=4)

        btns = ttk.Frame(in_frame)
        btns.grid(row=2, column=0, columnspan=2, pady=(6,0))
        ttk.Button(btns, text="Generate", command=self.generate).pack(side=tk.LEFT, padx=6)
        ttk.Button(btns, text="Clear Output", command=self.clear_output).pack(side=tk.LEFT, padx=6)
        ttk.Button(btns, text="Save Output...", command=self.save_output).pack(side=tk.LEFT, padx=6)

        # Output frame with tabs
        out_frame = ttk.LabelFrame(frame, text="Output", padding=8)
        out_frame.pack(fill=tk.BOTH, expand=True, pady=(8,0))

        # Using a notebook with two tabs: Summary (K1..K10 matrices) and Detail (full steps)
        self.notebook = ttk.Notebook(out_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Summary tab
        self.tab_summary = ttk.Frame(self.notebook, padding=6)
        self.notebook.add(self.tab_summary, text="Summary (K1..K10)")
        self.summary_text = ScrolledText(self.tab_summary, font=("Consolas", 11))
        self.summary_text.pack(fill=tk.BOTH, expand=True)

        # Detail tab
        self.tab_detail = ttk.Frame(self.notebook, padding=6)
        self.notebook.add(self.tab_detail, text="Detail (per-word steps)")
        self.detail_text = ScrolledText(self.tab_detail, font=("Consolas", 10))
        self.detail_text.pack(fill=tk.BOTH, expand=True)

        # sample defaults
        self.plain_entry.insert(0, "INI_PLAINTEXT_DEMO")
        self.key_entry.insert(0, "KUNCI16BYTEDUMMY")

    def clear_output(self):
        self.summary_text.delete("1.0", tk.END)
        self.detail_text.delete("1.0", tk.END)

    def save_output(self):
        content = f"--- SUMMARY ---\n{self.summary_text.get('1.0', tk.END)}\n\n--- DETAIL ---\n{self.detail_text.get('1.0', tk.END)}"
        if not content.strip():
            messagebox.showinfo("Save", "Tidak ada output untuk disimpan.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file","*.txt"),("All files","*.*")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Save", f"Output disimpan ke:\n{path}")

    def generate(self):
        self.clear_output()
        pt = self.plain_entry.get()
        key = self.key_entry.get()

        # normalize to 16 chars
        def norm16(s):
            if len(s) < 16:
                return s + " "*(16-len(s))
            return s[:16]

        pt16 = norm16(pt)
        key16 = norm16(key)

        # convert to hex bytes
        pt_hex = ascii_to_bytes_hex(pt16)
        key_hex = ascii_to_bytes_hex(key16)

        # show initial info
        self.summary_text.insert(tk.END, f"Plaintext (padded/truncated to 16): '{pt16}'\n")
        self.summary_text.insert(tk.END, "Plaintext HEX: " + " ".join(pt_hex) + "\n\n")
        self.summary_text.insert(tk.END, f"CipherKey (padded/truncated to 16): '{key16}'\n")
        self.summary_text.insert(tk.END, "CipherKey HEX: " + " ".join(key_hex) + "\n\n")

        # key matrix col-major
        key_mat = to_matrix_col_major(key_hex)
        self.summary_text.insert(tk.END, "CipherKey Matrix (4x4, column-major):\n")
        self.summary_text.insert(tk.END, int_matrix_to_hex_str(bytes_hex_to_int_matrix(key_mat)) + "\n\n")

        # perform verbose key expansion
        ve = key_expansion_verbose(key_mat)
        rounds = ve["rounds"]
        steps = ve["steps"]

        # Summary : show K1..K10 matrices nicely
        self.summary_text.insert(tk.END, "=== K1 .. K10 (each K_i is 4x4 matrix formed from W[4*i]..W[4*i+3]) ===\n\n")
        for rinfo in rounds:
            r = rinfo["round"]
            wwords = rinfo["words"]
            mat = words_to_matrix(wwords)
            self.summary_text.insert(tk.END, f"--- K{r} ---\n")
            self.summary_text.insert(tk.END, int_matrix_to_hex_str(mat) + "\n\n")

        # Detail : show per-word generation steps for all W4..W43 but grouped by round
        self.detail_text.insert(tk.END, "=== Detail Per-Word (W4 .. W43) ===\n\n")
        for idx in range(4, 44):
            info = steps[idx]
            self.detail_text.insert(tk.END, f"W{idx} generation:\n")
            # show previous word
            before = info.get("word_before_ops")
            if before is not None:
                self.detail_text.insert(tk.END, f"  Word before ops (W{idx-1}): {format_word_hex(before)}\n")
            gen = info.get("generated_from", [])
            for g in gen:
                if g[0] == "RotWord":
                    prev, rot = g[1], g[2]
                    self.detail_text.insert(tk.END, f"  RotWord(W{idx-1}): {format_word_hex(prev)} -> {format_word_hex(rot)}\n")
                elif g[0] == "SubWord":
                    rot, sub = g[1], g[2]
                    self.detail_text.insert(tk.END, f"  SubWord(Rot): {format_word_hex(rot)} -> {format_word_hex(sub)}\n")
                elif g[0] == "RCON XOR":
                    subval, subrc, rconv = g[1], g[2], g[3]
                    self.detail_text.insert(tk.END, f"  XOR with RCON: {format_word_hex(subval)} ^ RCON({rconv:02X}) -> {format_word_hex(subrc)}\n")
                elif g[0].startswith("XOR with W"):
                    temp, wprev, result = g[1], g[2], g[3]
                    # identify which W index is used:
                    used_idx = idx - 4
                    self.detail_text.insert(tk.END, f"  XOR: {format_word_hex(temp)} ^ W{idx-4}({format_word_hex(wprev)}) -> W{idx}({format_word_hex(result)})\n")
                else:
                    # generic
                    self.detail_text.insert(tk.END, f"  Step {g}\n")
            self.detail_text.insert(tk.END, "\n")

        # Also produce nicely formatted K1..K10 with indices and hex
        self.summary_text.insert(tk.END, "Catatan: Hasil di atas adalah K1 sampai K10. \n")
        self.detail_text.insert(tk.END, "dapat menyimpan output menggunakan tombol Save Output.\n")

        # switch to summary tab
        self.notebook.select(self.tab_summary)
        self.summary_text.see("1.0")
        self.detail_text.see("1.0")


def main():
    root = tk.Tk()
    app = AESKeyExpGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
