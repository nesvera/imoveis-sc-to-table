#!/bin/env python3

import requests
from bs4 import (
    BeautifulSoup,
    element,
)
from typing import (
    Optional,
    List,
    Dict,
)
import time
import re
import pandas as pd

url = "https://www.imoveis-sc.com.br/blumenau/comprar/apartamento"


class ImovelInfo:
    code = ""
    model = ""
    real_state = ""
    neighborhood = ""
    city = ""
    summary = ""
    url = ""
    bedrooms = ""
    suite = ("",)
    garage_slots = ""
    space = ""
    value = ""
    changed = False
    viewed = False
    disliked = False
    deleted = False
    comments = ""

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
        comments: str = "",
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
        self.comments = comments

    def __str__(
        self,
    ) -> str:
        info_str = f"code: {self.code}, model: {self.model}, real_state: {self.real_state}, "
        info_str += f"neighborhood: {self.neighborhood}, city: {self.city}, summary: {self.summary}, "
        info_str += f"url: {self.url}, bedrooms: {self.bedrooms}, suite: {self.suite}, "
        info_str += f"garage_slots: {self.garage_slots}, space: {self.space}, price: {self.price}, "
        info_str += f"changed: {self.changed}, viewed: {self.viewed}, disliked: {self.disliked}, "
        info_str += f"deleted: {self.deleted}, comments: {self.comments}"

        return info_str

    def table_serializer(
        self,
    ) -> str:
        dict_s = self.__dict__

        if dict_s.get("changed"):
            dict_s["changed"] = "x"
        else:
            dict_s["changed"] = ""

        if dict_s.get("viewed"):
            dict_s["viewed"] = "x"
        else:
            dict_s["viewed"] = ""

        if dict_s.get("disliked"):
            dict_s["disliked"] = "x"
        else:
            dict_s["disliked"] = ""

        if dict_s.get("deleted"):
            dict_s["deleted"] = "x"
        else:
            dict_s["deleted"] = ""

        return dict_s

    @classmethod
    def table_deserializer(
        cls,
        dict_s: Dict = None,
    ):
        if dict_s is None:
            return

        if dict_s.get("changed") == "x":
            dict_s["changed"] = True
        else:
            dict_s["changed"] = False

        if dict_s.get("viewed") == "x":
            dict_s["viewed"] = True
        else:
            dict_s["viewed"] = False

        if dict_s.get("disliked") == "x":
            dict_s["disliked"] = True
        else:
            dict_s["disliked"] = False

        if dict_s.get("deleted") == "x":
            dict_s["deleted"] = True
        else:
            dict_s["deleted"] = False

        return cls(
            code=dict_s.get("code"),
            model=dict_s.get("model"),
            real_state=dict_s.get("real_state"),
            neighborhood=dict_s.get("neighborhood"),
            city=dict_s.get("city"),
            summary=dict_s.get("summary"),
            url=dict_s.get("url"),
            bedrooms=dict_s.get("bedrooms"),
            suite=dict_s.get("suite"),
            garage_slots=dict_s.get("garage_slots"),
            space=dict_s.get("space"),
            price=dict_s.get("price"),
            changed=dict_s.get("changed"),
            viewed=dict_s.get("viewed"),
            disliked=dict_s.get("disliked"),
            deleted=dict_s.get("deleted"),
            comments=dict_s.get("comments"),
        )


class ImoveisSC:
    def __init__(
        self,
        url: str = "",
    ):
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

    def crawl(
        self,
    ) -> List:
        page_count = 0
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
            time.sleep(0.01)

        return imoveis_list

    def get_last_page_number(
        self,
        page: str = "",
    ) -> str:
        soup = BeautifulSoup(
            page,
            "html.parser",
        )
        snnipet = soup.find(
            "div",
            class_="navigation",
        ).get_text(strip=True)

        match = re.search(
            r"de \d+",
            snnipet,
        )

        if match:
            page_str = match.group()
            page_str = page_str.split(" ")[1]
            return int(page_str)

        else:
            return 20

    def make_request(
        self,
        page: int = 0,
    ) -> Optional[str]:

        url = self.url
        if page > 0:
            if "?" in url:
                url += f"&page={page}"
            else:
                url += f"?page={page}"

        try:
            response = self.session.get(url, headers=self.headers, timeout=5)
        except Exception as e:
            print("Failed to get page: ", url)
            print("Error: ", e)
            return None

        if response.status_code != 200:
            print("Failed to get page: ", url)
            print("Status code: ", response.status_code)
            return None

        return response.text

    def extract_info(
        self,
        page: str = "",
    ) -> List[ImovelInfo]:
        try:
            soup = BeautifulSoup(
                page,
                "html.parser",
            )
        except Exception as e:
            print("Error: ", e)
            return []

        imoveis_soup = soup.find_all(
            "div",
            class_="imovel-data",
        )

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
                price=price,
            )

            imoveis_list.append(imovel_info)

        return imoveis_list

    def get_model(
        self,
        snnipet: element.Tag = "",
    ) -> str:
        try:
            model = snnipet.find(
                "meta",
                itemprop="model",
            ).get("content")
        except:
            return ""

        return model

    def get_code(
        self,
        snnipet: element.Tag = "",
    ) -> str:
        try:
            code = snnipet.find(
                "meta",
                itemprop="sku",
            ).get("content")
        except:
            return ""

        return code

    def get_real_estate(
        self,
        snnipet: element.Tag = "",
    ) -> str:
        try:
            real_estate = snnipet.find(
                "meta",
                itemprop="brand",
            ).get("content")
        except:
            return ""

        return real_estate

    def get_neighborhood(
        self,
        snnipet: element.Tag = "",
    ) -> str:
        try:
            neighboor = (
                snnipet.find(
                    "div",
                    class_="imovel-extra",
                )
                .find("strong")
                .text
            )
            neighboor = neighboor.split(",")[1]
            neighboor = neighboor.strip()
        except:
            return ""

        return neighboor

    def get_city(
        self,
        snnipet: element.Tag = "",
    ) -> str:
        try:
            city = (
                snnipet.find(
                    "div",
                    class_="imovel-extra",
                )
                .find("strong")
                .text
            )
            city = city.split(",")[0]
            city = city.strip()
        except:
            return ""

        return city

    def get_summary(
        self,
        snnipet: element.Tag = "",
    ) -> str:
        try:
            summary = snnipet.find(
                "meta",
                itemprop="name",
            ).get("content")
        except:
            return ""

        return summary

    def get_url(
        self,
        snnipet: element.Tag = "",
    ) -> str:
        try:
            url = snnipet.find("a").get("href")
        except:
            return ""

        return url

    def get_bedrooms(
        self,
        snnipet: element.Tag = "",
    ) -> str:
        try:
            beedrooms_li = snnipet.find(
                "i",
                class_="mdi-bed-king-outline",
            ).find_parent("li")
            beedrooms = beedrooms_li.find("strong").text
        except:
            return ""

        return beedrooms

    def get_suite(
        self,
        snnipet: element.Tag = "",
    ) -> str:
        try:
            suite_li = snnipet.find(
                "i",
                class_="mdi-shower",
            ).find_parent("li")
            suite = suite_li.find("strong").text
        except:
            return ""

        return suite

    def get_garage_slots(
        self,
        snnipet: element.Tag = "",
    ) -> str:
        try:
            gararge_slot_li = snnipet.find(
                "i",
                class_="mdi-car",
            ).find_parent("li")
            gararge_slot = gararge_slot_li.find("strong").text
        except:
            return ""

        return gararge_slot

    def get_space(
        self,
        snnipet: element.Tag = "",
    ) -> str:
        try:
            space_slot_li = snnipet.find(
                "i",
                class_="mdi-arrow-expand",
            ).find_parent("li")
            space_slot = space_slot_li.find("strong").text
        except:
            return ""

        return space_slot

    def get_price(
        self,
        snnipet: element.Tag = "",
    ) -> str:
        try:
            price = snnipet.find(
                "meta",
                itemprop="lowprice",
            ).get("content")
        except:
            return ""

        return price


class ImoveisScTable:
    filepath = "imoveis.xlsx"

    def __init__(
        self,
        filepath: str = "",
    ):
        if len(filepath) > 0:
            filepath = filepath

    def load_file(
        self,
    ):
        try:
            df_existing = pd.read_excel(
                self.filepath,
                engine="openpyxl",
            )
        except:
            return []

        imovel_items = []
        for (
            _,
            row,
        ) in df_existing.iterrows():
            row_dict = row.to_dict()
            item = ImovelInfo.table_deserializer(row_dict)
            imovel_items.append(item)

        return imovel_items

    def create_index_dict(
        self,
        items: List[ImovelInfo] = None,
    ):
        if items is None:
            return False

        item_dict = {}

        for item in items:
            index = item.code
            item_dict[index] = item

        return item_dict

    def update_file(
        self,
        items: List[ImovelInfo] = None,
    ):
        if items is None:
            return False

        table_items = self.load_file()

        site_items_hash_table = self.create_index_dict(items)
        site_items_keys = list(site_items_hash_table.keys())
        table_items_hash_table = self.create_index_dict(table_items)
        table_items_keys = list(table_items_hash_table.keys())

        end_items_hash_table = {}

        for (
            index_site,
            item_site,
        ) in site_items_hash_table.items():
            item_table = table_items_hash_table.get(
                index_site,
                None,
            )

            # new item
            if item_table is None:
                end_items_hash_table[index_site] = item_site
                site_items_keys.remove(index_site)
                continue

            # item changed
            if self.is_different(
                item_site,
                item_table,
            ):
                item_site.changed = True
                end_items_hash_table[index_site] = item_site
                site_items_keys.remove(index_site)
                table_items_keys.remove(index_site)
                continue

            end_items_hash_table[index_site] = item_table
            site_items_keys.remove(index_site)
            table_items_keys.remove(index_site)

        # skip set deleting if file does not exist
        if len(table_items) > 0:
            for remaining_item_key in table_items_keys:
                item = table_items_hash_table.get(
                    remaining_item_key,
                    None,
                )
                if item is None:
                    continue

                item.deleted = True
                end_items_hash_table[remaining_item_key] = item

        end_items = []
        for (
            _,
            item,
        ) in end_items_hash_table.items():
            end_items.append(item)

        self.write_file(end_items)

    def is_different(
        self,
        new: ImovelInfo = None,
        old: ImovelInfo = None,
    ):
        if new is None or old is None:
            return False

        diff = new.price != old.price

        return diff

    def write_file(
        self,
        items: List[ImovelInfo] = None,
    ):
        if items is None:
            return False

        table_lines = []
        for item in items:
            table_lines.append(item.table_serializer())

        df_new = pd.DataFrame(table_lines)
        df_new.to_excel(
            self.filepath,
            index=False,
            engine="openpyxl",
        )


if __name__ == "__main__":
    site = ImoveisSC(url)
    site_items = site.crawl()

    imovel_table = ImoveisScTable()
    imovel_table.update_file(site_items)
