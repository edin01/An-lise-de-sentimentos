import twint
import json
import os
from textblob import TextBlob
import numpy as np
import pandas as pd
import matplotlib.pyplot as mpl

# Variáveis
tws = [] # Vetor com os tweets
formatTweet = 'Perfil: {username} | Hora: {time} | Data: {date} | Tweet: {tweet}' # formato de saida
diretorio = 'E:\CC\VSCode Workbench\IA - Orlando\dados\\' # diretorio que salvará o txt dos tweets
txt = 'Tweets.txt' # Nome do arquivo
jsonBox = 'json.json'
idioma = 'en' # Apenas tweets em portugues
qtd = 1
listTweets = [] # lista com os tweets, apenas
mPolaridade = [] # Lista para armazenar polaridades
mSubjetividade = [] # Lista para armazenar subjetividades

def limpa_arqv(pasta, arq):
    print('\n' + '=='*50 + '\n')
    d = os.listdir(pasta)
    if arq in d: # se existir arquivo no diretorio, ele é deletado
        print(f'--- Aguarde, {arq} está sendo limpo... ----')
        os.remove(f'{pasta}/{arq}')
        print(f'{arq} limpo com sucesso!! \n')
        print('=='*50)
    else: # se não existir, não deleta
        print(f'Arquivo {arq} nao existe, nada será deletado \n')
        print('=='*50)


def tweets_twint(dado):
    c = twint.Config() # seta configuração para a pesquisa
    c.Search = dado # o que será pesquisado
    c.Limit = qtd # quantos tweets serão exibidos. 1 = 20 tweets.
    c.Format = formatTweet
    c.Output = diretorio + txt # salva os tweets em txt
    c.Lang = idioma # idioma dos tweets
    print(f'--- Primeiros 20 tweets sobre {p} --- \n')
    twint.run.Search(c)
    print('\n' + '=='*50)


def vetor_tweets(): # Abre o txt com os tweets salvos
    with open(diretorio + txt, 'r', encoding="utf8") as texto:
        for conteudo in texto.readlines(): #enquanto tiver linha, salva cada linha no vetor
            tweet = conteudo.split('|')
            tws.append(tweet[3].replace('Tweet:', '').replace('\n', '').replace('\\', '|')) 
            # Vetor salva todos os tweets ( apenas os tweets )

def analise_tweets():
    for tweets in tws:
        analise = TextBlob(tweets)
        polaridade = analise.sentiment.polarity
        subjetividade = analise.sentiment.subjectivity
        listTweets.append(tweets)
        mPolaridade.append(polaridade)
        mSubjetividade.append(subjetividade)
        print(f'\n Tweet: {tweets} \n Polaridade: {polaridade:.02f} \n Subjetividade: {subjetividade:.02f}')

def gera_json():
    listJson = []
    with open(diretorio + jsonBox, 'a') as jb:
        for i in range(0, len(listTweets)): # pode ser usado qualquer um dos 3 vetores, já que o tamanho é igual
            j = {'Tweet': listTweets[i],  
            'Polaridade': mPolaridade[i], 
            'Subjetividade': mSubjetividade[i]}
            listJson.append(j)
        json.dump(listJson, jb)
        
def gera_box():
    dados = pd.read_json(diretorio + jsonBox)
    print('\n Boxplot dos tweets:')
    dados.boxplot(column=['Polaridade','Subjetividade'],vert=False)
    mpl.show()


limpa_arqv(diretorio, txt) # Deleta o arquivo de tweet, caso ele já exista 
p = input(str('O que pretende pesquisar? \n'))
tweets_twint(p) # Lista os 20 tweets
vetor_tweets() # Vetor com as frases criado
analise_tweets() # printa os tweets, com as respectivas polaridades e subjetividades
print('=='*50 + '\n')
print(f'Média de polaridade: {np.mean(mPolaridade):.02f}') # -1 = neg \\ 1 = posi
print(f'Média de subjetividade: {np.mean(mSubjetividade):.02f}') # 1 = subjetivo
limpa_arqv(diretorio, jsonBox) # Deleta o json caso ele já exista 
gera_json() # Gera o Json com os tweets pesquisados
gera_box() # Gera o boxplot