# Installation der nötigen Pakete
#   pip install pdfplumber pytesseract pillow
# Tesseract OCR installieren: Tesseract Installer
#
# Damit kannst du jede PDF auslesen – egal ob 
# reiner Text oder eingescanntes Bild.
# Du bekommst den Text in gesamt_text und kannst ihn danach 
# z. B. in eine Datei speichern.   

import pdfplumber
import pytesseract
from PIL import Image
import io

# Falls Tesseract nicht im Standardpfad ist:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pdf_datei = "beispiel.pdf"
ausgabe_datei = "beispiel_text.txt"
gesamt_text = ""

with pdfplumber.open(pdf_datei) as pdf:
    for seiten_nummer, seite in enumerate(pdf.pages):
        text = seite.extract_text()

        if text and text.strip():
            # Normale Textseite
            gesamt_text += f"\n--- Seite {seiten_nummer + 1} ---\n{text}"
        else:
            # OCR für gescannte Seite
            print(f"OCR auf Seite {seiten_nummer + 1}...")
            bild = seite.to_image(resolution=300).original
            text_ocr = pytesseract.image_to_string(bild, lang="deu")  # 'deu' für Deutsch
            gesamt_text += f"\n--- Seite {seiten_nummer + 1} (OCR) ---\n{text_ocr}"

# Text in Datei speichern
with open(ausgabe_datei, "w", encoding="utf-8") as f:
    f.write(gesamt_text)

print(f"✅ Text erfolgreich in '{ausgabe_datei}' gespeichert!")
