# PyPDF2 ist gut für einfachen Text. 
# Falls du komplexe Layouts, Bilder oder Tabellen auslesen möchtest, 
# eignet sich eher pdfplumber oder sogar OCR mit pytesseract.
# 
# Vorteile von pdfplumber

# - Bessere Erkennung von Spalten und Zeilenumbrüchen
# - Kann auch Positionen der Textelemente liefern
# - Möglichkeit, Tabellen direkt zu extrahieren (extract_table())
# - Falls deine PDF gescannte Bilder enthält, brauchst du zusätzlich OCR mit pytesseract.

# pip install pdfplumber

import pdfplumber

# Pfad zur PDF-Datei
pdf_datei = "beispiel.pdf"

gesamt_text = ""

# PDF öffnen und auslesen
with pdfplumber.open(pdf_datei) as pdf:
    for seiten_nummer, seite in enumerate(pdf.pages):
        text = seite.extract_text()
        if text:
            gesamt_text += f"\n--- Seite {seiten_nummer + 1} ---\n{text}"

# Ausgabe des extrahierten Textes
print(gesamt_text)