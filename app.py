import streamlit as st
from pdf2image import convert_from_bytes
import easyocr
import numpy as np
from deep_translator import GoogleTranslator, MyMemoryTranslator

st.set_page_config(page_title="Traducteur de PDF", page_icon="📄", layout="centered")
st.title("📄 Traducteur de PDF Scannés")
st.write("Téléchargez un PDF scanné pour extraire et traduire le texte automatiquement.")

@st.cache_resource
def get_reader():
    return easyocr.Reader(["fr", "en"], gpu=False)

@st.cache_data
def translate_text(texte, target="fr", source="auto"):
    traducteurs = [
        ("MyMemoryTranslator", lambda: MyMemoryTranslator(source=source, target=target)),
        ("GoogleTranslator", lambda: GoogleTranslator(source=source, target=target)),
    ]

    for nom, create in traducteurs:
        try:
            traducteur = create()
            return traducteur.translate(texte)
        except Exception as erreur:
            st.warning(f"{nom} indisponible : {erreur}")

    raise RuntimeError("Impossible de traduire le texte pour le moment.")

uploaded_file = st.file_uploader("Déposez votre PDF scanné ici", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Analyse du PDF en cours..."):
        try:
            images = convert_from_bytes(uploaded_file.read())
            if not images:
                st.error("Aucune page trouvée dans le PDF.")
            else:
                reader = get_reader()
                pages_text = []

                for image in images:
                    texte_page = reader.readtext(np.array(image), detail=0)
                    if texte_page:
                        pages_text.append(" ".join(texte_page))

                texte_complet = "\n\n".join(pages_text).strip()

                if not texte_complet:
                    st.warning("Aucun texte reconnu dans le PDF.")
                else:
                    st.subheader("Texte OCR extrait")
                    st.text_area("", texte_complet, height=250)

                    st.info("Traduction en cours...")
                    texte_traduit = translate_text(texte_complet)

                    st.subheader("Résultat de la traduction")
                    st.text_area("", texte_traduit, height=300)

        except Exception as e:
            st.error(f"Erreur : {e}")
