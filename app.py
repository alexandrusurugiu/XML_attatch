import streamlit as st
import xml.etree.ElementTree as ET
import io

# Interfața aplicației
st.title("Procesare XML 🧹")
st.write("Încarcă un fișier XML pentru a elimina liniile noi din tag-urile `<Attachment>`.")

# Componenta de Drag & Drop
uploaded_file = st.file_uploader("Trage fișierul XML aici", type=["xml"])

if uploaded_file is not None:
    try:
        # Citim și parsăm fișierul încărcat direct din memorie
        tree = ET.parse(uploaded_file)
        root = tree.getroot()

        # Prelucrarea exact cum ai făcut-o tu
        for attachment in root.iter("Attachment"):
            if attachment.text:
                attachment.text = attachment.text.replace("\n", "").replace("\r", "")

        # Transformăm XML-ul înapoi în bytes pentru a putea fi descărcat
        # Folosim io.BytesIO pentru a simula un fișier în memorie
        output_io = io.BytesIO()
        tree.write(output_io, encoding="utf-8", xml_declaration=True)
        xml_data = output_io.getvalue()

        st.success("Gata ✅! Fișierul a fost procesat cu succes.")

        # Generăm un nume nou pentru fișierul descărcat
        nume_original = uploaded_file.name
        nume_nou = nume_original.replace(".xml", "_clean.xml")

        # Butonul de descărcare
        st.download_button(
            label="Descarcă fișierul curățat",
            data=xml_data,
            file_name=nume_nou,
            mime="application/xml"
        )
    except Exception as e:
        st.error(f"A apărut o eroare la procesare: {e}")