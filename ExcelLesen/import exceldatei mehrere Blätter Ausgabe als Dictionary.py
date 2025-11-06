import pandas as pd
""" pip install pandas openpyxl """

def lese_excel_mehrere_sheets(dateipfad):
    """
    Liest alle Tabellenblätter einer Excel-Datei ein und gibt sie als Dictionary zurück.
    Schlüssel = Sheet-Name, Wert = DataFrame
    """
    try:
        # Alle Sheets einlesen
        excel_inhalt = pd.read_excel(dateipfad, sheet_name=None)

        print("✅ Excel-Datei erfolgreich eingelesen!")
        print(f"📄 Gefundene Tabellenblätter: {list(excel_inhalt.keys())}\n")

        # Inhalte der einzelnen Sheets anzeigen
        for sheet_name, df in excel_inhalt.items():
            print(f"--- 📑 Blatt: {sheet_name} ---")
            print(df.head())  # Zeigt die ersten 5 Zeilen
            print("\n")

        return excel_inhalt

    except FileNotFoundError:
        print(f"❌ Datei '{dateipfad}' wurde nicht gefunden.")
    except Exception as e:
        print(f"⚠️ Fehler beim Einlesen der Datei: {e}")

if __name__ == "__main__":
    dateipfad = input("Pfad zur Excel-Datei (.xlsx): ").strip()
    lese_excel_mehrere_sheets(dateipfad)

