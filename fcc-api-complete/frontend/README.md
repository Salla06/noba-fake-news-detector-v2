# FCC Fake News Detector - Frontend

Application Streamlit connectée à l'API Flask.

## 🚀 Installation Locale

```bash
cd frontend
pip install -r requirements.txt
```

## ▶️ Lancement

```bash
streamlit run app.py
```

App sur: http://localhost:8501

## ⚙️ Configuration API

Éditer `.streamlit/secrets.toml`:

```toml
API_URL = "http://localhost:5000"  # Local
# API_URL = "https://votre-api.onrender.com"  # Production
```

## ☁️ Déploiement Streamlit Cloud

1. Créer compte [Streamlit Cloud](https://streamlit.io/cloud)
2. New app
3. Connecter GitHub repo
4. Main file: `frontend/app.py`
5. Dans Settings > Secrets, ajouter:
   ```toml
   API_URL = "https://votre-api.onrender.com"
   ```
6. Deploy

## 🎯 Fonctionnalités

- ✅ Analyse de texte
- ✅ Upload fichiers (TXT, PDF, DOCX)
- ✅ Support multilingue
- ✅ Historique
- ✅ Visualisations Plotly
- ✅ Export CSV
- ✅ Interface FR/EN

## 🔗 Connexion API

L'app se connecte automatiquement à l'API via `requests.post()`.

Vérifier état API dans sidebar (🟢/🔴).
