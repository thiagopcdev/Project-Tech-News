import requests
from time import sleep
from parsel import Selector
from .database import create_news

URL_NEWS_PAGE = "https://www.tecmundo.com.br/novidades"


# Requisito 1
def fetch(url):
    sleep(1)
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text
        return None
    except requests.Timeout:
        return None


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(html_content)
    news_list = selector.css('h3 .tec--card__title__link::attr(href)').getall()
    return list(news_list)


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    next_page_link = selector.css('div .z--mt-48::attr(href)').get()
    return next_page_link


# Requisito 4
def scrape_noticia(html_content):
    selector = Selector(html_content)
    url = selector.css('meta[property="og:url"]::attr(content)').get()
    title = selector.css('.tec--article__header__title::text').get()
    timestamp = selector.css('#js-article-date::attr(datetime)').get()
    writer = (selector.css('.z--font-bold *::text').get() or '').strip()
    shares_count = (selector.css('.tec--toolbar__item::text').get() or '0')
    comments_count = selector.css('#js-comments-btn::attr(data-count)').get()
    summary_location = '.tec--article__body > p:nth-of-type(1) *::text'
    summary_list = selector.css(summary_location).getall()
    summary = list_to_string(summary_list)
    sources = blank_remover(selector.css('.z--mb-16 a::text').getall())
    categories = blank_remover(selector.css('#js-categories a::text').getall())

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": int(shares_count.strip()[:1]),
        "comments_count": int(comments_count),
        "summary": summary,
        "sources": sources,
        "categories": categories
    }


# Requisito 5
def get_tech_news(amount):
    page_news = fetch(URL_NEWS_PAGE)
    news_list_url = scrape_novidades(page_news)
    next_page_url = scrape_next_page_link(page_news)
    amount_news = len(news_list_url)

    while (amount_news < amount):
        next_page = fetch(next_page_url)
        news_list_url.extend(scrape_novidades(next_page))
        next_page_url = scrape_next_page_link(next_page)
        amount_news = len(news_list_url)
    news_list_url = news_list_url[:amount]

    news_list = []
    for notice in news_list_url:
        notice_page = fetch(notice)
        news_list.append(scrape_noticia(notice_page))

    create_news(news_list)

    return news_list


def blank_remover(array_list):
    return list(map(lambda str: str.strip(), array_list))


def list_to_string(array_list):
    return ''.join(map(str, array_list))
