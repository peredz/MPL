import pandas as pd
import requests
import re
from time import sleep

ST_ACCEPT = "text/html"
ST_USERAGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
HEADERS = {
    "Accept": ST_ACCEPT,
    "User-Agent": ST_USERAGENT
}


def get_ship_card_link(url):
    result = requests.get(url, headers=HEADERS)
    text = result.text
    match = re.search(r'<a class="ship-link" href="([^"]+)"', text)
    if not match:
        return None
    if len(match.groups()) != 1:
        return None
    link = r"https://www.vesselfinder.com" + match.groups()[0]
    return link


def ship_data(url, card_url):
    result_2 = requests.get(url, headers=HEADERS)
    text_2 = result_2.text

    IMO_search = re.search(r"IMO \d{7}", text_2)
    IMO = ''

    if IMO_search:
        IMO = IMO_search.group().split(' ')[1]

    MMSI_search = re.search(r"MMSI \d{9}", text_2)
    MMSI = ''

    if MMSI_search:
        MMSI = MMSI_search.group().split(' ')[1]

    name = "".join(card_url.split("=")[1])

    ship_type = ''
    type_search = re.findall(r'<span itemprop="name">\s*(.*?)\s*</span>', text_2)
    if type_search:
        ship_type = type_search[2]
    return name, IMO, MMSI, ship_type

def process_doc(file_path: str, sheet_name='Sheet1'):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    column_names = ['Название', 'IMO', 'MMSI', 'тип']
    result_df = pd.DataFrame(columns=column_names)
    for index, row in df.iterrows():

        link = get_ship_card_link(row['Ссылка'])

        sleep(1)
        if link is None:
            continue

        name, IMO, MMSI, ship_type = ship_data(link, row['Ссылка'])

        new_row_data = {
            'Название': name,
            'IMO': IMO,
            'MMSI': MMSI,
            'тип': ship_type
                        }
        new_row_df = pd.DataFrame([new_row_data])
        print(new_row_df)
        result_df = pd.concat([result_df, new_row_df], ignore_index=True)
        sleep(1)

    result_df.to_excel('result.xlsx', index=False)


if __name__ == "__main__":
    process_doc("Links.xlsx", "Лист1")