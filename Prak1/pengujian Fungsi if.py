import tkinter as tk
from tkinter import messagebox, filedialog

def hitung_nilai(sikap, tugas, uts, uas):
    # Hitung nilai akhir berdasarkan bobot
    nilai_akhir = (sikap * 0.10) + (tugas * 0.30) + (uts * 0.25) + (uas * 0.35)

    # Tentukan nilai huruf dan bobot
    if 81 <= nilai_akhir <= 100:
        nilai_huruf = "A"; bobot = 4
    elif 76 <= nilai_akhir <= 80:
        nilai_huruf = "B+"; bobot = 3.5
    elif 71 <= nilai_akhir <= 75:
        nilai_huruf = "B"; bobot = 3
    elif 66 <= nilai_akhir <= 70:
        nilai_huruf = "C+"; bobot = 2.5
    elif 56 <= nilai_akhir <= 65:
        nilai_huruf = "C"; bobot = 2
    elif 46 <= nilai_akhir <= 55:
        nilai_huruf = "D"; bobot = 1
    else:
        nilai_huruf = "E"; bobot = 0

    keterangan = "Lulus" if nilai_akhir >= 56 else "Tidak Lulus"
    return nilai_akhir, nilai_huruf, bobot, keterangan

def validate_and_compute():
    try:
        sikap = float(entry_sikap.get())
        tugas = float(entry_tugas.get())
        uts = float(entry_uts.get())
        uas = float(entry_uas.get())
    except ValueError:
        messagebox.showerror("Input Error", "Masukkan nilai numerik untuk semua bidang.")
        return

    for v, name in [(sikap, "Sikap"), (tugas, "Tugas"), (uts, "UTS"), (uas, "UAS")]:
        if not (0 <= v <= 100):
            messagebox.showerror("Input Error", f"Nilai {name} harus antara 0 dan 100.")
            return

    nilai_akhir, nilai_huruf, bobot, keterangan = hitung_nilai(sikap, tugas, uts, uas)

    lbl_hasil_val.config(text=f"{nilai_akhir:.2f}")
    lbl_huruf_val.config(text=nilai_huruf)
    lbl_bobot_val.config(text=str(bobot))
    lbl_ket_val.config(text=keterangan)

def reset_fields():
    entry_sikap.delete(0, tk.END)
    entry_tugas.delete(0, tk.END)
    entry_uts.delete(0, tk.END)
    entry_uas.delete(0, tk.END)
    lbl_hasil_val.config(text="-")
    lbl_huruf_val.config(text="-")
    lbl_bobot_val.config(text="-")
    lbl_ket_val.config(text="-")

def save_result():
    # Prepare current result
    if lbl_hasil_val.cget("text") == "-":
        messagebox.showinfo("Simpan Hasil", "Hitung terlebih dahulu sebelum menyimpan.")
        return

    data = (
        f"Sikap/Kehadiran: {entry_sikap.get()}\n"
        f"Tugas: {entry_tugas.get()}\n"
        f"UTS: {entry_uts.get()}\n"
        f"UAS: {entry_uas.get()}\n"
        f"Total Nilai Akhir: {lbl_hasil_val.cget('text')}\n"
        f"Nilai Huruf: {lbl_huruf_val.cget('text')}\n"
        f"Bobot Nilai: {lbl_bobot_val.cget('text')}\n"
        f"Keterangan: {lbl_ket_val.cget('text')}\n"
    )

    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Simpan Hasil Penilaian"
    )
    if path:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(data)
            messagebox.showinfo("Sukses", f"Hasil tersimpan di:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan: {e}")

# --- UI Setup ---
root = tk.Tk()
root.title("Aplikasi Hitung Nilai Akhir")
root.geometry("420x360")
root.resizable(False, False)

# Judul
judul = tk.Label(root, text="PROGRAM HITUNG NILAI AKHIR", font=("Arial", 14, "bold"))
judul.pack(pady=8)

frame = tk.Frame(root)
frame.pack(padx=12, pady=6, fill=tk.BOTH, expand=True)

# Labels + Entries
tk.Label(frame, text="Sikap/Kehadiran (10%)").grid(row=0, column=0, sticky="w", pady=4)
entry_sikap = tk.Entry(frame, width=12)
entry_sikap.grid(row=0, column=1, pady=4)

tk.Label(frame, text="Tugas (30%)").grid(row=1, column=0, sticky="w", pady=4)
entry_tugas = tk.Entry(frame, width=12)
entry_tugas.grid(row=1, column=1, pady=4)

tk.Label(frame, text="UTS (25%)").grid(row=2, column=0, sticky="w", pady=4)
entry_uts = tk.Entry(frame, width=12)
entry_uts.grid(row=2, column=1, pady=4)

tk.Label(frame, text="UAS (35%)").grid(row=3, column=0, sticky="w", pady=4)
entry_uas = tk.Entry(frame, width=12)
entry_uas.grid(row=3, column=1, pady=4)

# Tombol
btn_frame = tk.Frame(frame)
btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

btn_hitung = tk.Button(btn_frame, text="Hitung", width=10, command=validate_and_compute)
btn_hitung.grid(row=0, column=0, padx=6)

btn_reset = tk.Button(btn_frame, text="Reset", width=10, command=reset_fields)
btn_reset.grid(row=0, column=1, padx=6)

btn_save = tk.Button(btn_frame, text="Simpan Hasil", width=12, command=save_result)
btn_save.grid(row=0, column=2, padx=6)

# Hasil
hasil_frame = tk.LabelFrame(root, text="Hasil", padx=10, pady=8)
hasil_frame.pack(padx=12, pady=6, fill=tk.BOTH)

tk.Label(hasil_frame, text="Total Nilai Akhir:").grid(row=0, column=0, sticky="w")
lbl_hasil_val = tk.Label(hasil_frame, text="-", width=12)
lbl_hasil_val.grid(row=0, column=1, sticky="w")

tk.Label(hasil_frame, text="Nilai Huruf:").grid(row=1, column=0, sticky="w")
lbl_huruf_val = tk.Label(hasil_frame, text="-", width=12)
lbl_huruf_val.grid(row=1, column=1, sticky="w")

tk.Label(hasil_frame, text="Bobot Nilai:").grid(row=2, column=0, sticky="w")
lbl_bobot_val = tk.Label(hasil_frame, text="-", width=12)
lbl_bobot_val.grid(row=2, column=1, sticky="w")

tk.Label(hasil_frame, text="Keterangan:").grid(row=3, column=0, sticky="w")
lbl_ket_val = tk.Label(hasil_frame, text="-", width=12)
lbl_ket_val.grid(row=3, column=1, sticky="w")

# Footer
footer = tk.Label(root, text="Versi GUI — Latihan 3 (Bobot: Sikap 10%, Tugas 30%, UTS 25%, UAS 35%)", font=("Arial", 8))
footer.pack(side=tk.BOTTOM, pady=6)

root.mainloop()
