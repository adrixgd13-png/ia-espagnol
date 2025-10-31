# app.py
import streamlit as st
import requests
from googletrans import Translator
import time

# 🔑 Clé API et URL
API_KEY = "JR14hHchfiwyVYB9T8TsscwWk4o75gJh"
API_URL = "https://api.mistral.ai/v1/chat/completions"

translator = Translator()

# Prompt système avec les caractéristiques d'Adrien
SYSTEM_PROMPT = """
Tu es une IA représentant uniquement Adrien Grandval.
- Tu parles à la première personne comme si tu étais Adrien Grandval.
- Tu réponds uniquement aux questions qui concernent Adrien.
- Si la question est en espagnol, tu réponds en espagnol.
- Si la question n'a aucun rapport avec Adrien, réponds : 
  "Désolé — cette question n'est pas liée aux caractéristiques d'Adrien. Je ne répondrai pas."
- Si la question contient des fautes d'orthographe, tu les corriges avant de répondre.
Caractéristiques d'Adrien : 
{
  "name": "Adrien",
  "family_name": "Grandval",
  "birth_year": 2011,
  "age": 14,
  "height_cm": 181,
  "favorite_color": "bleu",
  "likes": ["piano", "montagne", "gaming (jeux vidéo)", "codage"],
  "favorite_movie": "Interstellar",
  "favorite_food": "sushi",
  "city": "Aubagne",
  "near_city": "Marseille",
  "future_goal": "convertirse en trader o investigador en biología y cáncer"
}
"""

# Fonction pour corriger le texte avec Mistral
def correct_text(text):
    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": "Corrige uniquement les fautes dans ce texte sans rien ajouter d'autre."},
            {"role": "user", "content": text}
        ]
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        corrected = data["choices"][0]["message"]["content"].strip()
        return corrected
    except Exception as e:
        return text  # si erreur, on garde le texte original

# Fonction principale
def ask_adrien(question: str):
    corrected = correct_text(question)
    time.sleep(1)

    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": corrected}
        ]
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        answer = data["choices"][0]["message"]["content"]

        # Traduction FR
        trad_fr = translator.translate(answer, dest='fr').text

        return corrected, answer, trad_fr

    except Exception as e:
        return question, f"Erreur API : {e}", ""


# 🔹 Interface Streamlit
st.set_page_config(page_title="IA Adrien", page_icon="🤖")
st.title("Assistant-personnel d'Adrien (avec correction automatique)")

question = st.text_input("Pose une question sur Adrien :")

if st.button("Envoyer"):
    if question:
        corrected, answer, trad_fr = ask_adrien(question)
        if corrected != question:
            st.info(f"✅ Phrase corrigée : {corrected}")
        st.markdown(f"### 🇪🇸 Réponse :\n{answer}")
        st.markdown(f"### 🇫🇷 Traduction :\n{trad_fr}")
    else:
        st.warning("Veuillez entrer une question.")
