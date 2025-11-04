# app.py
import streamlit as st
import requests
import time

# 🔑 Clé API et URL
API_KEY = "SoPniM3684OVJVORqIR4ut1AKuiWdj9k"
API_URL = "https://api.mistral.ai/v1/chat/completions"

# 🧠 Prompt système avec les infos d’Adrien
SYSTEM_PROMPT = """
Tu es une IA représentant uniquement Adrien Grandval.
- Tu parles à la première personne comme si tu étais Adrien Grandval. 
- Tu réponds uniquement aux questions qui concernent Adrien.
- Si la question est en espagnol, français ou toute autre langue, tu réponds en espagnol.
- Ne poses pas de questions supplementaire après avoir repond a une question.
- Si la question n'a aucun rapport avec Adrien, réponds : 
  "Désolé — cette question n'est pas liée aux caractéristiques d'Adrien. Je ne répondrai pas."
- Ne donne aucune information non fournie.
- Important : Lorsque quelqu'un te demande "qué te gustaría en la vida", tu dois inclure 
  "que quieres ser trader o investigador en cancerología y biología".
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
  "brother_and_sister": "3 sisters",
  "sisters_names": "Juliette (9 ans), Louise (25 ans), Mathilde (29 ans, née le même jour qu’Adrien)",
  "piano piece": "Debussy nocturne, morceau compliqué",
  "eyes color": "blue and gray",
  "pets": "1 dog, 2 cats, turtles and fishes",
}
"""

# 🔹 Fonction pour interroger Mistral
def mistral_request(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-small-latest",
        "messages": messages
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]

# 🔹 Fonction pour poser une question à Adrien
def ask_adrien(question: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]
    try:
        return mistral_request(messages)
    except Exception as e:
        return f"Erreur API : {e}"

# 🔹 Fonction pour traduire la réponse en français
def translate_to_french(text: str):
    messages = [
        {"role": "system", "content": "Tu es un traducteur. Traduis le texte suivant de l'espagnol vers le français, sans rien ajouter."},
        {"role": "user", "content": text}
    ]
    try:
        return mistral_request(messages)
    except Exception as e:
        return f"Erreur de traduction : {e}"

# 🎨 Interface Streamlit
st.set_page_config(page_title="IA Espagnol", page_icon="🤖")
st.title("mi presentation original :")

# Initialisation des variables de session
if "answer" not in st.session_state:
    st.session_state.answer = None
if "translation" not in st.session_state:
    st.session_state.translation = None

question = st.text_input("Pose une question sur Adrien :")

if st.button("Envoyer"):
    if question:
        with st.spinner("Réflexion en cours..."):
            answer = ask_adrien(question)
        st.session_state.answer = answer
        st.session_state.translation = None  # reset la trad
    else:
        st.warning("Veuillez entrer une question.")

# ✅ Affichage de la réponse espagnole si dispo
if st.session_state.answer:
    st.markdown("### 🇪🇸 Réponse en espagnol :")
    st.write(st.session_state.answer)

    # Bouton pour afficher la traduction
    if st.session_state.translation is None:
        if st.button("💬 Afficher la traduction en français"):
            with st.spinner("Traduction en cours..."):
                time.sleep(0.8)
                st.session_state.translation = translate_to_french(st.session_state.answer)

    # ✅ Afficher la traduction si elle existe déjà
    if st.session_state.translation:
        st.markdown("### 🇫🇷 Traduction en français :")
        st.write(st.session_state.translation)





