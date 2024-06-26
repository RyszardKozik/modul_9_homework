import os
import json
import logging
import pymongo
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JsonWriterPipeline:
    def open_spider(self, spider):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'quotes.json')
        self.file = open(file_path, 'w', encoding='utf-8')
        self.file.write('[')

    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        if self.first_item:
            self.first_item = False
        else:
            self.file.seek(self.file.tell() - 2)
            self.file.write(",\n")

        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item

class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
            collection_name=crawler.settings.get("MONGO_COLLECTION", "quotes")
        )

    def open_spider(self, spider):
        logging.info(f"Connecting to MongoDB at {self.mongo_uri}")
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        logging.info(f"Connected to MongoDB database: {self.mongo_db}")

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item

class QuotesScraperPipeline:
    def process_item(self, item, spider):
        return item
    
class QuotesPipeline:
    def process_item(self, item, spider):
        return item

class AuthorsPipeline:
    def process_item(self, item, spider):
        return item

