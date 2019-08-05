# -*- coding: utf-8 -*-
import scrapy

from amazon_books.items import AmazonBooksItem


class AmazonBookSpider(scrapy.Spider):
    name = 'amazon_book'
    start_urls = ['https://www.amazon.com/s?bbn=283155&rh=n%3A283155%2Cp_n_publ'
                  'ication_date%3A1250226011&dc&fst=as%3Aoff&qid=1564840578&rni'
                  'd=1250225011&ref=lp_283155_nr_p_n_publication_date_0']
    page_number = 2

    def parse(self, response):
        items = AmazonBooksItem()

        title = response.css(".a-color-base.a-text-normal::text").extract()
        author = response.css(".a-color-secondary .a-size-base+ .a-size-base").css('::text').extract()
        price = response.css(".a-spacing-top-small .a-price:nth-child(1) span").css('::text').extract()
        image = response.css(".s-image::attr(src)").extract()

        items['book_title'] = title
        items['book_author'] = author
        items['book_price'] = price
        items['book_image'] = image

        yield items

        next_page = 'https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&page=' + str(AmazonBookSpider.page_number) + '&fst=as%3Aoff&qid=1564973062&rnid=1250225011&ref=sr_pg_2'

        if AmazonBookSpider.page_number < 10:
            AmazonBookSpider.page_number += 1

            yield response.follow(next_page, callback=self.parse)