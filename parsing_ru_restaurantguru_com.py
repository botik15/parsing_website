import json
import time
from random import randint

import openpyxl
import requests
from bs4 import BeautifulSoup
from getuseragent import UserAgent

useragent = UserAgent()
theuseragent = useragent.Random()
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}



print(theuseragent)

xlsx = 'output2.xlsx'


# парсинг старинцы
def bs4(url):
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


# __________________________________________________startCreateJson()____________________________________________________
# пасринг всех url адросов с меню
def urlHomePage(url):
    urls = []
    count = 0
    # urls_all = []
    soup = bs4(url)  # Парсинг старницы
    for item in soup.find_all('div','cities_block'):

        if item.find('div','part_title').find('a'):
            urls.append(item.find('a')['href'])
        else:
            for i in item.find('ul','cities_link').find_all('li'):
                # urls_all.append(i.find('a')['href']) #url все
                count += int(i.find('a').find('span').text.replace("/","").replace(" ","")) # количество ресторанов

    print(urls)
    print(count)

    for i,url in enumerate(urls):
        print(f'{i} - {len(urls)} - {url}')
        soup = bs4(url)  # Парсинг старницы
        time.sleep(randint(1,2))
        for i in soup.find('ul','cities-list').find_all('li'):
            count += int(i.find('span', 'city-cnt').text.replace(" ",""))
        # break

    print(count)
    return urls


def startCreateJson(filename):
    # парсинг всех ссылок в json
    url = 'https://ru.restaurantguru.com/cities-Georgia-c'  # Ссылка на сайта
    data_urls = urlHomePage(url)

# ______________________________________________________Основые функции_________________________________________________
def main():
    filename = 'url.json'  # json файл с ссылками с категориями и url
    filename2 = 'url2.json'  # json файл с товароами(готовый json)

    startCreateJson(filename)


if __name__ == "__main__":
    main()
