"""
Funktionen

✅ Excel-Datei hochladen
✅ Mehrfachsuche (beliebig viele Begriffe)
✅ Filterung nach Spalten
✅ Automatische Speicherung der letzten Suchergebnisse
✅ Export als CSV oder Excel
✅ Numerische Filter (z. B. größer/kleiner als)
✅ Datumsfilter (von–bis Bereich)

Das Skript nutzt pandas (Standardbibliothek für Datenanalyse in Python).


Nutzung

- Datei speichern, z. B. als excel_suchtool.py
- Abhängigkeiten installieren:
- pip install streamlit pandas openpyxl

Starten:

streamlit run excel_suchtool_streamlit_mitfilter.py
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
        df = pd. read_excel(uploaded_file)
        st.success(f"Datei '{uploaded_file.name}' erfolgreich geladen.")
        return df
    except Exception as e:
        st.error(f"Fehler beim Laden der Datei: {e}")
        return None

def suche_dataframe(df, suchbegriffe, spalten):
    """Textsuche in den angegebenen Spalten."""
    mask = pd.Series([False] * len(df))
    for begriff in suchbegriffe:
        for spalte in spalten:
            mask |= df[spalte].astype(str).str.contains(begriff, case=False, na=False)
    return df[mask]

def filter_numerisch(df, spalte, min_wert, max_wert):
    """Filtert numerische Werte zwischen min und max."""
    return df[(df[spalte] >= min_wert) & (df[spalte] <= max_wert)]

def filter_datum(df, spalte, start, ende):
    """Filtert Datumswerte zwischen zwei Zeitpunkten."""
    df[spalte] = pd.to_datetime(df[spalte], errors='coerce')
    return df[(df[spalte] >= pd.to_datetime(start)) & (df[spalte] <= pd.to_datetime(ende))]

def exportiere_ergebnisse(df, format="csv"):
    dateiname = f"suchergebnisse_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
    if format == "csv":
        df.to_csv(dateiname, index=False, encoding="utf-8-sig")
    else:
        df.to_excel(dateiname, index=False)
    df.to_excel(ERGEBNIS_DATEI, index=False)
    return dateiname

# -------------------------------
# Streamlit App
# -------------------------------
st.set_page_config(page_title="Excel-Suchtool", page_icon="🔍", layout="wide")
st.title("🔍 Excel-Suchtool mit Text-, Zahlen- & Datumsfiltern")

uploaded_file = st.file_uploader("Bitte eine Excel-Datei hochladen (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = lade_excel(uploaded_file)
    if df is not None:
        st.subheader("Vorschau der Daten")
        st.dataframe(df.head())

        # ---- TEXTSUCHE ----
        st.divider()
        st.header("1️⃣ Textsuche")
        spalten_text = st.multiselect("Spalten für Textsuche", options=df.columns.tolist(), default=df.columns.tolist())
        suchtext = st.text_input("Suchbegriffe (durch Komma getrennt)", "")
        suchbegriffe = [s.strip() for s in suchtext.split(",") if s.strip()]

        # ---- NUMERISCHE FILTER ----
        st.divider()
        st.header("2️⃣ Numerische Filter (optional)")
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        num_filter_data = {}
        if numeric_columns:
            for col in numeric_columns:
                min_val, max_val = float(df[col].min()), float(df[col].max())
                values = st.slider(f"{col} – Wertebereich", min_val, max_val, (min_val, max_val))
                num_filter_data[col] = values

        # ---- DATUMSFILTER ----
        st.divider()
        st.header("3️⃣ Datumsfilter (optional)")
        date_columns = df.select_dtypes(include=['datetime', 'datetimetz']).columns.tolist()
        if not date_columns:
            # Versuch, Datumsspalten automatisch zu erkennen
            for col in df.columns:
                try:
                    pd.to_datetime(df[col])
                    date_columns.append(col)
                except:
                    continue

        date_filter_data = {}
        if date_columns:
            for col in date_columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                min_date = df[col].min()
                max_date = df[col].max()
                if pd.notna(min_date) and pd.notna(max_date):
                    start, end = st.date_input(f"{col} – Zeitraum", (min_date, max_date))
                    date_filter_data[col] = (start, end)

        # ---- SUCHE STARTEN ----
        st.divider()
        if st.button("🔎 Suche und Filter anwenden"):
            result_df = df.copy()

            # Textsuche
            if suchbegriffe:
                result_df = suche_dataframe(result_df, suchbegriffe, spalten_text)

            # Numerische Filter
            for col, (minv, maxv) in num_filter_data.items():
                result_df = filter_numerisch(result_df, col, minv, maxv)

            # Datumsfilter
            for col, (start, end) in date_filter_data.items():
                result_df = filter_datum(result_df, col, start, end)

            if not result_df.empty:
                st.success(f"{len(result_df)} Treffer gefunden.")
                st.dataframe(result_df)

                # Exportoptionen
                export_format = st.selectbox("Exportformat wählen", ["csv", "excel"])
                if st.button("💾 Ergebnisse exportieren"):
                    dateiname = exportiere_ergebnisse(result_df, format=export_format)
                    with open(dateiname, "rb") as f:
                        st.download_button(
                            label="📥 Datei herunterladen",
                            data=f,
                            file_name=dateiname,
                            mime="text/csv" if export_format == "csv" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
            else:
                st.warning("Keine Treffer mit den angegebenen Filtern gefunden.")

        # ---- Letzte Ergebnisse ----
        if os.path.exists(ERGEBNIS_DATEI):
            st.divider()
            st.subheader("📂 Letzte gespeicherte Suchergebnisse")
            letzte_df = pd.read_excel(ERGEBNIS_DATEI)
            st.dataframe(letzte_df.head())
else:
    st.info("Bitte zuerst eine Excel-Datei hochladen.")
