import tech_news.database as db
from datetime import date as lb_date


# Requisito 6
def search_by_title(title):
    query = {'title': {'$regex': title, '$options': 'i'}}
    results = db.search_news(query)

    return [(notice['title'], notice['url']) for notice in results]


# Requisito 7
def search_by_date(date):
    try:
        lb_date.fromisoformat(date)
        query = {'timestamp': {'$regex': date}}
        results = db.search_news(query)

        return [(notice['title'], notice['url']) for notice in results]
    except ValueError:
        raise ValueError('Data inválida')


# Requisito 8
def search_by_source(source):
    query = {'sources': {'$regex': source, '$options': 'i'}}
    results = db.search_news(query)

    return [(notice['title'], notice['url']) for notice in results]


# Requisito 9
def search_by_category(category):
    query = {'categories': {'$regex': category, '$options': 'i'}}
    results = db.search_news(query)

    return [(notice['title'], notice['url']) for notice in results]
