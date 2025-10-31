# app.py
import streamlit as st
import requests

# 🔑 Clé API et URL
API_KEY = "JR14hHchfiwyVYB9T8TsscwWk4o75gJh"
API_URL = "https://api.mistral.ai/v1/chat/completions"

# 🧠 Prompt système avec les infos d’Adrien
SYSTEM_PROMPT = """
Tu es une IA représentant uniquement Adrien Grandval.
- Tu parles à la première personne comme si tu étais Adrien Grandval. 
- Tu réponds uniquement aux questions qui concernent Adrien.
- Si la question est en espagnol, français ou toute autre langue, tu réponds en espagnol.
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
  "brother_and_sister": 3_sisters",
  "sisters_names": juillette(9 anos) louise(25 anos) mathilde(29 anos (née le meme jour que Adrien))",
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
        answer = mistral_request(messages)
        return answer
    except Exception as e:
        return f"Erreur API : {e}"

# 🔹 Fonction pour traduire la réponse en français
def translate_to_french(text: str):
    messages = [
        {"role": "system", "content": "Tu es un traducteur. Traduis le texte suivant de l'espagnol vers le français, sans rien ajouter."},
        {"role": "user", "content": text}
    ]
    try:
        translation = mistral_request(messages)
        return translation
    except Exception as e:
        return f"Erreur de traduction : {e}"

# 🎨 Interface Streamlit
st.set_page_config(page_title="IA Adrien", page_icon="🤖")
st.title("")

question = st.text_input("Pose une question sur Adrien :")

if st.button("Envoyer"):
    if question:
        with st.spinner("Réflexion en cours..."):
            answer = ask_adrien(question)
            translation = translate_to_french(answer)
        st.markdown("### 🇪🇸 Réponse en espagnol :")
        st.write(answer)
        st.markdown("### 🇫🇷 Traduction en français :")
        st.write(translation)
    else:
        st.warning("Veuillez entrer une question.")
