"""
Öffnet eine GUI mit folgenden Funktionen:

Excel-Datei auswählen
→ Es öffnet ein Dateidialog-Fenster.

Dropdown-Menü mit allen Tabellenblättern
→ Alle gefundenen Sheets werden automatisch geladen.

Anzeigen des ausgewählten Blattes
→ Zeigt die ersten 5 Zeilen des gewählten Sheets im Textfeld an."

Suchfeld + Button, 
→ um Ergebnisse anzuzeigen
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

        blatt_dropdown['values'] = blattnamen
        blatt_dropdown.set("Bitte Tabellenblatt wählen")

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
        global aktueller_df
        aktueller_df = pd.read_excel(aktuelle_datei, sheet_name=blatt)
        textfeld.delete("1.0", tk.END)
        textfeld.insert(tk.END, f"--- 📑 Blatt: {blatt} ---\n\n")
        textfeld.insert(tk.END, aktueller_df.head().to_string(index=False))
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Einlesen des Blatts:\n{e}")

def suche_in_daten():
    """Durchsucht das aktuell geladene Blatt nach einem Begriff"""
    if aktueller_df is None:
        messagebox.showwarning("Warnung", "Bitte zuerst ein Tabellenblatt anzeigen!")
        return

    suchbegriff = suchfeld.get().strip()
    if not suchbegriff:
        messagebox.showinfo("Hinweis", "Bitte einen Suchbegriff eingeben.")
        return

    # Suche: prüft, ob der Begriff in einer beliebigen Zelle vorkommt
    mask = aktueller_df.apply(lambda row: row.astype(str).str.contains(suchbegriff, case=False, na=False)).any(axis=1)
    treffer = aktueller_df[mask]

    textfeld.delete("1.0", tk.END)
    if treffer.empty:
        textfeld.insert(tk.END, f"❌ Keine Treffer für '{suchbegriff}' gefunden.")
    else:
        textfeld.insert(tk.END, f"🔍 Treffer für '{suchbegriff}':\n\n")
        textfeld.insert(tk.END, treffer.to_string(index=False))

# Hauptfenster
root = tk.Tk()
root.title("Excel-Reader mit Suchfunktion")
root.geometry("800x600")

aktuelle_datei = None
aktueller_df = None

# UI-Elemente
tk.Label(root, text="Excel-Datei einlesen", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="📂 Datei auswählen", command=lade_excel_datei).pack()

dateipfad_label = tk.Label(root, text="Keine Datei ausgewählt", fg="gray")
dateipfad_label.pack(pady=5)

blatt_dropdown = ttk.Combobox(root, state="readonly", width=50)
blatt_dropdown.pack(pady=10)

tk.Button(root, text="📊 Blatt anzeigen", command=zeige_ausgewaehltes_blatt).pack(pady=5)

# Suchfeld
suche_frame = tk.Frame(root)
suche_frame.pack(pady=10)

tk.Label(suche_frame, text="🔍 Suchbegriff:").pack(side=tk.LEFT, padx=5)
suchfeld = tk.Entry(suche_frame, width=40)
suchfeld.pack(side=tk.LEFT, padx=5)
tk.Button(suche_frame, text="Suchen", command=suche_in_daten).pack(side=tk.LEFT, padx=5)

# Textfeld zur Anzeige
textfeld = tk.Text(root, wrap="none", width=100, height=25)
textfeld.pack(pady=10, padx=10)

root.mainloop()
