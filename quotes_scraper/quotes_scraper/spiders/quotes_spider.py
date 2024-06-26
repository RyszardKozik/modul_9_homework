import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        # Follow pagination links
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # Follow links to author pages
        author_links = response.css('small.author + a::attr(href)').getall()
        for link in author_links:
            yield response.follow(link, self.parse_author)
            
        # Follow pagination links
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        yield {
            'name': response.css('h3.author-title::text').get(),
            'birth_date': response.css('span.author-born-date::text').get(),
            'birth_place': response.css('span.author-born-location::text').get(),
            'description': response.css('div.author-description::text').get(),
        }
