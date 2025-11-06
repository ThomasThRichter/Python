"""
Öffnet eine GUI mit folgenden Funktionen:

Excel-Datei auswählen
→ Es öffnet ein Dateidialog-Fenster.

Dropdown-Menü mit allen Tabellenblättern
→ Alle gefundenen Sheets werden automatisch geladen.

Anzeigen des ausgewählten Blattes
→ Zeigt die ersten 5 Zeilen des gewählten Sheets im Textfeld an."
"""
"""pip install pandas openpyxl"""

import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def lade_excel_datei():
    """Öffnet Dateidialog zum Auswählen einer Excel-Datei"""
    dateipfad = filedialog.askopenfilename(
        title="Excel-Datei auswählen",
        filetypes=[("Excel-Dateien", "*.xlsx *.xls")]
    )
    if dateipfad:
        dateipfad_label.config(text=f"📄 Ausgewählte Datei: {dateipfad}")
        lade_tabellenblaetter(dateipfad)

def lade_tabellenblaetter(dateipfad):
    """Liest die Blattnamen und füllt das Dropdown-Menü"""
    try:
        excel = pd.ExcelFile(dateipfad)
        blattnamen = excel.sheet_names

        # Dropdown befüllen
        blatt_dropdown['values'] = blattnamen
        blatt_dropdown.set("Bitte Tabellenblatt wählen")

        # Speichere Pfad global
        global aktuelle_datei
        aktuelle_datei = dateipfad

    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Lesen der Datei:\n{e}")

def zeige_ausgewaehltes_blatt():
    """Liest das ausgewählte Blatt und zeigt die ersten Zeilen an"""
    if not aktuelle_datei:
        messagebox.showwarning("Warnung", "Bitte zuerst eine Datei auswählen!")
        return

    blatt = blatt_dropdown.get()
    if not blatt or blatt.startswith("Bitte"):
        messagebox.showwarning("Warnung", "Bitte ein Tabellenblatt auswählen!")
        return

    try:
        df = pd.read_excel(aktuelle_datei, sheet_name=blatt)
        textfeld.delete("1.0", tk.END)
        textfeld.insert(tk.END, f"--- 📑 Blatt: {blatt} ---\n\n")
        textfeld.insert(tk.END, df.head().to_string(index=False))
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Einlesen des Blatts:\n{e}")

# Hauptfenster
root = tk.Tk()
root.title("Excel-Reader GUI")
root.geometry("700x500")

aktuelle_datei = None

# UI-Elemente
tk.Label(root, text="Excel-Datei einlesen", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="📂 Datei auswählen", command=lade_excel_datei).pack()

dateipfad_label = tk.Label(root, text="Keine Datei ausgewählt", fg="gray")
dateipfad_label.pack(pady=5)

blatt_dropdown = ttk.Combobox(root, state="readonly", width=50)
blatt_dropdown.pack(pady=10)

tk.Button(root, text="📊 Blatt anzeigen", command=zeige_ausgewaehltes_blatt).pack(pady=5)

# Textfeld zur Anzeige
textfeld = tk.Text(root, wrap="none", width=80, height=20)
textfeld.pack(pady=10, padx=10)

root.mainloop()
