import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
from threading import Thread

xlsx = 'test11.xlsx'


def append(*args):
    wb = openpyxl.load_workbook(xlsx)
    sheet = wb.active
    for row in args:
        sheet.append(row)
    wb.save(xlsx)


def pars_category():
    urls = []
    url = 'https://exkavator.ru/trade/#all_techtypes_click'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    x1 = soup.find_all('div', class_='col-3-types')
    for x2 in x1:
        for x3 in x2.find_all('div', class_='type-item'):
            ss = x3.find("ul").find_all("li")
            for sss in ss:
                url = sss.find('a').get('href')
                print(url)
                urls.append(url)
    # print(urls)
    return urls


def page_parsing_lot_user(url, page):
    data = {}
    # создаем ссылки со страницами и проходиим по каждой странице
    if page == 0:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # вытаскиваем все номера лотов
        x = soup.find('div', class_="trade-results-items")
        for i in x.find_all("div", class_="item"):
            data_lot = i.find("span", class_="tooltipster").get('data-lot')
            data_user = i.find("span", class_="tooltipster").get('data-user')
            data[data_lot] = data_user
    else:
        for i in range(0, 40 * int(page), 40):
            url_page = (url + 'pages/' + str(i) + '/')
            print(url_page)
            response = requests.get(url_page)
            soup = BeautifulSoup(response.text, 'html.parser')
            # вытаскиваем все номера лотов
            x = soup.find('div', class_="trade-results-items")
            for i in x.find_all("div", class_="item"):
                data_lot = i.find("span", class_="tooltipster").get('data-lot')
                data_user = i.find("span", class_="tooltipster").get('data-user')
                data[data_lot] = data_user
    return data


def parsing_phone(data_lots, data_user):
    url = 'https://exkavator.ru/trade/communication/trade_item_contacts/' + str(data_user) + '/' + str(
        data_lots) + '/lot-sample'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    phone = (soup.find('div', class_="phone").text)
    name = (soup.find('div', class_="name").text)
    print(phone, name)
    return phone, name


def insert_db(datas):
    import sqlite3

    con = sqlite3.connect("metanit.db")
    cursor = con.cursor()

    cursor.execute("INSERT INTO people (name, phone, cat)  VALUES (?, ?, ?)", datas)
    con.commit()


def page_parsing(urls):
    for url in urls:
        # вытаскиваем все лоты
        try:
            url = "https://exkavator.ru" + str(url) + "novye/"
            print(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            category = (soup.find('div', class_="title-line-cont").text)
            # узнаем сколько страниц на сайте есть
            try:
                page = len(soup.find('div', class_='pages-bottom-cen').find('div', class_='pages').find_all('a'))
                print(page)
            except:
                page = 0
            try:
                lots_user = page_parsing_lot_user(url, page)
                name_cat = str(category).replace("\n", "")
                for data_lots, data_user in lots_user.items():
                    try:
                        name_phone = parsing_phone(data_lots, data_user)
                        datas = (name_phone[0], name_phone[1], name_cat)
                        insert_db(datas)
                    except:
                        print("")

            except:
                print("")
        except:
            print("")


def main():
    # urls = pars_category() #при запуске вытаскивает все url
    # page_parsing(urls)

    urls = ['/trade/betonnoe-oborudovanie/avtobetonosmesiteli/', '/trade/betonnoe-oborudovanie/asfaltnye-zavody/',
            '/trade/betonnoe-oborudovanie/betonnye-zavody/', '/trade/betonnoe-oborudovanie/betononasosy/',
            '/trade/betonnoe-oborudovanie/betonorazdatochnye-strely/', '/trade/betonnoe-oborudovanie/bsu/',
            '/trade/betonnoe-oborudovanie/betonoukladchiki/', '/trade/betonnoe-oborudovanie/glubinnye-vibratory/',
            '/trade/betonnoe-oborudovanie/vibropressy/', '/trade/betonnoe-oborudovanie/vibrorejki/',
            '/trade/betonnoe-oborudovanie/gruntosmesitelnye-ustanovki/',
            '/trade/betonnoe-oborudovanie/zatirochnye-mashiny/',
            '/trade/betonnoe-oborudovanie/parogeneratory-promyshlennye/',
            '/trade/betonnoe-oborudovanie/rastvoronasosy/', '/trade/betonnoe-oborudovanie/rastvorosmesiteli/',
            '/trade/betonnoe-oborudovanie/silosy-dlya-cementa/',
            '/trade/betonnoe-oborudovanie/stacionarnye-betononasosy/',
            '/trade/betonnoe-oborudovanie/torkret-ustanovki/', '/trade/betonnoe-oborudovanie/shtukaturnye-stancii/',
            '/trade/burovoe-oborudovanie/yamobury-bkm/', '/trade/burovoe-oborudovanie/burovye-stanki-dlya-svaj/',
            '/trade/burovoe-oborudovanie/burovye-ustanovki/', '/trade/burovoe-oborudovanie/ustanovki-gnb/',
            '/trade/gruzovye-avtomobili/benzovozy/', '/trade/gruzovye-avtomobili/bitumovozy-neftevozy/',
            '/trade/gruzovye-avtomobili/bortovye-gruzoviki/', '/trade/gruzovye-avtomobili/bortovye-kuzova/',
            '/trade/gruzovye-avtomobili/bunkerovozy/', '/trade/gruzovye-avtomobili/gazovozy/',
            '/trade/gruzovye-avtomobili/gruzovye-furgony/', '/trade/gruzovye-avtomobili/zernovozy/',
            '/trade/gruzovye-avtomobili/izotermicheskie-furgony/',
            '/trade/gruzovye-avtomobili/izotermicheskie-refrizheratornye-kuzova/',
            '/trade/gruzovye-avtomobili/konteynerovozy/', '/trade/gruzovye-avtomobili/kontejnery-dlya-multilifta/',
            '/trade/gruzovye-avtomobili/kuzova-furgony/', '/trade/gruzovye-avtomobili/lesovozy/',
            '/trade/gruzovye-avtomobili/lomovozy/', '/trade/gruzovye-avtomobili/molokovozy-pishchevye-cisterny/',
            '/trade/gruzovye-avtomobili/multilifty/', '/trade/gruzovye-avtomobili/refrizheratory/',
            '/trade/gruzovye-avtomobili/samosvaly/', '/trade/gruzovye-avtomobili/samosvalnye-kuzova/',
            '/trade/gruzovye-avtomobili/tank-kontejnery-kontejnery-cisterny/',
            '/trade/gruzovye-avtomobili/tentovannye-gruzoviki/', '/trade/gruzovye-avtomobili/toplivozapravshhiki/',
            '/trade/gruzovye-avtomobili/trubovozy/', '/trade/gruzovye-avtomobili/sedelnye-tyagachi/',
            '/trade/gruzovye-avtomobili/himicheskie-cisterny/', '/trade/gruzovye-avtomobili/cementovozy/',
            '/trade/gruzovye-avtomobili/shassi/', '/trade/gruzovye-avtomobili/shtornye-gruzoviki/',
            '/trade/dorozhnaya-tehnika/avtogudronatory/', '/trade/dorozhnaya-tehnika/asfaltoukladchiki/',
            '/trade/dorozhnaya-tehnika/bitumoshhebneraspredeliteli/', '/trade/dorozhnaya-tehnika/bordyuroukladchiki/',
            '/trade/dorozhnaya-tehnika/vibroplity/', '/trade/dorozhnaya-tehnika/vibrotrambovki/',
            '/trade/dorozhnaya-tehnika/dorozhnye-katki/', '/trade/dorozhnaya-tehnika/dorozhnye-frezy/',
            '/trade/dorozhnaya-tehnika/zalivshhiki-shvov/', '/trade/dorozhnaya-tehnika/kohery-dlya-litogo-asfalta/',
            '/trade/dorozhnaya-tehnika/mashiny-dlya-ukladki-trotuarnoj-plitki/',
            '/trade/dorozhnaya-tehnika/mashiny-dlya-yamochnogo-remonta/',
            '/trade/dorozhnaya-tehnika/mashiny-dorozhnoj-razmetki/',
            '/trade/dorozhnaya-tehnika/peregruzhateli-asfalta/',
            '/trade/dorozhnaya-tehnika/raspredeliteli-vyazhushhego/', '/trade/dorozhnaya-tehnika/resajklery/',
            '/trade/dorozhnaya-tehnika/sushilki-dorozhnogo-pokrytiya/',
            '/trade/dorozhnaya-tehnika/ukladchiki-slarri-sil/', '/trade/dorozhnaya-tehnika/shvonarezchiki/',
            '/trade/dorozhnaya-tehnika/shhebneraspredeliteli/', '/trade/zemlerojnaya-tehnika/buldozery/',
            '/trade/zemlerojnaya-tehnika/grejdery/', '/trade/zemlerojnaya-tehnika/gusenichnye-ekskavatory/',
            '/trade/zemlerojnaya-tehnika/zemsnaryady/', '/trade/zemlerojnaya-tehnika/kolesnye-ekskavatory/',
            '/trade/zemlerojnaya-tehnika/svaeboi/', '/trade/zemlerojnaya-tehnika/skrepery/',
            '/trade/zemlerojnaya-tehnika/transheekopateli/',
            '/trade/zemlerojnaya-tehnika/ustanovki-dlya-zavinchivaniya-svaj/',
            '/trade/zemlerojnaya-tehnika/frontalnye-pogruzchiki/', '/trade/zemlerojnaya-tehnika/ekskavatory-amfibii/',
            '/trade/zemlerojnaya-tehnika/ekskavatory-planirovschiki/',
            '/trade/zemlerojnaya-tehnika/ekskavatory-pogruzchiki/',
            '/trade/karernaya-tehnika/vspomogatelnaya-gorno-shahtnaya-tehnika/',
            '/trade/karernaya-tehnika/gornye-kombajny/', '/trade/karernaya-tehnika/grohoty/',
            '/trade/karernaya-tehnika/draglajny/', '/trade/karernaya-tehnika/drobilki/',
            '/trade/karernaya-tehnika/karernye-samosvaly/', '/trade/karernaya-tehnika/karernye-ekskavatory/',
            '/trade/karernaya-tehnika/magnitnye-separatory/', '/trade/karernaya-tehnika/otvaloobrazovateli/',
            '/trade/karernaya-tehnika/pitateli/', '/trade/karernaya-tehnika/pogruzochno-dostavochnye-mashiny/',
            '/trade/karernaya-tehnika/podzemnye-samosvaly/', '/trade/karernaya-tehnika/promyvochnoe-oborudovanie/',
            '/trade/karernaya-tehnika/sochlenennye-samosvaly/', '/trade/karernaya-tehnika/sharovye-melnicy/',
            '/trade/karernaya-tehnika/shahtnye-konvejery/', '/trade/kommunalnaya-tehnika/assenizatorskie-mashiny/',
            '/trade/kommunalnaya-tehnika/voroshiteli-komposta/', '/trade/kommunalnaya-tehnika/izmelchiteli-othodov/',
            '/trade/kommunalnaya-tehnika/ilososy/', '/trade/kommunalnaya-tehnika/kanalopromyvochnye-mashiny/',
            '/trade/kommunalnaya-tehnika/kdm/', '/trade/kommunalnaya-tehnika/kompaktory/',
            '/trade/kommunalnaya-tehnika/musorovozy/', '/trade/kommunalnaya-tehnika/podmetalno-uborochnye-mashiny/',
            '/trade/kommunalnaya-tehnika/polivomoechnye-mashiny/',
            '/trade/kommunalnaya-tehnika/snegoplavilnye-ustanovki/', '/trade/kommunalnaya-tehnika/snegopogruzchiki/',
            '/trade/kommunalnaya-tehnika/snegouborshhiki/', '/trade/kommunalnaya-tehnika/traktory-gazonokosilki/',
            '/trade/lesnaya-tehnika/valochno-paketiruyushhie-mashiny/', '/trade/lesnaya-tehnika/lesopogruzchiki/',
            '/trade/lesnaya-tehnika/mulchery-lesnye/', '/trade/lesnaya-tehnika/rubitelnye-mashiny/',
            '/trade/lesnaya-tehnika/suchkoreznye-mashiny/', '/trade/lesnaya-tehnika/skiddery/',
            '/trade/lesnaya-tehnika/forvardery/', '/trade/lesnaya-tehnika/harvardery/',
            '/trade/lesnaya-tehnika/harvestery/', '/trade/mini-tehnika/dumpery/', '/trade/mini-tehnika/mini-krany/',
            '/trade/mini-tehnika/mini-pogruzchiki/', '/trade/mini-tehnika/mini-traktory/',
            '/trade/mini-tehnika/mini-ekskavatory/', '/trade/navesnoe_oborudovanie/kvik-kaplery/',
            '/trade/navesnoe_oborudovanie/vibropogruzhateli/', '/trade/navesnoe_oborudovanie/vibrotrambovki-navesnye/',
            '/trade/navesnoe_oborudovanie/vily/', '/trade/navesnoe_oborudovanie/gidrobury/',
            '/trade/navesnoe_oborudovanie/gidromagnity/', '/trade/navesnoe_oborudovanie/gidromoloty/',
            '/trade/navesnoe_oborudovanie/gidronozhnitsy/', '/trade/navesnoe_oborudovanie/grabli-navesnye/']
    urls2 = ['/trade/navesnoe_oborudovanie/grejfery/', '/trade/navesnoe_oborudovanie/dizel-moloty/',
             '/trade/navesnoe_oborudovanie/zahvaty/', '/trade/navesnoe_oborudovanie/kovshi/',
             '/trade/navesnoe_oborudovanie/korchevateli-pnej/', '/trade/navesnoe_oborudovanie/kosilki-navesnye/',
             '/trade/navesnoe_oborudovanie/kuny/', '/trade/navesnoe_oborudovanie/mulchery-navesnye/',
             '/trade/navesnoe_oborudovanie/nasosy-peskovye/', '/trade/navesnoe_oborudovanie/otvaly/',
             '/trade/navesnoe_oborudovanie/peskorazbrasyvateli/',
             '/trade/navesnoe_oborudovanie/polivomoechnoe-oborudovanie/',
             '/trade/navesnoe_oborudovanie/prochee-navesnoe/', '/trade/navesnoe_oborudovanie/ryhliteli/',
             '/trade/navesnoe_oborudovanie/snegoochistiteli-navesnye/',
             '/trade/navesnoe_oborudovanie/transheekopateli-navesnye/', '/trade/navesnoe_oborudovanie/frezy-navesnye/',
             '/trade/navesnoe_oborudovanie/harvesternye-golovki/', '/trade/navesnoe_oborudovanie/shchetki-kommunalnye/',
             '/trade/passazhirskij-transport/vahtovye-avtobusy/', '/trade/passazhirskij-transport/gorodskie-avtobusy/',
             '/trade/passazhirskij-transport/gruzopassazhirskie-mikroavtobusy/',
             '/trade/passazhirskij-transport/mezhdugorodnye_avtobusy/',
             '/trade/passazhirskij-transport/passazhirskie-mikroavtobusy/',
             '/trade/passazhirskij-transport/prigorodnye-avtobusy/',
             '/trade/passazhirskij-transport/turisticheskie-avtobusy/', '/trade/podemnaya-tehnika/avtovyshki/',
             '/trade/podemnaya-tehnika/avtokrany/', '/trade/podemnaya-tehnika/bashennye-krany/',
             '/trade/podemnaya-tehnika/gusenichnye-krany/', '/trade/podemnaya-tehnika/derrik-krany/',
             '/trade/podemnaya-tehnika/kozlovye-krany/', '/trade/podemnaya-tehnika/kolenchatye-podemniki/',
             '/trade/podemnaya-tehnika/konsolnye-krany/', '/trade/podemnaya-tehnika/krany-manipulyatory/',
             '/trade/podemnaya-tehnika/machtovye-podemniki/', '/trade/podemnaya-tehnika/mostovye-krany/',
             '/trade/podemnaya-tehnika/naklonnye-podyemniki/', '/trade/podemnaya-tehnika/nozhnichnye-podemniki/',
             '/trade/podemnaya-tehnika/peregruzhateli/', '/trade/podemnaya-tehnika/portalnye-krany/',
             '/trade/podemnaya-tehnika/sistemy-remonta-mostov/', '/trade/podemnaya-tehnika/sudovye-krany/',
             '/trade/podemnaya-tehnika/teleskopicheskie-pogruzchiki/',
             '/trade/podemnaya-tehnika/teleskopicheskie-podemniki/', '/trade/podemnaya-tehnika/truboukladchiki/',
             '/trade/podemnaya-tehnika/fasadnye-podemniki/', '/trade/polupricepy/bortovye-polupricepy/',
             '/trade/polupricepy/izotermicheskie-polupricepy/', '/trade/polupricepy/polupricepy-avtovozy/',
             '/trade/polupricepy/polupricepy-benzovozy/', '/trade/polupricepy/polupricepy-bitumovozy-neftevozy/',
             '/trade/polupricepy/polupricepy-gazovozy/', '/trade/polupricepy/polupricepy-zernovozy/',
             '/trade/polupricepy/polupricepy-kontejnerovozy/', '/trade/polupricepy/polupricepy-kormovozy/',
             '/trade/polupricepy/polupricepy-lesovozy-sortimentovozy/',
             '/trade/polupricepy/polupricepy-lomovozy-metallovozy/', '/trade/polupricepy/polupritsepy-molokovozy/',
             '/trade/polupricepy/polupricepy-panelevozy/', '/trade/polupricepy/polupritsepy-refrizheratory/',
             '/trade/polupricepy/polupritsepy-skotovozy/', '/trade/polupricepy/polupricepy-toplivozapravshchiki/',
             '/trade/polupricepy/polupricepy-furgony/', '/trade/polupricepy/polupricepy-cementovozy/',
             '/trade/polupricepy/samosvalnye-polupricepy/', '/trade/polupricepy/tentovannye-polupricepy/',
             '/trade/polupricepy/traly/', '/trade/polupricepy/himicheskie-polupricepy-cisterny/',
             '/trade/polupricepy/shtornye-polupricepy/', '/trade/pricepy/bortovye-pricepy/',
             '/trade/pricepy/izotermicheskie-pricepy/', '/trade/pricepy/pricepy-avtovozy/',
             '/trade/pricepy/pricepy-benzovozy/', '/trade/pricepy/pricepy-zernovozy/',
             '/trade/pricepy/pricepy-kontejnerovozy/', '/trade/pricepy/pricepy-kungi/',
             '/trade/pricepy/pricepy-lesovozy-sortimentovozy/', '/trade/pricepy/pricepy-lomovozy-metallovozy/',
             '/trade/pricepy/pricepy-molokovozy-pishchevye/', '/trade/pricepy/pritsepy-refrizheratory/',
             '/trade/pricepy/pricepy-skotovozy/', '/trade/pricepy/pricepy-toplivozapravshchiki/',
             '/trade/pricepy/pricepy-trubovozy/', '/trade/pricepy/pricepy-tyazhelovozy/',
             '/trade/pricepy/pricepy-furgony/', '/trade/pricepy/samosvalnye_pritsepy/',
             '/trade/pricepy/tentovannye-pricepy/', '/trade/pricepy/shassi-pricepov/',
             '/trade/pricepy/shtornye-pricepy/', '/trade/prochaya-tehnika/kabeleukladchiki/',
             '/trade/prochaya-tehnika/natyazhnye-mashiny/', '/trade/prochaya-tehnika/nestandartnye-ekskavatory/',
             '/trade/prochaya-tehnika/peredvizhnye-nasosnye-ustanovki/',
             '/trade/prochaya-tehnika/tehnika-dlya-razrusheniya/', '/trade/skladskaya-tehnika/bokovye-pogruzchiki/',
             '/trade/skladskaya-tehnika/vilochnye-pogruzchiki/', '/trade/skladskaya-tehnika/gidravlicheskie-telezhki/',
             '/trade/skladskaya-tehnika/podborshhiki-zakazov/', '/trade/skladskaya-tehnika/platformy/',
             '/trade/skladskaya-tehnika/richstakery/', '/trade/skladskaya-tehnika/richtraki/',
             '/trade/skladskaya-tehnika/ruchnye-shtabelery/', '/trade/skladskaya-tehnika/samohodnye-shtabelery/',
             '/trade/skladskaya-tehnika/uzkoprohodnye-shtabelery/',
             '/trade/skladskaya-tehnika/elektricheskie-shtabelery/', '/trade/skladskaya-tehnika/elektropogruzchiki/',
             '/trade/skladskaya-tehnika/elektrotelezhki/', '/trade/skladskaya-tehnika/elektrotyagachi/',
             '/trade/specialnye-avtomobili/avtolavki-torgovye-furgony/', '/trade/specialnye-avtomobili/avtomobili-mvd/',
             '/trade/specialnye-avtomobili/avtomobili-skoroj-pomoshchi/', '/trade/specialnye-avtomobili/vezdekhody/',
             '/trade/specialnye-avtomobili/kungi/', '/trade/specialnye-avtomobili/peredvizhnye-laboratorii/',
             '/trade/specialnye-avtomobili/peredvizhnye-masterskie-avarijno-remontnye-avtomobili/',
             '/trade/specialnye-avtomobili/pozharnye-mashiny/',
             '/trade/specialnye-avtomobili/transportno-bytovye-mashiny/', '/trade/specialnye-avtomobili/ehvakuatory/',
             '/trade/stroitelnoe-oborudovanie/bytovki/', '/trade/stroitelnoe-oborudovanie/vyshki-tury/',
             '/trade/stroitelnoe-oborudovanie/dizelnye-generatory/',
             '/trade/stroitelnoe-oborudovanie/dizelnye-kompressory/',
             '/trade/stroitelnoe-oborudovanie/kompaktnye-gidrostanczii/', '/trade/stroitelnoe-oborudovanie/motopompy/',
             '/trade/stroitelnoe-oborudovanie/opalubka/', '/trade/stroitelnoe-oborudovanie/osvetitelnye-machty/',
             '/trade/stroitelnoe-oborudovanie/peredvizhnye-svarochnye-agregaty/',
             '/trade/stroitelnoe-oborudovanie/podmosti-stroitelnye/',
             '/trade/stroitelnoe-oborudovanie/sistemy-pylepodavleniya/',
             '/trade/stroitelnoe-oborudovanie/stroitelnye-lesa/', '/trade/traktornaya-tehnika/traktornye-polupricepy/',
             '/trade/traktornaya-tehnika/traktornye-pricepy/', '/trade/traktornaya-tehnika/traktory/']

    thread1 = Thread(target=page_parsing, args=(urls,))
    thread2 = Thread(target=page_parsing, args=(urls2,))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


if __name__ == "__main__":
    main()
