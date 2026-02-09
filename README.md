# 🛡️ FCC Fake News Detector v2.0

Système de détection de fake news par Machine Learning avec architecture API.

## 🏗️ Architecture

```
Frontend (Streamlit)  ←→  Backend (Flask API)
     app.py          HTTP      Render.com
                     JSON
```

## 🚀 Déploiement Rapide

### Prérequis
- Backend API déjà déployé sur Render: `https://fcc-fake-news-detector-v2.onrender.com`

### Déployer sur Streamlit Cloud

1. Push ce code sur GitHub
2. Aller sur https://streamlit.io/cloud
3. **New app**
4. Configuration:
   - Repository: `ton-username/fcc-fake-news-detector-v2`
   - Branch: `main`
   - Main file: `app.py`
   - Python version: `3.11`
5. **Deploy**

## 📦 Fichiers

- `app.py` - Application Streamlit (utilise l'API)
- `utils.py` - Fonctions utilitaires (traduction, extraction fichiers)
- `requirements.txt` - Dépendances Python
- `.python-version` - Force Python 3.11

## 🎯 Fonctionnalités

✅ Page d'accueil avec hero section animée
✅ Analyse de texte multilingue (5 langues)
✅ Upload de fichiers (TXT, PDF, DOCX, XLSX)
✅ Historique des analyses avec graphiques
✅ Interface bilingue FR/EN
✅ Architecture API (Backend Flask séparé)

## 🔗 URLs

- **API Backend:** https://fcc-fake-news-detector-v2.onrender.com
- **Application:** (sera déployée sur Streamlit Cloud)

## ⚠️ Note

L'API Render gratuite se met en veille après 15min d'inactivité.
La première requête peut prendre 30-60 secondes (cold start).

## 📊 Performance

- **Accuracy:** 98.34%
- **Modèle:** Logistic Regression + TF-IDF
- **Dataset:** 32,456 articles
