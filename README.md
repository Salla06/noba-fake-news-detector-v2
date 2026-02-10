# Détecteur de Fake News FCC

**Système Avancé de Détection de Fake News par Apprentissage Automatique**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Précision](https://img.shields.io/badge/Précision-98.34%25-brightgreen)
![Statut](https://img.shields.io/badge/Statut-Production-success)

---

## Table des Matières

- [Vue d'Ensemble](#vue-densemble)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Stack Technologique](#stack-technologique)
- [Métriques de Performance](#métriques-de-performance)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Documentation API](#documentation-api)
- [Déploiement](#déploiement)
- [Structure du Projet](#structure-du-projet)
- [Entraînement du Modèle](#entraînement-du-modèle)
- [Contribution](#contribution)
- [Licence](#licence)
- [Contact](#contact)

---

## Vue d'Ensemble

Le **Détecteur de Fake News FCC** est une application web prête pour la production qui exploite l'apprentissage automatique pour identifier la désinformation et les fake news avec une précision de 98,34%. Le système utilise le Traitement Automatique du Langage Naturel (NLP) et la Régression Logistique pour analyser le texte d'un article et le classifier comme fake ou fiable.

### Points Clés

- **Haute Précision :** 98,34% sur un ensemble de test de 7 728 articles
- **Support Multilingue :** Traduction automatique depuis 5 langues (Anglais, Français, Espagnol, Arabe, Chinois)
- **Méthodes d'Entrée Multiples :** Texte direct, extraction depuis URL, upload de fichier (TXT, PDF, DOCX, XLSX)
- **Analyse en Temps Réel :** Résultats livrés en moins de 2 secondes
- **Interface Professionnelle :** Interface web moderne, bilingue (FR/EN)
- **API REST :** API complètement documentée pour intégration
- **Aucune Configuration Requise :** Déployé sur des plateformes cloud avec tiers gratuits

### Démo en Direct

- **Application Web :** [https://fcc-fake-news-detector.streamlit.app](https://fcc-fake-news-detector.streamlit.app)
- **Point de Terminaison API :** [https://fcc-fake-news-detector-v2.onrender.com](https://fcc-fake-news-detector-v2.onrender.com)

---

## Fonctionnalités

### Fonctionnalités Principales

**Analyse de Texte**
- Analyser du texte d'article directement via copier-coller
- Détection automatique de la langue (5 langues supportées)
- Traduction en temps réel vers l'anglais pour les textes non-anglais
- Aperçu de la traduction avec comparaison du texte original

**Extraction depuis URL**
- Extraire le texte depuis des pages web (HTML)
- Parser des documents PDF depuis des URLs
- Support pour les fichiers DOCX hébergés en ligne
- Nettoyage et formatage automatique du contenu

**Upload de Fichier**
- Support pour plusieurs formats de fichiers : TXT, PDF, DOCX, XLSX
- Extraction automatique du texte
- Capacité de traitement par lots

**Résultats d'Analyse**
- Classification binaire : FAKE ou REAL
- Score de confiance (pourcentage)
- Visualisation de la distribution des probabilités
- Graphiques interactifs Plotly (jauge, barres, timeline)
- Historique des analyses avec statistiques

### Interface Utilisateur

**Design Professionnel**
- Section hero avec diaporama dynamique
- Typographie IBM Plex Sans
- Palette de couleurs dégradées (bleu/rouge)
- Layout responsive pour toutes les tailles d'écran
- Interface bilingue (Français/Anglais)

**Composants Interactifs**
- 5 onglets principaux : Analyse de Texte, Upload de Fichier, Historique, Information, Documentation
- Sections extensibles pour une meilleure organisation
- Onglets internes pour les exemples de code et guides
- Changement de langue en temps réel

**Visualisation**
- Jauge de confiance (0-100%)
- Graphique en barres de distribution des probabilités
- Graphique d'analyse chronologique
- Tableau de bord des statistiques d'historique

---

## Architecture

L'application suit une **architecture microservices** avec une séparation claire entre les composants frontend et backend.

### Architecture de Haut Niveau

```
┌──────────────────┐
│ Navigateur User  │
│  (Côté client)   │
└────────┬─────────┘
         │ HTTPS
         ↓
┌──────────────────────────────────────────────┐
│        FRONTEND (Streamlit Cloud)            │
│  ┌────────────────────────────────────────┐  │
│  │  app.py                                │  │
│  │  - Interface utilisateur               │  │
│  │  - Gestion des entrées                 │  │
│  │  - Visualisation des résultats         │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │  utils.py                              │  │
│  │  - Traduction de langues               │  │
│  │  - Extraction depuis URL               │  │
│  │  - Traitement de fichiers              │  │
│  └────────────────────────────────────────┘  │
└────────┬─────────────────────────────────────┘
         │ HTTP POST
         │ JSON: {"text": "contenu article..."}
         ↓
┌──────────────────────────────────────────────┐
│         BACKEND (Render.com)                 │
│  ┌────────────────────────────────────────┐  │
│  │  API REST Flask                        │  │
│  │  - Endpoint /predict                   │  │
│  │  - Prétraitement du texte              │  │
│  │  - Inférence du modèle                 │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │  Modèles ML (.pkl)                     │  │
│  │  - Régression Logistique               │  │
│  │  - Vectorizer TF-IDF                   │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

### Détails des Composants

**Frontend (Streamlit)**
- **Hébergement :** Streamlit Cloud (tier gratuit)
- **Framework :** Streamlit 1.29.0
- **Responsabilités :**
  - Rendu de l'interface utilisateur
  - Validation des entrées
  - Communication avec l'API
  - Visualisation des résultats
  - Gestion de session

**Backend (Flask)**
- **Hébergement :** Render.com (tier gratuit)
- **Framework :** Flask 3.0
- **Serveur :** Gunicorn
- **Responsabilités :**
  - Points de terminaison de l'API REST
  - Prétraitement du texte
  - Inférence du modèle ML
  - Formatage de la réponse JSON

**Protocole de Communication**
- **Méthode :** HTTP POST
- **Format :** JSON
- **Authentification :** Aucune (API publique)
- **Timeout :** 60 secondes (tient compte du cold start)

---

## Stack Technologique

### Apprentissage Automatique

| Composant | Technologie | Version | Objectif |
|-----------|-----------|---------|---------|
| Algorithme | Régression Logistique | scikit-learn 1.5.2 | Classification binaire |
| Vectorisation | TF-IDF | scikit-learn 1.5.2 | Texte vers features numériques |
| Traitement Texte | NLTK | 3.8.1 | Tokenisation, lemmatisation |
| Framework | scikit-learn | 1.5.2 | Entraînement & inférence |

### Backend

| Composant | Technologie | Version | Objectif |
|-----------|-----------|---------|---------|
| Framework | Flask | 3.0.0 | API REST |
| Serveur WSGI | Gunicorn | 21.2.0 | Serveur de production |
| CORS | flask-cors | 4.0.0 | Requêtes cross-origin |
| Déploiement | Render.com | - | Hébergement cloud |

### Frontend

| Composant | Technologie | Version | Objectif |
|-----------|-----------|---------|---------|
| Framework | Streamlit | 1.29.0 | Interface web |
| Visualisation | Plotly | 5.18.0 | Graphiques interactifs |
| Gestion Données | Pandas | 2.1.4 | Manipulation de données |
| Traduction | deep-translator | 1.11.4 | API Google Translate |
| Détection Langue | langdetect | 1.0.9 | Détection auto de langue |
| Web Scraping | BeautifulSoup4 | 4.12.2 | Parsing HTML |
| Traitement PDF | PyPDF2 | 3.0.1 | Extraction texte PDF |
| Traitement DOCX | python-docx | 1.1.0 | Gestion fichiers Word |
| Traitement Excel | openpyxl | 3.1.2 | Gestion fichiers Excel |
| Requêtes HTTP | requests | 2.31.0 | Communication API |
| Déploiement | Streamlit Cloud | - | Hébergement cloud |

### Outils de Développement

- **Contrôle de Version :** Git & GitHub
- **Version Python :** 3.11
- **Gestionnaire de Paquets :** pip
- **Environnement :** Environnement virtuel (venv)

---

## Métriques de Performance

### Performance du Modèle

Le modèle a été entraîné sur le Dataset Kaggle Fake News et évalué sur un ensemble de test séparé.

| Métrique | Score | Description |
|--------|-------|-------------|
| **Précision (Accuracy)** | 98,34% | Prédictions correctes globales |
| **Précision (Precision)** | 98,34% | Vrais positifs / (Vrais positifs + Faux positifs) |
| **Rappel (Recall)** | 98,34% | Vrais positifs / (Vrais positifs + Faux négatifs) |
| **Score F1** | 98,34% | Moyenne harmonique de précision et rappel |

### Statistiques du Dataset

| Catégorie | Nombre | Pourcentage |
|----------|-------|------------|
| **Articles Totaux** | 32 456 | 100% |
| **Ensemble d'Entraînement** | 24 728 | 76% |
| **Ensemble de Test** | 7 728 | 24% |
| **Fake News** | 23 481 | 72,3% |
| **Vraies News** | 8 975 | 27,7% |

### Matrice de Confusion

```
                Prédit
              RÉEL    FAKE
Réel RÉEL     2150     32
Réel FAKE       98   5498
```

**Interprétation :**
- **Vrais Positifs (Réel → Réel) :** 2 150
- **Vrais Négatifs (Fake → Fake) :** 5 498
- **Faux Positifs (Réel → Fake) :** 32 (faible taux de fausse alerte)
- **Faux Négatifs (Fake → Réel) :** 98 (fake news manquées)

### Ingénierie des Features

- **Méthode de Vectorisation :** TF-IDF (Term Frequency-Inverse Document Frequency)
- **Nombre de Features :** 5 000
- **N-grammes :** (1, 2) - unigrammes et bigrammes
- **Fréquence Document Min :** 1
- **Fréquence Document Max :** 0,8 (80%)
- **Normalisation :** L2

---

## Installation

### Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.11+** - [Télécharger ici](https://www.python.org/downloads/)
- **Git** - [Télécharger ici](https://git-scm.com/downloads)
- **pip** - Gestionnaire de paquets Python (inclus avec Python)

### Configuration pour Développement Local

#### 1. Cloner le Dépôt

```bash
git clone https://github.com/VOTRE-USERNAME/fcc-fake-news-detector.git
cd fcc-fake-news-detector
```

#### 2. Créer un Environnement Virtuel

**Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux :**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Installer les Dépendances

**Backend :**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend :**
```bash
cd frontend
pip install -r requirements.txt
```

#### 4. Télécharger les Ressources NLTK

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
```

#### 5. Lancer Localement

**Démarrer l'API Backend (Terminal 1) :**
```bash
cd backend
python app.py
```
L'API sera disponible à `http://localhost:5000`

**Démarrer le Frontend (Terminal 2) :**
```bash
cd frontend
streamlit run app.py
```
L'interface web s'ouvrira automatiquement à `http://localhost:8501`

---

## Utilisation

### Interface Web

**Méthode 1 : Analyse de Texte Direct**

1. Naviguez vers l'application web
2. Cliquez sur "DÉCOUVRIR LE SYSTÈME" sur la page hero
3. Allez dans l'onglet "Analyse de Texte"
4. Sélectionnez la méthode d'entrée "Texte"
5. Collez le texte de l'article dans la zone de texte
6. Sélectionnez la langue source (ou utilisez auto-détection)
7. Cliquez sur "Analyser"
8. Visualisez les résultats avec score de confiance et graphiques

**Méthode 2 : Extraction depuis URL**

1. Allez dans l'onglet "Analyse de Texte"
2. Sélectionnez la méthode d'entrée "URL"
3. Collez l'URL de l'article (page web, PDF, ou DOCX)
4. Le texte est extrait automatiquement
5. Cliquez sur "Analyser"
6. Vérifiez le texte extrait et les résultats

**Méthode 3 : Upload de Fichier**

1. Allez dans l'onglet "Téléchargement de Fichier"
2. Cliquez sur "Parcourir les fichiers"
3. Sélectionnez un fichier (.txt, .pdf, .docx, .xlsx)
4. Choisissez la langue du document
5. Cliquez sur "Analyser le Fichier"
6. Le texte est extrait et analysé automatiquement

**Consulter l'Historique**

1. Allez dans l'onglet "Historique de l'Analyse"
2. Visualisez toutes vos analyses précédentes
3. Consultez les statistiques (analyses totales, pourcentage de fake)
4. Explorez le graphique chronologique interactif
5. Exportez l'historique en CSV (si nécessaire)

### Utilisation de l'API

L'API REST peut être intégrée dans d'autres applications.

**Endpoint :** `POST /predict`

**Requête :**
```json
{
  "text": "Votre texte d'article ici..."
}
```

**Réponse :**
```json
{
  "prediction": 0,
  "label": "REAL",
  "confidence": 0.9234,
  "probabilities": {
    "real": 0.9234,
    "fake": 0.0766
  },
  "text_length": 1523,
  "cleaned_length": 892
}
```

**Exemple Python :**

```python
import requests

url = "https://fcc-fake-news-detector-v2.onrender.com/predict"
payload = {
    "text": "Breaking news! Les scientifiques ont découvert une vérité choquante!"
}

response = requests.post(url, json=payload, timeout=60)
resultat = response.json()

print(f"Label: {resultat['label']}")
print(f"Confiance: {resultat['confidence']:.2%}")
```

**Exemple cURL :**

```bash
curl -X POST https://fcc-fake-news-detector-v2.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Votre texte d article ici"}'
```

---

## Documentation API

### Points de Terminaison

#### 1. Vérification de Santé

**GET /**

Retourne les informations et le statut de l'API.

**Réponse :**
```json
{
  "message": "FCC Fake News Detector API",
  "version": "2.0",
  "status": "operational",
  "endpoints": {
    "/": "Informations API",
    "/health": "Vérification de santé",
    "/predict": "Prédiction fake news"
  }
}
```

#### 2. Statut de Santé

**GET /health**

Vérifie si l'API et les modèles ML sont chargés correctement.

**Réponse (Succès) :**
```json
{
  "status": "healthy",
  "model": "loaded"
}
```

**Réponse (Erreur) :**
```json
{
  "status": "unhealthy",
  "model": "not loaded"
}
```

**Code de Statut :** 200 (sain) ou 500 (non sain)

#### 3. Prédiction

**POST /predict**

Analyse le texte et retourne la prédiction de fake news.

**Corps de la Requête :**
```json
{
  "text": "Texte de l'article à analyser (minimum 10 caractères)"
}
```

**Réponse (Succès) :**
```json
{
  "prediction": 1,
  "label": "FAKE",
  "confidence": 0.8534,
  "probabilities": {
    "real": 0.1466,
    "fake": 0.8534
  },
  "text_length": 245,
  "cleaned_length": 178
}
```

**Champs de Réponse :**
- `prediction` : 0 (RÉEL) ou 1 (FAKE)
- `label` : "REAL" ou "FAKE"
- `confidence` : Probabilité maximale (0-1)
- `probabilities.real` : Probabilité d'être réel (0-1)
- `probabilities.fake` : Probabilité d'être fake (0-1)
- `text_length` : Nombre de caractères du texte original
- `cleaned_length` : Nombre de caractères du texte traité

**Réponses d'Erreur :**

*Champ texte manquant :*
```json
{
  "error": "Champ 'text' manquant dans la requête"
}
```
**Code de Statut :** 400

*Texte trop court :*
```json
{
  "error": "Texte trop court (minimum 10 caractères)"
}
```
**Code de Statut :** 400

*Erreur interne :*
```json
{
  "error": "Erreur interne du serveur",
  "details": "Description de l'erreur"
}
```
**Code de Statut :** 500

### Limitation de Débit

L'API de tier gratuit n'a pas de limitation de débit explicite, mais veuillez l'utiliser de manière responsable :
- **Recommandé :** Max 60 requêtes par minute
- **Timeout :** 60 secondes par requête
- **Cold Start :** La première requête après 15 minutes d'inactivité peut prendre 30-60 secondes

### Bonnes Pratiques

1. **Longueur de Texte :** Fournir au moins 50 caractères pour une meilleure précision
2. **Gestion d'Erreurs :** Toujours implémenter le timeout et la gestion d'erreurs
3. **Logique de Réessai :** Implémenter un backoff exponentiel pour les requêtes échouées
4. **Mise en Cache :** Mettre en cache les résultats pour un texte identique afin de réduire les appels API

---

## Déploiement

### Déploiement Backend (Render.com)

**Prérequis :**
- Compte GitHub
- Compte Render.com (gratuit)

**Étapes :**

1. **Pousser le Code vers GitHub**
```bash
cd backend
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/VOTRE-USERNAME/fcc-backend.git
git push -u origin main
```

2. **Déployer sur Render**
   - Allez sur [Render.com](https://render.com)
   - Cliquez sur "New +" → "Web Service"
   - Connectez le dépôt GitHub
   - Configurez :
     - **Nom :** fcc-fake-news-backend
     - **Runtime :** Python 3
     - **Commande de Build :** `pip install -r requirements.txt`
     - **Commande de Démarrage :** `gunicorn app:app`
     - **Plan :** Gratuit
   - Cliquez sur "Create Web Service"

3. **Attendre le Déploiement**
   - Déploiement initial : 5-10 minutes
   - Déploiements suivants : 2-3 minutes

4. **Obtenir l'URL de l'API**
   - Format : `https://votre-nom-service.onrender.com`
   - Tester : `curl https://votre-nom-service.onrender.com/health`

### Déploiement Frontend (Streamlit Cloud)

**Prérequis :**
- Compte GitHub
- Compte Streamlit Cloud (gratuit)

**Étapes :**

1. **Mettre à Jour l'URL de l'API**

Éditez `frontend/app.py` ligne 26 :
```python
API_URL = "https://votre-url-render-reelle.onrender.com"
```

2. **Pousser le Code vers GitHub**
```bash
cd frontend
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/VOTRE-USERNAME/fcc-frontend.git
git push -u origin main
```

3. **Déployer sur Streamlit Cloud**
   - Allez sur [Streamlit Cloud](https://streamlit.io/cloud)
   - Cliquez sur "New app"
   - Configurez :
     - **Dépôt :** VOTRE-USERNAME/fcc-frontend
     - **Branche :** main
     - **Chemin du fichier principal :** app.py
     - **Version Python :** 3.11 (si disponible)
   - Cliquez sur "Deploy"

4. **Attendre le Déploiement**
   - Déploiement initial : 3-5 minutes
   - Redéploiements automatiques à chaque push GitHub

5. **Accéder à l'Application**
   - URL : `https://votre-nom-app.streamlit.app`

### Variables d'Environnement

**Backend (Optionnel) :**
Aucune variable d'environnement requise pour le déploiement de base.

**Frontend :**
L'URL de l'API est codée en dur dans `app.py`. Pour la production, considérez l'utilisation des secrets Streamlit :

Créez `.streamlit/secrets.toml` :
```toml
API_URL = "https://votre-backend.onrender.com"
```

Mettez à jour `app.py` :
```python
API_URL = st.secrets["API_URL"]
```

---

## Structure du Projet

```
fcc-fake-news-detector/
│
├── backend/                      # API Flask (Backend)
│   ├── app.py                   # Application API principale
│   ├── model.pkl                # Modèle Régression Logistique entraîné
│   ├── vectorizer.pkl           # Vectorizer TF-IDF
│   ├── requirements.txt         # Dépendances Python
│   └── README.md               # Documentation backend
│
├── frontend/                     # Application Streamlit (Frontend)
│   ├── app.py                   # Application Streamlit principale (1837 lignes)
│   ├── utils.py                 # Fonctions utilitaires (121 lignes)
│   ├── requirements.txt         # Dépendances Python
│   ├── .python-version          # Spécification version Python (3.11)
│   └── README.md               # Documentation frontend
│
├── model_training/               # Scripts d'entraînement du modèle
│   ├── train_model.py           # Pipeline d'entraînement complet
│   ├── data/                    # Répertoire du dataset
│   │   └── train.csv           # Dataset Kaggle Fake News
│   └── notebooks/              # Notebooks Jupyter (optionnel)
│       └── EDA.ipynb           # Analyse Exploratoire des Données
│
├── docs/                         # Documentation
│   ├── API.md                   # Documentation API
│   ├── DEPLOYMENT.md            # Guide de déploiement
│   └── ARCHITECTURE.md          # Détails d'architecture
│
├── .gitignore                    # Fichier d'ignore Git
├── LICENSE                       # Licence MIT
└── README.md                     # Ce fichier
```

### Description des Fichiers

**Fichiers Backend :**
- `app.py` : API REST Flask avec endpoint `/predict`, chargement du modèle et prétraitement du texte
- `model.pkl` : Modèle de Régression Logistique sérialisé (5 MB)
- `vectorizer.pkl` : Vectorizer TF-IDF sérialisé (10 MB)
- `requirements.txt` : Dépendances Flask, scikit-learn, nltk, gunicorn

**Fichiers Frontend :**
- `app.py` : Application Streamlit principale avec 5 onglets, visualisations et intégration API
- `utils.py` : Fonctions helper pour traduction, extraction URL et traitement de fichiers
- `.python-version` : Force Python 3.11 pour le déploiement Streamlit Cloud

**Fichiers d'Entraînement :**
- `train_model.py` : Pipeline ML complet du chargement de données à l'export du modèle
- `train.csv` : Dataset Kaggle original (32 456 articles)

---

## Entraînement du Modèle

### Dataset

**Source :** [Dataset Kaggle Fake News](https://www.kaggle.com/c/fake-news/data)

**Statistiques :**
- Articles totaux : 32 456
- Fake news : 23 481 (72,3%)
- Vraies news : 8 975 (27,7%)
- Longueur moyenne d'article : ~500 mots

**Features :**
- `id` : Identifiant unique
- `title` : Titre de l'article
- `author` : Nom de l'auteur
- `text` : Corps de l'article
- `label` : 0 (RÉEL) ou 1 (FAKE)

### Pipeline d'Entraînement

Le processus d'entraînement complet est automatisé dans `train_model.py` :

**Étape 1 : Chargement des Données**
```python
import pandas as pd

df = pd.read_csv('data/train.csv')
df = df.dropna()  # Supprimer les valeurs manquantes
df['content'] = df['title'] + " " + df['text']  # Combiner titre et texte
```

**Étape 2 : Prétraitement du Texte**
```python
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def clean_text(text):
    # Minuscules
    text = text.lower()
    
    # Supprimer les URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # Supprimer les caractères spéciaux
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Supprimer les stopwords
    stop_words = set(stopwords.words('english'))
    words = [w for w in text.split() if w not in stop_words]
    
    # Lemmatisation
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(w) for w in words]
    
    return ' '.join(words)

df['cleaned'] = df['content'].apply(clean_text)
```

**Étape 3 : Vectorisation TF-IDF**
```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=1,
    max_df=0.8
)

X = vectorizer.fit_transform(df['cleaned'])
y = df['label']
```

**Étape 4 : Division Train-Test**
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.24, random_state=42
)
```

**Étape 5 : Entraînement du Modèle**
```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(
    max_iter=1000,
    solver='liblinear',
    random_state=42
)

model.fit(X_train, y_train)
```

**Étape 6 : Évaluation**
```python
from sklearn.metrics import accuracy_score, classification_report

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Précision: {accuracy:.4f}")  # 0.9834
print(classification_report(y_test, y_pred))
```

**Étape 7 : Export du Modèle**
```python
import pickle

# Sauvegarder le modèle
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Sauvegarder le vectorizer
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
```

### Hyperparamètres

| Paramètre | Valeur | Description |
|-----------|-------|-------------|
| `max_features` | 5000 | Les 5000 mots les plus importants |
| `ngram_range` | (1, 2) | Unigrammes et bigrammes |
| `min_df` | 1 | Fréquence document minimum |
| `max_df` | 0,8 | Fréquence document maximum (80%) |
| `max_iter` | 1000 | Itérations max pour convergence |
| `solver` | liblinear | Algorithme d'optimisation |
| `random_state` | 42 | Seed pour reproductibilité |

### Reproduction des Résultats

Pour réentraîner le modèle depuis zéro :

```bash
# 1. Télécharger le dataset
# Télécharger train.csv depuis la Compétition Kaggle Fake News

# 2. Installer les dépendances
pip install pandas scikit-learn nltk numpy

# 3. Télécharger les ressources NLTK
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"

# 4. Lancer le script d'entraînement
python model_training/train_model.py

# Sortie attendue :
# ✅ Dataset chargé : 32456 articles
# ✅ Prétraitement terminé
# ✅ Vectorisation terminée
# ✅ Modèle entraîné
# Précision : 0.9834 (98,34%)
# ✅ Modèles sauvegardés : model.pkl, vectorizer.pkl
```

**Temps d'Entraînement :**
- CPU : ~10-15 minutes (Intel i5/i7)
- RAM : ~4-8 GB requis
- Sortie : `model.pkl` (5 MB), `vectorizer.pkl` (10 MB)

---

## Contribution

Les contributions sont les bienvenues ! Veuillez suivre ces directives :

### Comment Contribuer

1. **Forker le Dépôt**
```bash
# Cliquez sur "Fork" sur GitHub, puis clonez votre fork
git clone https://github.com/VOTRE-USERNAME/fcc-fake-news-detector.git
```

2. **Créer une Branche de Feature**
```bash
git checkout -b feature/nom-de-votre-feature
```

3. **Faire des Changements**
- Suivre le guide de style PEP 8 pour le code Python
- Ajouter des docstrings à toutes les fonctions
- Mettre à jour la documentation si nécessaire

4. **Tester Vos Changements**
```bash
# Tests backend
cd backend
python -m pytest tests/

# Tests frontend
cd frontend
streamlit run app.py  # Tests manuels
```

5. **Commit et Push**
```bash
git add .
git commit -m "Ajout : description de votre feature"
git push origin feature/nom-de-votre-feature
```

6. **Créer une Pull Request**
- Allez sur GitHub et créez une Pull Request
- Décrivez vos changements clairement
- Référencez les issues liées si applicable

### Configuration de Développement

**Installer les Dépendances de Développement :**
```bash
pip install -r requirements-dev.txt
```

**Lancer les Tests :**
```bash
pytest tests/ -v --cov
```

**Formatage du Code :**
```bash
black app.py
flake8 app.py
```

### Domaines de Contribution

- Améliorer la précision du modèle avec le deep learning (BERT, RoBERTa)
- Ajouter support pour plus de langues
- Implémenter l'authentification utilisateur
- Ajouter une couche de cache (Redis)
- Créer une application mobile (React Native)
- Améliorer le design UI/UX
- Écrire des tests unitaires
- Ajouter un pipeline CI/CD

---

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour les détails.

```
Licence MIT

Copyright (c) 2024 Équipe de Développement FCC

Permission est accordée, gratuitement, à toute personne obtenant une copie
de ce logiciel et des fichiers de documentation associés (le "Logiciel"), de traiter
le Logiciel sans restriction, y compris sans limitation les droits
d'utiliser, copier, modifier, fusionner, publier, distribuer, sous-licencier et/ou vendre
des copies du Logiciel, et de permettre aux personnes à qui le Logiciel est
fourni de le faire, sous réserve des conditions suivantes :

L'avis de copyright ci-dessus et cet avis de permission doivent être inclus dans toutes
les copies ou portions substantielles du Logiciel.

LE LOGICIEL EST FOURNI "TEL QUEL", SANS GARANTIE D'AUCUNE SORTE, EXPRESSE OU
IMPLICITE, Y COMPRIS MAIS SANS S'Y LIMITER LES GARANTIES DE QUALITÉ MARCHANDE,
D'ADÉQUATION À UN USAGE PARTICULIER ET D'ABSENCE DE CONTREFAÇON. EN AUCUN CAS LES
AUTEURS OU TITULAIRES DU COPYRIGHT NE SERONT RESPONSABLES DE TOUTE RÉCLAMATION, DOMMAGE OU AUTRE
RESPONSABILITÉ, QUE CE SOIT DANS UNE ACTION CONTRACTUELLE, DÉLICTUELLE OU AUTRE, DÉCOULANT DE,
HORS DE OU EN RELATION AVEC LE LOGICIEL OU L'UTILISATION OU D'AUTRES TRANSACTIONS DANS LE
LOGICIEL.
```

---

## Contact

**Équipe du Projet :** Équipe de Développement FCC

**Dépôt GitHub :** [https://github.com/VOTRE-USERNAME/fcc-fake-news-detector](https://github.com/VOTRE-USERNAME/fcc-fake-news-detector)

**Application en Direct :** [https://fcc-fake-news-detector.streamlit.app](https://fcc-fake-news-detector.streamlit.app)

**Point de Terminaison API :** [https://fcc-fake-news-detector-v2.onrender.com](https://fcc-fake-news-detector-v2.onrender.com)

**Signaler des Problèmes :** [GitHub Issues](https://github.com/VOTRE-USERNAME/fcc-fake-news-detector/issues)

**Année :** 2024

---

## Remerciements

- **Dataset :** Compétition Kaggle Fake News
- **Hébergement :** Render.com et Streamlit Cloud (tiers gratuits)
- **Bibliothèques :** scikit-learn, NLTK, Flask, Streamlit, Plotly
- **Inspiration :** Combattre la désinformation à l'ère numérique

---

**Construit avec passion pour la vérité et la transparence.**
