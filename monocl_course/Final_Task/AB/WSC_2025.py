import re
import pandas as pd


def split_on_presentations(data):
    presentations_list = []
    presentations = re.split(r"^[A-Z]{2}\d{3}\s/.*$", data, flags=re.MULTILINE)
    for presentation in presentations:
        if presentation and presentation.strip():
            presentations_list.append(presentation.strip())
    return presentations_list


def parse_presentation(presentation):
    lines = presentation.split("\n")
    title = lines[0].strip()
    abstract = "\n".join(line.strip() for line in lines[3:] if line.strip())
    raw_affiliations = lines[2]
    session_name_and_authors = lines[1]
    if "." in session_name_and_authors:
        session_name, raw_authors = session_name_and_authors.split(".", 1)
        session_name = session_name.strip()
        raw_authors = raw_authors.strip()
    else:
        session_name = ""
        raw_authors = session_name_and_authors.strip()

    return title, abstract, session_name, raw_authors, raw_affiliations


def parse_authors_and_affiliations(raw_authors, raw_affiliations):
    authors_with_indices = []
    affiliations_with_indices = []

    if re.search(r"\d", raw_authors):
        authors = re.split(r",\s(?=[A-Za-zÀ-ÖØ-öø-ÿĀ-ſ])", raw_authors)
        for author in authors:
            name = re.sub(r"\d", "", author).strip(" ,.")
            indices = re.findall(r"\d+", author)
            authors_with_indices.append((name, indices))

        affiliations = re.split(r",\s*(?=\d+)", raw_affiliations)
        for aff in affiliations:
            affiliation = re.sub(r"^\d+", "", aff).strip(" ,.")
            ind = re.findall(r"^\d+", aff)
            affiliations_with_indices.append((affiliation, ind))

    else:
        authors = raw_authors.split(",")
        for author in authors:
            name = author.strip(" ,.")
            indices = ["1"]
            authors_with_indices.append((name, indices))
        affiliation = raw_affiliations.strip(" ,.")
        ind = ["1"]
        affiliations_with_indices.append((affiliation, ind))

    return authors_with_indices, affiliations_with_indices


def match_authors_and_affiliations(authors_with_indices, affiliations_with_indices):
    matched = []
    for author, author_inds in authors_with_indices:
        affs = []
        for aff, ind_list in affiliations_with_indices:
            if any(ind in author_inds for ind in ind_list):
                affs.append(aff)
        matched.append({"name": author, "affiliation": " ___ ".join(affs)})

    return matched


if __name__ == "__main__":
    with open(
        "/Users/ivanna/Documents/python_lessons/monocl_course/Final_Task/AB/WSC_2025.txt",
        "r",
        encoding="utf-8",
    ) as f:
        data = f.read()
    presentations_list = split_on_presentations((data))
    collected_data = []
    for p in presentations_list:
        title, abstract, session_name, raw_authors, raw_affiliations = (
            parse_presentation(p)
        )
        authors_with_indices, affiliations_with_indices = (
            parse_authors_and_affiliations(raw_authors, raw_affiliations)
        )
        matched_authors = match_authors_and_affiliations(
            authors_with_indices, affiliations_with_indices
        )
        for author in matched_authors:
            collected_data.append(
                {
                    "Name (incl. titles)": author["name"],
                    "Affiliation/Organisation and location": author["affiliation"],
                    "Role": "Abstract author",
                    "Email": "",
                    "Session Name": session_name,
                    "Session Description": "",
                    "Presentation Title": title,
                    "Presentation Abstract": abstract,
                    "Abstract URL": "https://journals.sagepub.com/doi/epub/10.1177/17474930251371440",
                }
            )
df = pd.DataFrame(collected_data)
df.to_excel("WSC_2025_AB.xlsx", index=False)
