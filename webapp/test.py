from app import app
from app.search import add_to_index, query_index
from app.models import Animes


# # Elastic search test
for anime in Animes.query.all():
    add_to_index('animes', anime)

query_index('animes', 'one punch man', 1, 100)

app.elasticsearch.indices.delete('animes')

# Testing search
Animes.reindex()
query, total = Animes.search('one punch man', 1, 5)
print(total)
print(query.all())