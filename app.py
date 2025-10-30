# app.py
import streamlit as st
import requests

# 🔑 Clé API et URL
API_KEY = "JR14hHchfiwyVYB9T8TsscwWk4o75gJh"
API_URL = "https://api.mistral.ai/v1/chat/completions"

# Prompt système avec les caractéristiques d'Adrien
SYSTEM_PROMPT = """
Tu es une IA représentant uniquement Adrien Grandval.
-tu parles à la première personne comme si tu étais Adrien Grandval. 
-Tu réponds uniquement aux questions qui concernent Adrien.
- Si la question est en espagnol ou français ou toute autre langue, tu réponds en espagnol.
- Si la question n'a aucun rapport avec Adrien, réponds : 
  "Désolé — cette question n'est pas liée aux caractéristiques d'Adrien. Je ne répondrai pas."
- Ne donne aucune information non fournie.
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
  "near_city": "Marseille"
}
"""


# Fonction pour interroger Mistral
def ask_adrien(question: str):
    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
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
        return answer
    except Exception as e:
        return f"Erreur API : {e}"

# 🔹 Interface Streamlit
st.set_page_config(page_title="Assistant Adrien", page_icon="🤖")
st.title("Assistant-personnel d'Adrien (proxy Mistral)")

question = st.text_input("Pose une question sur Adrien :")

if st.button("Envoyer"):
    if question:
        answer = ask_adrien(question)
        st.markdown(f"**Réponse :** {answer}")
    else:
        st.warning("Veuillez entrer une question.")
