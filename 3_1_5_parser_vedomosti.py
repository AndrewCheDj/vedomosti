from selenium import webdriver
from lxml.html import fromstring
import pandas as pd
# from multiprocessing.dummy import Pool

ff = 'venv/chromedriver'
driver = webdriver.Chrome(executable_path=ff) # здесь показываем путь к вебдрайверу если система просит

listOfLinks = []
texts = []


"""Создание ссылок на архивные страницы"""

def find_date_pages():
    url_date_template = 'https://www.vedomosti.ru/archive/{}/{}/{}' # путь для формирования ссылок по датам
    url_date_template_zero = 'https://www.vedomosti.ru/archive/{}/0{}/{}' # путь для формирования ссылок по датам с нулём в конце
    url_date_template_zero2 = 'https://www.vedomosti.ru/archive/{}/{}/0{}'
    url_date_template_zero3 = 'https://www.vedomosti.ru/archive/{}/0{}/0{}'
    url_dates = [] # список для ссылок с разными датами
    for y in [2019]:
        for m in range(1,3):
            for d in range(1,10):
                if m<10 and d>=10:
                    url_dates.append(url_date_template_zero.format(y, m, d))
                elif d<10 and m>=10:
                    url_dates.append(url_date_template_zero2.format(y, m, d))
                elif d<10 and m<10:
                    url_dates.append(url_date_template_zero3.format(y, m, d))
                else:
                    url_dates.append(url_date_template.format(y, m, d))

    return url_dates


"""создание ссылок на статьи"""

def find_article_urls(url_dates):
    for url in url_dates:
        url_for_links = 'https://www.vedomosti.ru'
        driver.get(url)

        htmlText = driver.page_source  # создаем из странички  html-текст

        pattern = '.articles-preview-list__item'  # назначаем css-селектор по которому находим ссылки
        parser = fromstring(htmlText) # парсим получившийся html

        links = parser.cssselect(pattern)  # выдергиваем нужную нам инфу по селектору
        [listOfLinks.append(url_for_links + el.get('href')) for el in links] # выдергиваем из элементов ссылки
        # for el in links:
        #     print(el.get('href'))
        #     listOfLinks.append(url_for_links + el.get('href'))
    print(listOfLinks)
    print(len(listOfLinks))
    return listOfLinks



"""Парсим сами тексты статей"""

def article_text_parser(listOfLinks):
    txt = []
    for art in listOfLinks:
        driver.get(art)
        htmlText = driver.page_source  # создаем из странички html-текст
        pattern = '.box-paragraph__text'  # назначаем css-селектор, в котором сидит текст
        parser = fromstring(htmlText)  # создаем класс парсера

        textOfPage = parser.cssselect(pattern)  # выдергиваем нужные нам элементы по селектору
        # txt = [txt.append(l.text) for l in textOfPage]
        for l in textOfPage: # выдергиваем из этих элементов текст
            txt = []
            if l.text == None:
                print('l.text in ', l, ' == None')
            else:
                txt.append(l.text)
        txt = [' '.join(txt)]
        texts.append(txt)
        print(texts)


# def article_text_parser(LinkFromList):
    # ff = 'venv/chromedriver'
    # driver = webdriver.Chrome(executable_path=ff)  # здесь показываем путь к вебдрайверу если система просит

    # driver.get(LinkFromList)
    #
    # htmlText = driver.page_source  # создаем из странички html-текст
    # pattern = '.box-paragraph__text'  # назначаем css-селектор, в котором сидит текст
    # parser = fromstring(htmlText)  # создаем класс парсера
    #
    # textOfPage = parser.cssselect(pattern)  # выдергиваем нужные нам элементы по селектору
    # for l in textOfPage:
    #     print(l.text)  # выдергиваем из этих элементов текст
    # driver.close()

find_article_urls(find_date_pages())
# pool = Pool(processes=2)
# print(pool.map(article_text_parser, listOfLinks))
article_text_parser(listOfLinks)
print(texts)

print(len(listOfLinks), len(texts))
driver.close()

"""Формируем датафрейм из данных"""

df = pd.DataFrame({"url": listOfLinks})
df["topic"] = df.url.apply(lambda x: x.split('/')[3])
df["format"] = df.url.apply(lambda x: x.split('/')[4])
df["text"] = [t for t in texts]


print(df.head())
print(df.info)

df.to_pickle('vedomosti_archive.pkl')
df.to_excel('pars_vedomosti.xlsx')










