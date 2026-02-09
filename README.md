# 🛡️ FCC Fake News Detector v2.0

Système intelligent de détection de fake news par Machine Learning avec architecture API.

## 📋 Table des Matières

- [Architecture](#architecture)
- [Installation Rapide](#installation-rapide)
- [Déploiement](#deploiement)
- [Utilisation](#utilisation)
- [Technologies](#technologies)

## 🏗️ Architecture

```
┌─────────────────────┐         ┌─────────────────────┐
│   FRONTEND          │  HTTP   │   BACKEND           │
│   Streamlit         │◄──────►│   Flask API         │
│   Port 8501         │  JSON   │   Port 5000         │
└─────────────────────┘         └─────────────────────┘
         │                               │
         │                               │
    Interface UI                  Modèle ML + TF-IDF
```

## 🚀 Installation Rapide

### Backend (API Flask)

```bash
cd backend
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"

# Copier les modèles dans backend/models/
# - fake_news_model.pkl
# - tfidf_vectorizer.pkl

python app.py
```

API disponible sur: http://localhost:5000

### Frontend (Streamlit)

```bash
cd frontend
pip install -r requirements.txt

# Configurer l'URL API dans .streamlit/secrets.toml
# API_URL = "http://localhost:5000"

streamlit run app.py
```

App disponible sur: http://localhost:8501

## ☁️ Déploiement

### Backend sur Render.com

1. Créer compte sur [Render](https://render.com)
2. **New Web Service**
3. Connecter votre repo GitHub
4. Configurer:
   - **Name:** fcc-api
   - **Root Directory:** `backend`
   - **Environment:** Python 3
   - **Build Command:** 
     ```bash
     pip install -r requirements.txt && python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
     ```
   - **Start Command:** `gunicorn app:app`
5. **Create Web Service**
6. Copier l'URL: `https://fcc-api-xxx.onrender.com`

### Frontend sur Streamlit Cloud

1. Créer compte sur [Streamlit Cloud](https://streamlit.io/cloud)
2. **New app**
3. Connecter votre repo GitHub
4. Configurer:
   - **Main file path:** `frontend/app.py`
5. Dans **Settings > Secrets**, ajouter:
   ```toml
   API_URL = "https://fcc-api-xxx.onrender.com"
   ```
6. **Deploy**

## 📖 Utilisation

### Via l'interface web

1. Ouvrir l'app Streamlit
2. Vérifier que l'API est connectée (🟢 dans sidebar)
3. Aller sur "Analyser Texte"
4. Coller un article
5. Cliquer "Analyser"
6. Voir le résultat (FAKE/REAL + confiance)

### Via l'API directement

```bash
curl -X POST https://fcc-api-xxx.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Breaking news! Shocking discovery!"}'
```

Réponse:
```json
{
  "prediction": 0,
  "label": "FAKE",
  "confidence": 0.87,
  "probabilities": {
    "fake": 0.87,
    "real": 0.13
  }
}
```

## 🛠️ Technologies

### Backend
- Python 3.11+
- Flask 3.0
- flask-cors 4.0
- scikit-learn 1.5.2
- NLTK 3.8.1
- gunicorn 21.2

### Frontend
- Python 3.11+
- Streamlit 1.29
- Requests 2.31
- Plotly 5.18
- Pandas 2.1

### Machine Learning
- **Modèle:** Logistic Regression
- **Vectoriseur:** TF-IDF (5000 features, n-grams 1-2)
- **Accuracy:** 98.34%
- **Dataset:** 32,456 articles

## 📁 Structure du Projet

```
fcc-fake-news-detector/
│
├── backend/                    # API Flask
│   ├── models/                # Modèles ML (.pkl)
│   ├── app.py                 # Application Flask
│   ├── requirements.txt       # Dépendances
│   ├── Procfile              # Config Render
│   └── README.md
│
├── frontend/                  # App Streamlit
│   ├── .streamlit/
│   │   ├── config.toml       # Config UI
│   │   └── secrets.toml      # URL API
│   ├── app.py                # Application Streamlit
│   ├── requirements.txt      # Dépendances
│   └── README.md
│
└── README.md                 # Ce fichier
```

## 🎯 Fonctionnalités

- ✅ Analyse de texte en temps réel
- ✅ Upload de fichiers (TXT, PDF, DOCX)
- ✅ Support multilingue (5 langues)
- ✅ Historique des analyses
- ✅ Visualisations interactives (Plotly)
- ✅ Export CSV
- ✅ Interface bilingue (FR/EN)
- ✅ API REST publique
- ✅ Documentation complète

## 📊 Performance

- **Accuracy:** 98.34%
- **Precision:** 98.34%
- **Recall:** 98.34%
- **F1-Score:** 98.34%
- **Temps de réponse:** < 2 secondes
- **Articles traités:** 32,456

## 🔗 Liens

- **GitHub:** https://github.com/noba-ibrahim/fcc-fake-news-detector
- **Documentation:** https://github.com/noba-ibrahim/fcc-fake-news-detector/wiki
- **Rapport PDF:** https://github.com/noba-ibrahim/fcc-fake-news-detector/blob/main/docs/rapport.pdf

## 👥 Équipe

Développé par FCC Development Team - Février 2024

## 📄 Licence

MIT License - Voir fichier LICENSE

---

**Note:** Ce projet utilise une architecture API séparée pour permettre la scalabilité et la réutilisabilité du modèle ML.
