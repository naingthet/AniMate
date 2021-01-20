# Initialize elasticsearch indices for a database
from app import app
from app.search import add_to_index, query_index
from app.models import Animes

for anime in Animes.query.all():
    add_to_index('animes', anime)

# Query the index
query_index('animes', 'one punch man', 1, 100)

# Delete the index
app.elasticsearch.indices.delete('animes')

# Easier way of searching
Animes.reindex()
query, total = Animes.search('one punch man', 1, 5)
print(total)
print(query.all())