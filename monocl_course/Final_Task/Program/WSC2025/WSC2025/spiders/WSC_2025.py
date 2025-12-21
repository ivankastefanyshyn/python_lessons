import scrapy
from scrapy.selector import Selector
import pandas as pd


class Wsc2025Spider(scrapy.Spider):
    name = "WSC_2025"
    allowed_domains = ["cslide.ctimeetingtech.com"]
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,hu;q=0.7,uk;q=0.6,ru;q=0.5",
        "Connection": "keep-alive",
        "Referer": "https://cslide.ctimeetingtech.com/wsc25/attendee/confcal/session/list",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "Cookie": "SID=5n54fg13k4kh2dmq4t95a39dp6; SID=v3j2ij9elaqll83c2dquunpdgv",
    }

    collected_data = []

    def start_requests(self):
        for page in range(1, 11):
            url = f"https://cslide.ctimeetingtech.com/wsc25/attendee/confcal/session/list?p={page}"
            yield scrapy.Request(
                url=url, method="GET", headers=self.headers, callback=self.parse_page
            )

    def parse_page(self, response):
        session_blocks = response.xpath(
            '//div[contains(@class, "card item-container session")]'
        ).getall()
        for session_block in session_blocks:
            session_selector = Selector(text=session_block)
            session_url = session_selector.xpath(
                './/h4[@class="session-title card-title"]/a/@href'
            ).get("")
            if not session_url:
                continue
            session_name = (
                session_selector.xpath(
                    './/h4[@class="session-title card-title"]/a/text()'
                )
                .get("")
                .strip()
            )

            moderators = []
            moderator_blocks = session_selector.xpath(
                './/ul[@class="persons"]/li'
            ).getall()
            for m_block in moderator_blocks:
                m_selector = Selector(text=m_block)
                name = m_selector.xpath(".//a/text()").get("").strip()
                affiliation = m_selector.xpath(".//a/small/text()").get("").strip(" ()")
                moderator = {
                    "name": name,
                    "affiliation": affiliation,
                }
                moderators.append(moderator)

            yield scrapy.Request(
                url=session_url,
                method="GET",
                headers=self.headers,
                callback=self.parse_session,
                meta={"session_name": session_name, "moderators": moderators},
            )

    def parse_session(self, response):
        session_name = response.meta.get("session_name")
        moderators = response.meta.get("moderators")
        for moderator in moderators:
            self.collected_data.append(
                {
                    "Name (incl. titles)": moderator.get("name", ""),
                    "Affiliation/Organisation and location": moderator.get(
                        "affiliation", ""
                    ),
                    "Role": "Moderator",
                    "Email": "",
                    "Session Name": session_name,
                    "Session Description": "",
                    "Presentation Title": "",
                    "Presentation Abstract": "",
                    "Abstract URL": "",
                }
            )
        presentation_blocks = response.xpath(
            '//div[contains(@class, "card presentation")]'
        ).getall()
        for p_block in presentation_blocks:
            p_selector = Selector(text=p_block)
            title = (
                p_selector.xpath('.//h4[@class="card-title"]//text()').get("").strip()
            )
            abstract = " ".join(
                p_selector.xpath('.//div[@class="abstract-section"]//text()').getall()
            )
            authors_block = p_selector.xpath('.//ul[@class="persons"]/li').getall()
            if not authors_block:
                continue
            for author in authors_block:
                a_selector = Selector(text=author)
                name = a_selector.xpath(".//a/text()").get("").strip()
                affiliation = a_selector.xpath(".//a/small/text()").get("").strip(" ()")
                if "poster" in session_name.lower():
                    role = "Poster Presenter"
                elif "panel discussion" in title.lower():
                    role = "Panelist"
                else:
                    role = "Speaker"

                self.collected_data.append(
                    {
                        "Name (incl. titles)": name,
                        "Affiliation/Organisation and location": affiliation,
                        "Role": role,
                        "Email": "",
                        "Session Name": session_name,
                        "Session Description": "",
                        "Presentation Title": title,
                        "Presentation Abstract": abstract,
                        "Abstract URL": response.url,
                    }
                )

    def closed(self, reason):
        df = pd.DataFrame(self.collected_data)
        df.to_excel("WSC_2025_Program.xlsx", index=False, engine="openpyxl")
