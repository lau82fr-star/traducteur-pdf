import streamlit as st
import pypdf
from pdf2image import convert_from_bytes
import easyocr
import numpy as np
from deep_translator import GoogleTranslator

# Configuration de la page
st.set_page_config(page_title="Traducteur de PDF", page_icon="📄")
st.title("📄 Traducteur de PDF Scannés")

# Téléchargement du fichier
uploaded_file = st.file_uploader("Déposez votre PDF scanné ici", type=["pdf"])

if uploaded_file is not None:
    st.info("Analyse du PDF en cours... Merci de patienter.")
    try:
        # Conversion PDF en images
        images = convert_from_bytes(uploaded_file.read())
        
        # Initialisation du moteur de texte (OCR)
        reader = easyocr.Reader(['fr', 'en'], gpu=False)
        texte_complet = ""
        
        # Lecture des pages
        for i, image in enumerate(images):
            img_np = np.array(image)
            resultat = reader.readtext(img_np, detail=0)
            texte_complet += " ".join(resultat) + "\n\n"
        
        # Traduction
        st.success("Extraction réussie ! Traduction...")
        texte_traduit = GoogleTranslator(source='auto', target='fr').translate(texte_complet)
        
        # Affichage
        st.subheader("Résultat de la Traduction :")
        st.text_area("", texte_traduit, height=300)
        
    except Exception as e:
        st.error(f"Erreur : {e}")
