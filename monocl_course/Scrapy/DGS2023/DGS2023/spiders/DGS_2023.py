import scrapy
import pandas as pd


class Dgs2023Spider(scrapy.Spider):
    name = "DGS_2023"
    allowed_domains = [
        "seno2023.abstractserver.com",
        "seno2023.planner.documedias.systems",
    ]
    collected_data = []

    def start_requests(self):
        for day in range(1, 4):
            start_url = f"https://seno2023.planner.documedias.systems/api/program/days/{day}?program_mode=list&program_sort=date&filter_display_type=7,9&filter_group=is_not_child"
            yield scrapy.Request(
                url=start_url, method="GET", callback=self.parse_sessions_list
            )

    def parse_sessions_list(self, response):
        sessions = response.json()
        for session in sessions:
            session_id = session.get("id")
            session_url = f"https://seno2023.planner.documedias.systems/api/program/sessions/{session_id}"
            yield scrapy.Request(
                url=session_url, method="GET", callback=self.parse_session
            )

    def parse_session(self, response):
        session_data = response.json()

        if not session_data:
            return

        session_name = session_data[0]["title"]
        if "poster" not in session_name.lower():
            return

        moderators_block = session_data[0]["persons"]
        for mod in moderators_block:
            mod_data = mod["person"]
            name = " ".join(
                (mod_data.get("first_name", ""), mod_data.get("last_name", ""))
            )
            affiliation = ", ".join(
                part
                for part in (
                    mod_data.get("institution") or "",
                    mod_data.get("city") or "",
                    mod_data.get("state") or "",
                    (mod_data.get("country") or {}).get("name") or "",
                )
                if part
            )
            email = mod_data.get("email")
            self.collected_data.append(
                {
                    "Name (incl. titles)": name,
                    "Affiliation/Organisation and location": affiliation,
                    "Role": "Moderator",
                    "Email": email,
                    "Session Name": session_name,
                    "Session Description": "",
                    "Presentation Title": "",
                    "Presentation Abstract": "",
                    "Abstract URL": "",
                }
            )

        presentations_block = session_data[0]["presentations"]
        for presentation in presentations_block:
            pres_title = presentation["title"]
            pres_id = presentation["id"]
            pres_url = f"https://seno2023.abstractserver.com/program/#/details/presentations/{pres_id}"
            authors = presentation["persons"]
            for author in authors:
                author_data = author["person"]
                name = " ".join(
                    (
                        author_data.get("first_name", ""),
                        author_data.get("last_name", ""),
                    )
                )
                affiliation = ", ".join(
                    part
                    for part in (
                        author_data.get("institution") or "",
                        author_data.get("city") or "",
                        author_data.get("state") or "",
                        (author_data.get("country") or {}).get("name") or "",
                    )
                    if part
                )
                email = author_data.get("email", "")
                self.collected_data.append(
                    {
                        "Name (incl. titles)": name,
                        "Affiliation/Organisation and location": affiliation,
                        "Role": "Poster presenter",
                        "Email": email,
                        "Session Name": session_name,
                        "Session Description": "",
                        "Presentation Title": pres_title,
                        "Presentation Abstract": "",
                        "Abstract URL": pres_url,
                    }
                )

    def closed(self, reason):
        df = pd.DataFrame(self.collected_data)
        df.to_excel("DGS_test.xlsx", index=False, engine="openpyxl")
