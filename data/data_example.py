import pandas as pd
import csv
from google_play_scraper import Sort, reviews_all

result = reviews_all('tv.pluto.android',
                    lang='pt',
                    country='br',
                    sort=Sort.NEWEST)

df = pd.DataFrame(result)
df = df.drop(['reviewId', 'userName', 'userImage', 'reviewCreatedVersion', 'replyContent', 'repliedAt'], axis=1)
df = df.dropna()

#quotechar e escapechar evitam de dar erro em comentários com caracteres especiais (emojis, apenas pontuações e etc)
df.to_csv('plutotv_example.csv', quotechar='"', escapechar='\\', quoting=csv.QUOTE_NONNUMERIC, index=False)