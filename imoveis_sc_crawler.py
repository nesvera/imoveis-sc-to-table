#!/bin/env python3

import requests
from bs4 import BeautifulSoup, element
from typing import Optional, List
import time
import re

url = "https://www.imoveis-sc.com.br/blumenau/comprar/apartamento/agua-verde_boa-vista_bom-retiro_centro_itoupava-seca_jardim-blumenau_ponta-aguda_ribeirao-fresco_velha_victor-konder_vila-formosa_vila-nova/quartos/2?ordenacao=menor-preco&valor=300000-450000&area=49-&suites=1"

class ImovelInfo:
    code = ""
    model = ""
    real_state = ""
    neighborhood = ""
    city = ""
    summary = ""
    url = ""
    bedrooms = ""
    suite = "",
    garage_slots = ""
    space = ""
    value = ""
    changed = False
    viewed = False
    disliked = False
    deleted = False

    def __init__(
        self,
        code: str = "",
        model: str = "",
        real_state: str = "",
        neighborhood: str = "",
        city: str = "",
        summary: str = "",
        url: str = "",
        bedrooms: str = "",
        suite: str = "",
        garage_slots: str = "",
        space: str = "",
        price: str = "",
        changed: bool = False,
        viewed: bool = False,
        disliked: bool = False,
        deleted: bool = False,
    ):
        self.code = code
        self.model = model
        self.real_state = real_state
        self.neighborhood = neighborhood
        self.city = city
        self.summary = summary
        self.url = url
        self.bedrooms = bedrooms
        self.suite = suite
        self.garage_slots = garage_slots
        self.space = space
        self.price = price
        self.changed = changed
        self.viewed = viewed
        self.disliked = disliked
        self.deleted = deleted

    def __str__(self) -> str:
        return f"code: {self.code}, model: {self.model}, real_state: {self.real_state}, neighborhood: {self.neighborhood}, city: {self.city}, summary: {self.summary}, url: {self.url}, bedrooms: {self.bedrooms}, suite: {self.suite}, garage_slots: {self.garage_slots}, space: {self.space}, price: {self.price}, changed: {self.changed}, viewed: {self.viewed}, disliked: {self.disliked}, deleted: {self.deleted}"


class ImoveisSC:
    def __init__(self, url: str = ""):
        self.url = url
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,pt;q=0.8,pt-BR;q=0.7",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

        self.session = requests.session()

    def crawl(self) -> List:
        page_count = 1
        page_last = -1

        imoveis_list = []
        while True:
            response = self.make_request(page=page_count)

            if page_last == -1:
                page_last = self.get_last_page_number(response)

            print(f"Querying page {page_count} of {page_last}")

            tmp_imoveis_list = self.extract_info(response)

            if tmp_imoveis_list is None:
                break

            imoveis_list += tmp_imoveis_list
            page_count += 1
            time.sleep(0.3)


        for im in imoveis_list:
            print(im.code)

        print("Len: ", len(imoveis_list))


    def get_last_page_number(self, page: str = "") -> str:
        soup = BeautifulSoup(page, "html.parser")
        snnipet = soup.find("div", class_="navigation").get_text(strip=True)

        match = re.search(r"de \d+", snnipet)

        if match:
            page_str = match.group()
            page_str = page_str.split(" ")[1]
            return int(page_str)

        else:
            return 20

    def make_request(self, page: int =  0) -> Optional[str]:

        url = self.url
        if page > 0:
            url += f"&page={page}"

        response = self.session.get(url, headers=self.headers)

        if response.status_code != 200:
            return None

        return response.text

    def extract_info(self, page: str = "") -> List[ImovelInfo]:
        soup = BeautifulSoup(page, "html.parser")
        imoveis_soup = soup.find_all("div", class_="imovel-data")

        if len(imoveis_soup) == 0:
            return None

        imoveis_list = []
        for imovel_tag in imoveis_soup:
            model = self.get_model(imovel_tag)
            code = self.get_code(imovel_tag)
            real_state = self.get_real_estate(imovel_tag)
            neighborhood = self.get_neighborhood(imovel_tag)
            city = self.get_city(imovel_tag)
            summary = self.get_summary(imovel_tag)
            url = self.get_url(imovel_tag)
            bedrooms = self.get_bedrooms(imovel_tag)
            suite = self.get_suite(imovel_tag)
            garage_slots = self.get_garage_slots(imovel_tag)
            space = self.get_space(imovel_tag)
            price = self.get_price(imovel_tag)

            imovel_info = ImovelInfo(
                code=code,
                model=model,
                real_state=real_state,
                neighborhood=neighborhood,
                city=city,
                summary=summary,
                url=url,
                bedrooms=bedrooms,
                suite=suite,
                garage_slots=garage_slots,
                space=space,
                price=price
            )

            imoveis_list.append(imovel_info)

        return imoveis_list

    def get_model(self, snnipet: element.Tag = "") -> str:
        try:
            model = snnipet.find("meta", itemprop="model").get("content")
        except:
            return ""

        return model

    def get_code(self, snnipet: element.Tag = "") -> str:
        try:
            code = snnipet.find("meta", itemprop="sku").get("content")
        except:
            return ""

        return code

    def get_real_estate(self, snnipet: element.Tag = "") -> str:
        try:
            real_estate = snnipet.find("meta", itemprop="brand").get("content")
        except:
            return ""

        return real_estate

    def get_neighborhood(self, snnipet: element.Tag = "") -> str:
        try:
            neighboor = snnipet.find("div", class_="imovel-extra").find("strong").text
            neighboor = neighboor.split(",")[1]
            neighboor = neighboor.strip()
        except:
            return ""

        return neighboor

    def get_city(self, snnipet: element.Tag = "") -> str:
        try:
            city = snnipet.find("div", class_="imovel-extra").find("strong").text
            city = city.split(",")[0]
            city = city.strip()
        except:
            return ""

        return city

    def get_summary(self, snnipet: element.Tag = "") -> str:
        try:
            summary = snnipet.find("meta", itemprop="name").get("content")
        except:
            return ""

        return summary

    def get_url(self, snnipet: element.Tag = "") -> str:
        try:
            url = snnipet.find("a").get("href")
        except:
            return ""

        return url

    def get_bedrooms(self, snnipet: element.Tag = "") -> str:
        try:
            beedrooms_li = snnipet.find("i", class_="mdi-bed-king-outline").find_parent(
                "li"
            )
            beedrooms = beedrooms_li.find("strong").text
        except:
            return ""

        return beedrooms

    def get_suite(self, snnipet: element.Tag = "") -> str:
        try:
            suite_li = snnipet.find("i", class_="mdi-shower").find_parent("li")
            suite = suite_li.find("strong").text
        except:
            return ""

        return suite

    def get_garage_slots(self, snnipet: element.Tag = "") -> str:
        try:
            gararge_slot_li = snnipet.find("i", class_="mdi-car").find_parent("li")
            gararge_slot = gararge_slot_li.find("strong").text
        except:
            return ""

        return gararge_slot

    def get_space(self, snnipet: element.Tag = "") -> str:
        try:
            space_slot_li = snnipet.find("i", class_="mdi-arrow-expand").find_parent(
                "li"
            )
            space_slot = space_slot_li.find("strong").text
        except:
            return ""

        return space_slot

    def get_price(self, snnipet: element.Tag = "") -> str:
        try:
            price = snnipet.find("meta", itemprop="lowprice").get("content")
        except:
            return ""

        return price


class ImovelTable:
    def __init__(self):
        pass

    def load_file():
        pass

    def update_file():
        pass

    def write_file():
        pass


if __name__ == "__main__":
    site = ImoveisSC(url)
    site_items = site.crawl()
