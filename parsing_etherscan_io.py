import asyncio
import time
import aiohttp
import requests
from bs4 import BeautifulSoup
from getuseragent import UserAgent

# Ссылка с указанием в URL страниц но без номера
url_page = 'https://etherscan.io/blocks?ps=100&p='
# Страницы
pages_first = 1
pages_last = 10


# парсинг старинцы
# не меняется ничего
async def bs4(url):
    useragent = UserAgent()
    headers = {'User-Agent': useragent.Random()}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


# работа с сессией
# не меняется ничего
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


# работа со страницей
# не меняется ничего
async def parse_data(url):
    async with aiohttp.ClientSession() as session:
        soup = await bs4(url)

        '''
        Тут можно и нужно менять 
        '''

        for item in soup.find('tbody', 'align-middle').find_all('tr'):
            pass


# Основной скрипт
# не меняется ничего
async def start(url_page, pages_first, pages_last):
    urls = [f'{url_page}{i}' for i in range(pages_first, pages_last)]
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(asyncio.ensure_future(parse_data(url)))
        await asyncio.gather(*tasks)


def main(url_page, pages_first, pages_last):
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(url_page, pages_first, pages_last))
    print("--- Асинхронный парсинг -  %s seconds ---" % (time.time() - start_time))


def test_main(url_page, pages_first, pages_last):
    start_time = time.time()
    useragent = UserAgent()
    headers = {'User-Agent': useragent.Random()}
    for i in range(pages_first, pages_last):
        url = f'{url_page}{i}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.find('tbody', 'align-middle').find_all('tr'):
            pass

    print("--- Не асинхронный парсинг - %s seconds ---" % (time.time() - start_time))

# Запуск
# не меняется ничего
if __name__ == '__main__':

    main(url_page, pages_first, pages_last)
    test_main(url_page, pages_first, pages_last)
    print('Успешно завершено')
