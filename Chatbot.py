# importation des modules
# json : pour manipuler les données au format JSON.
# openai : pour utiliser le modèle GPT-4 pour les interactions en langage naturel.
# pandas : pour la manipulation des données.
# matplotlib : pour les visualisations graphiques.
# streamlit : pour créer l'interface utilisateur web.
# yfinance : pour récupérer les données financières.
import json
import openai
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf

# la clé API d'OpenAI est lue à partir d'un fichier appelé API_KEY.
openai.api_key = open('API_KEY', 'r').read()

# Fonctions pour le calcul des indicateurs financiers
# get_stock_price(ticker): Récupère le dernier prix de clôture de l'action.
# calculate_SMA(ticker, window): Calcule la moyenne mobile simple.
# calculate_EMA(ticker, window): Calcule la moyenne mobile exponentielle.
# calculate_RSI(ticker): Calcule l'indice de force relative (si l'action est surachetée ou survendue).
# calculate_MACD(ticker): Calcule le MACD Moving Average Convergence/Divergence (convergence et divergence des moyennes mobiles).
# plot_stock_price(ticker): Affiche le graphique des prix de l'action sur un an.formule de collecte des prix
def get_stock_price(ticker):
    return str(yf.Ticker(ticker).history(period='1y').iloc[-1]['Close'])
def calculate_SMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.rolling(window=window).mean().iloc[-1])
def calculate_EMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.ewm(span=window, adjust=false).mean().iloc[-1])
def calculate_RSI(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    delta = data.diff()
    up = delta.clip(upper=8)
    down = -1 * delta.clip(upper=8)
    ema_up = up.ewm(com=14-1, adjust=False).mean()
    ema_down = down.ewm(com=14-1, adjust=False).mean()
    rs = ema_up / ema_down
    return str(100 - (100 / (1+rs)).iloc[-1])
def calculate_MACD(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    short_EMA = data.ewm(span=12, adjust=False).mean()
    long_EMA = data.ewm(span=26, adjust=False).mean()
    MACD = short_EMA - long_EMA
    signal = MACD.ewm(span=9, adjust=False).mean()
    MACD_histogram = MACD - signal
    return f'{MACD[-1]}, {signal[-1]}, {MACD_histogram[-1]}'
def plot_stock_price(ticker):
    data = yf.Ticker(ticker).history(period='1y')
    plt.figure(figsize=(10,5))
    plt.plot(data.index, data.Close)
    plt.title('{ticker} Stock Prise Over Last Year')
    plt.xlabel('Date')
    plt.ylabel('Stock Prise (MAD)')
    plt.grid(True)
    plt.savefig('stock.png')
    plt.close()

#La liste functions définit les fonctions disponibles, leurs descriptions et les paramètres requis.
functions = [
    {
        'name': 'get_stock_price',
        'description': "obtient le dernier prix de l'action en fonction du symbole d'une action d'entreprise en bourse.",
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': "le symbole d'une action d'entreprise en bourse (par exemple le ticker de l'entreprise Tesla est TSLA)",
                },
            },
            'required': ['ticker'],
        },
    },
    {
        'name':'calculate_SMA',
        'description':"Calcule la moyenne mobile simple pour un symbole boursier donné et une fenêtre de temps",
        'parameters' : {
            'type':'object',
            'properties':{
                'ticker':{
                    'type': 'string',
                    'description':"le symbole boursier d'une action d'entreprise (par exemple le ticker de l'entreprise Tesla est TSLA)",
                },
                 'window':{
                    'type': 'integer',
                    'description':"le nombre de jours ouvrés sur la période de calcul",
                },
            },
             'required':['ticker','window'],
        },
    },
    {
        'name':'calculate_EMA',
        'description':"Calcule la moyenne mobile exponentielle pour un symbole boursier donné et une fenêtre de temps (entre deux dates spécifiques).",
        'parameters' : {
            'type':'object',
            'properties':{
                'ticker':{
                    'type': 'string',
                    'description':"le symbole boursier d'une action d'entreprise (par exemple le ticker de l'entreprise Tesla est TSLA)",
                },
                 'window':{
                    'type': 'integer',
                    'description':"le nombre de jours ouvrés sur la période de calcul",
                },
            },
             'required':['ticker','window'],
        },
    },
    {
        'name':'calculate_RSI',
        'description':"Calcule l'Indice de Force Relative (Relative Strength Index) pour un symbole boursier donné.",
        'parameters' : {
            'type':'object',
            'properties':{
                'ticker':{
                    'type': 'string',
                    'description':"le symbole boursier d'une action d'entreprise (par exemple le ticker de l'entreprise Tesla est TSLA)",
                },
            },
             'required':['ticker'],
        },
    },
    {
        'name':'calculate_MACD',
        'description':'Calcule les tendances de convergence et divergence des moyennes mobiles (Moving Average Convergence Divergence) pour un symbole boursier donné.',
        'parameters' : {
            'type':'object',
            'properties':{
                'ticker':{
                    'type': 'string',
                    'description':"le symbole boursier d'une action d'entreprise (par exemple le ticker de l'entreprise Tesla est TSLA)",
                },
            },
             'required':['ticker'],
        },
    },
    {
        'name':'plot_stock_price',
        'description':"donnes moi l'Analyse graphique des variations de prix pour un symbole boursier donné.",
        'parameters' : {
            'type':'object',
            'properties':{
                'ticker':{
                    'type': 'string',
                    'description':"le symbole boursier d'une action d'entreprise (par exemple le ticker de l'entreprise Tesla est TSLA)",
                },
            },
             'required':['ticker'],
        },
    },
]
available_functions = {
    'get_stock_price': get_stock_price,
    'calculate_SMA': calculate_SMA,
    'calculate_EMA': calculate_EMA,
    'calculate_RSI' : calculate_RSI,
    'calculate_MACD' : calculate_MACD,
    'plot_stock_price': plot_stock_price
}
#Streamlit pour l'interface utilisateur
#Configuration initiale: on initialise le stockage des messages échangés pour la session
if 'messages' not in st.session_state:
    st.session_state['messages']=[]
#Définit le titre et le champ de saisie pour l'utilisateur
st.title("ChatBot \n Plateforme interactive et intuitive pour l'analyse financière des actions en bourse.")
user_input = st.text_input('Posez votre question:')

#IMPORTANT! Traitement du message de l'utilisateur selon les étapes suivantes:
# 1. Le message de l'utilisateur est ajouté à la conversation st.session_state['messages'].
# 2. Une requête est envoyée à l'API OpenAI pour générer une réponse.
# 3. Si une fonction doit être appelée, elle est exécutée et sa réponse est affichée.
# 4. Sinon, le message généré par l'assistant est affiché.

# Si l'utilisateur a entré un message, il est ajouté à st.session_state['messages'], une liste qui conserve l'historique de la conversation.
if user_input:
    try:
        st.session_state['messages'].append({'role':'user', 'content':f'{user_input}'})
        # Appel à l'API GPT-4. On envoie l'historique des messages et les fonctions disponibles à OpenAI.
        # Le paramètre function_call='auto' permet au modèle de déclencher automatiquement des appels de fonction s'il le juge nécessaire.
        response = openai.ChatCompletion.create(
            model='gpt-4',
            #model='GPT-3.5-turbo-0613',
            messages=st.session_state['messages'],
            functions=functions,
            function_call='auto'
            )
        #La réponse est stockée dans response_message.
        response_message = response['choices'][0]['message']
        #Si le modèle a déclenché un appel de fonction, le nom de la fonction et ses arguments sont extraits.
        if response_message.get('function_call'):
            function_name=response_message['function_call']['name']
            # La function_args récupère les arguments que le modèle veut passer à cette fonction.
            # Les arguments sont au format JSON, donc ils sont convertis en un objet Python à l'aide de json.loads()
            function_args=json.loads(response_message['function_call']['arguments'])
             #Cette section prépare un dictionnaire args_dict qui contiendra les arguments à passer à la fonction.
            if function_name in ['get_stock_price','calculate_RSI', 'calculate_MACD', 'plot_stock_price']:
                 args_dict={'ticker':function_args.get('ticker')}
            # Pour les fonctions calculate_SMA et calculate_EMA, deux arguments sont nécessaires : ticker et window.
            elif function_name in ['calculate_SMA', 'calculate_EMA']:
                args_dict={'ticker':function_args.get('ticker'), 'window':function_args.get('window')}
            # La fonction correspondante est ensuite appelée avec les arguments appropriés.
            function_to_call = available_functions[function_name]
            function_response=function_to_call(**args_dict)
            # Si la fonction appelée était plot_stock_price, une image du graphique est affichée (stock.png).
            if function_name== 'plot_stock_price':
                st.image('stock.png')
            #Si une autre fonction a été appelée, alors le code fait actualise la conversation et fait à nouveau appel à l'API GPT :
            else:
                # Il ajoute le message de réponse initial à la conversation st.session_state['messages']. Ce message contiendra probablement une question de GPT comme "Voulez-vous connaître le dernier prix de l'action XYZ ?".
                st.session_state['messages'].append(response_message)
                # Il ajoute un autre message à la conversation qui représente la sortie de la fonction appelée. Ce message a un rôle spécial 'function' et contient le nom de la fonction appelée (function_name) ainsi que la réponse de cette fonction (function_response).
                st.session_state['messages'].append(
                    {
                        'role':'function',
                        'name':function_name,
                        'content':function_response
                    }
                )
                # Un second appel à l'API GPT est effectué. Cette fois, l'historique des messages contient également la sortie de la fonction appelée. Cela permet au modèle d'utiliser cette information pour générer une réponse plus contextualisée.
                second_response = openai.ChatCompletion.create(
                    model='gpt-4',
                    #model='GPT-3.5-turbo-0613',
                    messages=st.session_state['messages']
                    )
                # La nouvelle réponse du modèle est ensuite affichée à l'utilisateur via st.text(...).
                st.text(second_response['choices'][0]['message']['content'])
                # ce nouveau message est ajouté à st.session_state['messages'] pour maintenir l'historique de la conversation.
                st.session_state['messages'].append({'role':'assistant', 'content':second_response['choices'][0]['message']['content']})
        #Sinon, le texte de la réponse générée est affiché.
        else:
            st.text(response_message['content'])
            # Ce nouveau message est ajouté à st.session_state['messages'] pour maintenir l'historique de la conversation.
            st.session_state['messages'].append({'role':'assistant', 'content':response_message['content']})
    except Exception as e:
        # Gérer l'exception
        st.text(f"Une exception s'est produite : {e}")
        # raise e
        # st.text('Try again')
