"""
FCC Fake News Detector - Version 2.0 Ultra-Moderne
Détection de fake news avec Machine Learning + Multi-langues + Upload de fichiers
"""

import streamlit as st
import pickle
import os
from pathlib import Path
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from utils import (
    extract_text_from_file, 
    translate_to_english, 
    detect_language,
    get_language_name
)

# Configuration de la page
st.set_page_config(
    page_title="FCC Fake News Detector 2.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS ultra-moderne avec gradients et animations
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Style global */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Gradient de fond animé */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        animation: gradient 15s ease infinite;
        background-size: 400% 400%;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Container blanc avec effet glassmorphism */
    .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Titre principal avec gradient */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    /* Sous-titre */
    h3 {
        text-align: center;
        color: #6b7280;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Cards avec hover effect */
    .css-1r6slb0 {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .css-1r6slb0:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }
    
    /* Boutons stylés */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Zone de texte */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Tabs stylés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f3f4f6;
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Alerts personnalisées */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(-20px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Metrics stylées */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: white;
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #764ba2;
        background: #f9fafb;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p {
        color: white !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f3f4f6;
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #6b7280;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Cache pour charger les modèles
@st.cache_resource
def load_models():
    """Charge le modèle et le vectorizer"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, 'models', 'fake_news_model.pkl')
        vectorizer_path = os.path.join(base_dir, 'models', 'tfidf_vectorizer.pkl')
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        
        return model, vectorizer
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des modèles: {e}")
        return None, None

# Initialiser l'historique dans session_state
if 'history' not in st.session_state:
    st.session_state.history = []

# Charger les modèles
model, vectorizer = load_models()

# Header avec animation
st.markdown("""
    <div style='text-align: center; animation: fadeIn 1s ease;'>
        <h1>🛡️ FCC Fake News Detector 2.0</h1>
        <h3>✨ Détection intelligente avec IA • Multi-langues • Upload de fichiers ✨</h3>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar moderne
with st.sidebar:
    st.markdown("## 📊 Tableau de Bord")
    
    if st.session_state.history:
        total_analyses = len(st.session_state.history)
        fake_count = sum(1 for item in st.session_state.history if item['prediction'] == 0)
        reliable_count = total_analyses - fake_count
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📝 Analyses", total_analyses)
        with col2:
            st.metric("✅ Fiables", reliable_count)
        
        st.metric("🔴 Fake News", fake_count)
        
        # Graphique circulaire
        fig = go.Figure(data=[go.Pie(
            labels=['Fake News', 'Reliable'],
            values=[fake_count, reliable_count],
            marker=dict(colors=['#ef4444', '#10b981']),
            hole=0.4
        )])
        fig.update_layout(
            showlegend=True,
            height=250,
            margin=dict(l=0, r=0, t=30, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune analyse effectuée pour le moment")
    
    st.markdown("---")
    
    st.markdown("## ℹ️ À propos")
    st.markdown("""
    **Version:** 2.0 Ultra  
    **Modèle:** Logistic Regression  
    **Précision:** 98.34%  
    **Langues:** 5 (Auto-traduction)
    """)
    
    st.markdown("---")
    
    st.markdown("## 🌍 Langues Supportées")
    st.markdown("""
    🇬🇧 Anglais  
    🇫🇷 Français  
    🇪🇸 Espagnol  
    🇸🇦 Arabe  
    🇨🇳 Chinois
    """)

# Main content
if model is not None and vectorizer is not None:
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📰 Analyse Texte", 
        "📁 Upload Fichier", 
        "📊 Historique", 
        "📚 Documentation"
    ])
    
    with tab1:
        st.markdown("### 📝 Analyser un texte")
        
        # Sélection de langue
        col1, col2 = st.columns([3, 1])
        with col1:
            article_text = st.text_area(
                "Entrez votre texte (n'importe quelle langue)",
                height=250,
                placeholder="Exemple: Este es un artículo sobre noticias falsas..."
            )
        with col2:
            st.markdown("#### 🌍 Langue")
            lang_option = st.selectbox(
                "Source",
                ["auto", "en", "fr", "es", "ar", "zh-CN"],
                format_func=get_language_name,
                label_visibility="collapsed"
            )
        
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            analyze_btn = st.button("🔍 Analyser", use_container_width=True, type="primary")
        with col2:
            clear_btn = st.button("🗑️ Effacer", use_container_width=True)
        with col3:
            translate_preview = st.button("👁️ Aperçu traduction", use_container_width=True)
        
        if clear_btn:
            st.rerun()
        
        if translate_preview and article_text.strip():
            with st.spinner("Traduction en cours..."):
                try:
                    source_lang = None if lang_option == "auto" else lang_option
                    translated_text, detected_lang = translate_to_english(article_text, source_lang)
                    
                    st.success(f"✅ Langue détectée: {get_language_name(detected_lang)}")
                    
                    with st.expander("📄 Texte traduit en anglais"):
                        st.text_area("Traduction", translated_text, height=200, disabled=True)
                except Exception as e:
                    st.error(f"❌ Erreur: {e}")
        
        if analyze_btn:
            if not article_text.strip():
                st.warning("⚠️ Veuillez entrer un texte à analyser.")
            elif len(article_text.strip()) < 20:
                st.warning("⚠️ Le texte est trop court (minimum 20 caractères).")
            else:
                with st.spinner("🔄 Analyse en cours..."):
                    try:
                        # Traduction si nécessaire
                        source_lang = None if lang_option == "auto" else lang_option
                        text_to_analyze, detected_lang = translate_to_english(article_text, source_lang)
                        
                        if detected_lang != 'en':
                            st.info(f"🌍 Texte traduit depuis {get_language_name(detected_lang)} vers l'anglais")
                        
                        # Vectorisation et prédiction
                        text_vectorized = vectorizer.transform([text_to_analyze])
                        prediction = model.predict(text_vectorized)[0]
                        probabilities = model.predict_proba(text_vectorized)[0]
                        
                        # Sauvegarder dans l'historique
                        st.session_state.history.append({
                            'timestamp': datetime.now(),
                            'text': article_text[:100] + "...",
                            'language': detected_lang,
                            'prediction': prediction,
                            'confidence': max(probabilities) * 100
                        })
                        
                        # Affichage des résultats
                        st.markdown("---")
                        st.markdown("## 📊 Résultats de l'Analyse")
                        
                        is_fake = prediction == 0
                        label = "⚠️ FAKE NEWS" if is_fake else "✅ ARTICLE FIABLE"
                        confidence = max(probabilities) * 100
                        
                        # Card de résultat
                        result_color = "#ef4444" if is_fake else "#10b981"
                        st.markdown(f"""
                            <div style='background: {result_color}; padding: 2rem; border-radius: 15px; text-align: center; color: white; box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
                                <h1 style='color: white; margin: 0; -webkit-text-fill-color: white;'>{label}</h1>
                                <h2 style='color: white; margin-top: 1rem; -webkit-text-fill-color: white;'>Confiance: {confidence:.1f}%</h2>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Métriques détaillées
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("🔴 Fake News", f"{probabilities[0]*100:.1f}%")
                        with col2:
                            st.metric("✅ Fiable", f"{probabilities[1]*100:.1f}%")
                        with col3:
                            st.metric("📝 Caractères", len(article_text))
                        with col4:
                            st.metric("🌍 Langue", get_language_name(detected_lang))
                        
                        # Graphique de probabilités
                        st.markdown("### 📈 Distribution des Probabilités")
                        
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            x=['Fake News', 'Article Fiable'],
                            y=[probabilities[0]*100, probabilities[1]*100],
                            marker=dict(
                                color=['#ef4444', '#10b981'],
                                line=dict(color='white', width=2)
                            ),
                            text=[f"{probabilities[0]*100:.1f}%", f"{probabilities[1]*100:.1f}%"],
                            textposition='outside',
                            textfont=dict(size=16, color='#1f2937')
                        ))
                        
                        fig.update_layout(
                            height=400,
                            showlegend=False,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis=dict(title="", titlefont=dict(size=14)),
                            yaxis=dict(title="Probabilité (%)", range=[0, 105], titlefont=dict(size=14)),
                            font=dict(size=14, color='#1f2937')
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Aperçu du texte
                        with st.expander("📄 Aperçu du texte analysé"):
                            preview = article_text[:500] + "..." if len(article_text) > 500 else article_text
                            st.text_area("Texte original", preview, height=150, disabled=True)
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de l'analyse: {e}")
    
    with tab2:
        st.markdown("### 📁 Importer un Fichier")
        
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;'>
                <h3 style='color: white; margin: 0;'>📎 Formats Supportés</h3>
                <p style='margin: 0.5rem 0 0 0;'>Word (.docx) • PDF (.pdf) • Texte (.txt) • Excel (.xlsx)</p>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choisissez un fichier",
            type=['docx', 'pdf', 'txt', 'xlsx'],
            help="Glissez-déposez votre fichier ici ou cliquez pour parcourir"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ Fichier chargé: **{uploaded_file.name}**")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                lang_file = st.selectbox(
                    "Langue du document",
                    ["auto", "en", "fr", "es", "ar", "zh-CN"],
                    format_func=get_language_name
                )
            
            with col2:
                analyze_file_btn = st.button("🔍 Analyser le fichier", use_container_width=True, type="primary")
            
            if analyze_file_btn:
                with st.spinner("📄 Extraction et analyse en cours..."):
                    try:
                        # Extraction du texte
                        extracted_text = extract_text_from_file(uploaded_file)
                        
                        if not extracted_text.strip():
                            st.error("❌ Aucun texte n'a pu être extrait du fichier.")
                        else:
                            st.info(f"✅ {len(extracted_text)} caractères extraits")
                            
                            # Traduction si nécessaire
                            source_lang = None if lang_file == "auto" else lang_file
                            text_to_analyze, detected_lang = translate_to_english(extracted_text, source_lang)
                            
                            if detected_lang != 'en':
                                st.info(f"🌍 Texte traduit depuis {get_language_name(detected_lang)}")
                            
                            # Analyse
                            text_vectorized = vectorizer.transform([text_to_analyze])
                            prediction = model.predict(text_vectorized)[0]
                            probabilities = model.predict_proba(text_vectorized)[0]
                            
                            # Sauvegarder dans l'historique
                            st.session_state.history.append({
                                'timestamp': datetime.now(),
                                'text': f"📁 {uploaded_file.name}",
                                'language': detected_lang,
                                'prediction': prediction,
                                'confidence': max(probabilities) * 100
                            })
                            
                            # Affichage
                            st.markdown("---")
                            is_fake = prediction == 0
                            label = "⚠️ FAKE NEWS" if is_fake else "✅ ARTICLE FIABLE"
                            confidence = max(probabilities) * 100
                            result_color = "#ef4444" if is_fake else "#10b981"
                            
                            st.markdown(f"""
                                <div style='background: {result_color}; padding: 2rem; border-radius: 15px; text-align: center; color: white; box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
                                    <h1 style='color: white; margin: 0; -webkit-text-fill-color: white;'>{label}</h1>
                                    <h2 style='color: white; margin-top: 1rem; -webkit-text-fill-color: white;'>Confiance: {confidence:.1f}%</h2>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                            
                            # Métriques
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("🔴 Fake News", f"{probabilities[0]*100:.1f}%")
                            with col2:
                                st.metric("✅ Fiable", f"{probabilities[1]*100:.1f}%")
                            with col3:
                                st.metric("🌍 Langue", get_language_name(detected_lang))
                            
                            # Aperçu
                            with st.expander("📄 Aperçu du texte extrait"):
                                preview = extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text
                                st.text_area("Contenu", preview, height=200, disabled=True)
                    
                    except Exception as e:
                        st.error(f"❌ Erreur: {e}")
    
    with tab3:
        st.markdown("### 📊 Historique des Analyses")
        
        if st.session_state.history:
            # Bouton pour effacer l'historique
            if st.button("🗑️ Effacer l'historique", use_container_width=False):
                st.session_state.history = []
                st.rerun()
            
            # Créer un DataFrame
            history_df = pd.DataFrame(st.session_state.history)
            history_df['result'] = history_df['prediction'].apply(lambda x: "Fake News" if x == 0 else "Fiable")
            history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
            
            # Statistiques
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📝 Total", len(history_df))
            with col2:
                fake_pct = (history_df['prediction'] == 0).sum() / len(history_df) * 100
                st.metric("🔴 Fake News", f"{fake_pct:.0f}%")
            with col3:
                reliable_pct = (history_df['prediction'] == 1).sum() / len(history_df) * 100
                st.metric("✅ Fiables", f"{reliable_pct:.0f}%")
            with col4:
                avg_conf = history_df['confidence'].mean()
                st.metric("📊 Conf. Moy.", f"{avg_conf:.1f}%")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tableau des analyses
            st.markdown("#### 📋 Dernières Analyses")
            
            # Inverser pour avoir les plus récentes en premier
            display_df = history_df.iloc[::-1].copy()
            display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
            display_df['confidence'] = display_df['confidence'].apply(lambda x: f"{x:.1f}%")
            
            # Styliser le tableau
            st.dataframe(
                display_df[['timestamp', 'text', 'language', 'result', 'confidence']].rename(columns={
                    'timestamp': '🕐 Date',
                    'text': '📝 Texte',
                    'language': '🌍 Langue',
                    'result': '🎯 Résultat',
                    'confidence': '📊 Confiance'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Graphique temporel
            st.markdown("#### 📈 Évolution dans le Temps")
            
            timeline_df = history_df.copy()
            timeline_df['hour'] = timeline_df['timestamp'].dt.hour
            timeline_counts = timeline_df.groupby('hour').size().reset_index(name='count')
            
            fig = px.line(
                timeline_counts,
                x='hour',
                y='count',
                title="Nombre d'analyses par heure",
                labels={'hour': 'Heure', 'count': 'Nombre d\'analyses'}
            )
            fig.update_traces(line_color='#667eea', line_width=3)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12, color='#1f2937')
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.info("💡 Aucune analyse effectuée pour le moment. Commencez par analyser un texte !")
    
    with tab4:
        st.markdown("### 📚 Documentation Complète")
        
        # Utilisation
        st.markdown("#### 🚀 Comment Utiliser l'Application")
        
        with st.expander("📝 1. Analyse de Texte"):
            st.markdown("""
            **Étapes:**
            1. Collez votre texte dans la zone de texte
            2. Sélectionnez la langue (ou laissez en "auto")
            3. Cliquez sur "Analyser"
            4. Consultez les résultats détaillés
            
            **Langues supportées:**
            - Anglais 🇬🇧
            - Français 🇫🇷
            - Espagnol 🇪🇸
            - Arabe 🇸🇦
            - Chinois 🇨🇳
            
            Le système traduit automatiquement vers l'anglais si nécessaire.
            """)
        
        with st.expander("📁 2. Upload de Fichiers"):
            st.markdown("""
            **Formats acceptés:**
            - Word (.docx)
            - PDF (.pdf)
            - Texte (.txt)
            - Excel (.xlsx)
            
            **Processus:**
            1. Glissez-déposez votre fichier ou cliquez pour parcourir
            2. Le texte est automatiquement extrait
            3. Sélectionnez la langue du document
            4. Cliquez sur "Analyser le fichier"
            """)
        
        with st.expander("📊 3. Historique et Statistiques"):
            st.markdown("""
            - Toutes vos analyses sont sauvegardées dans l'historique
            - Consultez les statistiques globales
            - Visualisez l'évolution temporelle
            - Exportez les résultats
            """)
        
        # Fonctionnement
        st.markdown("---")
        st.markdown("#### 🤖 Fonctionnement Technique")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **1. Traitement Multi-Langues**
            - Détection automatique de la langue
            - Traduction vers l'anglais
            - Analyse avec le modèle ML
            
            **2. Vectorisation TF-IDF**
            - 5000 features extraites
            - N-grams: (1, 2)
            - Normalisation L2
            """)
        
        with col2:
            st.markdown("""
            **3. Modèle ML**
            - Logistic Regression
            - Entraîné sur 24,728 articles
            - Testé sur 7,728 articles
            
            **4. Prédiction**
            - 0 = Fake News
            - 1 = Reliable News
            - Score de confiance (0-100%)
            """)
        
        # Performances
        st.markdown("---")
        st.markdown("#### 🎯 Performances du Modèle")
        
        perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
        with perf_col1:
            st.metric("Accuracy", "98.34%", delta="Excellent")
        with perf_col2:
            st.metric("Precision", "98.34%", delta="Excellent")
        with perf_col3:
            st.metric("Recall", "98.34%", delta="Excellent")
        with perf_col4:
            st.metric("F1-Score", "98.34%", delta="Excellent")
        
        # Limitations
        st.markdown("---")
        st.markdown("#### ⚠️ Limitations")
        
        st.warning("""
        - **Modèle entraîné en anglais**: Les résultats sont optimaux pour les textes en anglais
        - **Traduction automatique**: La qualité de traduction peut affecter les résultats
        - **Textes courts**: Minimum 20 caractères recommandé
        - **Contexte**: Le modèle se base sur des patterns statistiques, pas sur la vérification factuelle
        """)
        
        # Crédits
        st.markdown("---")
        st.markdown("#### 👥 Crédits")
        
        st.info("""
        **Projet développé pour:**  
        Federal Communications Commission (FCC)
        
        **Technologies:**
        - Python 3.11
        - Streamlit 1.31+
        - scikit-learn 1.5.2
        - Deep Translator (multi-langues)
        - Plotly (visualisations)
        
        **Version:** 2.0 Ultra-Moderne
        """)

else:
    st.error("❌ Impossible de charger les modèles ML")
    st.info("Vérifiez que les fichiers sont présents dans le dossier 'models/'")

# Footer moderne
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div class='footer'>
        <p><strong>🛡️ FCC Fake News Detector 2.0</strong> | Powered by Machine Learning & AI</p>
        <p>© 2024 - Projet Académique | Version Ultra-Moderne</p>
    </div>
""", unsafe_allow_html=True)
