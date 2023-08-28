import os
import json
from typing import Any
import psycopg2
from config import config

directory = 'temp/'
params = config()


def create_database(database_name: str, params_: dict):
    """Создание базы данных и таблиц для работодателей и их вакансий."""

    conn = psycopg2.connect(dbname='postgres', **params_)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params_)

    with conn.cursor() as cur:
        cur.execute("""
               CREATE TABLE employers (
                   employer_id SERIAL PRIMARY KEY,
                   company_name VARCHAR(50) NOT NULL,
                   url_emp_hh VARCHAR(50) NOT NULL
                   )
                """)

    with conn.cursor() as cur:
        cur.execute("""
               CREATE TABLE vacancies (
                   vacancy_id SERIAL PRIMARY KEY,
                   vacancy_name VARCHAR(100) NOT NULL,
                   employer_id INT REFERENCES employers(employer_id),
                   url_vac_hh VARCHAR(50) NOT NULL,
                   salary INT              
               )
           """)

    conn.commit()
    conn.close()


def get_list_datafile():
    """Создает список из временных файлов в которых
       содержаться данные о работодателях и их вакансиях"""
    list_datafile = []
    for data in os.scandir(directory):
        if data.is_file() and data.name.endswith('.json'):
            list_datafile.append(data.path)
    return list_datafile


def save_lots_of_data_to_database(list_datafile, database_name) -> None:
    """Сохранение данных о множестве работодателей и их вакансиях"""
    for json_file in list_datafile:
        with open(json_file, 'r', encoding='utf8') as data:
            data_file = json.load(data)
            save_data_to_database(data_file, database_name, params)


def save_data_to_database(data_: dict[str, list[Any] | Any], database_name: str, params_: dict) -> None:
    """Сохранение данных о работодателе и его вакансиях."""
    conn = psycopg2.connect(dbname=database_name, **params_)
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO employers (company_name, url_emp_hh)
            VALUES (%s, %s)
            RETURNING employer_id
            """,
            (data_['name'], data_['url'])
        )

        employer_id = cur.fetchone()[0]
        data = data_['items']
        for vacancy in data:
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_name, employer_id, url_vac_hh, salary)
                VALUES (%s, %s, %s, %s)
                """,
                (vacancy['name'], employer_id, vacancy['alternate_url'],
                 vacancy['salary']['from'] if isinstance(vacancy["salary"], dict) else None)
            )

    conn.commit()
    conn.close()
