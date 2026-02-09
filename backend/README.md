# FCC Fake News Detector - Backend API

API Flask pour détection de fake news.

## 🚀 Installation Locale

```bash
cd backend
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
```

## ▶️ Lancement

```bash
python app.py
```

API sur: http://localhost:5000

## 📡 Endpoints

- `GET /` - Info API
- `GET /health` - État
- `GET /info` - Info modèle  
- `POST /predict` - Prédiction

## 🧪 Test

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Breaking news!"}'
```

## ☁️ Déploiement Render.com

1. Créer compte [Render](https://render.com)
2. New Web Service
3. Connecter GitHub repo
4. Root Directory: `backend`
5. Build: `pip install -r requirements.txt && python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"`
6. Start: `gunicorn app:app`
7. Deploy

## 📦 Fichiers requis

Copier dans `backend/models/`:
- `fake_news_model.pkl`
- `tfidf_vectorizer.pkl`
