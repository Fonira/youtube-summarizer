# 🎬 YouTube Summarizer Pro v12.0

> Transformez n'importe quelle vidéo YouTube en synthèse professionnelle grâce à l'IA.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-191919?style=for-the-badge&logo=anthropic&logoColor=white)

## ✨ Fonctionnalités

- 🔍 **Détection automatique** de 12 catégories de vidéos
- 🤖 **IA avancée** : Claude (Anthropic) ou GPT-4 (OpenAI)
- 🌍 **Multilingue** : Français et Anglais
- 📊 **2 modes** : Accessible ou Expert
- 📥 **Export** : Markdown, Word (DOCX), PDF
- ⚡ **Ultra-rapide** : Résumé en moins de 60 secondes

## 🚀 Déploiement sur Streamlit Cloud

### Étape 1 : Créer un repo GitHub

1. Créez un nouveau repository sur GitHub
2. Uploadez tous les fichiers de ce dossier
3. Assurez-vous que la structure est :

```
your-repo/
├── app.py                 # Application principale
├── requirements.txt       # Dépendances
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── channels.py
├── core/
│   ├── __init__.py
│   ├── extractor.py
│   ├── detector.py
│   ├── summarizer.py
│   └── exporter.py
├── prompts/
│   ├── __init__.py
│   ├── fr.py
│   └── en.py
└── utils/
    ├── __init__.py
    ├── validators.py
    └── formatters.py
```

### Étape 2 : Déployer sur Streamlit Cloud

1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez-vous avec votre compte GitHub
3. Cliquez sur "New app"
4. Sélectionnez votre repository
5. Main file path : `app.py`
6. Cliquez sur "Deploy!"

### Étape 3 : C'est prêt ! 🎉

Votre app sera accessible à : `https://votre-app.streamlit.app`

## 🔧 Configuration locale

```bash
# Cloner le repo
git clone https://github.com/votre-user/youtube-summarizer.git
cd youtube-summarizer

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

## 📋 Catégories détectées

| Catégorie | Emoji | Description |
|-----------|-------|-------------|
| Interview/Podcast | 🎙️ | Entretiens, podcasts, discussions |
| Vulgarisation | 🔬 | Science, éducation grand public |
| Tutoriel | 🎓 | Guides pratiques, how-to |
| Cours | 📚 | Formations académiques |
| Conférence | 🎤 | TED talks, présentations |
| Documentaire | 🎬 | Reportages, enquêtes |
| Débat | ⚖️ | Confrontations d'idées |
| Journalisme | 📰 | Actualités, news |
| Gaming | 🎮 | Gameplay, let's play |
| Finance | 💰 | Investissement, crypto |
| Review | ⭐ | Tests produits |
| Lifestyle | 🌟 | Vlogs, routines |

## 🔑 Clés API requises

- **Anthropic (Claude)** : [console.anthropic.com](https://console.anthropic.com)
- **OpenAI (GPT-4)** : [platform.openai.com](https://platform.openai.com)

## 📄 Licence

MIT License - Libre d'utilisation et de modification.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une PR.

---

Made with ❤️ using Claude & Streamlit
