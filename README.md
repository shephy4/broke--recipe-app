# 🥘 Broke Recipe App



Sometimes you have foodstuffs, but you just can't think of what to eat or prepare.  
It’s even worse when you have **limited ingredients**, your brain goes blank.  
Personally, I’d rather stay hungry than try to figure it out.  
And if you ask me, “What should we cook?” … I might just take it as a declaration of war. 😂

So… I built **Broke Recipe App** — a simple tool that **generates Nigerian meal ideas** from the ingredients you already have.  
All you need to do is list your ingredients (comma separated), and it will suggest one or more Nigerian dishes for you.

---

## 🚀 Features
- 🍛 **Generates meal ideas** from your ingredients.
- 🇳🇬 Focused on **Nigerian dishes**.
- ⚡ Built with **Streamlit** for instant results.
- 📜 **Logs your searches** to Google Sheets for tracking.

---

## 🛠️ Tech Stack
- **Python**
- **Streamlit** (Frontend)
- **Google Sheets API** (Logging)
- **Gemini API** (AI meal suggestions)
- **gspread** (Google Sheets integration)

---

## 📦 Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/broke-recipe-app.git
   cd broke-recipe-app
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```


3. **Set up your secrets**
  Create a .streamlit/secrets.toml file and add:
    ```bash
    GEMINI_API_KEY = "your-gemini-api-key"

    [google_service_account]
    type = "service_account"
    project_id = "your-project-id"
    private_key_id = "your-private-key-id"
    private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
    client_email = "your-service-account-email"
    client_id = "your-client-id"
    auth_uri = "https://accounts.google.com/o/oauth2/auth"
    token_uri = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
    client_x509_cert_url = "your-cert-url"
    universe_domain = "googleapis.com"
    ```
▶️ Usage

Run the app locally:

streamlit run broke_recipe_streamlit_v2.py


Enter your ingredients, hit **Help my life!!!**, and enjoy your food inspiration! 🍲

🌍 Live Demo

You can try it here: https://broke--recipe-app.streamlit.app/


📜 License

This project is licensed under the [MIT License](LICENSE).

✨ Author

Built with ❤️ by Oluwasefunmi Bamidele

