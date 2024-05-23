import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Ensure the quotes_scraper module is on the path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quotes_scraper'))
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'quotes_scraper.settings')

# Import the QuotesSpider from the quotes_scraper.spiders module
from quotes_scraper.spiders.quotes_spider import QuotesSpider

def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(QuotesSpider)
    process.start()
    
if __name__ == '__main__':
    main()
