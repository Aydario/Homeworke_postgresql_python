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
    # Сначала по имени и фамилии находим id ном. телефона в таблице, далее удаляем
    # после удаляем клиента по найденному id клиента
    firstname = input('Введите имя клиента (латинницей), которого хотите удалить: ')
    lastname = input('Введите фамилию клиента (латинницей), которого хотите удалить: ')
    db.find_phoneid(firstname, lastname)
    phoneid = input('Введите id ном. телефона клиента из предложенного варианта (цифрой), которого хотите удалить: ')
    db.delete_clientphones(phoneid)
    db.find_clientid(firstname, lastname)
    clientid = input('Введите id клиента из предложенного варианта (цифрой), которого хотите удалить: ')
    db.delete_client(clientid)

if __name__ == '__main__':
    main()