# -*- coding: utf-8 -*-
"""
🎬 YouTube Summarizer Pro — Application Streamlit
Version 12.0

Usage:
    streamlit run app.py
"""

import streamlit as st
import sys
import os

# Ajouter le répertoire au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import VERSION, APP_NAME, CATEGORIES, LANGUAGES, MODES
from utils.validators import is_valid_youtube_url, extract_video_id, is_playlist_url
from utils.formatters import format_duration_human, truncate_text
from core.extractor import extract_transcript, get_playlist_videos
from core.detector import detect_category
from core.summarizer import generate_summary, generate_meta_analysis
from core.exporter import export_to_markdown, export_to_docx, export_to_pdf, get_download_filename


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION DE LA PAGE
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': f"# {APP_NAME} v{VERSION}\n\nRésumez n'importe quelle vidéo YouTube en quelques secondes."
    }
)

# ═══════════════════════════════════════════════════════════════════════════════
# STYLES CSS PERSONNALISÉS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* Style général */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FF0000, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    /* Cards de statistiques */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .stat-label {
        font-size: 0.85rem;
        opacity: 0.9;
    }
    
    /* Badges catégorie */
    .category-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Zone de résumé */
    .summary-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        border-left: 4px solid #667eea;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #999;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# INITIALISATION DE L'ÉTAT
# ═══════════════════════════════════════════════════════════════════════════════

if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'video_info' not in st.session_state:
    st.session_state.video_info = None
if 'category' not in st.session_state:
    st.session_state.category = None
if 'processing' not in st.session_state:
    st.session_state.processing = False


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR - CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_%282017%29.svg", width=50)
    st.title("⚙️ Configuration")
    
    st.divider()
    
    # API Key
    st.subheader("🔑 Clé API")
    provider = st.radio(
        "Provider",
        ["Anthropic (Claude)", "OpenAI (GPT-4)"],
        horizontal=True,
        help="Choisissez votre fournisseur d'IA"
    )
    
    provider_key = "anthropic" if "Anthropic" in provider else "openai"
    
    api_key = st.text_input(
        "Clé API",
        type="password",
        placeholder="sk-ant-... ou sk-...",
        help="Votre clé API Anthropic ou OpenAI"
    )
    
    st.divider()
    
    # Langue
    st.subheader("🌍 Langue")
    lang_options = {f"{v['flag']} {v['name']}": k for k, v in LANGUAGES.items()}
    selected_lang = st.radio(
        "Langue du résumé",
        list(lang_options.keys()),
        horizontal=True
    )
    lang = lang_options[selected_lang]
    
    st.divider()
    
    # Mode
    st.subheader("📊 Mode d'analyse")
    mode_options = {f"{v['icon']} {v['name']}": k for k, v in MODES.items()}
    selected_mode = st.radio(
        "Niveau de détail",
        list(mode_options.keys()),
        help="Accessible = synthèse claire | Expert = analyse approfondie"
    )
    mode = mode_options[selected_mode]
    
    st.divider()
    
    # Options d'export
    st.subheader("📁 Export")
    export_md = st.checkbox("Markdown (.md)", value=True)
    export_docx = st.checkbox("Word (.docx)", value=True)
    export_pdf = st.checkbox("PDF (.pdf)", value=False)
    
    st.divider()
    
    # Infos
    st.caption(f"v{VERSION} • Made with ❤️")
    st.caption("[GitHub](https://github.com) • [Documentation](https://docs.example.com)")


# ═══════════════════════════════════════════════════════════════════════════════
# CONTENU PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

# Header
st.markdown('<h1 class="main-header">🎬 YouTube Summarizer Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transformez n\'importe quelle vidéo YouTube en synthèse professionnelle</p>', unsafe_allow_html=True)

# Zone d'input
col1, col2 = st.columns([4, 1])

with col1:
    url = st.text_input(
        "📺 URL YouTube",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed"
    )

with col2:
    analyze_btn = st.button(
        "🚀 Analyser",
        type="primary",
        use_container_width=True,
        disabled=not url or not api_key
    )

# Message si pas de clé API
if not api_key:
    st.info("👈 Entrez votre clé API dans la barre latérale pour commencer.")


# ═══════════════════════════════════════════════════════════════════════════════
# TRAITEMENT
# ═══════════════════════════════════════════════════════════════════════════════

if analyze_btn and url and api_key:
    
    # Validation de l'URL
    if not is_valid_youtube_url(url):
        st.error("❌ URL YouTube invalide. Vérifiez le format de l'URL.")
    else:
        # Réinitialiser l'état
        st.session_state.summary = None
        st.session_state.video_info = None
        st.session_state.category = None
        
        # Conteneur de progression
        with st.status("🔄 Analyse en cours...", expanded=True) as status:
            
            try:
                # ═══════════════════════════════════════════════════════════════
                # ÉTAPE 1: Extraction
                # ═══════════════════════════════════════════════════════════════
                st.write("📥 **Extraction du transcript...**")
                
                video_info = extract_transcript(url, lang)
                st.session_state.video_info = video_info
                
                st.success(f"✅ Vidéo trouvée : {truncate_text(video_info.title, 60)}")
                st.caption(f"Durée : {format_duration_human(video_info.duration, lang)} • {len(video_info.transcript):,} caractères")
                
                # ═══════════════════════════════════════════════════════════════
                # ÉTAPE 2: Détection de catégorie
                # ═══════════════════════════════════════════════════════════════
                st.write("🔍 **Détection de la catégorie...**")
                
                category, confidence, method = detect_category(
                    video_info.transcript,
                    video_info.title,
                    video_info.channel,
                    api_key,
                    provider_key
                )
                st.session_state.category = category
                
                cat_info = CATEGORIES.get(category, CATEGORIES["default"])
                st.success(f"✅ Catégorie : {cat_info['name']} (confiance: {confidence:.0%})")
                
                # ═══════════════════════════════════════════════════════════════
                # ÉTAPE 3: Génération du résumé
                # ═══════════════════════════════════════════════════════════════
                st.write("✨ **Génération du résumé...**")
                st.caption("Cela peut prendre 30-60 secondes selon la longueur de la vidéo...")
                
                summary = generate_summary(
                    transcript=video_info.transcript,
                    title=video_info.title,
                    category=category,
                    api_key=api_key,
                    lang=lang,
                    mode=mode,
                    provider=provider_key,
                    duration_str=format_duration_human(video_info.duration, lang)
                )
                st.session_state.summary = summary
                
                st.success("✅ Résumé généré avec succès !")
                
                status.update(label="✅ Analyse terminée !", state="complete", expanded=False)
                
            except Exception as e:
                status.update(label="❌ Erreur", state="error")
                st.error(f"Une erreur s'est produite : {str(e)}")
                st.exception(e)


# ═══════════════════════════════════════════════════════════════════════════════
# AFFICHAGE DU RÉSULTAT
# ═══════════════════════════════════════════════════════════════════════════════

if st.session_state.summary:
    
    st.divider()
    
    # Métadonnées
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.session_state.category:
            cat_info = CATEGORIES.get(st.session_state.category, CATEGORIES["default"])
            st.metric("📁 Catégorie", cat_info['name'])
    
    with col2:
        if st.session_state.video_info:
            st.metric("⏱️ Durée", format_duration_human(st.session_state.video_info.duration, lang))
    
    with col3:
        word_count = len(st.session_state.summary.split())
        st.metric("📝 Mots", f"{word_count:,}")
    
    with col4:
        reading_time = max(1, round(word_count / 200))
        st.metric("📖 Lecture", f"~{reading_time} min")
    
    st.divider()
    
    # Résumé
    st.subheader("📝 Résumé")
    
    # Container scrollable pour le résumé
    st.markdown(st.session_state.summary)
    
    st.divider()
    
    # Boutons de téléchargement
    st.subheader("📥 Télécharger")
    
    col1, col2, col3 = st.columns(3)
    
    # Métadonnées pour l'export
    metadata = {}
    if st.session_state.video_info:
        metadata = {
            "category": CATEGORIES.get(st.session_state.category, {}).get("name", ""),
            "duration": format_duration_human(st.session_state.video_info.duration, lang),
            "video_id": st.session_state.video_info.video_id
        }
    
    title = st.session_state.video_info.title if st.session_state.video_info else "video"
    
    with col1:
        if export_md:
            md_content = export_to_markdown(st.session_state.summary, title, metadata)
            st.download_button(
                "📄 Markdown (.md)",
                md_content,
                file_name=get_download_filename(title, "md"),
                mime="text/markdown",
                use_container_width=True
            )
    
    with col2:
        if export_docx:
            try:
                docx_bytes = export_to_docx(st.session_state.summary, title, metadata)
                st.download_button(
                    "📘 Word (.docx)",
                    docx_bytes,
                    file_name=get_download_filename(title, "docx"),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            except ImportError:
                st.warning("Module python-docx non installé")
    
    with col3:
        if export_pdf:
            try:
                pdf_bytes = export_to_pdf(st.session_state.summary, title, metadata)
                st.download_button(
                    "📕 PDF (.pdf)",
                    pdf_bytes,
                    file_name=get_download_filename(title, "pdf"),
                    mime="application/pdf",
                    use_container_width=True
                )
            except ImportError:
                st.warning("Module fpdf2 non installé")


# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(
    f'<div class="footer">YouTube Summarizer Pro v{VERSION} • '
    f'Powered by Claude & GPT-4 • '
    f'<a href="https://github.com">GitHub</a></div>',
    unsafe_allow_html=True
)
