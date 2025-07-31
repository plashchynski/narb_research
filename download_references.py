import marimo

__generated_with = "0.14.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import requests
    from tqdm.auto import tqdm
    from bs4 import BeautifulSoup

    BASE_URL = "https://narb.by/"
    INDEX_URL = BASE_URL + "ru/%D0%BE%D0%B1-%D0%B0%D1%80%D1%85%D0%B8%D0%B2%D0%B5/%D0%BD%D0%B0%D1%83%D1%87%D0%BD%D0%BE-%D1%81%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%D1%87%D0%BD%D1%8B%D0%B9-%D0%B0%D0%BF%D0%BF%D0%B0%D1%80%D0%B0%D1%82/%D0%BE%D0%BF%D0%B8%D1%81%D0%B8"

    response = requests.get(INDEX_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    paths = [link.get("href") for link in soup.select("a.read_more[href]")]

    items = []
    for _path in tqdm(paths, desc="Fetching pages"):
        response = requests.get(BASE_URL + _path)
        soup = BeautifulSoup(response.text, "html.parser")
        items += [tr for tr in soup.select("tr")][1:]
    return (items,)


@app.cell
def _(items):
    references = []

    for item in items:
        tds = item.select("td")
        fonds = tds[0].text.strip()
        inventory = tds[1].text.strip()
        description = tds[2].text.strip()
        link = tds[3].select("a")[0].get("href")

        references.append((fonds, inventory, description, link))
    return (references,)


@app.cell
def _(references):
    import csv

    with open("references.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['fonds', 'inventory', 'description', 'link'])
        for row in references:
            writer.writerow(row)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
