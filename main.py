import csv
import threading
import time
from google_play_scraper import app, reviews
import os

#Use o arquivo "info.txt" para escolher os apps que irao ser scrapados
#Basta inserir os ids deles
#Caso queira um numero diferente de 100000 para reviews, altere "max_reviews"

def scraper(line):
    # Limpa os caracteres no fim da linha
    line = line.strip()
    app_id = line

    # Quantidade de reviews a serem buscadas
    max_reviews = 100000
    parse_numeric = 0

    print('Iniciando Scraping de', app_id)

    #Conferindo o total de reviews atual do app
    result = app(app_id, 'pt', 'br')
    reviews_total = result['reviews']
    print(app_id, 'total de reviews:', reviews_total)

    # Confere se max_reviews esta acima da quantidade atual de reviews do app, se sim alerta o usuario
    if reviews_total < max_reviews:
        max_reviews = reviews_total
        print('Novo total de reviews de', app_id,'eh:', max_reviews)

    # Inicia o timer da operacao
    start_time = time.time()
    while parse_numeric < max_reviews:
        # Faz o scraping dos dados
        reviews_list, parse = reviews(app_id, 'pt', 'br', count=max_reviews-parse_numeric)
        # Cria uma thread para salvar as reviews em um arquivo CSV
        t = threading.Thread(target=save_reviews, args=(app_id, reviews_list))
        t.start()
        # Sleep necessario para finalizar a escrita do arquivo, se conseguir uma forma mais eficiente, remova-o
        time.sleep(2)
        # Abre o arquivo recem criado, conta a quantidade de linhas e passa novamente
        # A API nao trabalha perfeitamente e entrega valores semi-aleatorios para "max_reviews"
        # isso e um failsafe para evitar que seu CSV nao tenha o minimo requerido 
        file_name = app_id + '_reviews.csv'
        with open('data/'+file_name, 'r', encoding='utf-8') as f:
            # Conta a quantidade de linhas
            reader = csv.reader(f)
            parse_numeric = sum(1 for row in reader) - 1
            parse = parse_numeric
    # Finaliza o timer da operacao
    elapsed_time= time.time() - start_time
    print('Finalizado o Scraping de', app_id,'com o tempo final:', elapsed_time)


def save_reviews(app_id, reviews_list):
    file_name = app_id + '_reviews.csv'
    with open('data/'+file_name, 'a', newline='', encoding='utf-8') as file:
        # Criando o CSV
        writer = csv.DictWriter(file, fieldnames=reviews_list[0].keys())
        writer.writeheader()
        writer.writerows(reviews_list)


if __name__ == '__main__':

    if not os.path.exists('data'):
        os.makedirs('data')

    # Abre o arquivo "info.txt"
    # Para usar o programa basta inserir em cada linha o id do aplicativo
    with open('info.txt', 'r') as f:
        threads = []
        for line in f:
            t = threading.Thread(target=scraper, args=(line,))
            threads.append(t)
            t.start()

        # Espera todas as threads finalizarem antes de encerrar o programa
        for t in threads:
            t.join()