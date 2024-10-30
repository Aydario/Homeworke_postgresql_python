from ClientsDatabase import ClientsDatabase
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    database = os.getenv("database")
    user = os.getenv("user")
    password = os.getenv("password")

    # Подключаемся к базе данных и создаем таблицы Clients и ClientPhones
    db = ClientsDatabase(database, user, password)

    # Изменение данных клиента
    # Сначала по имени и фамилии находим id клиента в таблице, далее вносим изменения
    firstname = input('Введите имя клиента (латинницей), данные которого хотите изменить: ')
    lastname = input('Введите фамилию клиента (латинницей), данные которого хотите изменить: ')
    db.find_clientid(firstname, lastname)
    clientid = input('Введите id клиента из предложенного варианта (цифрой), данные которого хотите изменить: ')
    new_firstname = input('Введите измененное имя клиента (латинницей): ')
    new_lastname = input('Введите измененную фамилию клиента (латинницей): ')
    new_email = input('Введите измененный email клиента: ')
    db.update_data_clients(clientid, new_firstname, new_lastname, new_email)

if __name__ == '__main__':
    main()