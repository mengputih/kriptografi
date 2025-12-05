import tkinter as tk
from tkinter import messagebox

# ================= SBOX =================
SBOX = [
99,124,119,123,242,107,111,197,48,1,103,43,254,215,171,118,
202,130,201,125,250,89,71,240,173,212,162,175,156,164,114,192,
183,253,147,38,54,63,247,204,52,165,229,241,113,216,49,21,
4,199,35,195,24,150,5,154,7,18,128,226,235,39,178,117,
9,131,44,26,27,110,90,160,82,59,214,179,41,227,47,132,
83,209,0,237,32,252,177,91,106,203,190,57,74,76,88,207,
208,239,170,251,67,77,51,133,69,249,2,127,80,60,159,168,
81,163,64,143,146,157,56,245,188,182,218,33,16,255,243,210,
205,12,19,236,95,151,68,23,196,167,126,61,100,93,25,115,
96,129,79,220,34,42,144,136,70,238,184,20,222,94,11,219,
224,50,58,10,73,6,36,92,194,211,172,98,145,149,228,121,
231,200,55,109,141,213,78,169,108,86,244,234,101,122,174,8,
186,120,37,46,28,166,180,198,232,221,116,31,75,189,139,138,
112,62,181,102,72,3,246,14,97,53,87,185,134,193,29,158,
225,248,152,17,105,217,142,148,155,30,135,233,206,85,40,223,
140,161,137,13,191,230,66,104,65,153,45,15,176,84,187,22
]

# =============== INV SBOX ================
INV_SBOX = [
82,9,106,213,48,54,165,56,191,64,163,158,129,243,215,251,
124,227,57,130,155,47,255,135,52,142,67,68,196,222,233,203,
84,123,148,50,166,194,35,61,238,76,149,11,66,250,195,78,
8,46,161,102,40,217,36,178,118,91,162,73,109,139,209,37,
114,248,246,100,134,104,152,22,212,164,92,204,93,101,182,146,
108,112,72,80,253,237,185,218,94,21,70,87,167,141,157,132,
144,216,171,0,140,188,211,10,247,228,88,5,184,179,69,6,
208,44,30,143,202,63,15,2,193,175,189,3,1,19,138,107,
58,145,17,65,79,103,220,234,151,242,207,206,240,180,230,115,
150,172,116,34,231,173,53,133,226,249,55,232,28,117,223,110,
71,241,26,113,29,41,197,137,111,183,98,14,170,24,190,27,
252,86,62,75,198,210,121,32,154,219,192,254,120,205,90,244,
31,221,168,51,136,7,199,49,177,18,16,89,39,128,236,95,
96,81,127,169,25,181,74,13,45,229,122,159,147,201,156,239,
160,224,59,77,174,42,245,176,200,235,187,60,131,83,153,97,
23,43,4,126,186,119,214,38,225,105,20,99,85,33,12,125
]

RCON = [1,2,4,8,16,32,64,128,27,54]

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

def pad_pkcs7(text):
    data=[ord(c) for c in text]
    pad_len=16-(len(data)%16)
    return data+[pad_len]*pad_len

def unpad_pkcs7(data):
    return data[:-data[-1]]

def bytes_to_matrix(b):
    return [b[i:i+4] for i in range(0,16,4)]

def matrix_to_bytes(m):
    return [b for r in m for b in r]

def add_round_key(s,k):
    return [[a^b for a,b in zip(x,y)] for x,y in zip(s,k)]

def sub_bytes(s):
    return [[SBOX[b] for b in row] for row in s]

def inv_sub_bytes(s):
    return [[INV_SBOX[b] for b in row] for row in s]

def shift_rows(s):
    return [
        s[0],
        s[1][1:]+s[1][:1],
        s[2][2:]+s[2][:2],
        s[3][3:]+s[3][:3],
    ]

def inv_shift_rows(s):
    return [
        s[0],
        s[1][-1:]+s[1][:-1],
        s[2][-2:]+s[2][:-2],
        s[3][-3:]+s[3][:-3],
    ]

def xtime(a):
    return ((a<<1)^0x1B)&0xFF if a&0x80 else (a<<1)

def mix_single_column(c):
    a=c
    b=[xtime(x) for x in a]
    return [
        b[0]^a[3]^a[2]^b[1]^a[1],
        b[1]^a[0]^a[3]^b[2]^a[2],
        b[2]^a[1]^a[0]^b[3]^a[3],
        b[3]^a[2]^a[1]^b[0]^a[0],
    ]

def mix_columns(s):
    cols=list(zip(*s))
    mixed=[mix_single_column(list(c)) for c in cols]
    return [list(col) for col in zip(*mixed)]

def mul(a,b):
    r=0
    for _ in range(8):
        if b&1: r^=a
        h=a&0x80
        a=(a<<1)&0xFF
        if h: a^=0x1B
        b>>=1
    return r

def inv_mix_single_column(c):
    return [
        mul(c[0],14)^mul(c[1],11)^mul(c[2],13)^mul(c[3],9),
        mul(c[0],9)^mul(c[1],14)^mul(c[2],11)^mul(c[3],13),
        mul(c[0],13)^mul(c[1],9)^mul(c[2],14)^mul(c[3],11),
        mul(c[0],11)^mul(c[1],13)^mul(c[2],9)^mul(c[3],14),
    ]

def inv_mix_columns(s):
    cols=list(zip(*s))
    mixed=[inv_mix_single_column(list(c)) for c in cols]
    return [list(c) for c in zip(*mixed)]

def key_expansion(key):
    w=[key[i:i+4] for i in range(0,16,4)]
    for i in range(4,44):
        t=w[i-1]
        if i%4==0:
            t=t[1:]+t[:1]
            t=[SBOX[x] for x in t]
            t[0]^=RCON[(i//4)-1]
        w.append([t[j]^w[i-4][j] for j in range(4)])
    return [w[i:i+4] for i in range(0,44,4)]

def aes_encrypt_block(b,rk):
    s=bytes_to_matrix(b)
    s=add_round_key(s,rk[0])
    for r in range(1,10):
        s=sub_bytes(s)
        s=shift_rows(s)
        s=mix_columns(s)
        s=add_round_key(s,rk[r])
    s=sub_bytes(s)
    s=shift_rows(s)
    s=add_round_key(s,rk[10])
    return matrix_to_bytes(s)

def aes_decrypt_block(b,rk):
    s=bytes_to_matrix(b)
    s=add_round_key(s,rk[10])
    for r in range(9,0,-1):
        s=inv_shift_rows(s)
        s=inv_sub_bytes(s)
        s=add_round_key(s,rk[r])
        s=inv_mix_columns(s)
    s=inv_shift_rows(s)
    s=inv_sub_bytes(s)
    s=add_round_key(s,rk[0])
    return matrix_to_bytes(s)

def run_aes():
    plaintext = entry_plaintext.get()
    key = entry_key.get()
    
    if not plaintext or not key:
        messagebox.showerror("Error", "Plaintext dan Key tidak boleh kosong!")
        return
    
    try:
        pb = pad_pkcs7(plaintext)
        kb = [ord(c) for c in key]
        kb = (kb + [0] * 16)[:16]
        
        rk = key_expansion(kb)
        
        cipher = []
        for i in range(0, len(pb), 16):
            cipher += aes_encrypt_block(pb[i:i+16], rk)
        
        dec = []
        for i in range(0, len(cipher), 16):
            dec += aes_decrypt_block(cipher[i:i+16], rk)
        
        dec_text = ''.join(chr(x) for x in unpad_pkcs7(dec))
        
        # Tampilkan hasil
        text_cipher.delete(1.0, tk.END)
        text_cipher.insert(tk.END, str(cipher))
        
        text_decrypt.delete(1.0, tk.END)
        text_decrypt.insert(tk.END, dec_text)
        
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# Membuat UI dengan Tkinter (dengan warna)
root = tk.Tk()
root.title("AES Encryption/Decryption Tool")
root.geometry("500x400")
root.configure(bg="#E0F7FA")  # Background biru muda

# Label dan Entry untuk Plaintext (textbox input 1)
tk.Label(root, text="Plaintext:", bg="#E0F7FA", fg="#00796B", font=("Arial", 10, "bold")).pack(pady=5)
entry_plaintext = tk.Entry(root, width=50, bg="#FFFFFF", fg="#000000")
entry_plaintext.pack(pady=5)

# Label dan Entry untuk Key (textbox input 2)
tk.Label(root, text="Key:", bg="#E0F7FA", fg="#00796B", font=("Arial", 10, "bold")).pack(pady=5)
entry_key = tk.Entry(root, width=50, bg="#FFFFFF", fg="#000000")
entry_key.pack(pady=5)

# Tombol Proses
tk.Button(root, text="Proses", command=run_aes, bg="#4CAF50", fg="#FFFFFF", font=("Arial", 10, "bold")).pack(pady=10)

# Label dan Text Area untuk Ciphertext (output panel 1)
tk.Label(root, text="Ciphertext (bytes):", bg="#E0F7FA", fg="#00796B", font=("Arial", 10, "bold")).pack(pady=5)
text_cipher = tk.Text(root, height=3, width=50, bg="#FFFFFF", fg="#000000")
text_cipher.pack(pady=5)

# Label dan Text Area untuk Decrypted (output panel 2)
tk.Label(root, text="Decrypted Text:", bg="#E0F7FA", fg="#00796B", font=("Arial", 10, "bold")).pack(pady=5)
text_decrypt = tk.Text(root, height=3, width=50, bg="#FFFFFF", fg="#000000")
text_decrypt.pack(pady=5)

# Jalankan UI
root.mainloop()
