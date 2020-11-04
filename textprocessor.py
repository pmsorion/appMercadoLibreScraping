from bs4 import BeautifulSoup
import requests
import random
import json

class textprocessor:

    def processWordtoWord(word):
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
        url = (f'http://listado.mercadolibre.com.mx/{word}#D[A:{word},L:1]')

        response = requests.get(url,headers=headers)#, proxies=proxies)

        items = []

        content = response.content
        soup = BeautifulSoup(content, 'lxml')

        for item in soup.select('.ui-search-layout__item'):
            try:
                items.append([item.select('a')[0]['title'], item.select('a')[0]['href'], item.select('.price-tag')[0].get_text(), item.select('.ui-search-result-image__element')[0]['data-src']])
            except:
                Exception

        LIMIT = 3
        counter = 0
        podium = []
        while counter < LIMIT:
            podium.append(items[random.randrange(0, len(items), 1)])
            counter += 1

        json_podium = json.dumps(podium, ensure_ascii=False)
        data_podium = {}
        data_podium["products"] = []
        data_podium["products"].append(json_podium)

        return data_podium

    def processWords(words):
        word = words[random.randrange(0, len(words), 1)]
        data_podium = textprocessor.processWordtoWord(word)
        return data_podium