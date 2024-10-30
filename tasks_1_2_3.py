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
    db.create_database()

    # Добавление новых клиентов
    db.add_client('Petr', 'Semenov', 'semio@mail.ru')
    db.add_client('Andrey', 'Ivanov', 'vanes@mail.ru')
    db.add_client('Nina', 'Antonova', 'nina@mail.ru')

    # Добавление номеров телефонов клиентов
    db.add_phone_number(1, '+79111111111')
    db.add_phone_number(1, '+79222222222')
    db.add_phone_number(3, '+79333333333')

if __name__ == '__main__':
    main()