# 🚀 GUIDE DE DÉPLOIEMENT COMPLET

## Étapes pour déployer l'application FCC Fake News Detector

---

## 📦 PRÉPARATION

### 1. Avoir les fichiers modèles

Vous devez avoir ces 2 fichiers dans `backend/models/`:
- `fake_news_model.pkl`
- `tfidf_vectorizer.pkl`

Si vous ne les avez pas, exécutez le notebook d'entraînement pour les générer.

### 2. Pousser sur GitHub

```bash
# Initialiser git (si pas déjà fait)
git init

# Ajouter les fichiers
git add .

# Commit
git commit -m "feat: architecture API séparée backend + frontend"

# Pousser (remplacer par votre repo)
git push origin main
```

---

## 🔧 DÉPLOIEMENT BACKEND (API Flask)

### Option 1: Render.com (RECOMMANDÉ - Gratuit)

1. **Créer un compte**
   - Aller sur https://render.com
   - Sign up avec GitHub

2. **Nouveau Web Service**
   - Dashboard > **New +** > **Web Service**
   - Connecter votre repo GitHub
   - Autoriser l'accès

3. **Configuration**
   - **Name:** `fcc-api` (ou autre nom)
   - **Region:** Frankfurt (EU) ou Oregon (US)
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt && python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
     ```
   - **Start Command:**
     ```bash
     gunicorn app:app
     ```
   - **Instance Type:** `Free`

4. **Create Web Service**
   - Attendre 5-10 minutes
   - L'URL sera: `https://fcc-api-xxx.onrender.com`

5. **Tester l'API**
   ```bash
   curl https://fcc-api-xxx.onrender.com/health
   ```
   Doit retourner: `{"status": "healthy"}`

6. **IMPORTANT: Copier l'URL**
   - Copier `https://fcc-api-xxx.onrender.com`
   - Vous en aurez besoin pour le frontend

### Option 2: Heroku

```bash
cd backend

# Installer Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Créer app
heroku create fcc-api

# Déployer
git subtree push --prefix backend heroku main

# URL: https://fcc-api.herokuapp.com
```

---

## 💻 DÉPLOIEMENT FRONTEND (Streamlit)

### Sur Streamlit Cloud (Gratuit)

1. **Créer un compte**
   - Aller sur https://streamlit.io/cloud
   - Sign up avec GitHub

2. **Nouveau déploiement**
   - Dashboard > **New app**
   - Connecter votre repo GitHub

3. **Configuration**
   - **Repository:** `votre-username/fcc-fake-news-detector`
   - **Branch:** `main`
   - **Main file path:** `frontend/app.py`
   - **App URL:** `fcc-fake-news-detector` (ou autre)

4. **Configuration Secrets**
   - **AVANT de déployer**, cliquer sur **Advanced settings**
   - Aller dans **Secrets**
   - Ajouter:
     ```toml
     API_URL = "https://fcc-api-xxx.onrender.com"
     ```
     ⚠️ **REMPLACER** par votre URL Render !

5. **Deploy!**
   - Cliquer sur **Deploy**
   - Attendre 3-5 minutes
   - URL: `https://fcc-fake-news-detector.streamlit.app`

6. **Vérifier**
   - Ouvrir l'URL
   - Dans sidebar, vérifier: 🟢 API Connectée
   - Tester une analyse

---

## ✅ VÉRIFICATION COMPLÈTE

### 1. Tester l'API

```bash
# Health check
curl https://fcc-api-xxx.onrender.com/health

# Info modèle
curl https://fcc-api-xxx.onrender.com/info

# Prédiction
curl -X POST https://fcc-api-xxx.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Breaking news! Shocking discovery about vaccines!"}'
```

### 2. Tester le Frontend

1. Ouvrir `https://fcc-fake-news-detector.streamlit.app`
2. Vérifier 🟢 API Connectée dans sidebar
3. Aller sur "Analyser Texte"
4. Coller un article
5. Cliquer "Analyser"
6. Vérifier le résultat

---

## 🐛 DÉPANNAGE

### Problème 1: API 🔴 Déconnectée

**Cause:** URL API incorrecte dans secrets

**Solution:**
1. Streamlit Cloud > App > Settings > Secrets
2. Vérifier que `API_URL` est correct
3. Doit être: `https://fcc-api-xxx.onrender.com` (sans `/` final)
4. Sauvegarder
5. Redémarrer l'app (Reboot)

### Problème 2: API ne démarre pas

**Cause:** Fichiers modèles manquants

**Solution:**
1. Vérifier que `backend/models/` contient les .pkl
2. Si manquants, pousser les fichiers:
   ```bash
   git add backend/models/*.pkl
   git commit -m "add ML models"
   git push
   ```
3. Render redéploiera automatiquement

### Problème 3: CORS Error

**Cause:** CORS mal configuré

**Solution:**
1. Dans `backend/app.py`, vérifier:
   ```python
   CORS(app, resources={r"/*": {"origins": ["*"]}})
   ```
2. Pousser et redéployer

### Problème 4: Timeout

**Cause:** API Render en sleep (plan gratuit)

**Solution:**
- Première requête après 15min d'inactivité = 30-60s
- Attendre que l'API se réveille
- Ensuite, réponses rapides

---

## 📊 MONITORING

### Render Dashboard

- Logs en temps réel
- Métriques CPU/RAM
- Requêtes/seconde

### Streamlit Dashboard

- Nombre de visiteurs
- Temps d'activité
- Erreurs

---

## 🔄 MISES À JOUR

### Mise à jour du code

```bash
# Modifier le code
git add .
git commit -m "fix: amélioration UI"
git push origin main
```

- **Render:** Redéploie automatiquement
- **Streamlit:** Redéploie automatiquement

### Mise à jour du modèle

1. Réentraîner le modèle (notebook)
2. Remplacer les .pkl dans `backend/models/`
3. Push:
   ```bash
   git add backend/models/*.pkl
   git commit -m "update: nouveau modèle v2.1"
   git push
   ```
4. Render redéploie automatiquement

---

## 💰 COÛTS

### Plan Gratuit (actuel)

- **Render:** Gratuit
  - Limitations: Sleep après 15min inactivité
  - 750h/mois

- **Streamlit:** Gratuit
  - Limitations: 1GB RAM
  - Ressources partagées

### Pour Upgrade (si besoin)

- **Render Starter:** 7$/mois
  - Pas de sleep
  - Plus de RAM

- **Streamlit Team:** Gratuit pour équipes académiques
  - Demander via formulaire

---

## 🎉 RÉSULTAT FINAL

Après déploiement, vous aurez:

✅ **API Backend:** `https://fcc-api-xxx.onrender.com`
✅ **App Frontend:** `https://fcc-fake-news-detector.streamlit.app`
✅ **Communication:** Frontend → API → Résultat
✅ **Accès public:** Monde entier peut utiliser
✅ **Auto-déploiement:** Push = déploiement auto

---

**🎯 URLs à partager:**

- App Web: `https://fcc-fake-news-detector.streamlit.app`
- API: `https://fcc-api-xxx.onrender.com`
- GitHub: `https://github.com/votre-username/fcc-fake-news-detector`

---

**Développé par FCC Team | Guide v2.0**
