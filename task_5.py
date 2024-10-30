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
    firstname = input('Введите имя клиента (латинницей), номер телефона которого хотите удалить: ')
    lastname = input('Введите фамилию клиента (латинницей), номер телефона которого хотите удалить: ')
    db.find_phoneid(firstname, lastname)
    phoneid = input('Введите id ном. телефона из предложенного варианта (цифрой), который хотите удалить: ')
    db.delete_clientphones(phoneid)

if __name__ == '__main__':
    main()