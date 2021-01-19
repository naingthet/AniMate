# Elastic search test
from app.search import add_to_index, query_index

for anime in Animes.query.all():
    add_to_index('animes', anime)

query_index('animes', 'one punch man', 1, 100)

app.elasticsearch.indices.delete('animes')