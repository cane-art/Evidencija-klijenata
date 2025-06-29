import tkinter as tk
from tkinter import messagebox
import sqlite3

# Kreiraj bazu
conn = sqlite3.connect("klijenti.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS klijenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ime TEXT NOT NULL,
    email TEXT,
    telefon TEXT
)
""")
conn.commit()
conn.close()

# Funkcije
def dodaj_klijenta():
    ime = entry_ime.get()
    email = entry_email.get()
    telefon = entry_telefon.get()

    if not ime:
        messagebox.showwarning("Upozorenje", "Ime je obavezno!")
        return

    conn = sqlite3.connect("klijenti.db")
    c = conn.cursor()
    c.execute("INSERT INTO klijenti (ime, email, telefon) VALUES (?, ?, ?)", (ime, email, telefon))
    conn.commit()
    conn.close()

    entry_ime.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefon.delete(0, tk.END)

    prikazi_klijente()

def prikazi_klijente():
    listbox.delete(0, tk.END)
    conn = sqlite3.connect("klijenti.db")
    c = conn.cursor()
    c.execute("SELECT * FROM klijenti")
    for row in c.fetchall():
        listbox.insert(tk.END, f"{row[0]}. {row[1]} | {row[2]} | {row[3]}")
    conn.close()

def pretrazi():
    ime = entry_pretraga.get()
    listbox.delete(0, tk.END)
    conn = sqlite3.connect("klijenti.db")
    c = conn.cursor()
    c.execute("SELECT * FROM klijenti WHERE ime LIKE ?", ('%' + ime + '%',))
    for row in c.fetchall():
        listbox.insert(tk.END, f"{row[0]}. {row[1]} | {row[2]} | {row[3]}")
    conn.close()

def obrisi_klijenta():
    try:
        selektovano = listbox.get(listbox.curselection())
        klijent_id = selektovano.split(".")[0]
        conn = sqlite3.connect("klijenti.db")
        c = conn.cursor()
        c.execute("DELETE FROM klijenti WHERE id = ?", (klijent_id,))
        conn.commit()
        conn.close()
        prikazi_klijente()
    except:
        messagebox.showwarning("Greška", "Niste izabrali klijenta.")

# GUI
root = tk.Tk()
root.title("Evidencija Klijenata")

# Unos
tk.Label(root, text="Ime:").grid(row=0, column=0)
entry_ime = tk.Entry(root)
entry_ime.grid(row=0, column=1)

tk.Label(root, text="Email:").grid(row=1, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1)

tk.Label(root, text="Telefon:").grid(row=2, column=0)
entry_telefon = tk.Entry(root)
entry_telefon.grid(row=2, column=1)

tk.Button(root, text="Dodaj klijenta", command=dodaj_klijenta).grid(row=3, column=0, columnspan=2, pady=5)

# Lista
listbox = tk.Listbox(root, width=60)
listbox.grid(row=4, column=0, columnspan=2, pady=10)

# Pretraga
tk.Label(root, text="Pretraga po imenu:").grid(row=5, column=0)
entry_pretraga = tk.Entry(root)
entry_pretraga.grid(row=5, column=1)
tk.Button(root, text="Pretraži", command=pretrazi).grid(row=6, column=0, columnspan=2)

# Brisanje
tk.Button(root, text="Obriši izabrano", command=obrisi_klijenta).grid(row=7, column=0, columnspan=2, pady=10)

prikazi_klijente()
root.mainloop()