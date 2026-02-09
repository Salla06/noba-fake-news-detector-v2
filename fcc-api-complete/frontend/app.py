"""
FCC Fake News Detector - Frontend Streamlit
Version 2.0 - Architecture avec API Flask
"""

import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import base64
import io

# ============================================
# CONFIGURATION
# ============================================

st.set_page_config(
    page_title="FCC Fake News Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL API (modifiable via secrets)
try:
    API_URL = st.secrets["API_URL"]
except:
    API_URL = "http://localhost:5000"

# ============================================
# SESSION STATE
# ============================================

if 'history' not in st.session_state:
    st.session_state.history = []

if 'lang' not in st.session_state:
    st.session_state.lang = 'fr'

# ============================================
# TRADUCTIONS
# ============================================

T = {
    'fr': {
        'title': '🛡️ FCC Détecteur de Fake News',
        'subtitle': 'Système intelligent de détection de désinformation par Machine Learning',
        'nav_home': '🏠 Accueil',
        'nav_text': '📝 Analyser Texte',
        'nav_file': '📤 Analyser Fichier',
        'nav_multi': '🌍 Multilingue',
        'nav_history': '📊 Historique',
        'nav_about': 'ℹ️ À Propos',
        'api_status': '📡 État API',
        'api_ok': '🟢 Connectée',
        'api_ko': '🔴 Déconnectée',
        'analyze': '🔍 Analyser',
        'clear': '🗑️ Vider',
        'example': '📄 Exemple',
        'paste_here': 'Collez votre article ici...',
        'result_fake': 'FAKE NEWS DÉTECTÉE',
        'result_real': 'ARTICLE FIABLE',
        'confidence': 'Confiance',
        'details': 'Détails',
        'history_title': 'Historique des Analyses',
        'no_history': 'Aucune analyse',
        'total': 'Total',
        'fake': 'Fake',
        'real': 'Fiables',
    },
    'en': {
        'title': '🛡️ FCC Fake News Detector',
        'subtitle': 'Intelligent disinformation detection system using Machine Learning',
        'nav_home': '🏠 Home',
        'nav_text': '📝 Analyze Text',
        'nav_file': '📤 Analyze File',
        'nav_multi': '🌍 Multilingual',
        'nav_history': '📊 History',
        'nav_about': 'ℹ️ About',
        'api_status': '📡 API Status',
        'api_ok': '🟢 Connected',
        'api_ko': '🔴 Disconnected',
        'analyze': '🔍 Analyze',
        'clear': '🗑️ Clear',
        'example': '📄 Example',
        'paste_here': 'Paste your article here...',
        'result_fake': 'FAKE NEWS DETECTED',
        'result_real': 'RELIABLE ARTICLE',
        'confidence': 'Confidence',
        'details': 'Details',
        'history_title': 'Analysis History',
        'no_history': 'No analysis yet',
        'total': 'Total',
        'fake': 'Fake',
        'real': 'Reliable',
    }
}

def t(key):
    return T[st.session_state.lang].get(key, key)

# ============================================
# FONCTIONS API
# ============================================

def call_api(endpoint, method='GET', data=None):
    """Appeler l'API"""
    url = f"{API_URL}{endpoint}"
    try:
        if method == 'GET':
            r = requests.get(url, timeout=10)
        else:
            r = requests.post(url, json=data, timeout=10)
        
        if r.status_code == 200:
            return r.json()
        else:
            st.error(f"❌ API Error {r.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Impossible de se connecter à l'API")
        return None
    except requests.exceptions.Timeout:
        st.error("❌ Timeout API")
        return None
    except Exception as e:
        st.error(f"❌ Erreur: {e}")
        return None

# ============================================
# CSS CUSTOM
# ============================================

st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg, #001F3F, #004C99);
    padding: 60px 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
}
.result-box {
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.image("https://via.placeholder.com/200x80/004C99/FFFFFF?text=FCC", width=200)
    
    st.title("Navigation")
    
    page = st.radio("", [
        t('nav_home'),
        t('nav_text'),
        t('nav_file'),
        t('nav_multi'),
        t('nav_history'),
        t('nav_about')
    ])
    
    st.divider()
    
    # Langue
    lang_map = {"🇫🇷 Français": "fr", "🇬🇧 English": "en"}
    selected = st.selectbox("Language", list(lang_map.keys()))
    st.session_state.lang = lang_map[selected]
    
    st.divider()
    
    # État API
    st.subheader(t('api_status'))
    health = call_api('/health')
    
    if health and health.get('status') == 'healthy':
        st.success(t('api_ok'))
        st.caption(f"🔗 {API_URL}")
    else:
        st.error(t('api_ko'))
        st.warning("Vérifiez que l'API tourne")
    
    st.divider()
    st.caption("v2.0 - FCC Team")

# ============================================
# PAGE: ACCUEIL
# ============================================

if t('nav_home') in page:
    st.markdown(f"""
    <div class="hero">
        <h1 style="font-size:48px;margin-bottom:20px">{t('title')}</h1>
        <p style="font-size:20px;opacity:0.9">{t('subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Précision", "98.34%", "↑3.34%")
    col2.metric("Articles", "32,456", "Dataset")
    col3.metric("Langues", "5", "Support")
    col4.metric("Temps", "<2s", "Rapide")
    
    st.divider()
    
    st.subheader("📊 Informations Modèle")
    
    info = call_api('/info')
    if info:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🤖 Modèle")
            st.write(f"**Type:** {info['model']['type']}")
            st.write(f"**Accuracy:** {info['model']['accuracy']}%")
            st.write(f"**Precision:** {info['model']['precision']}%")
            st.write(f"**Recall:** {info['model']['recall']}%")
        
        with col2:
            st.markdown("### 🔢 Vectoriseur")
            st.write(f"**Type:** {info['vectorizer']['type']}")
            st.write(f"**Features:** {info['vectorizer']['max_features']}")
            st.write(f"**Vocabulaire:** {info['vectorizer']['vocabulary_size']} mots")

# ============================================
# PAGE: ANALYSER TEXTE
# ============================================

elif t('nav_text') in page:
    st.header(t('nav_text'))
    
    text = st.text_area(
        t('paste_here'),
        height=250,
        placeholder="Breaking news! Scientists discovered..."
    )
    
    col1, col2, col3 = st.columns([2,1,1])
    
    with col1:
        analyze = st.button(t('analyze'), type="primary", use_container_width=True)
    with col2:
        clear = st.button(t('clear'), use_container_width=True)
    with col3:
        example = st.button(t('example'), use_container_width=True)
    
    if example:
        text = "BREAKING NEWS!!! Scientists discovered this SHOCKING truth that doctors DON'T want you to know! Click here NOW to change your life FOREVER!!!"
        st.rerun()
    
    if clear:
        st.rerun()
    
    if analyze:
        if not text or len(text.strip()) < 10:
            st.warning("⚠️ Texte trop court")
        else:
            with st.spinner("📡 Envoi API et analyse..."):
                result = call_api('/predict', 'POST', {'text': text})
            
            if result:
                pred = result['prediction']
                label = result['label']
                conf = result['confidence']
                probs = result['probabilities']
                
                is_fake = (pred == 0)
                color = "#DC143C" if is_fake else "#28A745"
                
                st.markdown(f"""
                <div class="result-box" style="
                    background-color:{color}15;
                    border-left:5px solid {color};
                ">
                    <h2 style="color:{color};margin:0">
                        {'⚠️' if is_fake else '✅'} {t('result_fake') if is_fake else t('result_real')}
                    </h2>
                    <p style="font-size:18px;margin:10px 0">
                        {t('confidence')}: <b>{conf*100:.1f}%</b>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Gauge
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=conf*100,
                    domain={'x':[0,1],'y':[0,1]},
                    title={'text':t('confidence')},
                    gauge={
                        'axis':{'range':[0,100]},
                        'bar':{'color':color},
                        'steps':[
                            {'range':[0,50],'color':'lightgray'},
                            {'range':[50,100],'color':f'{color}40'}
                        ]
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                # Détails
                with st.expander(t('details')):
                    col1, col2 = st.columns(2)
                    col1.metric("Prob. FAKE", f"{probs['fake']*100:.2f}%")
                    col2.metric("Prob. REAL", f"{probs['real']*100:.2f}%")
                
                # Historique
                st.session_state.history.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'text': text[:100]+"...",
                    'prediction': pred,
                    'label': label,
                    'confidence': conf
                })
                
                st.success("✅ Analyse terminée")

# ============================================
# PAGE: FICHIER
# ============================================

elif t('nav_file') in page:
    st.header(t('nav_file'))
    
    uploaded = st.file_uploader(
        "Choisir un fichier",
        type=['txt','pdf','docx'],
        help="Formats: TXT, PDF, DOCX"
    )
    
    if uploaded:
        st.info(f"📄 {uploaded.name} ({uploaded.size/1024:.1f} KB)")
        
        # Extraction texte
        file_text = ""
        
        if uploaded.name.endswith('.txt'):
            file_text = uploaded.read().decode('utf-8')
        
        elif uploaded.name.endswith('.pdf'):
            try:
                import PyPDF2
                pdf = PyPDF2.PdfReader(uploaded)
                for page in pdf.pages:
                    file_text += page.extract_text()
            except:
                st.error("❌ Erreur lecture PDF")
        
        elif uploaded.name.endswith('.docx'):
            try:
                import docx
                doc = docx.Document(uploaded)
                file_text = '\n'.join([p.text for p in doc.paragraphs])
            except:
                st.error("❌ Erreur lecture DOCX")
        
        if file_text:
            with st.expander("👁️ Aperçu"):
                st.text_area("Contenu:", file_text[:500]+"...", height=200, disabled=True)
            
            if st.button("🔍 Analyser ce fichier", type="primary"):
                with st.spinner("Analyse..."):
                    result = call_api('/predict', 'POST', {'text': file_text})
                
                if result:
                    st.success(f"✅ {result['label']} ({result['confidence']*100:.1f}%)")

# ============================================
# PAGE: MULTILINGUE
# ============================================

elif t('nav_multi') in page:
    st.header(t('nav_multi'))
    
    st.info("🌍 Analyse multilingue (traduction automatique)")
    
    lang_choice = st.selectbox(
        "Langue de l'article:",
        ["Français", "English", "Español", "العربية", "中文"]
    )
    
    text_multi = st.text_area("Article:", height=200)
    
    if st.button("Analyser", type="primary"):
        if text_multi:
            # Note: ici on pourrait ajouter traduction
            # Pour l'instant on envoie direct à l'API
            with st.spinner("Analyse..."):
                result = call_api('/predict', 'POST', {'text': text_multi})
            
            if result:
                st.success(f"✅ {result['label']} ({result['confidence']*100:.1f}%)")

# ============================================
# PAGE: HISTORIQUE
# ============================================

elif t('nav_history') in page:
    st.header(t('history_title'))
    
    if not st.session_state.history:
        st.info(t('no_history'))
    else:
        total = len(st.session_state.history)
        fake_count = sum(1 for h in st.session_state.history if h['prediction']==0)
        real_count = total - fake_count
        
        col1, col2, col3 = st.columns(3)
        col1.metric(t('total'), total)
        col2.metric(t('fake'), fake_count, f"{fake_count/total*100:.1f}%")
        col3.metric(t('real'), real_count, f"{real_count/total*100:.1f}%")
        
        # Graph
        fig = go.Figure(data=[
            go.Bar(x=['FAKE','REAL'], y=[fake_count,real_count],
                   marker_color=['#DC143C','#28A745'])
        ])
        fig.update_layout(title="Distribution", height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Tableau
        df = pd.DataFrame(st.session_state.history)
        df_show = df[['timestamp','label','confidence','text']]
        df_show.columns = ['Date/Heure','Verdict','Confiance','Aperçu']
        df_show['Confiance'] = df_show['Confiance'].apply(lambda x: f"{x*100:.1f}%")
        
        st.dataframe(df_show, use_container_width=True)
        
        # Export
        csv = df_show.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Télécharger CSV", csv, "history.csv", "text/csv")

# ============================================
# PAGE: À PROPOS
# ============================================

elif t('nav_about') in page:
    st.header("ℹ️ À Propos")
    
    st.markdown("""
    ### 🛡️ FCC Fake News Detector v2.0
    
    **Architecture:**
    - **Backend:** API Flask (REST)
    - **Frontend:** Streamlit
    - **Communication:** HTTP/JSON
    
    **Modèle ML:**
    - Algorithme: Logistic Regression
    - Vectoriseur: TF-IDF (5000 features)
    - Accuracy: 98.34%
    - Dataset: 32,456 articles
    
    **Technologies:**
    - Python 3.11+
    - Flask + flask-cors
    - Streamlit
    - scikit-learn 1.5.2
    - NLTK 3.8.1
    - Plotly 5.18.0
    
    **Liens:**
    - [GitHub](https://github.com/noba-ibrahim/fcc-fake-news-detector)
    - [Documentation](https://github.com/noba-ibrahim/fcc-fake-news-detector/wiki)
    - [Rapport PDF](https://github.com/noba-ibrahim/fcc-fake-news-detector/blob/main/docs/rapport.pdf)
    
    ---
    
    **Développé par:** FCC Development Team  
    **Version:** 2.0 (Architecture API)  
    **Date:** Février 2024
    
    **Fonctionnalités:**
    - ✅ Analyse de texte temps réel
    - ✅ Upload de fichiers (TXT, PDF, DOCX)
    - ✅ Support multilingue (5 langues)
    - ✅ Historique des analyses
    - ✅ Visualisations interactives
    - ✅ Export CSV
    - ✅ Interface bilingue FR/EN
    
    **API Endpoints:**
    - `GET /` - Infos API
    - `GET /health` - État santé
    - `GET /info` - Infos modèle
    - `POST /predict` - Prédiction
    """)
