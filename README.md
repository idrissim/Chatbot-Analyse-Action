---

# ChatBot : Plateforme d'Analyse Financière des Actions en Bourse 📈

## Description

ChatBot est une plateforme interactive et intuitive pour l'analyse financière des actions en bourse. Elle utilise des techniques de machine learning et de visualisation de données pour fournir aux utilisateurs des métriques financières en temps réel et une analyse graphique pour n'importe quel symbole boursier. Les technologies utilisées incluent Python, OpenAI GPT-4, Streamlit et yfinance.

## Fonctionnalités 🌟

- Récupération du dernier prix de l'action en temps réel
- Calcul de la Moyenne Mobile Simple (SMA)
- Calcul de la Moyenne Mobile Exponentielle (EMA)
- Calcul de l'Indice de Force Relative (RSI)
- Calcul du MACD (Moving Average Convergence/Divergence)
- Affichage graphique du prix de l'action

## Prérequis 📋

- Python 3.x
- pip (Gestionnaire de paquets Python)
- Clé API OpenAI

## Installation 🛠

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/idrissim/Chatbot-Analyse-Action.git
   ```
   
2. Accédez au répertoire du projet :
   ```bash
   cd Chatbot-Analyse-Action
   ```
   
3. Installez les paquets requis :
   ```bash
   pip install -r requirements.txt
   ```
   
4. Placez votre clé API OpenAI dans un fichier nommé `API_KEY`.

## Build 🏗

Pour le moment, le projet ne nécessite pas d'étape de build spécifique. Il s'exécute directement via Streamlit.

## Utilisation 🚀

Lancez l'application Streamlit :
```bash
streamlit run Chatbot.py
```

Rendez-vous simplement sur l'interface web et commencez à interagir avec le chatbot pour effectuer des analyses financières sur divers symboles boursiers.

## Structure du Code 🏗

- La fonction `get_stock_price(ticker)` récupère le dernier prix de l'action.
- `calculate_SMA(ticker, window)` calcule la Moyenne Mobile Simple.
- `calculate_EMA(ticker, window)` calcule la Moyenne Mobile Exponentielle.
- `calculate_RSI(ticker)` calcule l'Indice de Force Relative.
- `calculate_MACD(ticker)` calcule le MACD.
- `plot_stock_price(ticker)` affiche le graphique du prix de l'action sur la dernière année.

## Contribution 👥

Si vous souhaitez contribuer, merci de forker le dépôt et de faire les modifications que vous jugez utiles. Les pull requests sont les bienvenues.

## Licence 📝

Licence MIT

## Contact 📞

Pour toute question, n'hésitez pas à ouvrir une issue github.
---
