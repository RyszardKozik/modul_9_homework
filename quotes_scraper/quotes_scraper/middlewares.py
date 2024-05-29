# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class QuotesScraperSpiderMiddleware:
    def process_item(self, item, spider):
        # Create an adapter for the item
        adapter = ItemAdapter(item)
        
        # Validate the item fields
        if not self.is_valid_item(adapter):
            logging.warning(f"Invalid item found: {item}")
            raise DropItem(f"Missing fields in item: {item}")
        
        # Clean the item fields
        self.clean_item(adapter)
        
        # Process or save the item
        self.save_item(adapter)
        
        return item
    
    def is_valid_item(self, adapter):
        # Example validation: Ensure 'quote' and 'author' fields are present
        required_fields = ['quote', 'author']
        for field in required_fields:
            if not adapter.get(field):
                return False
        return True
    
    def clean_item(self, adapter):
        # Example cleaning: Strip whitespace from 'quote' and 'author' fields
        fields_to_clean = ['quote', 'author']
        for field in fields_to_clean:
            value = adapter.get(field)
            if value:
                adapter[field] = value.strip()
    
    def save_item(self, adapter):
        # Example saving: Print the item (this could be replaced with database saving logic)
        print(f"Saving item: {adapter.asdict()}")
    

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class QuotesScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

    