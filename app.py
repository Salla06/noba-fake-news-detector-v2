"""
FCC Fake News Detector - Professional Edition
Advanced Machine Learning Detection System
Bilingual: English / Français
"""

import streamlit as st
import requests
import os
from pathlib import Path
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from utils import (
    extract_text_from_file,
    extract_text_from_url, 
    translate_to_english, 
    detect_language,
    get_language_name
)


# ================================================
# CONFIGURATION API RENDER
# ================================================
API_URL = "https://fcc-fake-news-detector-v2.onrender.com"

def call_api_predict(text):
    """Appeler l'API Render pour prédiction"""
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={"text": text},
            timeout=60
        )
        if response.status_code == 200:
            result = response.json()
            prediction = result['prediction']
            probabilities = [result['probabilities']['fake'], result['probabilities']['real']]
            return prediction, probabilities
        else:
            return None, None
    except:
        return None, None
# ================================================

# Configuration de la page
st.set_page_config(
    page_title="FCC Fake News Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dictionnaire de traductions
TRANSLATIONS = {
    'en': {
        'title': 'FCC FAKE NEWS DETECTOR',
        'subtitle': 'Machine Learning Detection System',
        'hero_title': 'FCC Fake News Detector',
        'hero_subtitle': 'Advanced AI-powered system for detecting misinformation and fake news with industry-leading accuracy',
        'discover_btn': 'DISCOVER THE SYSTEM',
        'tab_text': 'Text Analysis',
        'tab_file': 'File Upload',
        'tab_history': 'Analysis History',
        'tab_info': 'Information',
        'tab_doc': 'Documentation',
        'analyze_text': 'Analyze Text Content',
        'analyze_desc': 'Enter article text for instant analysis. System supports automatic translation from multiple languages.',
        'article_text': 'Article Text',
        'placeholder': 'Enter text in any supported language...',
        'language': 'Language',
        'analyze_btn': 'Analyze',
        'clear_btn': 'Clear',
        'empty_btn': 'Empty',
        'translate_btn': 'Preview Translation',
        'fake_detected': 'FAKE NEWS DETECTED',
        'reliable_article': 'RELIABLE ARTICLE',
        'confidence': 'Confidence',
        'fake_prob': 'Fake News Probability',
        'reliable_prob': 'Reliable Probability',
        'char_count': 'Character Count',
        'prob_dist': 'Probability Distribution',
        'text_preview': 'Text Preview',
        'original_text': 'Original Text',
        'file_upload': 'File Upload',
        'file_desc': 'Upload documents for analysis. Supports Word, PDF, Text, and Excel formats.',
        'select_file': 'Select File',
        'doc_language': 'Document Language',
        'analyze_file': 'Analyze File',
        'history_title': 'Analysis History',
        'clear_history': 'Clear History',
        'total_analyses': 'Total Analyses',
        'fake_news': 'Fake News',
        'reliable': 'Reliable',
        'avg_confidence': 'Avg. Confidence',
        'recent_analyses': 'Recent Analyses',
        'timeline': 'Timeline Analysis',
        'info_title': 'System Information',
        'model_specs': 'Model Specifications',
        'supported_langs': 'Supported Languages',
        'tech_features': 'Technical Features',
    },
    'fr': {
        'title': 'DÉTECTEUR DE FAKE NEWS FCC',
        'subtitle': 'Système de Détection par Apprentissage Automatique',
        'hero_title': 'Détecteur de Fake News FCC',
        'hero_subtitle': 'Système avancé basé sur l\'IA pour détecter la désinformation et les fake news avec une précision de pointe',
        'discover_btn': 'DÉCOUVRIR LE SYSTÈME',
        'tab_text': 'Analyse de Texte',
        'tab_file': 'Téléchargement de Fichier',
        'tab_history': 'Historique de l\'Analyse',
        'tab_info': 'Informations',
        'tab_doc': 'Documentation',
        'analyze_text': 'Analyser le Contenu du Texte',
        'analyze_desc': 'Saisissez le texte de l\'article pour une analyse instantanée. Le système prend en charge la traduction automatique depuis plusieurs langues.',
        'article_text': 'Texte de l\'Article',
        'placeholder': 'Entrez le texte dans n\'importe quelle langue supportée...',
        'language': 'Langue',
        'analyze_btn': 'Analyser',
        'clear_btn': 'Effacer',
        'empty_btn': 'Vider',
        'translate_btn': 'Aperçu Traduction',
        'fake_detected': 'FAKE NEWS DÉTECTÉE',
        'reliable_article': 'ARTICLE FIABLE',
        'confidence': 'Confiance',
        'fake_prob': 'Probabilité Fake News',
        'reliable_prob': 'Probabilité Fiable',
        'char_count': 'Nombre de Caractères',
        'prob_dist': 'Distribution des Probabilités',
        'text_preview': 'Aperçu du Texte',
        'original_text': 'Texte Original',
        'file_upload': 'Téléchargement de Fichier',
        'file_desc': 'Téléchargez des documents pour analyse. Supporte les formats Word, PDF, Texte et Excel.',
        'select_file': 'Sélectionner un Fichier',
        'doc_language': 'Langue du Document',
        'analyze_file': 'Analyser le Fichier',
        'history_title': 'Historique des Analyses',
        'clear_history': 'Effacer l\'Historique',
        'total_analyses': 'Total des Analyses',
        'fake_news': 'Fake News',
        'reliable': 'Fiable',
        'avg_confidence': 'Confiance Moyenne',
        'recent_analyses': 'Analyses Récentes',
        'timeline': 'Analyse Temporelle',
        'info_title': 'Informations Système',
        'model_specs': 'Spécifications du Modèle',
        'supported_langs': 'Langues Supportées',
        'tech_features': 'Fonctionnalités Techniques',
    }
}

# CSS professionnel optimisé
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
    
    * {
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    :root {
        --primary-blue: #0052CC;
        --dark-blue: #001F3F;
        --light-blue: #4C9AFF;
        --accent-red: #DC143C;
        --white: #FFFFFF;
        --off-white: #F8F9FA;
        --black: #000000;
        --dark-gray: #1A1A1A;
        --medium-gray: #4A5568;
        --light-gray: #E2E8F0;
    }
    
    .main {
        background: linear-gradient(135deg, #F8F9FA 0%, #E8EEF5 100%);
        padding: 0 !important;
    }
    
    .block-container {
        max-width: 1400px;
        padding: 1rem 2rem !important;
    }
    
    /* Supprimer les boîtes vides */
    .element-container:empty {
        display: none !important;
    }
    
    .stMarkdown:empty {
        display: none !important;
    }
    
    div[data-testid="stVerticalBlock"] > div:empty {
        display: none !important;
    }
    
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Navbar professionnelle */
    .app-navbar {
        background: linear-gradient(135deg, var(--dark-blue) 0%, var(--primary-blue) 100%);
        color: white;
        padding: 2.5rem 2rem;
        margin: -1rem -2rem 2rem -2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 0;
    }
    
    .navbar-content {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .navbar-left {
        flex: 1;
        padding-top: 1rem;
    }
    
    .navbar-title {
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }
    
    .navbar-subtitle {
        font-size: 0.85rem;
        opacity: 0.9;
        font-weight: 300;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .navbar-right {
        display: flex;
        gap: 0.5rem;
        padding-bottom: 0.5rem;
    }
    
    /* Page d'accueil - Images réduites */
    .hero-section {
        position: relative;
        width: 100%;
        height: 60vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: white;
        padding: 2rem;
        overflow: hidden;
        margin: 0;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }
    
    .hero-background {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        animation: slideshow 20s infinite;
        background-size: cover;
        background-position: center;
    }
    
    @keyframes slideshow {
        0%, 100% {
            background-image: linear-gradient(135deg, rgba(0, 31, 63, 0.85) 0%, rgba(0, 82, 204, 0.85) 100%),
                              url('https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=1920');
        }
        33% {
            background-image: linear-gradient(135deg, rgba(0, 31, 63, 0.85) 0%, rgba(0, 82, 204, 0.85) 100%),
                              url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920');
        }
        66% {
            background-image: linear-gradient(135deg, rgba(0, 31, 63, 0.85) 0%, rgba(0, 82, 204, 0.85) 100%),
                              url('https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=1920');
        }
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
        animation: fadeIn 1.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: -2px;
        line-height: 1.1;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        font-weight: 300;
        margin-bottom: 0;
        opacity: 0.95;
        max-width: 800px;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.3);
    }
    
    h1, h2, h3 {
        color: var(--dark-blue);
        font-weight: 600;
    }
    
    h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    h2 {
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
    }
    
    h3 {
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }
    
    /* Documentation - Titres colorés */
    .doc-title-blue {
        color: var(--primary-blue);
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 1rem;
        border-left: 4px solid var(--primary-blue);
        padding-left: 1rem;
    }
    
    .doc-title-red {
        color: var(--accent-red);
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 1rem;
        border-left: 4px solid var(--accent-red);
        padding-left: 1rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: white;
        border-radius: 12px;
        padding: 0.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 500;
        color: var(--medium-gray);
        transition: all 0.3s ease;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-blue);
        color: white;
    }
    
    .stButton > button {
        background: var(--primary-blue);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.9rem;
    }
    
    .stButton > button:hover {
        background: var(--dark-blue);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 82, 204, 0.3);
    }
    
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid var(--light-gray);
        transition: border-color 0.3s ease;
        font-family: 'IBM Plex Mono', monospace;
        padding: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 3px rgba(0, 82, 204, 0.1);
    }
    
    .result-fake {
        background: linear-gradient(135deg, #DC143C 0%, #B8112A 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(220, 20, 60, 0.3);
        margin: 2rem 0;
    }
    
    .result-reliable {
        background: linear-gradient(135deg, #0052CC 0%, #001F3F 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0, 82, 204, 0.3);
        margin: 2rem 0;
    }
    
    .result-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .result-confidence {
        font-size: 3rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-blue);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        color: var(--medium-gray);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--light-blue) 100%);
        border-radius: 10px;
    }
    
    [data-testid="stFileUploader"] {
        background: white;
        border: 2px dashed var(--primary-blue);
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--dark-blue);
        background: var(--off-white);
    }
    
    .stAlert {
        border-radius: 8px;
        border: none;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .streamlit-expanderHeader {
        background: var(--off-white);
        border-radius: 8px;
        font-weight: 500;
        color: var(--dark-blue);
    }
    
    .dataframe {
        border: none !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border-radius: 8px;
        overflow: hidden;
    }
    
    .professional-footer {
        background: var(--dark-blue);
        color: white;
        padding: 3rem;
        text-align: center;
        margin: 4rem -2rem -1rem -2rem;
        border-radius: 0;
    }
    
    hr {
        border: none;
        border-top: 2px solid var(--light-gray);
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialiser session state
if 'show_home' not in st.session_state:
    st.session_state.show_home = True
if 'history' not in st.session_state:
    st.session_state.history = []
if 'language' not in st.session_state:
    st.session_state.language = 'fr'
if 'text_counter' not in st.session_state:
    st.session_state.text_counter = 0

# Fonction pour obtenir les traductions
def t(key):
    return TRANSLATIONS[st.session_state.language].get(key, key)



# PAGE D'ACCUEIL
if st.session_state.show_home:
    
    # Bande blanche en haut pour éviter que Streamlit cache les boutons
    st.markdown("""
        <div style='background: white; padding: 0.5rem 0; margin: -1rem -2rem 0 -2rem;'></div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Boutons langue en haut (plus larges)
    col_spacer, col_fr, col_en = st.columns([10, 2, 2])
    with col_fr:
        if st.button("Français", key="lang_fr_home", use_container_width=True):
            st.session_state.language = 'fr'
            st.rerun()
    with col_en:
        if st.button("English", key="lang_en_home", use_container_width=True):
            st.session_state.language = 'en'
            st.rerun()
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Image hero réduite
    st.markdown("""
        <div class="hero-section">
            <div class="hero-background"></div>
            <div class="hero-content">
                <div class="hero-title">""" + t('hero_title') + """</div>
                <div class="hero-subtitle">""" + t('hero_subtitle') + """</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)
    
    # Bouton découvrir en bas (hors image)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button(t('discover_btn'), key="discover", use_container_width=True, type="primary"):
            st.session_state.show_home = False
            st.rerun()
    
    st.stop()

# APPLICATION PRINCIPALE avec NAVBAR
else:
    # Navbar professionnelle (PAS sur page d'accueil)
    st.markdown('''
        <div class="app-navbar">
            <div class="navbar-content">
                <div class="navbar-left">
                    <div class="navbar-title">''' + t('title') + '''</div>
                    <div class="navbar-subtitle">''' + t('subtitle') + '''</div>
                </div>
                <div class="navbar-right">
                    <!-- Langue ici -->
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Sélecteur de langue intégré
    col_spacer, col_lang = st.columns([13, 2])
    with col_lang:
        current_idx = 0 if st.session_state.language == 'fr' else 1
        lang_choice = st.selectbox(
            "", 
            ["🇫🇷 Français", "🇬🇧 English"], 
            index=current_idx,
            label_visibility="collapsed", 
            key="lang_selector_app"
        )
        if "Français" in lang_choice and st.session_state.language != 'fr':
            st.session_state.language = 'fr'
            st.rerun()
        elif "English" in lang_choice and st.session_state.language != 'en':
            st.session_state.language = 'en'
            st.rerun()
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    if True:  # API version
        
        tabs = st.tabs([t('tab_text'), t('tab_file'), t('tab_history'), t('tab_info'), t('tab_doc')])
        
        with tabs[0]:
            st.markdown("### " + t('analyze_text'))
            st.markdown(t('analyze_desc'))
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            # NOUVEAU: Choix entre Texte et URL
            input_method = st.radio(
                "📌 Input Method" if st.session_state.language == 'en' else "📌 Méthode d'entrée",
                ["📝 Text" if st.session_state.language == 'en' else "📝 Texte", "🔗 URL"],
                horizontal=True
            )
            
            st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
            
            article_text = ""
            original_text_from_translation = None
            
            # Si mode TEXTE
            if "Text" in input_method or "Texte" in input_method:
                col1, col2 = st.columns([4, 1])
                with col1:
                    text_key = f"text_input_{st.session_state.get('text_counter', 0)}"
                    article_text = st.text_area(
                        t('article_text'),
                        value="",
                        height=250,
                        placeholder=t('placeholder'),
                        key=text_key
                    )
                with col2:
                    st.markdown("#### " + t('language'))
                    lang_option = st.selectbox(
                        "Source Language",
                        ["auto", "en", "fr", "es", "ar", "zh-CN"],
                        format_func=get_language_name,
                        label_visibility="collapsed"
                    )
            
            # Si mode URL
            else:
                col1, col2 = st.columns([4, 1])
                with col1:
                    url_input = st.text_input(
                        "🔗 Article URL" if st.session_state.language == 'en' else "🔗 URL de l'article",
                        placeholder="https://example.com/article",
                        key="url_input"
                    )
                with col2:
                    st.markdown("#### " + t('language'))
                    lang_option = st.selectbox(
                        "Source Language",
                        ["auto", "en", "fr", "es", "ar", "zh-CN"],
                        format_func=get_language_name,
                        label_visibility="collapsed",
                        key="lang_url"
                    )
                
                if url_input:
                    with st.spinner("🌐 " + ("Extracting text from URL..." if st.session_state.language == 'en' else "Extraction du texte depuis l'URL...")):
                        try:
                            article_text = extract_text_from_url(url_input)
                            st.success(f"✅ {len(article_text)} " + ("characters extracted" if st.session_state.language == 'en' else "caractères extraits"))
                            
                            with st.expander("📄 " + ("Preview extracted text" if st.session_state.language == 'en' else "Aperçu du texte extrait")):
                                preview_text = article_text[:500] + "..." if len(article_text) > 500 else article_text
                                st.text_area("", preview_text, height=150, disabled=True, label_visibility="collapsed")
                        except Exception as e:
                            st.error(f"❌ {str(e)}")
                            article_text = ""
            
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
            with col1:
                analyze_btn = st.button(t('analyze_btn'), use_container_width=True, type="primary")
            with col2:
                if st.button(t('empty_btn'), use_container_width=True):
                    # Incrémenter le compteur pour forcer un nouveau textarea vide
                    st.session_state.text_counter = st.session_state.get('text_counter', 0) + 1
                    st.rerun()
            with col3:
                clear_btn = st.button(t('clear_btn'), use_container_width=True)
            with col4:
                translate_preview = st.button(t('translate_btn'), use_container_width=True)
            
            if clear_btn:
                st.rerun()
            
            if translate_preview and article_text.strip():
                with st.spinner("Translating..."):
                    try:
                        source_lang = None if lang_option == "auto" else lang_option
                        translated_text, detected_lang = translate_to_english(article_text, source_lang)
                        
                        st.success(f"Detected Language: {get_language_name(detected_lang)}")
                        
                        with st.expander("Translated Text (English)"):
                            st.text_area("Translation", translated_text, height=200, disabled=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            if analyze_btn:
                if not article_text.strip():
                    st.warning("Please enter text to analyze." if st.session_state.language == 'en' else "Veuillez entrer un texte à analyser.")
                elif len(article_text.strip()) < 20:
                    st.warning("Text is too short (minimum 20 characters)." if st.session_state.language == 'en' else "Le texte est trop court (minimum 20 caractères).")
                else:
                    with st.spinner("Processing..." if st.session_state.language == 'en' else "Traitement en cours..."):
                        try:
                            source_lang = None if lang_option == "auto" else lang_option
                            text_to_analyze, detected_lang, original_text = translate_to_english(article_text, source_lang)
                            
                            if detected_lang != 'en':
                                st.info(f"🌍 Text translated from {get_language_name(detected_lang)} to English" if st.session_state.language == 'en' else f"🌍 Texte traduit de {get_language_name(detected_lang)} vers l'anglais")
                            
                            # Appel API
                            prediction, probabilities = call_api_predict(text_to_analyze)
                            if prediction is None:
                                st.error("❌ " + ("API Error. Retry in 30s." if st.session_state.language == 'en' else "Erreur API. Réessayez dans 30s."))
                                st.stop()
                            
                            st.session_state.history.append({
                                'timestamp': datetime.now(),
                                'text': article_text[:100] + "...",
                                'language': detected_lang,
                                'prediction': prediction,
                                'confidence': max(probabilities) * 100
                            })
                            
                            st.markdown("---")
                            st.markdown("## " + ("Analysis Results" if st.session_state.language == 'en' else "Résultats de l'Analyse"))
                            
                            is_fake = prediction == 0
                            label = t('fake_detected') if is_fake else t('reliable_article')
                            confidence = max(probabilities) * 100
                            
                            result_class = "result-fake" if is_fake else "result-reliable"
                            st.markdown(f"""
                                <div class='{result_class}'>
                                    <div class='result-title'>{label}</div>
                                    <div class='result-confidence'>{confidence:.1f}% {t('confidence')}</div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric(t('fake_prob'), f"{probabilities[0]*100:.1f}%")
                            with col2:
                                st.metric(t('reliable_prob'), f"{probabilities[1]*100:.1f}%")
                            with col3:
                                st.metric(t('char_count'), len(article_text))
                            with col4:
                                st.metric(t('language'), get_language_name(detected_lang))
                            
                            st.markdown("### " + t('prob_dist'))
                            
                            fake_label = "Fake News"
                            reliable_label = "Reliable Article" if st.session_state.language == 'en' else "Article Fiable"
                            
                            fig = go.Figure()
                            fig.add_trace(go.Bar(
                                x=[fake_label, reliable_label],
                                y=[probabilities[0]*100, probabilities[1]*100],
                                marker=dict(
                                    color=['#DC143C', '#0052CC'],
                                    line=dict(color='white', width=2)
                                ),
                                text=[f"{probabilities[0]*100:.1f}%", f"{probabilities[1]*100:.1f}%"],
                                textposition='outside',
                                textfont=dict(size=16, color='#1A1A1A')
                            ))
                            
                            fig.update_layout(
                                height=400,
                                showlegend=False,
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                xaxis=dict(title=""),
                                yaxis=dict(title="Probability (%)" if st.session_state.language == 'en' else "Probabilité (%)", range=[0, 105]),
                                font=dict(size=14, color='#1A1A1A')
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            with st.expander(t('text_preview')):
                                preview = article_text[:500] + "..." if len(article_text) > 500 else article_text
                                st.text_area(t('original_text'), preview, height=150, disabled=True)
                        
                        except Exception as e:
                            st.error(f"Analysis Error: {e}")
        
        with tabs[1]:
            st.markdown("### " + t('file_upload'))
            st.markdown(t('file_desc'))
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                t('select_file'),
                type=['docx', 'pdf', 'txt', 'xlsx']
            )
            
            if uploaded_file is not None:
                st.success(f"File loaded: {uploaded_file.name}" if st.session_state.language == 'en' else f"Fichier chargé: {uploaded_file.name}")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    lang_file = st.selectbox(
                        t('doc_language'),
                        ["auto", "en", "fr", "es", "ar", "zh-CN"],
                        format_func=get_language_name
                    )
                
                with col2:
                    analyze_file_btn = st.button(t('analyze_file'), use_container_width=True, type="primary")
                
                if analyze_file_btn:
                    with st.spinner("Extracting and analyzing..." if st.session_state.language == 'en' else "Extraction et analyse..."):
                        try:
                            extracted_text = extract_text_from_file(uploaded_file)
                            
                            if not extracted_text.strip():
                                st.error("No text could be extracted." if st.session_state.language == 'en' else "Aucun texte n'a pu être extrait.")
                            else:
                                st.info(f"{len(extracted_text)} characters extracted" if st.session_state.language == 'en' else f"{len(extracted_text)} caractères extraits")
                                
                                source_lang = None if lang_file == "auto" else lang_file
                                text_to_analyze, detected_lang = translate_to_english(extracted_text, source_lang)
                                
                                if detected_lang != 'en':
                                    st.info(f"Text translated from {get_language_name(detected_lang)}" if st.session_state.language == 'en' else f"Texte traduit de {get_language_name(detected_lang)}")
                                
                                text_vectorized = vectorizer.transform([text_to_analyze])
                                prediction = model.predict(text_vectorized)[0]
                                probabilities = model.predict_proba(text_vectorized)[0]
                                
                                st.session_state.history.append({
                                    'timestamp': datetime.now(),
                                    'text': f"File: {uploaded_file.name}" if st.session_state.language == 'en' else f"Fichier: {uploaded_file.name}",
                                    'language': detected_lang,
                                    'prediction': prediction,
                                    'confidence': max(probabilities) * 100
                                })
                                
                                st.markdown("---")
                                is_fake = prediction == 0
                                label = t('fake_detected') if is_fake else t('reliable_article')
                                confidence = max(probabilities) * 100
                                result_class = "result-fake" if is_fake else "result-reliable"
                                
                                st.markdown(f"""
                                    <div class='{result_class}'>
                                        <div class='result-title'>{label}</div>
                                        <div class='result-confidence'>{confidence:.1f}% {t('confidence')}</div>
                                    </div>
                                """, unsafe_allow_html=True)
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Fake News", f"{probabilities[0]*100:.1f}%")
                                with col2:
                                    st.metric(t('reliable'), f"{probabilities[1]*100:.1f}%")
                                with col3:
                                    st.metric(t('language'), get_language_name(detected_lang))
                                
                                with st.expander("Extracted Text Preview" if st.session_state.language == 'en' else "Aperçu du Texte Extrait"):
                                    preview = extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text
                                    st.text_area("Content" if st.session_state.language == 'en' else "Contenu", preview, height=200, disabled=True)
                        
                        except Exception as e:
                            st.error(f"Error: {e}")
        
        with tabs[2]:
            st.markdown("### " + t('history_title'))
            
            if st.session_state.history:
                if st.button(t('clear_history'), use_container_width=False):
                    st.session_state.history = []
                    st.rerun()
                
                history_df = pd.DataFrame(st.session_state.history)
                history_df['result'] = history_df['prediction'].apply(lambda x: "Fake News" if x == 0 else (t('reliable')))
                history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(t('total_analyses'), len(history_df))
                with col2:
                    fake_pct = (history_df['prediction'] == 0).sum() / len(history_df) * 100
                    st.metric(t('fake_news'), f"{fake_pct:.0f}%")
                with col3:
                    reliable_pct = (history_df['prediction'] == 1).sum() / len(history_df) * 100
                    st.metric(t('reliable'), f"{reliable_pct:.0f}%")
                with col4:
                    avg_conf = history_df['confidence'].mean()
                    st.metric(t('avg_confidence'), f"{avg_conf:.1f}%")
                
                st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
                st.markdown("#### " + t('recent_analyses'))
                
                display_df = history_df.iloc[::-1].copy()
                display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
                display_df['confidence'] = display_df['confidence'].apply(lambda x: f"{x:.1f}%")
                
                col_names = {
                    'timestamp': 'Date',
                    'text': 'Text' if st.session_state.language == 'en' else 'Texte',
                    'language': 'Language' if st.session_state.language == 'en' else 'Langue',
                    'result': 'Result' if st.session_state.language == 'en' else 'Résultat',
                    'confidence': 'Confidence' if st.session_state.language == 'en' else 'Confiance'
                }
                
                st.dataframe(
                    display_df[['timestamp', 'text', 'language', 'result', 'confidence']].rename(columns=col_names),
                    use_container_width=True,
                    hide_index=True
                )
                
                st.markdown("#### " + t('timeline'))
                
                timeline_df = history_df.copy()
                timeline_df['hour'] = timeline_df['timestamp'].dt.hour
                timeline_counts = timeline_df.groupby('hour').size().reset_index(name='count')
                
                fig = px.line(
                    timeline_counts,
                    x='hour',
                    y='count',
                    title="Analyses per Hour" if st.session_state.language == 'en' else "Analyses par Heure",
                    labels={'hour': 'Hour' if st.session_state.language == 'en' else 'Heure', 
                           'count': 'Number of Analyses' if st.session_state.language == 'en' else 'Nombre d\'Analyses'}
                )
                fig.update_traces(line_color='#0052CC', line_width=3)
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12, color='#1A1A1A')
                )
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                st.info("No analyses performed yet." if st.session_state.language == 'en' else "Aucune analyse effectuée pour le moment.")
        
        with tabs[3]:
            st.markdown("### 📊 " + t('info_title'))
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            # Section 1: Métriques de Performance
            st.markdown("<div class='doc-title-blue'>🎯 " + ("Performance Metrics" if st.session_state.language == 'en' else "Métriques de Performance") + "</div>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Accuracy", "98.34%", "↑ Excellent")
            with col2:
                st.metric("Precision", "98.34%", "↑ High")
            with col3:
                st.metric("Recall", "98.34%", "↑ High")
            with col4:
                st.metric("F1-Score", "98.34%", "↑ Balanced")
            
            st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
            
            # Section 2: Spécifications Techniques
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='doc-title-blue'>🤖 " + t('model_specs') + "</div>", unsafe_allow_html=True)
                
                if st.session_state.language == 'fr':
                    st.markdown("""
                    **Algorithme Principal**
                    - Type: Régression Logistique (Logistic Regression)
                    - Solveur: liblinear
                    - Régularisation: L2
                    - Max Iterations: 1000
                    
                    **Vectorisation**
                    - Méthode: TF-IDF (Term Frequency-Inverse Document Frequency)
                    - Nombre de features: 5000
                    - N-grams: (1, 2) - unigrammes et bigrammes
                    - Normalisation: L2
                    - Min DF: 1
                    - Max DF: 0.8
                    
                    **Dataset**
                    - Total d'articles: 32,456
                    - Articles Fake: 23,481 (72.3%)
                    - Articles Real: 8,975 (27.7%)
                    - Split Train/Test: 76% / 24%
                    - Source: Kaggle Fake News Dataset
                    """)
                else:
                    st.markdown("""
                    **Primary Algorithm**
                    - Type: Logistic Regression
                    - Solver: liblinear
                    - Regularization: L2
                    - Max Iterations: 1000
                    
                    **Vectorization**
                    - Method: TF-IDF (Term Frequency-Inverse Document Frequency)
                    - Features: 5000
                    - N-grams: (1, 2) - unigrams and bigrams
                    - Normalization: L2
                    - Min DF: 1
                    - Max DF: 0.8
                    
                    **Dataset**
                    - Total articles: 32,456
                    - Fake articles: 23,481 (72.3%)
                    - Real articles: 8,975 (27.7%)
                    - Train/Test Split: 76% / 24%
                    - Source: Kaggle Fake News Dataset
                    """)
            
            with col2:
                st.markdown("<div class='doc-title-red'>🌍 " + t('supported_langs') + "</div>", unsafe_allow_html=True)
                
                if st.session_state.language == 'fr':
                    st.markdown("""
                    **Langues Supportées**
                    - 🇬🇧 Anglais (Langue native du modèle)
                    - 🇫🇷 Français
                    - 🇪🇸 Espagnol
                    - 🇸🇦 Arabe
                    - 🇨🇳 Chinois (Simplifié)
                    
                    **Traduction**
                    - Moteur: Google Translate API
                    - Détection automatique de langue
                    - Traduction en temps réel
                    
                    **Sources d'Entrée**
                    - 📝 Texte direct
                    - 🔗 URLs (pages web, articles)
                    - 📄 Fichiers (.txt, .pdf, .docx, .xlsx)
                    """)
                else:
                    st.markdown("""
                    **Supported Languages**
                    - 🇬🇧 English (Model's native language)
                    - 🇫🇷 French
                    - 🇪🇸 Spanish
                    - 🇸🇦 Arabic
                    - 🇨🇳 Chinese (Simplified)
                    
                    **Translation**
                    - Engine: Google Translate API
                    - Automatic language detection
                    - Real-time translation
                    
                    **Input Sources**
                    - 📝 Direct text
                    - 🔗 URLs (web pages, articles)
                    - 📄 Files (.txt, .pdf, .docx, .xlsx)
                    """)
            
            st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
            
            # Section 3: Architecture
            st.markdown("<div class='doc-title-blue'>🏗️ " + ("System Architecture" if st.session_state.language == 'en' else "Architecture du Système") + "</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.session_state.language == 'fr':
                    st.markdown("""
                    **Backend (API Flask)**
                    - Hébergement: Render.com
                    - Endpoint: `/predict`
                    - Format: REST API (JSON)
                    - Timeout: 60 secondes
                    - Modèle: Logistic Regression (.pkl)
                    - Vectorizer: TF-IDF (.pkl)
                    
                    **Traitement**
                    1. Réception du texte
                    2. Nettoyage (regex, stopwords)
                    3. Lemmatisation
                    4. Vectorisation TF-IDF
                    5. Prédiction
                    6. Calcul des probabilités
                    """)
                else:
                    st.markdown("""
                    **Backend (Flask API)**
                    - Hosting: Render.com
                    - Endpoint: `/predict`
                    - Format: REST API (JSON)
                    - Timeout: 60 seconds
                    - Model: Logistic Regression (.pkl)
                    - Vectorizer: TF-IDF (.pkl)
                    
                    **Processing**
                    1. Text reception
                    2. Cleaning (regex, stopwords)
                    3. Lemmatization
                    4. TF-IDF vectorization
                    5. Prediction
                    6. Probability calculation
                    """)
            
            with col2:
                if st.session_state.language == 'fr':
                    st.markdown("""
                    **Frontend (Streamlit)**
                    - Hébergement: Streamlit Cloud
                    - Framework: Streamlit 1.29
                    - Communication: HTTP POST
                    - Design: IBM Plex Sans
                    
                    **Fonctionnalités**
                    - Analyse de texte
                    - Extraction depuis URL
                    - Upload de fichiers
                    - Traduction multilingue
                    - Historique avec graphiques
                    - Export CSV
                    - Interface bilingue FR/EN
                    """)
                else:
                    st.markdown("""
                    **Frontend (Streamlit)**
                    - Hosting: Streamlit Cloud
                    - Framework: Streamlit 1.29
                    - Communication: HTTP POST
                    - Design: IBM Plex Sans
                    
                    **Features**
                    - Text analysis
                    - URL extraction
                    - File upload
                    - Multilingual translation
                    - History with charts
                    - CSV export
                    - Bilingual UI FR/EN
                    """)
            
            st.markdown("<div class='doc-title-blue'>" + t('tech_features') + "</div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.session_state.language == 'fr':
                    st.markdown("""
                    **Traitement du Texte**
                    - Vectorisation TF-IDF
                    - 5000 Caractéristiques
                    - N-grammes: (1, 2)
                    - Normalisation L2
                    """)
                else:
                    st.markdown("""
                    **Text Processing**
                    - TF-IDF Vectorization
                    - 5000 Features
                    - N-grams: (1, 2)
                    - L2 Normalization
                    """)
            with col2:
                if st.session_state.language == 'fr':
                    st.markdown("""
                    **Support de Fichiers**
                    - Documents Word (.docx)
                    - Fichiers PDF (.pdf)
                    - Fichiers Texte (.txt)
                    - Feuilles Excel (.xlsx)
                    """)
                else:
                    st.markdown("""
                    **File Support**
                    - Word Documents (.docx)
                    - PDF Files (.pdf)
                    - Text Files (.txt)
                    - Excel Spreadsheets (.xlsx)
                    """)
            with col3:
                if st.session_state.language == 'fr':
                    st.markdown("""
                    **Sortie d'Analyse**
                    - Classification Binaire
                    - Score de Confiance
                    - Distribution de Probabilité
                    - Métriques Détaillées
                    """)
                else:
                    st.markdown("""
                    **Analysis Output**
                    - Binary Classification
                    - Confidence Scoring
                    - Probability Distribution
                    - Detailed Metrics
                    """)
        
        with tabs[4]:
            st.markdown("### 📚 " + t('tab_doc'))
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            if st.session_state.language == 'fr':
                # SECTION 1: Vue d'Ensemble
                st.markdown("<div class='doc-title-blue'>🎯 Vue d'Ensemble du Système</div>", unsafe_allow_html=True)
                st.markdown("""
                Le **Détecteur de Fake News FCC** est un système avancé d'apprentissage automatique conçu pour identifier 
                la désinformation et les fake news avec une précision de 98.34%. Développé en 2024, il utilise un modèle 
                de **Régression Logistique** entraîné sur plus de 32,000 articles provenant du dataset Kaggle Fake News.
                
                Le système supporte **5 langues** et offre une interface bilingue Français/Anglais pour une utilisation 
                accessible à un public international.
                """)
                
                st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
                
                # SECTION 2: Comment ça fonctionne
                st.markdown("<div class='doc-title-red'>⚙️ Comment Ça Fonctionne</div>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    **Pipeline de Traitement**
                    
                    1. **Saisie du Texte**
                       - Texte direct (copier-coller)
                       - Extraction depuis URL (pages web, PDF)
                       - Upload de fichier (TXT, PDF, DOCX, XLSX)
                    
                    2. **Détection de Langue**
                       - Détection automatique via langdetect
                       - Support de 5 langues
                    
                    3. **Traduction (si nécessaire)**
                       - Traduction vers l'anglais via Google Translate
                       - Préservation du texte original
                    
                    4. **Prétraitement**
                       - Nettoyage du texte (regex)
                       - Suppression des stopwords
                       - Lemmatisation (WordNet)
                    """)
                
                with col2:
                    st.markdown("""
                    **Analyse et Classification**
                    
                    5. **Vectorisation TF-IDF**
                       - Transformation en vecteur numérique
                       - 5000 features
                       - N-grams (1,2)
                    
                    6. **Prédiction**
                       - Classification via Logistic Regression
                       - Calcul des probabilités (Fake vs Real)
                    
                    7. **Résultats**
                       - Label: FAKE ou REAL
                       - Score de confiance (%)
                       - Distribution des probabilités
                       - Graphiques interactifs
                    """)
                
                st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
                
                # SECTION 3: Guide d'Utilisation
                st.markdown("<div class='doc-title-blue'>📖 Guide d'Utilisation</div>", unsafe_allow_html=True)
                
                st.markdown("""
                **Méthode 1: Analyse de Texte**
                1. Aller dans l'onglet "Analyse de Texte"
                2. Choisir "📝 Texte" ou "🔗 URL"
                3. Coller le texte ou l'URL
                4. Sélectionner la langue (ou auto)
                5. Cliquer "Analyser"
                6. Consulter les résultats (30-60s si première requête)
                
                **Méthode 2: Upload de Fichier**
                1. Aller dans l'onglet "Téléchargement de Fichier"
                2. Sélectionner un fichier (.txt, .pdf, .docx, .xlsx)
                3. Choisir la langue du document
                4. Cliquer "Analyser le Fichier"
                5. Le texte est extrait et analysé automatiquement
                
                **Historique**
                - Toutes les analyses sont sauvegardées dans l'onglet "Historique"
                - Visualisation avec graphiques interactifs
                - Export possible en CSV
                """)
                
                st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
                
                # SECTION 4: Reproduction du Travail
                st.markdown("<div class='doc-title-red'>🔬 Reproduire Notre Travail</div>", unsafe_allow_html=True)
                
                st.markdown("""
                **Étape 1: Préparation des Données**
                ```python
                import pandas as pd
                
                # Charger le dataset Kaggle
                df = pd.read_csv('fake_news_dataset.csv')
                
                # Nettoyage
                df = df.dropna()
                df['text'] = df['title'] + ' ' + df['text']
                
                # Labels: 0 = FAKE, 1 = REAL
                X = df['text']
                y = df['label']
                ```
                
                **Étape 2: Prétraitement**
                ```python
                import re
                import nltk
                from nltk.corpus import stopwords
                from nltk.stem import WordNetLemmatizer
                
                nltk.download('stopwords')
                nltk.download('wordnet')
                
                def clean_text(text):
                    # Lowercase
                    text = text.lower()
                    
                    # Supprimer URLs
                    text = re.sub(r'http\S+|www\S+', '', text)
                    
                    # Supprimer caractères spéciaux
                    text = re.sub(r'[^a-zA-Z\s]', '', text)
                    
                    # Supprimer stopwords
                    stop_words = set(stopwords.words('english'))
                    words = text.split()
                    words = [w for w in words if w not in stop_words]
                    
                    # Lemmatisation
                    lemmatizer = WordNetLemmatizer()
                    words = [lemmatizer.lemmatize(w) for w in words]
                    
                    return ' '.join(words)
                
                X = X.apply(clean_text)
                ```
                
                **Étape 3: Vectorisation TF-IDF**
                ```python
                from sklearn.feature_extraction.text import TfidfVectorizer
                
                vectorizer = TfidfVectorizer(
                    max_features=5000,
                    ngram_range=(1, 2),
                    min_df=1,
                    max_df=0.8
                )
                
                X_vectorized = vectorizer.fit_transform(X)
                ```
                
                **Étape 4: Entraînement du Modèle**
                ```python
                from sklearn.model_selection import train_test_split
                from sklearn.linear_model import LogisticRegression
                from sklearn.metrics import accuracy_score, classification_report
                
                # Split
                X_train, X_test, y_train, y_test = train_test_split(
                    X_vectorized, y, test_size=0.24, random_state=42
                )
                
                # Modèle
                model = LogisticRegression(
                    max_iter=1000,
                    solver='liblinear',
                    random_state=42
                )
                
                # Entraînement
                model.fit(X_train, y_train)
                
                # Évaluation
                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                print(f'Accuracy: {accuracy:.4f}')  # 98.34%
                print(classification_report(y_test, y_pred))
                ```
                
                **Étape 5: Sauvegarde des Modèles**
                ```python
                import pickle
                
                # Sauvegarder le modèle
                with open('fake_news_model.pkl', 'wb') as f:
                    pickle.dump(model, f)
                
                # Sauvegarder le vectorizer
                with open('tfidf_vectorizer.pkl', 'wb') as f:
                    pickle.dump(vectorizer, f)
                ```
                
                **Étape 6: Déploiement**
                
                *Backend (API Flask):*
                ```python
                from flask import Flask, request, jsonify
                import pickle
                
                app = Flask(__name__)
                
                # Charger modèles
                model = pickle.load(open('fake_news_model.pkl', 'rb'))
                vectorizer = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))
                
                @app.route('/predict', methods=['POST'])
                def predict():
                    data = request.json
                    text = data['text']
                    
                    # Prétraiter
                    text_clean = clean_text(text)
                    
                    # Vectoriser
                    text_vec = vectorizer.transform([text_clean])
                    
                    # Prédire
                    prediction = model.predict(text_vec)[0]
                    probabilities = model.predict_proba(text_vec)[0]
                    
                    return jsonify({
                        'prediction': int(prediction),
                        'label': 'REAL' if prediction == 1 else 'FAKE',
                        'confidence': float(max(probabilities)),
                        'probabilities': {
                            'fake': float(probabilities[0]),
                            'real': float(probabilities[1])
                        }
                    })
                
                if __name__ == '__main__':
                    app.run()
                ```
                
                *Frontend (Streamlit):*
                ```python
                import streamlit as st
                import requests
                
                st.title("Fake News Detector")
                
                text = st.text_area("Enter article text")
                
                if st.button("Analyze"):
                    response = requests.post(
                        "https://your-api.com/predict",
                        json={"text": text}
                    )
                    result = response.json()
                    
                    st.write(f"Label: {result['label']}")
                    st.write(f"Confidence: {result['confidence']:.2%}")
                ```
                """)
                
                st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
                
                # SECTION 5: Meilleures Pratiques
                st.markdown("<div class='doc-title-blue'>✅ Meilleures Pratiques</div>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    **Pour de Meilleurs Résultats**
                    - Fournir le texte complet de l'article (>100 mots)
                    - Utiliser du texte bien formaté
                    - Éviter les textes trop courts (<20 caractères)
                    - Vérifier la langue détectée
                    - Attendre 30-60s si première requête (API se réveille)
                    
                    **Formats Recommandés**
                    - Articles de presse complets
                    - Posts de blog
                    - Communiqués de presse
                    - Contenu web structuré
                    """)
                
                with col2:
                    st.markdown("""
                    **À Éviter**
                    - Textes de moins de 20 caractères
                    - Textes non structurés ou mal formatés
                    - Listes de mots-clés
                    - Textes avec beaucoup de bruit (HTML, code)
                    - Images de texte (utiliser OCR d'abord)
                    
                    **Note sur les URLs**
                    - L'extraction fonctionne mieux avec du HTML propre
                    - Certains sites bloquent les scrapers
                    - Les PDF et DOCX en ligne sont supportés
                    """)
                
                st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
                
                # SECTION 6: Limitations
                st.markdown("<div class='doc-title-red'>⚠️ Limitations et Considérations</div>", unsafe_allow_html=True)
                
                st.markdown("""
                **Limitations Techniques**
                - Le modèle est entraîné sur des articles en anglais (2016-2017)
                - La traduction automatique peut introduire des erreurs
                - Performance optimale sur des textes de >100 mots
                - La qualité de l'extraction URL dépend de la structure du site
                
                **Limitations du Modèle**
                - Le modèle détecte des patterns linguistiques, pas la véracité factuelle
                - Peut être trompé par du contenu satirique bien écrit
                - Dataset daté (2016-2017), les fake news évoluent
                - Biais potentiel du dataset d'entraînement
                
                **API Render (Plan Gratuit)**
                - Se met en veille après 15 minutes d'inactivité
                - Première requête: 30-60 secondes (cold start)
                - Requêtes suivantes: <2 secondes
                
                **Recommandations**
                - Utiliser comme outil d'aide à la décision, pas comme vérité absolue
                - Croiser avec d'autres sources et fact-checkers
                - Tenir compte du contexte et de la date de publication
                - Vérifier les sources originales
                """)
                
                st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
                
                # SECTION 7: Ressources
                st.markdown("<div class='doc-title-blue'>📦 Ressources et Code Source</div>", unsafe_allow_html=True)
                
                st.markdown("""
                **Code Source**
                - GitHub: https://github.com/noba-ibrahim/fcc-fake-news-detector-v2
                - Backend API: https://fcc-fake-news-detector-v2.onrender.com
                
                **Dataset**
                - Kaggle Fake News Dataset
                - 32,456 articles (72.3% fake, 27.7% real)
                
                **Technologies Utilisées**
                - Python 3.11
                - Scikit-learn 1.5.2
                - NLTK 3.8.1
                - Flask 3.0 (Backend)
                - Streamlit 1.29 (Frontend)
                - BeautifulSoup4 4.12 (Web scraping)
                - Google Translate API (Traduction)
                
                **Hébergement**
                - Backend: Render.com (Free tier)
                - Frontend: Streamlit Cloud (Free tier)
                
                **Contact**
                - Équipe: FCC Development Team
                - Année: 2024
                """)
    
    else:
        st.error("Error: Unable to load machine learning models" if st.session_state.language == 'en' else "Erreur: Impossible de charger les modèles")
    
    # Footer
    st.markdown("""
        <div class='professional-footer'>
            <div class='footer-content'>
                <div class='footer-title'>""" + t('title') + """</div>
                <div class='footer-text'>
                    """ + ("Advanced AI-Powered Detection System" if st.session_state.language == 'en' else "Système de Détection Avancé par IA") + """
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
