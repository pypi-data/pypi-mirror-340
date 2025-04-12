import asyncio
from collections.abc import Sequence
import logging
import re
import math
import json

from bs4 import BeautifulSoup, Tag
import httpx
from .models import AbstractParser, ParsedItem, ParsedPriceByRegion, Price


class ItemParser:
    def __init__(self, data: dict):
        self._data = data

    def _parse_price(self, s: str) -> Price:
        price_regex = re.compile(
            r"(?:(?P<price>\d[\d\s.,]*)\s*([A-Z]{2,3})|([A-Z]{2,3})\s*(\d[\d\s.,]*))"
        )
        price_match = price_regex.search(s)
        assert price_match is not None
        # may be 2 different variations of price form on page
        value, currency_code = None, None
        if price_match.group(1) is not None:
            value, currency_code = price_match.group(1, 2)
        elif price_match.group(3) is not None:
            value, currency_code = price_match.group(4, 3)
        assert value is not None and currency_code is not None, "Unable to parse price"
        normalized_value = (
            value.replace(".", "")
            .replace(",", ".")
            .replace(" ", "")
            .replace("\xa0", "")
        )
        curr = currency_code.strip()
        if curr == "TL":
            curr = "TRY"  # change abbreviated to official currency code for turkish
        return Price(value=float(normalized_value), currency_code=curr)

    def _parse_discount(self, s: str | None) -> int:
        if s is None:
            return 0
        normalized = s.replace("%", "")
        return abs(int(normalized))

    def _find_cover_url(self) -> str | None:
        for el in self._data["media"]:
            if el["type"] == "IMAGE" and el["role"] == "MASTER":
                return el["url"]
        return None

    def parse(self, region: str) -> ParsedItem:
        name = self._data["name"]
        discounted_price = self._parse_price(self._data["price"]["discountedPrice"])
        base_price = self._parse_price(self._data["price"]["basePrice"])
        prices = {region: ParsedPriceByRegion(base_price, discounted_price)}
        discount = self._parse_discount(self._data["price"]["discountText"])
        image_url = self._find_cover_url()
        return ParsedItem(
            name,
            discount,
            prices,
            image_url or "",
        )


class PsnParser(AbstractParser):
    """Parses sales from psn official website. CAUTION: there might be products which looks absolutely the same but have different discount and prices.
    That's due to the fact that on psn price depends on product platform (ps4, ps5, etc). Such products aren't handled in parser."""

    _url = "https://store.playstation.com/{region}/category/3f772501-f6f8-49b7-abac-874a88ca4897/"

    def __init__(
        self,
        parse_regions: Sequence[str],
        client: httpx.AsyncClient,
        limit: int | None = None,
        max_concurrent_req: int = 5,
        logger: logging.Logger | None = None,
    ):
        super().__init__(parse_regions, client, limit)
        lang_to_region_mapping = {"tr": "en", "ua": "ru"}
        self._regions = {
            f"{lang_to_region_mapping.get( region, "en" )}-{region}"
            for region in parse_regions
        }
        self._sem = asyncio.Semaphore(max_concurrent_req)
        self._items_mapping: dict[str, ParsedItem] = {}
        self._curr_url = self._url

    async def _load_page(self, url: str) -> BeautifulSoup:
        async with self._sem:
            resp = await self._client.get(url, timeout=None)
        return BeautifulSoup(resp.text, "html.parser")

    async def _get_last_page_num_with_page_size(self) -> tuple[int, int]:
        soup = await self._load_page(self._curr_url)
        json_data_container = soup.find("script", id="__NEXT_DATA__")
        assert (
            isinstance(json_data_container, Tag) and json_data_container.string
        ), "Rate limit exceed! Please wait some time and try again later"
        data = json.loads(json_data_container.string)["props"]["apolloState"]
        page_info = None
        for key, value in data.items():
            if key.lower().startswith("categorygrid"):
                page_info = value["pageInfo"]
        assert page_info
        return math.ceil(page_info["totalCount"] / page_info["size"]), page_info["size"]

    async def _parse_single_page(self, page_num: int):
        self._logger.info("Parsing page %d", page_num)
        url = self._curr_url + str(page_num)
        soup = await self._load_page(url)
        json_data_container = soup.find("script", id="__NEXT_DATA__")
        assert isinstance(json_data_container, Tag) and json_data_container.string
        data = json.loads(json_data_container.string)["props"]["apolloState"]
        skipped_count = 0
        for key, value in data.items():
            if not key.lower().startswith("product:"):
                continue
            _, id, lang_with_region = key.split(":")
            region = lang_with_region.split("-")[1]
            try:
                parsed_item = ItemParser(value).parse(region)
            except AssertionError as e:
                self._logger.info(
                    "Failed to parse item: %s. KEY: %s, VALUE: %s", e, key, value
                )
                skipped_count += 1
                continue
            if id in self._items_mapping:
                self._items_mapping[id].prices.update(parsed_item.prices)
            else:
                self._items_mapping[id] = parsed_item
        self._logger.info("Page %d parsed. %d items skipped", page_num, skipped_count)

    async def _parse_all_for_region(self, region: str):
        self._curr_url = self._url.format(region=region)
        last_page_num, page_size = await self._get_last_page_num_with_page_size()
        if self._limit is not None:
            last_page_num = math.ceil(self._limit / page_size)
        self._logger.info("Parsing up to %d page", last_page_num)
        coros = [self._parse_single_page(i) for i in range(1, last_page_num + 1)]
        await asyncio.gather(*coros)

    async def parse(self) -> Sequence[ParsedItem]:
        [await self._parse_all_for_region(region) for region in self._regions]
        return list(self._items_mapping.values())[: self._limit]
