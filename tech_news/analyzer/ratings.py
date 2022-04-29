import tech_news.database as db


# Requisito 10
def top_5_news():
    query = [
        {'$addFields': {
            'top5_order': {'$add': ['$shares_count', '$comments_count']}
            }},
        {'$sort': {'top5_order': -1, 'title': 1}},
        {'$limit': 5}
    ]
    results = db.get_collection().aggregate(query)
    return [(notice['title'], notice['url']) for notice in results]


# Requisito 11
def top_5_categories():
    query = [
        {'$unwind': '$categories'},
        {'$group': {'_id': '$categories', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1, '_id': 1}},
        {'$limit': 5}
    ]
    results = db.get_collection().aggregate(query)
    return [(notice['_id']) for notice in results]
