import json
from pymongo import MongoClient

# Configure the MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['quotes_database']
quotes_collection = db['quotes']
authors_collection = db['authors']

# Load data from quotes.json
with open('/quotes_scraper/quotes_scraper/quotes.json', encoding='utf-8') as quotes_file:
    quotes_data = json.load(quotes_file)

# Load data from authors.json
with open('/quotes_scraper/quotes_scraper/authors.json', encoding='utf-8') as authors_file:
    authors_data = json.load(authors_file)

# Insert data into MongoDB
quotes_collection.insert_many(quotes_data)
authors_collection.insert_many(authors_data)

print("Data has been successfully uploaded to MongoDB.")
