# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import psycopg2

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PostgresPipeline:
    def __init__(self):
        self.connection = psycopg2.connect("")
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute(
            """\
        insert into certificates (uuid, category_name, year, brand_name, set_name, card_name, card_number, variation, certificate_value, tag_grade)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        on conflict (uuid) do update set (category_name, year, brand_name, set_name, card_name, card_number, variation, certificate_value, tag_grade) =
        (excluded.category_name, excluded.year, excluded.brand_name, excluded.set_name, excluded.card_name, excluded.card_number, excluded.variation, excluded.certificate_value, excluded.tag_grade)""",
            (
                item["uuid"],
                item["category_name"],
                item["year"],
                item["brand_name"],
                item["set_name"],
                item["card_name"],
                item["card_number"],
                item["variation"],
                item["certificate_value"],
                item["tag_grade"],
            ),
        )
        self.connection.commit()
        return item
