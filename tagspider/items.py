# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

import scrapy


class TagspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


@dataclass
class TagRankItem:
    category_name: str
    year: str
    brand_name: str
    set_name: str
    card_name: str
    variation: str
    certificate_value: str
    tag_grade: int
    uuid: str
