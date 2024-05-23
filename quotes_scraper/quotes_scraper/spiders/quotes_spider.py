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

            # Extract author URLs and follow them to get author information
            author_urls = quote.css('span a::attr(href)').getall()
            for author_url in author_urls:
                yield response.follow(author_url, callback=self.parse_author)

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
