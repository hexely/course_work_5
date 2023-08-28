import psycopg2
from config import config


class DBManager:

    def __init__(self, database):
        self.database = database

    def get_companies_and_vacancies_count(self):
        params = config()
        conn = psycopg2.connect(dbname=self.database, **params)
        cur = conn.cursor()
        """Получает список всех компаний и количество вакансий у каждой компании."""
        cur.execute("""SELECT company_name, COUNT(vacancy_name) FROM vacancies
                           INNER JOIN employers USING(employer_id)
                           GROUP BY company_name"""
                    )
        rows = cur.fetchall()
        return rows

    def get_all_vacancies(self):
        params = config()
        conn = psycopg2.connect(dbname=self.database, **params)
        cur = conn.cursor()
        """Получает список всех вакансий с указанием названия компании,
           названия вакансии и зарплаты и ссылки на вакансию."""
        cur.execute("""SELECT company_name, vacancy_name, salary, url_vac_hh
                           FROM vacancies
                           INNER JOIN employers USING(employer_id)"""
                    )
        rows = cur.fetchall()
        return rows

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        params = config()
        conn = psycopg2.connect(dbname=self.database, **params)
        cur = conn.cursor()
        cur.execute("""SELECT AVG(salary)
                           FROM vacancies"""
                    )
        rows = cur.fetchall()
        return rows

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        params = config()
        conn = psycopg2.connect(dbname=self.database, **params)
        cur = conn.cursor()
        cur.execute("""SELECT * FROM vacancies 
                           WHERE salary > (SELECT AVG(salary) FROM vacancies)"""
                    )
        rows = cur.fetchall()
        return rows

    def get_vacancies_with_keyword(self, words):
        """Получает список всех вакансий, в названии которых содержатся переданные
           в метод слова, например python."""
        params = config()
        conn = psycopg2.connect(dbname=self.database, **params)
        cur = conn.cursor()

        request = f"""SELECT * FROM vacancies 
                     WHERE LOWER(vacancy_name) LIKE '%{words[0]}%'"""

        if len(words) > 1:
            for i in words[1:]:
                request += f" OR LOWER(vacancy_name) LIKE '%{i}%'"
            cur.execute(request)
            rows = cur.fetchall()
            return rows

        cur.execute(request)
        rows = cur.fetchall()
        return rows

    @staticmethod
    def iteration_rows(rows):
        for row in rows:
            print(row)
