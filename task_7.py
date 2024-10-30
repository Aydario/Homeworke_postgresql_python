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

    # Поиск клиента по имени и фамилии
    firstname = input('Введите имя клиента (латинницей), которого хотите найти: ')
    lastname = input('Введите фамилию клиента (латинницей), которого хотите найти: ')
    db.find_clientid(firstname, lastname)

    # Поиск клиента по email
    email = input('Введите email клиента, которого хотите найти: ')
    db.find_client(Email=email)

    # Поиск клиента по номеру телефона
    number = input('Введите номер телефона клиента, которого хотите найти: ')
    db.find_client(PhoneNumber=number)

if __name__ == '__main__':
    main()