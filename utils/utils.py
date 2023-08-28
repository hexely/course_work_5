import json
import requests
import time
from anec import dot

# Список id работодателей
ids_emp = ["1740", "9498112", "5008932", "40554", "2417", "1833581", "28275", "3778", "5672", "9697721"]


def get_vac(employer_id: str, page_=0):
    """Запрашивает данные о вакансии работодателя через api hh
       Возвращает JSON"""
    url_vac = f'https://api.hh.ru/vacancies?employer_id={employer_id}'
    params = {'page': page_, 'per_page': 50}

    response = requests.get(url_vac, params=params)

    if response.status_code != 200:
        raise Exception("cервер не отвечает")
    else:
        return response.json()


def iteration():
    """По id работодателя(из списка выше) загружает данные при
       помощи функции 'get_vac' и сохраняет при помощи функции 'save'"""
    # Перебор работодателей
    for id_ in ids_emp:
        print(dot[ids_emp.index(id_)])
        # Кол-во страниц, словарь для записи вакансий работодателя
        pages = get_vac(id_)['pages']
        name_company = get_vac(id_)['items'][0]['employer']['name']
        url_company = get_vac(id_)['items'][0]['employer']['alternate_url']
        list_vac = []

        # Перебор страниц
        for page in range(pages):
            vac = get_vac(id_, page)['items']
            list_vac.extend(vac)
            time.sleep(0.5)
        time.sleep(0.5)
        dict_vac = {'name': name_company, 'url': url_company, 'items': list_vac}
        save(dict_vac, f'{name_company}_vacancies.json')


def save(json_file, name_file='hh.json'):
    """Сохранят в файл данные JSON"""
    with open(f'temp/{name_file}', 'w', encoding="utf8") as f:
        json.dump(json_file, f, indent=4, ensure_ascii=False)