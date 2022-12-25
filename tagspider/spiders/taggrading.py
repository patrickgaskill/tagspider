from urllib.parse import urlencode

import scrapy


class TaggradingSpider(scrapy.Spider):
    name = "taggrading"
    allowed_domains = ["taggrading.com"]
    start_urls = ["https://api.taggrading.com/references/category"]

    def make_request(self, response, url, params, callback, cb_kwargs={}):
        return response.follow(
            url + "?" + urlencode(params), callback=callback, cb_kwargs=cb_kwargs
        )

    def parse(self, response):
        categories = response.json()["data"]
        for category in categories:
            self.logger.debug(category)
            yield self.make_year_request(response, category["name"])

    def make_year_request(self, response, category_name, page=1, limit=200):
        return self.make_request(
            response,
            "/pops/year",
            {"categoryName": category_name, "page": page, "limit": limit},
            self.parse_year,
            {"category_name": category_name, "page": page},
        )

    def parse_year(self, response, category_name, page):
        data = response.json()["data"]

        for item in data["items"]:
            self.logger.debug(item)
            yield self.make_set_request(response, category_name, item["cardYear"])

        limit = int(data["limit"])
        total = int(data["total"])

        if page * limit < total:
            yield self.make_year_request(response, category_name, page + 1, limit)

    def make_set_request(self, response, category_name, year, page=1, limit=200):
        return self.make_request(
            response,
            "/pops/set",
            {
                "categoryName": category_name,
                "year": year,
                "page": page,
                "limit": limit,
            },
            self.parse_set,
            {"category_name": category_name, "year": year, "page": page},
        )

    def parse_set(self, response, category_name, year, page):
        data = response.json()["data"]

        for item in data["items"]:
            self.logger.debug(item)
            yield self.make_card_request(
                response,
                category_name,
                year,
                item["brandName"],
                item["cardSetName"],
            )

        limit = int(data["limit"])
        total = int(data["total"])

        if page * limit < total:
            yield self.make_set_request(response, category_name, year, page + 1, limit)

    def make_card_request(
        self, response, category_name, year, brand_name, set_name, page=1, limit=200
    ):
        return self.make_request(
            response,
            "/pops/card",
            {
                "category": category_name,
                "year": year,
                "brandName": brand_name,
                "setName": set_name,
                "page": page,
                "limit": limit,
            },
            self.parse_card,
            {
                "category_name": category_name,
                "year": year,
                "brand_name": brand_name,
                "set_name": set_name,
                "page": page,
            },
        )

    def parse_card(self, response, category_name, year, brand_name, set_name, page):
        data = response.json()["data"]

        for item in data["items"]:
            self.logger.debug(item)
            yield self.make_rank_request(
                response,
                category_name,
                year,
                brand_name,
                set_name,
                item["cardName"],
                item["cardNumber"],
                item["variation"],
            )

        limit = int(data["limit"])
        total = int(data["total"])

        if page * limit < total:
            yield self.make_card_request(
                response, category_name, year, brand_name, set_name, page + 1, limit
            )

    def make_rank_request(
        self,
        response,
        category_name,
        year,
        brand_name,
        set_name,
        card_name,
        card_number,
        variation,
        page=1,
        limit=200,
    ):
        return self.make_request(
            response,
            "/pops/card/rank",
            {
                "category": category_name,
                "year": year,
                "brandName": brand_name,
                "setName": set_name,
                "cardName": card_name,
                "cardNumber": card_number,
                "variation": variation,
                "page": page,
                "limit": limit,
                "sort": "tagGrade:desc",
                "grades": "",
            },
            self.parse_rank,
            {
                "category_name": category_name,
                "year": year,
                "brand_name": brand_name,
                "set_name": set_name,
                "card_name": card_name,
                "card_number": card_number,
                "variation": variation,
                "page": page,
            },
        )

    def parse_rank(
        self,
        response,
        category_name,
        year,
        brand_name,
        set_name,
        card_name,
        card_number,
        variation,
        page,
    ):
        data = response.json()["data"]

        for item in data["items"]:
            self.logger.debug(item)
            yield {
                "category_name": category_name,
                "year": year,
                "brand_name": brand_name,
                "set_name": set_name,
                "card_name": card_name,
                "card_number": card_number,
                "variation": variation,
                "certificate_value": item["certificateValue"],
                "tag_grade": item["tagGrade"],
                "uuid": item["uuid"],
            }

        limit = int(data["limit"])
        total = int(data["total"])

        if page * limit < total:
            yield self.make_rank_request(
                response,
                category_name,
                year,
                brand_name,
                set_name,
                card_name,
                card_number,
                variation,
                page + 1,
                limit,
            )
