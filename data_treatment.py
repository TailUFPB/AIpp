import threading
import os
import pandas as pd
import re
import csv
import datetime
from google_play_scraper import app

#O objetivo inicial era usar a biblioteca PyDrive para acessar o GoogleDrive de Icaro e não precisar baixar todos os .csvs
#Mas, por bugs que não consegui resolver (nem com ajuda do chat gpt), tive que baixar os arquivos na minha máquina 

def data_cleaning(df):
    df = df.drop(['reviewId', 'userName', 'userImage', 'reviewCreatedVersion', 'replyContent', 'repliedAt'], axis=1)

    df['at'] = pd.to_datetime(df['at'], errors='coerce')
    df['at'] = df['at'].dt.strftime('%d/%m/%Y')

    df = df.rename({'content': 'reviews', 'thumbsUpCount':'likes', 'at':'time'}, axis = 1)

    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df['likes'] = pd.to_numeric(df['likes'], errors='coerce')

    regex = r'^\d\d/\d\d/'
    df['year'] = df['time'].str.replace(regex, '', regex=True).str.strip()
    df['year'] = pd.to_numeric(df['year'], errors='coerce')

    df = df.dropna()

    return df

def df_concat(folder_name):
    print(f'Concatenando {folder_name}')

    basepath = f'../Datasets/{folder_name}'
    save_path = f'data/'
    files = os.listdir(basepath) #Lista de todos os arquivos .csv do diretorio
    df_final = pd.DataFrame()

    for f in files:
        if f == folder_name+'.csv': #Se rodar o codigo outra vez, evita de pegar o csv que ja foi concatenado antes
            continue

        file_path = os.path.join(basepath, f)

        #Gera warning de mixed dtypes para colunas de score, thumbsUpCount, replyContent e repliedAt
        #É possível corrigir o warning passando o parâmetro low_memory=False, porém é muito custoso
        #Também é possível passar um dicionário como parâmetro, definindo em que tipo de dados essas colunas devem ser lidas, porém quando fiz bugou o código
        df = pd.read_csv(file_path)

        app_id = re.sub(r'_reviews.csv$', '', f) #Remove o final '_reviews.csv' para usar apenas o id do aplicativo
        result = app(app_id, lang='pt', country='br')

        df['app_name'] = result['title']
        df_final = pd.concat([df_final, df], ignore_index=True)
    
    df_final = data_cleaning(df_final)

    df_final.to_csv(f'{os.path.join(save_path, folder_name)}.csv', quotechar='"', escapechar='\\', quoting=csv.QUOTE_NONNUMERIC, index=False)

    print(f'Finalizou a concatenacao de {folder_name}')

if __name__ == '__main__':
    basepath = '../Datasets/'
    folders = []

    #Para rodar esse código, você deve conter os arquivos .csvs dos aplicativos em uma pasta Datasets na sua máquina
    #Para alterar o caminho dessa pasta, modifique a variável basepath na main e no método df_concat  
    for entry in os.listdir(basepath):
        if os.path.isdir(os.path.join(basepath, entry)): #Lista dos diretorios da pasta 'data/'
            folders.append(entry)
    
    threads = []
    for folder in folders:
        t = threading.Thread(target=df_concat, args=(folder,))
        threads.append(t)
        t.start() #Inicia as threads para cada um dos diretorios
    
    for t in threads:
        t.join()
