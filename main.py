from utils.create_db import create_database, get_list_datafile, save_lots_of_data_to_database
from utils import utils
from config import config
from cls import DBManager

params = config()
database = 'database5'

print('Загрузка данных с сайта HeadHunter (Из-за проблем с капчей, это может занят до трех минут)...')
utils.iteration()

print('Создание базы данных...')
# создание базы
create_database(database, params)
# заполнение базы
save_lots_of_data_to_database(get_list_datafile(), database)

cls_db = DBManager(database)
print('Завершено')

while True:
    request = str(input('Выберете один из следующих пунктов и введите соответсвующую цифру:\n'
                        ' - 1 - Список всех компаний и количество вакансий у каждой компании\n'
                        ' - 2 - Список всех вакансий с указанием названия компании, '
                        'названия вакансии и зарплаты и ссылки на вакансию\n'
                        ' - 3 - Средняя зарплата по вакансиям\n'
                        ' - 4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
                        ' - 5 - Список всех вакансий, в названии которых содержатся переданные слова, например python\n'
                        ' - 6 - Выход\n'))
    if request == '1':
        cls_db.iteration_rows(cls_db.get_companies_and_vacancies_count())
    elif request == '2':
        cls_db.iteration_rows(cls_db.get_all_vacancies())
    elif request == '3':
        cls_db.iteration_rows(cls_db.get_avg_salary())
    elif request == '4':
        cls_db.iteration_rows(cls_db.get_vacancies_with_higher_salary())
    elif request == '5':
        words = input(str('Введите через пробел слова для поиска ').lower())
        words_list = words.split(' ')
        cls_db.iteration_rows(cls_db.get_vacancies_with_keyword(words_list))
    elif request == '6':
        break
    else:
        print('Вы ввели недопустимое значение')
