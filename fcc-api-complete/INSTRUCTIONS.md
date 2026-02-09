# 🎯 INSTRUCTIONS ULTRA-SIMPLES

## Boss, voici comment faire en 5 ÉTAPES ! 🚀

---

## ✅ ÉTAPE 1: Télécharger et Préparer

1. **Télécharger** ce dossier complet `fcc-api-complete/`

2. **Copier vos modèles** dans `backend/models/`:
   - `fake_news_model.pkl`
   - `tfidf_vectorizer.pkl`

3. **Vérifier** la structure:
   ```
   fcc-api-complete/
   ├── backend/
   │   ├── models/
   │   │   ├── fake_news_model.pkl  ← ICI
   │   │   └── tfidf_vectorizer.pkl  ← ICI
   │   ├── app.py
   │   └── requirements.txt
   ├── frontend/
   │   ├── app.py
   │   └── requirements.txt
   └── README.md
   ```

---

## ✅ ÉTAPE 2: Pousser sur GitHub

```bash
cd fcc-api-complete

# Initialiser git
git init

# Ajouter tous les fichiers
git add .

# Commit
git commit -m "feat: architecture API backend + frontend"

# Ajouter remote (remplacer par VOTRE repo)
git remote add origin https://github.com/VOTRE-USERNAME/fcc-fake-news-detector.git

# Push
git push -u origin main
```

---

## ✅ ÉTAPE 3: Déployer l'API (Backend)

### Sur Render.com (Gratuit)

1. Aller sur https://render.com
2. **Sign up** avec GitHub
3. Cliquer **New +** > **Web Service**
4. Sélectionner votre repo GitHub
5. Configurer:
   - Name: `fcc-api`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt && python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"`
   - Start Command: `gunicorn app:app`
6. Cliquer **Create Web Service**
7. **Attendre 5-10 minutes**
8. **COPIER l'URL**: `https://fcc-api-XXX.onrender.com`

---

## ✅ ÉTAPE 4: Déployer le Frontend (Streamlit)

### Sur Streamlit Cloud (Gratuit)

1. Aller sur https://streamlit.io/cloud
2. **Sign up** avec GitHub
3. Cliquer **New app**
4. Configurer:
   - Repository: `VOTRE-USERNAME/fcc-fake-news-detector`
   - Branch: `main`
   - Main file: `frontend/app.py`
5. **Advanced settings** > **Secrets**
6. Ajouter:
   ```toml
   API_URL = "https://fcc-api-XXX.onrender.com"
   ```
   ⚠️ REMPLACER par votre URL Render de l'étape 3 !
7. Cliquer **Deploy**
8. **Attendre 3-5 minutes**

---

## ✅ ÉTAPE 5: Tester

1. Ouvrir l'URL Streamlit: `https://VOTRE-APP.streamlit.app`
2. Dans sidebar, vérifier: **🟢 API Connectée**
3. Aller sur "Analyser Texte"
4. Coller un article
5. Cliquer "Analyser"
6. **BOOM ! Ça marche ! 🎉**

---

## 🎤 POUR TON PROF

Dis-lui:

> "J'ai refait l'architecture en **séparant le backend (API Flask) du frontend (Streamlit)**. 
> 
> **Backend** héberge le modèle ML et expose des endpoints REST.
> 
> **Frontend** Streamlit communique avec l'API via requêtes HTTP.
> 
> C'est une **architecture microservices** moderne avec séparation des responsabilités."

Montre-lui:
1. Le code `backend/app.py` (l'API)
2. Le code `frontend/app.py` (qui appelle l'API)
3. Les deux URLs déployées qui communiquent

---

## 🐛 SI PROBLÈME

### API 🔴 Déconnectée

1. Streamlit Cloud > App > Settings > Secrets
2. Vérifier `API_URL` correct
3. Redémarrer (Reboot)

### API ne démarre pas

1. Vérifier que les .pkl sont dans `backend/models/`
2. Re-push si manquants

---

## 📊 RÉSULTAT FINAL

Tu auras:
- ✅ API: `https://fcc-api-XXX.onrender.com`
- ✅ App: `https://VOTRE-APP.streamlit.app`
- ✅ Communication: App → API → Résultat
- ✅ Accessible monde entier

**C'est tout boss ! 🚀**

---

Questions? Regarde `DEPLOIEMENT.md` pour plus de détails !
