# Ein einfaches Beispiel in Python geben, 
# wie man den Text aus einer PDF-Datei ausliest.
# Dafür eignet sich die Bibliothek PyPDF2 ganz gut.

# 1. Installiere PyPDF2 (falls noch nicht vorhanden):
#     bash
#     pip install PyPDF2
# 2. Lege deine PDF im gleichen Ordner wie das Skript oder passe den Pfad an.

# 3. Skript starten – der Text wird in der Konsole angezeigt.

import PyPDF2

# Pfad zur PDF-Datei
pdf_datei = "beispiel.pdf"

# PDF-Datei im Lesemodus öffnen (binär)
with open(pdf_datei, "rb") as datei:
    reader = PyPDF2.PdfReader(datei)
    gesamt_text = ""

    # Jede Seite durchgehen und Text extrahieren
    for seiten_nummer, seite in enumerate(reader.pages):
        text = seite.extract_text()
        if text:
            gesamt_text += f"\n--- Seite {seiten_nummer + 1} ---\n{text}"

# Ausgabe des extrahierten Textes
print(gesamt_text)