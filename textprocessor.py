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
        data_podium = {}

        if len(items) > 0:
            while counter < LIMIT:
                subitem = random.randrange(0, len(items), 1)
                # podium.append(({"name": items[subitem][0]}, {"url": items[subitem][1]}, {"price": items[subitem][2]}, {"img": items[subitem][3]}))
                podium.append([{"name": items[subitem][0], "url": items[subitem][1], "price": items[subitem][2], "img": items[subitem][3]}])
                counter += 1

            json_podium = json.dumps(podium, ensure_ascii=False)
            data_podium["products"] = []
            data_podium["products"].append(json_podium)

        if not 'products' in data_podium or len(data_podium['products']) == 0:
            data_podium = {'error': 'informacion no encontrada'}

        return data_podium

    def processWords(words):
        if len(words) > 0:
            word = words[random.randrange(0, len(words), 1)]
            data_podium = textprocessor.processWordtoWord(word)
        else:
            data_podium = {'error': 'informacion no encontrada'}

        return data_podium