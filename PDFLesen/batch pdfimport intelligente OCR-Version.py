# Hier kommt die Batch-Version, die alle 
# PDFs in einem Ordner verarbeitet und für jede automatisch 
# eine .txt-Datei mit dem extrahierten Text erstellt.

# So benutzt du das Skript:

# 1. Erstelle einen Ordner pdfs und lege alle PDF-Dateien hinein.

# 2.Erstelle einen leeren Ordner texte (oder das Skript macht es automatisch).

# 3.Speichere das Skript als pdf_batch_ocr.py.

# 4.Installiere die nötigen Pakete:
#   pip install pdfplumber pytesseract pillow
#   Installiere Tesseract OCR (siehe vorherige Anleitung).

# 5.Führe das Skript aus:
#  python pdf_batch_ocr.py
#  Fertig – im Ordner texte findest du für jede PDF eine .txt-Datei.'

# Intelligente OCR-Version, die erst prüft, 
# ob eine Seite bereits durchsuchbaren Text enthält
# und nur dann OCR macht, wenn nötig. 
# Das spart enorm viel Zeit.

import os
import pdfplumber
import pytesseract
from PIL import Image

# Falls Tesseract nicht im Standardpfad ist, hier den Pfad angeben:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\\tesseract.exe"

# Ordner mit PDFs
pdf_ordner = "C:\\Projekte\\Python\\PDFLesen\\pdfs"
# Ausgabeordner für Textdateien
ausgabe_ordner = "texte"

os.makedirs(ausgabe_ordner, exist_ok=True)

for dateiname in os.listdir(pdf_ordner):
    if dateiname.lower().endswith(".pdf"):
        pdf_pfad = os.path.join(pdf_ordner, dateiname)
        txt_datei = os.path.splitext(dateiname)[0] + ".txt"
        txt_pfad = os.path.join(ausgabe_ordner, txt_datei)

        print(f"📄 Verarbeite: {dateiname}")
        gesamt_text = ""

        with pdfplumber.open(pdf_pfad) as pdf:
            for seiten_nummer, seite in enumerate(pdf.pages):
                text = seite.extract_text()

                if text and text.strip():
                    # Bereits durchsuchbarer Text → OCR überspringen
                    gesamt_text += f"\n--- Seite {seiten_nummer + 1} ---\n{text}"
                else:
                    # Kein Text vorhanden → OCR anwenden
                    print(f"  🔍 OCR auf Seite {seiten_nummer + 1}...")
                    bild = seite.to_image(resolution=300).original
                    text_ocr = pytesseract.image_to_string(bild, lang="deu")
                    gesamt_text += f"\n--- Seite {seiten_nummer + 1} (OCR) ---\n{text_ocr}"

        with open(txt_pfad, "w", encoding="utf-8") as f:
            f.write(gesamt_text)

        print(f"✅ Gespeichert: {txt_pfad}")

print("🎯 Fertig! Alle PDFs wurden optimiert verarbeitet.")

