
"""
Funktionen

✅ Excel-Datei hochladen
✅ Mehrfachsuche (beliebig viele Begriffe)
✅ Filterung nach Spalten
✅ Automatische Speicherung der letzten Suchergebnisse
✅ Export als CSV oder Excel

Das Skript nutzt pandas (Standardbibliothek für Datenanalyse in Python).


Nutzung

- Datei speichern, z. B. als excel_suchtool.py
- Abhängigkeiten installieren:
- pip install streamlit pandas openpyxl

Starten:

streamlit run excel_suchtool.py
Browser öffnet sich automatisch (Standard: http://localhost:8501
)
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# -------------------------------
# Einstellungen
# -------------------------------
ERGEBNIS_DATEI = "letzte_suchergebnisse.xlsx"

# -------------------------------
# Hilfsfunktionen
# -------------------------------
def lade_excel(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)
        st.success(f"Datei '{uploaded_file.name}' erfolgreich geladen.")
        return df
    except Exception as e:
        st.error(f"Fehler beim Laden der Datei: {e}")
        return None

def suche_dataframe(df, suchbegriffe, spalten):
    mask = pd.Series([False] * len(df))
    for begriff in suchbegriffe:
        for spalte in spalten:
            mask |= df[spalte].astype(str).str.contains(begriff, case=False, na=False)
    return df[mask]

def exportiere_ergebnisse(df, format="csv"):
    dateiname = f"suchergebnisse_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
    if format == "csv":
        df.to_csv(dateiname, index=False, encoding="utf-8-sig")
    else:
        df.to_excel(dateiname, index=False)
    df.to_excel(ERGEBNIS_DATEI, index=False)  # Automatische Speicherung
    return dateiname

# -------------------------------
# Streamlit App
# -------------------------------
st.set_page_config(page_title="Excel-Suchtool", page_icon="🔍", layout="wide")
st.title("🔍 Excel-Suchtool mit Mehrfachsuche & Export")

# 1️⃣ Excel-Datei hochladen
uploaded_file = st.file_uploader("Bitte eine Excel-Datei hochladen (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = lade_excel(uploaded_file)
    if df is not None:
        st.subheader("Vorschau der Daten")
        st.dataframe(df.head())

        # 2️⃣ Auswahl der Spalten
        spalten = st.multiselect("Wähle Spalten für die Suche", options=df.columns.tolist(), default=df.columns.tolist())

        # 3️⃣ Mehrfachsuche
        suchtext = st.text_input("Suchbegriffe (durch Komma getrennt)", "")
        if suchtext:
            suchbegriffe = [s.strip() for s in suchtext.split(",") if s.strip()]
        else:
            suchbegriffe = []

        # 4️⃣ Suche starten
        if st.button("🔎 Suche starten"):
            if suchbegriffe:
                ergebnisse = suche_dataframe(df, suchbegriffe, spalten)
                if not ergebnisse.empty:
                    st.success(f"{len(ergebnisse)} Treffer gefunden.")
                    st.dataframe(ergebnisse)

                    # Exportoptionen
                    export_format = st.selectbox("Exportformat wählen", ["csv", "excel"])
                    if st.button("💾 Ergebnisse exportieren"):
                        dateiname = exportiere_ergebnisse(ergebnisse, format=export_format)
                        with open(dateiname, "rb") as f:
                            st.download_button(
                                label="📥 Datei herunterladen",
                                data=f,
                                file_name=dateiname,
                                mime="text/csv" if export_format == "csv" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            )
                else:
                    st.warning("Keine Ergebnisse gefunden.")
            else:
                st.info("Bitte mindestens einen Suchbegriff eingeben.")

        # 5️⃣ Letzte gespeicherte Ergebnisse anzeigen
        if os.path.exists(ERGEBNIS_DATEI):
            st.divider()
            st.subheader("📂 Letzte gespeicherte Suchergebnisse")
            letzte_df = pd.read_excel(ERGEBNIS_DATEI)
            st.dataframe(letzte_df.head())
else:
    st.info("Bitte zuerst eine Excel-Datei hochladen.")
