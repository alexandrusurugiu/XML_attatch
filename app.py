import streamlit as st
import xml.etree.ElementTree as ET
import io

st.set_page_config(page_title="Curățare XML", page_icon="🧹", layout="centered")

st.title("Procesare Multi-XML 🧹")
st.markdown("Încarcă fișierele XML mai jos. Fiecare fișier va fi curățat și pregătit pentru descărcare individuală.")

uploaded_files = st.file_uploader(
    "Trage fișierele XML aici",
    type=["xml"],
    accept_multiple_files=True
)

if uploaded_files:
    st.divider()

    st.subheader("🎉 Fișiere pregătite pentru descărcare")
    st.caption("Procesarea s-a terminat cu succes. Descarcă fișierele dorite făcând click pe butoanele de mai jos.")

    st.write("")

    for uploaded_file in uploaded_files:
        try:
            tree = ET.parse(uploaded_file)
            root = tree.getroot()

            for attachment in root.iter("Attachment"):
                if attachment.text:
                    attachment.text = attachment.text.replace("\n", "").replace("\r", "")

            output_io = io.BytesIO()
            tree.write(output_io, encoding="utf-8", xml_declaration=True)
            xml_data = output_io.getvalue()

            nume_original = uploaded_file.name
            nume_nou = nume_original.replace(".xml", "_clean.xml")

            with st.container(border=True):
                col1, col2 = st.columns([3, 1], vertical_alignment="center")

                with col1:
                    st.markdown(f"**Fișier original:** `{nume_original}`")
                    st.markdown(f"✨ **Fișier curățat:** `{nume_nou}`")

                with col2:
                    st.download_button(
                        label="⬇️ Descarcă XML",
                        data=xml_data,
                        file_name=nume_nou,
                        mime="application/xml",
                        key=f"btn_{uploaded_file.name}",
                        use_container_width=True
                    )
            # ---------------------------

        except Exception as e:
            st.error(f"A apărut o eroare la procesarea fișierului {uploaded_file.name}: {e}")