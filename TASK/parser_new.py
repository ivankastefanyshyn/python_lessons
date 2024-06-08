import json


def parse_file(session_data):
    collected_data = []
    session_title = session_data[0]["title"]
    moderators_block = session_data[0]["persons"]
    for mod in moderators_block:
        mod_data = mod["person"]
        name = " ".join((mod_data.get("first_name", ""), mod_data.get("last_name", "")))
        institution = " ".join(
            (
                mod_data.get("city", ""),
                mod_data.get("country", "").get("name", ""),
            )
        )
        email = mod_data.get("email", "")
        collected_data.append(
            {
                "Name": name,
                "Location": institution,
                "Role": "Moderator",
                "e-mail": email,
                "Session": session_title,
                "Description": "",
                "Title": "",
                "Abstract": "",
            }
        )
    presentations_block = session_data[0]["presentations"]
    for presentation in presentations_block:
        pres_data = presentation["presentation"]
        title = pres_data["title"]
        persons = pres_data["persons"]
        for person in persons:
            speaker_data = person["person"]
            speaker_name = " ".join(
                (speaker_data.get("first_name", ""), speaker_data.get("last_name", ""))
            )
            speaker_email = speaker_data.get("email", "")
            speaker_city = speaker_data.get("city", "")
            collected_data.append(
                {
                    "Name": speaker_name,
                    "Location": speaker_city,
                    "Role": "Speaker",
                    "e-mail": speaker_email,
                    "Session": session_title,
                    "Description": "",
                    "Title": title,
                    "Abstract": "",
                }
            )
    return collected_data


if __name__ == "__main__":
    with open(
        "/Users/ivanna/Documents/python_lessons/TASK/252.json", encoding="utf-8"
    ) as f:
        sessions_data = json.load(f)
        processed_data = parse_file(sessions_data)
