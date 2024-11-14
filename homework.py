import psycopg2
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()
database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")


def create_database() -> None:
    """
    Создает таблицы Clients и ClientPhones, если они не существуют.
    Удаляет таблицы, если они уже существуют.
    """
    try:
        with psycopg2.connect(database=database, user=user, password=password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                DROP TABLE IF EXISTS ClientPhones;
                DROP TABLE IF EXISTS Clients;
                """)

                cur.execute("""
                CREATE TABLE IF NOT EXISTS Clients
                (
                    ClientID serial PRIMARY KEY,
                    FirstName varchar(50) NOT NULL,
                    LastName varchar(50) NOT NULL,
                    Email varchar(100) NOT NULL UNIQUE
                );
                """)

                cur.execute("""
                CREATE TABLE IF NOT EXISTS ClientPhones
                (
                    PhoneID serial PRIMARY KEY,
                    ClientID integer REFERENCES Clients(ClientID),
                    PhoneNumber varchar(20) NOT NULL UNIQUE
                );
                """)
                conn.commit()
                print('Таблицы успешно созданы!\n')
    except Exception as e:
        print(e)


def add_client(FirstName: str, LastName: str, Email: str, PhoneNumber: str = None) -> None:
    """
    Добавляет нового клиента в таблицу Clients.
    Если указан номер телефона, добавляет его в таблицу ClientPhones.

    :param FirstName: Имя клиента.
    :param LastName: Фамилия клиента.
    :param Email: Email клиента.
    :param PhoneNumber: Номер телефона клиента.
    """
    try:
        with psycopg2.connect(database=database, user=user, password=password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO Clients (FirstName, LastName, Email)
                VALUES (%s, %s, %s)
                RETURNING ClientID, FirstName, LastName, Email;
                """, (FirstName, LastName, Email))
                client = cur.fetchone()

                if PhoneNumber:
                    cur.execute("""
                    INSERT INTO ClientPhones (ClientID, PhoneNumber)
                    VALUES (%s, %s)
                    RETURNING PhoneNumber;
                    """, (client[0], PhoneNumber))
                    phone = cur.fetchone()
                    print(f'В базу добавлены данные о новом клиенте:\nFirstName: {client[1]}\n'
                          f'LastName: {client[2]}\nEmail: {client[3]}\nPhoneNumber: {phone[0]}\n')
                else:
                    print(f'В базу добавлены данные о новом клиенте:\nFirstName: {client[1]}\n'
                          f'LastName: {client[2]}\nEmail: {client[3]}\n')
    except Exception as e:
        print(e)


def add_phonenumber(ClientID: int, PhoneNumber: str) -> None:
    """
    Добавляет номер телефона клиента в таблицу ClientPhones.

    :param ClientID: Идентификатор клиента.
    :param PhoneNumber: Номер телефона клиента.
    """
    try:
        with psycopg2.connect(database=database, user=user, password=password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT FirstName, LastName, Email FROM Clients
                WHERE ClientID=%s
                """, (ClientID,))
                client = cur.fetchone()

                cur.execute("""
                INSERT INTO ClientPhones (ClientID, PhoneNumber)
                VALUES (%s, %s)
                RETURNING PhoneNumber;
                """, (ClientID, PhoneNumber))
                print(f'Клиенту под идентификатором: {ClientID} ({client[0]} {client[1]}, {client[2]})\n'
                      f'добавлен номер телефона: {PhoneNumber}\n')
    except Exception as e:
        print(e)


def update_client_data(ClientID: int, FirstName: str = None, LastName: str = None, Email: str = None) -> None:
    """
    Обновляет данные клиента в таблице Clients.

    :param ClientID: Идентификатор клиента.
    :param FirstName: Новое имя клиента.
    :param LastName: Новая фамилия клиента.
    :param Email: Новый email клиента.
    """
    try:
        with psycopg2.connect(database=database, user=user, password=password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE Clients
                SET FirstName=COALESCE(%s, FirstName),
                    LastName=COALESCE(%s, LastName),
                    Email=COALESCE(%s, Email)
                WHERE ClientID=%s
                RETURNING FirstName, LastName, Email;
                """, (FirstName, LastName, Email, ClientID))
                client = cur.fetchone()

                if client:
                    data = {
                        'FirstName': [client[0], FirstName],
                        'LastName': [client[1], LastName],
                        'Email': [client[2], Email],
                    }
                    print(f'У клиента под идентификатором "{ClientID}" изменились данные:')
                    for k, v in data.items():
                        if v[1]:
                            print(f'{k}: {v[0]}')
                    print()
                else:
                    print(f'Клиента под идентификатором "{ClientID}" не существует\n')
    except Exception as e:
        print(e)


def update_phonenumber(ClientID: int, old_phone: str = None, new_phone: str = None) -> None:
    """
    Обновляет номер телефона клиента в таблице ClientPhones.

    :param ClientID: Идентификатор клиента.
    :param old_phone: Старый номер телефона.
    :param new_phone: Новый номер телефона.
    """
    try:
        with psycopg2.connect(database=database, user=user, password=password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT FirstName, LastName, Email FROM Clients
                WHERE ClientID=%s
                """, (ClientID,))
                client = cur.fetchone()

                cur.execute("""
                UPDATE ClientPhones
                SET PhoneNumber=COALESCE(%s, PhoneNumber)
                WHERE ClientID=%s AND PhoneNumber=%s
                RETURNING PhoneNumber;
                """, (new_phone, ClientID, old_phone))
                phone = cur.fetchone()

                if client and phone:
                    print(f'У клиента под идентификатором "{ClientID}" изменился номер телефона:\n'
                          f'old phone number: {old_phone}\nnew phone number: {new_phone}\n')
                else:
                    print(f'Клиента под идентификатором "{ClientID}" не существует '
                          f'или у него нет номера "{old_phone}"\n')
    except Exception as e:
        print(e)


def delete_clientphone(ClientID: int, PhoneNumber: str) -> None:
    """
    Удаляет номер телефона клиента из таблицы ClientPhones.

    :param ClientID: Идентификатор клиента.
    :param PhoneNumber: Номер телефона клиента.
    """
    try:
        with psycopg2.connect(database=database, user=user, password=password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT PhoneID FROM ClientPhones WHERE ClientID=%s AND PhoneNumber=%s
                """, (ClientID, PhoneNumber))
                PhoneID = cur.fetchone()

                if PhoneID:
                    cur.execute("""
                    DELETE FROM ClientPhones WHERE PhoneID=%s
                    """, (PhoneID,))
                    conn.commit()
                    print('Номер телефона успешно удален!\n')
                else:
                    print(f'Клиента под идентификатором "{ClientID}" не существует '
                          f'или у него нет номера "{PhoneNumber}"\n')
    except Exception as e:
        print(e)


def delete_client(ClientID: int) -> None:
    """
    Удаляет данные клиента из таблицы Clients и все его номера телефонов из таблицы ClientPhones.

    :param ClientID: Идентификатор клиента.
    """
    try:
        with psycopg2.connect(database=database, user=user, password=password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT FirstName, LastName, Email FROM Clients
                WHERE ClientID=%s
                """, (ClientID,))
                client = cur.fetchone()

                cur.execute("""
                DELETE FROM ClientPhones WHERE ClientID=%s
                """, (ClientID,))

                cur.execute("""
                DELETE FROM Clients WHERE ClientID=%s
                """, (ClientID,))
                conn.commit()

                if client:
                    print(f'Данные о клиенте под идентификатором "{ClientID}" удалены!\n')
                else:
                    print(f'Клиента под идентификатором "{ClientID}" не существует!\n')
    except Exception as e:
        print(e)


def find_client(FirstName: str = None, LastName: str = None, Email: str = None, PhoneNumber: str = None) -> None:
    """
    Ищет клиента в таблице Clients по заданным параметрам.

    :param FirstName: Имя клиента.
    :param LastName: Фамилия клиента.
    :param Email: Email клиента.
    :param PhoneNumber: Номер телефона клиента.
    """
    try:
        with psycopg2.connect(database=database, user=user, password=password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT C.ClientID, C.FirstName, C.LastName, C.Email, ARRAY_AGG(CP.PhoneNumber) AS PhoneNumbers
                FROM Clients C
                LEFT JOIN ClientPhones CP ON C.ClientID = CP.ClientID
                WHERE (C.FirstName = %s OR %s IS NULL)
                AND (C.LastName = %s OR %s IS NULL)
                AND (C.Email = %s OR %s IS NULL)
                AND (CP.PhoneNumber=%s OR %s IS NULL)
                GROUP BY C.ClientID, C.FirstName, C.LastName, C.Email;
                """, (FirstName, FirstName, LastName, LastName, Email, Email, PhoneNumber, PhoneNumber))
                clients = cur.fetchall()

                if clients:
                    for client in clients:
                        print(f'Данные найденного клиента:\nClientID: {client[0]}\nFirstName: {client[1]}\n'
                              f'LastName: {client[2]}\nEmail: {client[3]}\nPhoneNumber: {client[4]}\n')
                else:
                    print(f'Клиента не существует!\n')
    except Exception as e:
        print(e)


# Пример вызова функций
create_database()
add_client('Алексей', 'Бубнов', 'buba@mail.ru')
add_client('Матвей', 'Ярцев', 'motya@mail.ru', '+7-999-999-99-22')
add_client('Петр', 'Максимов', 'maks@mail.ru', '+7-999-999-99-22')
add_client('Григорий', 'Боров', 'bor@mail.ru', '+7-999-999-99-44')
add_client('Иван', 'Матросов', 'matros@mail.ru')
add_client('Иван', 'Богатырев', 'ivan@mail.ru', '+7-999-999-99-66')
add_phonenumber(1, '+7-999-999-99-11')
add_phonenumber(1, '+7-999-999-11-11')
add_phonenumber(3, '+7-999-999-99-33')
add_phonenumber(6, '+7-999-999-66-66')
update_client_data(1, 'Бубен', 'Алексеев', 'alex@mail.ru')
update_client_data(2, LastName='Албанов')
update_client_data(-1, 'Алекс', 'Смирнов', 'true@mail.ru')
update_client_data(1, Email='bor@mail.ru')
update_phonenumber(1, '+7-999-999-99-11', '+7-999-999-91-11')
update_phonenumber(4, '+7-999-999-99-44', '+7-999-999-91-11')
update_phonenumber(55, '+7-999-999-99-44', '+7-999-999-91-11')
delete_clientphone(1, '+7-999-999-11-11')
delete_clientphone(2, '+7-944-444-44-44')
delete_clientphone(-1, '+7-944-444-44-44')
delete_clientphone(4, '+7-999-999-99-44')
delete_client(1)
delete_client(3)
delete_client(4)
find_client(LastName='Матросов')
find_client(FirstName='Евгений')
find_client(Email='motya@mail.ru')
find_client(FirstName='Иван')
