import streamlit as st
import gspread, json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import uuid
import pandas as pd
from difflib import SequenceMatcher
import google.generativeai as genai

# --- API Key ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash")

# --- Session and User ID ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

#user_id = st.text_input("Enter your name or email (optional)")
user_id = ''

# Google Sheets setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds_dict = {
    "type": st.secrets["type"],
    "project_id": st.secrets["project_id"],
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"],
    "client_email": st.secrets["client_email"],
    "client_id": st.secrets["client_id"],
    "auth_uri": st.secrets["auth_uri"],
    "token_uri": st.secrets["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["client_x509_cert_url"],
    "universe_domain": st.secrets["universe_domain"]
}


# Load service account from secrets
CREDS = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
GSHEET_CLIENT = gspread.authorize(CREDS)
SHEET = GSHEET_CLIENT.open("RecipeAppLog").sheet1

# --- Logging function ---
def log_to_sheet(action, value=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    SHEET.append_row([timestamp, user_id, st.session_state.session_id, action, value])

# --- Load dataset ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(r"C:\Users\T490\Downloads\Nigerian Palatable meals.csv")
        df.columns = df.columns.str.lower()
    except FileNotFoundError:
        df = pd.DataFrame(columns=["food_name", "ingredients", "procedures"])
        st.warning("⚠ Recipe dataset not found — will only use AI suggestions.")
    return df

df = load_data()

# --- Strict Recipe Matching ---
def get_matching_recipes(user_input, top_n=3):
    if df.empty:
        return []
    input_ingredients = [i.strip().lower() for i in user_input.split(",") if i.strip()]
    matches = []
    for _, row in df.iterrows():
        ingredients_str = str(row.iloc[1]).lower()
        if all(ing in ingredients_str for ing in input_ingredients):
            score = SequenceMatcher(None, user_input.lower(), ingredients_str).ratio()
            matches.append((score, row.iloc[0], row.iloc[1], row.iloc[2]))
    matches.sort(reverse=True, key=lambda x: x[0])
    return matches[:top_n]

# --- Streamlit UI ---
st.title("🥘 Broke Recipe Finder")
st.write("Enter what you have, and I’ll see what I can do...")

ingredients = st.text_input("Enter ingredients (e.g. rice, tomato, onion)")

if st.button("Help My Life!!!"):
    if not ingredients.strip():
        st.warning("Please enter some ingredients.")
    else:
        log_to_sheet("button_click", "Help My Life!!!")
        log_to_sheet("text_input", ingredients)

        # Step 1: Dataset grounding
        top_recipes = get_matching_recipes(ingredients)

        if top_recipes:
            st.subheader("Top Matches from Dataset:")
            for idx, (_, title, ing, steps) in enumerate(top_recipes, start=1):
                with st.expander(f"{idx}. {title}"):
                    st.write(f"**Ingredients:** {ing}")
                    st.write(f"**Steps:** {steps}")
                    # Log each recipe selection
                    if st.button(f"Use Recipe: {title}", key=f"use_{idx}"):
                        log_to_sheet("button_click", f"Use Recipe: {title}")
                        st.success(f"You selected: {title}")

            # Give AI context from matches
            context = "\n\n".join([f"Recipe: {t}\nIngredients: {i}\nSteps: {s}"
                                   for _, t, i, s in top_recipes])
            prompt = (
                f"I have the following ingredients: {ingredients}. "
                f"Here are some real recipes from my dataset:\n{context}\n\n"
                f"Suggest either the best single option or a creative combination, "
                f"with a name, ingredients, and step-by-step instructions."
            )
        else:
            st.info("No exact dataset matches found — going full creative mode!")
            prompt = (
                f"I have these ingredients: {ingredients}. "
                f"Suggest a creative recipe with name, ingredients, and steps."
            )

        # Step 2: AI generation
        try:
            response = model.generate_content(prompt)
            recipe_text = response.text
            st.subheader("💡 Suggested Recipe")
            st.markdown(recipe_text)
            # Log AI suggestion
            log_to_sheet("AI_recipe", recipe_text)
        except Exception as e:
            st.error(f"Error: {e}")
