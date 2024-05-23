import json
import os

# Get the full path to quotes.json
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
quotes_file_path = os.path.join(current_dir, 'quotes.json')

# Load the scraped data from quotes.json
with open(quotes_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract unique authors from the quotes
authors = {quote['author']: {'name': quote['author']} for quote in data}

# Write the author data to authors.json
authors_file_path = os.path.join(current_dir, 'authors.json')
with open(authors_file_path, 'w', encoding='utf-8') as f:
    json.dump(list(authors.values()), f, ensure_ascii=False, indent=2)

print("Authors data has been successfully written to authors.json.")
