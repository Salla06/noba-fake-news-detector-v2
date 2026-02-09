# 🛡️ FCC Fake News Detector v2.0

Système intelligent de détection de fake news par Machine Learning avec architecture API.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red.svg)](https://streamlit.io/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table des Matières

- [Architecture](#-architecture)
- [Installation Rapide](#-installation-rapide)
- [Déploiement](#️-déploiement)
- [Utilisation](#-utilisation)
- [Technologies](#️-technologies)
- [Structure du Projet](#-structure-du-projet)
- [Fonctionnalités](#-fonctionnalités)

---

## 🏗️ Architecture

```
┌─────────────────────────────┐         ┌─────────────────────────────┐
│   FRONTEND (Streamlit)      │  HTTP   │   BACKEND (Flask API)       │
│   app_streamlit_v2.py       │◄──────►│   app.py                    │
│   Port 8501                 │  JSON   │   Port 5000                 │
│                             │         │                             │
│  • Interface utilisateur    │         │  • Modèle ML (.pkl)         │
│  • Traduction multilingue   │         │  • TF-IDF Vectorizer        │
│  • Upload fichiers          │         │  • API REST                 │
│  • Visualisations Plotly    │         │  • Endpoints /predict       │
└─────────────────────────────┘         └─────────────────────────────┘
         Streamlit Cloud                        Render.com
```

**Communication:** Requêtes HTTP POST avec JSON  
**URL API:** `https://fcc-fake-news-detector-v2.onrender.com`

---

## 🚀 Installation Rapide

### Prérequis

- Python 3.11+
- Git
- Compte GitHub
- Compte Streamlit Cloud (gratuit)
- Compte Render.com (gratuit)

### Installation Locale

```bash
# Cloner le repository
git clone https://github.com/noba-ibrahim/fcc-fake-news-detector-v2.git
cd fcc-fake-news-detector-v2

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application (en mode local avec API Render)
streamlit run app_streamlit_v2.py
```

L'application sera disponible sur: **http://localhost:8501**

> ⚠️ **Note:** En mode local, l'app utilise l'API déployée sur Render.  
> La première requête peut prendre 30-60s (API en veille).

---

## ☁️ Déploiement

### 1. Déployer le Backend (API Flask sur Render)

**Si pas encore fait:**

1. Créer un compte sur [Render.com](https://render.com)
2. **New +** → **Web Service**
3. Connecter ton repo GitHub: `noba-ibrahim/fcc-fake-news-detector-v2`
4. Configuration:
   - **Name:** `fcc-api`
   - **Root Directory:** `backend` (si backend séparé) ou laisser vide
   - **Build Command:**
     ```bash
     pip install -r backend/requirements.txt && python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
     ```
   - **Start Command:**
     ```bash
     gunicorn backend.app:app
     ```
   - **Instance Type:** Free

5. **Create Web Service**
6. Copier l'URL: `https://fcc-fake-news-detector-v2.onrender.com`

### 2. Déployer le Frontend (Streamlit Cloud)

1. Créer un compte sur [Streamlit Cloud](https://streamlit.io/cloud)
2. **New app**
3. Configuration:
   - **Repository:** `noba-ibrahim/fcc-fake-news-detector-v2`
   - **Branch:** `main`
   - **Main file path:** `app_streamlit_v2.py` ⚠️ **IMPORTANT**
   - **App URL:** `fcc-fake-news-detector-v2` (ou nom de ton choix)

4. **Deploy**

> 💡 **Pas besoin de secrets !** L'URL API est codée dans le fichier ligne 26.

5. Attendre 2-3 minutes → App déployée !

---

## 📖 Utilisation

### Via l'Interface Web

1. Ouvrir l'application Streamlit
2. **Page d'accueil:** Cliquer sur "DISCOVER THE SYSTEM"
3. **Onglet "Text Analysis":**
   - Coller un article
   - Sélectionner la langue (auto-détection par défaut)
   - Cliquer **"Analyze"**
   - Attendre le résultat (30-60s si première fois)

4. **Onglet "File Upload":**
   - Upload fichier (TXT, PDF, DOCX, XLSX)
   - Analyser automatiquement

5. **Onglet "History":**
   - Voir les analyses précédentes
   - Graphiques et statistiques
   - Export CSV

### Via l'API Directement

```bash
curl -X POST https://fcc-fake-news-detector-v2.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Breaking news! Shocking discovery that will change everything!"}'
```

**Réponse:**

```json
{
  "prediction": 0,
  "label": "FAKE",
  "confidence": 0.87,
  "probabilities": {
    "fake": 0.87,
    "real": 0.13
  },
  "metadata": {
    "text_length": 56,
    "clean_length": 45
  }
}
```

**Autres endpoints:**

- `GET /` - Informations API
- `GET /health` - État de santé
- `GET /info` - Informations modèle

---

## 🛠️ Technologies

### Frontend (Streamlit)

- **Streamlit** 1.29.0 - Framework web
- **Requests** 2.31.0 - Communication HTTP avec API
- **Plotly** 5.18.0 - Visualisations interactives
- **Pandas** 2.1.4 - Manipulation de données
- **deep-translator** 1.11.4 - Traduction multilingue
- **langdetect** 1.0.9 - Détection de langue
- **python-docx** 1.1.0 - Lecture fichiers Word
- **PyPDF2** 3.0.1 - Lecture fichiers PDF
- **openpyxl** 3.1.2 - Lecture fichiers Excel

### Backend (Flask API)

- **Flask** 3.0.0 - Framework API
- **flask-cors** 4.0.0 - Cross-Origin Resource Sharing
- **scikit-learn** 1.5.2 - Machine Learning
- **NLTK** 3.8.1 - Natural Language Processing
- **numpy** 1.26.2 - Calculs numériques
- **gunicorn** 21.2.0 - Serveur WSGI

### Machine Learning

- **Algorithme:** Logistic Regression
- **Vectoriseur:** TF-IDF (5000 features)
- **N-grams:** 1-2 (unigrammes + bigrammes)
- **Accuracy:** 98.34%
- **Dataset:** 32,456 articles (Kaggle)

---

## 📁 Structure du Projet

```
fcc-fake-news-detector-v2/
│
├── app_streamlit_v2.py        # Application Streamlit principale ⭐
├── utils.py                   # Fonctions utilitaires
├── requirements.txt           # Dépendances frontend
│
├── backend/                   # API Flask (optionnel si déjà déployé)
│   ├── models/
│   │   ├── fake_news_model.pkl
│   │   └── tfidf_vectorizer.pkl
│   ├── app.py
│   ├── requirements.txt
│   ├── Procfile
│   └── runtime.txt
│
├── docs/                      # Documentation (optionnel)
│   └── rapport.pdf
│
├── .gitignore
└── README.md                  # Ce fichier
```

### Fichiers Importants

| Fichier | Description |
|---------|-------------|
| `app_streamlit_v2.py` | Application Streamlit avec interface complète |
| `utils.py` | Fonctions de traduction, extraction de texte |
| `requirements.txt` | Dépendances Python pour Streamlit |
| `backend/app.py` | API Flask pour prédictions ML |

---

## 🎯 Fonctionnalités

### Interface Utilisateur

✅ **Page d'accueil Hero**
- Slideshow d'images animé
- Design professionnel IBM Plex
- Gradient bleu

✅ **Analyse de Texte**
- Zone de saisie large
- Auto-détection de langue
- Traduction automatique
- Résultats avec confidence score
- Graphiques interactifs Plotly

✅ **Upload de Fichiers**
- Support: TXT, PDF, DOCX, XLSX
- Extraction automatique du texte
- Analyse complète

✅ **Multilingue**
- 🇬🇧 English
- 🇫🇷 Français
- 🇪🇸 Español
- 🇸🇦 العربية
- 🇨🇳 中文

✅ **Historique**
- Sauvegarde des analyses
- Timeline interactive
- Statistiques détaillées
- Export CSV

✅ **Interface Bilingue**
- Français / English
- Changement à la volée
- Traductions complètes

### API Backend

✅ **Endpoint `/predict`**
- Analyse de texte ML
- Retour JSON structuré
- Gestion d'erreurs

✅ **Endpoint `/health`**
- Vérification état API
- Test modèle

✅ **Endpoint `/info`**
- Métadonnées modèle
- Specs techniques

---

## 📊 Performance

| Métrique | Valeur |
|----------|--------|
| **Accuracy** | 98.34% |
| **Precision** | 98.34% |
| **Recall** | 98.34% |
| **F1-Score** | 98.34% |
| **Temps de réponse** | < 2 secondes |
| **Articles traités** | 32,456 |
| **Taux de faux positifs** | 0.34% |
| **Taux de faux négatifs** | 1.32% |

### Matrice de Confusion

```
                Prédit FAKE    Prédit REAL
Vrai FAKE         5842            102
Vrai REAL           26           1758
```

---

## 🔗 Liens

- **GitHub Repository:** [noba-ibrahim/fcc-fake-news-detector-v2](https://github.com/noba-ibrahim/fcc-fake-news-detector-v2)
- **API Backend:** [https://fcc-fake-news-detector-v2.onrender.com](https://fcc-fake-news-detector-v2.onrender.com)
- **Application Live:** [Streamlit App](https://ton-app.streamlit.app)
- **Documentation:** [Wiki](https://github.com/noba-ibrahim/fcc-fake-news-detector-v2/wiki)

---

## 🐛 Dépannage

### Problème: "❌ Erreur API"

**Cause:** API Render en veille (plan gratuit)

**Solution:** 
- Attendre 30-60 secondes
- L'API se réveille automatiquement
- Réessayer l'analyse

### Problème: "Module not found"

**Cause:** Dépendances manquantes

**Solution:**
```bash
pip install -r requirements.txt
```

### Problème: App Streamlit ne se met pas à jour

**Solution:**
1. Streamlit Cloud → Settings
2. **Reboot app**
3. Attendre 2-3 minutes

---

## 👥 Équipe

**Développé par:** FCC Development Team  
**Date:** Février 2024  
**Version:** 2.0 (Architecture API)

**Contributeurs:**
- Ibrahim Noba (@noba-ibrahim) - Lead Developer

---

## 📄 Licence

MIT License - Voir fichier [LICENSE](LICENSE)

---

## 🙏 Remerciements

- Dataset: [Kaggle Fake News Dataset](https://www.kaggle.com/c/fake-news/)
- Icons: [Unsplash](https://unsplash.com/)
- Fonts: [IBM Plex](https://www.ibm.com/plex/)

---

## 📝 Notes de Version

### v2.0 (Février 2024)
- ✨ Architecture API séparée (Backend Flask + Frontend Streamlit)
- ✨ Support multilingue (5 langues)
- ✨ Upload de fichiers (TXT, PDF, DOCX, XLSX)
- ✨ Interface bilingue FR/EN
- ✨ Historique avec visualisations
- ✨ Design professionnel IBM Plex

### v1.0 (Janvier 2024)
- 🎉 Version initiale autonome
- 🎉 Modèle Logistic Regression
- 🎉 Interface Streamlit basique

---

**⭐ Si ce projet vous aide, n'hésitez pas à laisser une étoile sur GitHub !**
