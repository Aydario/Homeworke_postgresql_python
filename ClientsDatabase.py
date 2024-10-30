import psycopg2
from typing import Optional, Tuple, List


class ClientsDatabase():
    """Класс для работы с базой данных клиентов."""

    def __init__(self, database: str, user: str, password: str):
        """
        Инициализация объекта базы данных.

        :param database: Название базы данных.
        :param user: Имя пользователя для подключения к базе данных.
        :param password: Пароль для подключения к базе данных.
        """
        self.database = database
        self.user = user
        self.password = password

    def create_database(self) -> None:
        """
        Создание таблиц Clients и ClientPhones, если они не существуют.
        """
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
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
        conn.close()

    def add_client(self, FirstName: str, LastName: str, Email: str) -> Optional[Tuple]:
        """
        Добавление нового клиента в таблицу Clients.

        :param FirstName: Имя клиента.
        :param LastName: Фамилия клиента.
        :param Email: Email клиента.
        :return: Кортеж с информацией о добавленном клиенте или None.
        """
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO Clients (FirstName, LastName, Email)
                VALUES (%s, %s, %s)
                RETURNING ClientID, FirstName, LastName, Email;
                """, (FirstName, LastName, Email))
                print(cur.fetchone())
        conn.close()
        

    def add_phone_number(self, ClientID: int, PhoneNumber: str) -> Optional[Tuple]:
        """
        Добавление номера телефона клиента в таблицу ClientPhones.

        :param ClientID: Идентификатор клиента.
        :param PhoneNumber: Номер телефона клиента.
        :return: Кортеж с информацией о добавленном номере телефона или None.
        """
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO ClientPhones (ClientID, PhoneNumber)
                VALUES (%s, %s)
                RETURNING PhoneID, ClientID, PhoneNumber;
                """, (ClientID, PhoneNumber))
                print(cur.fetchone())
        conn.close()

    def find_clientid(self, FirstName: str, LastName: str) -> List[Tuple]:
        """
        Поиск идентификатора клиента по имени и фамилии.

        :param FirstName: Имя клиента.
        :param LastName: Фамилия клиента.
        :return: Список кортежей с информацией о найденных клиентах.
        """
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT ClientID, FirstName, LastName, Email FROM Clients
                WHERE FirstName=%s AND LastName=%s
                """, (FirstName, LastName))
                print(*cur.fetchall(), sep='\n')
        conn.close()

    def update_data_clients(self, ClientID: int, FirstName: str, LastName: str, Email: str) -> Optional[Tuple]:
        """
        Обновление данных клиента в таблице Clients.

        :param ClientID: Идентификатор клиента.
        :param FirstName: Новое имя клиента.
        :param LastName: Новая фамилия клиента.
        :param Email: Новый email клиента.
        :return: Кортеж с обновленной информацией о клиенте или None.
        """
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE Clients SET FirstName=%s, LastName=%s, Email=%s
                WHERE ClientID=%s
                RETURNING ClientID, FirstName, LastName, Email;
                """, (FirstName, LastName, Email, ClientID))
                print(cur.fetchone())
        conn.close()

    def find_phoneid(self, FirstName: str, LastName: str) -> List[Tuple]:
        """
        Поиск идентификатора телефона клиента по имени и фамилии.

        :param FirstName: Имя клиента.
        :param LastName: Фамилия клиента.
        :return: Список кортежей с информацией о найденных телефонах.
        """
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT cp.PhoneID, c.FirstName, c.LastName, cp.PhoneNumber FROM Clients c
                LEFT JOIN ClientPhones cp ON c.ClientID = cp.ClientID
                WHERE FirstName=%s AND LastName=%s
                """, (FirstName, LastName))
                print(*cur.fetchall(), sep='\n')
        conn.close()

    def update_data_clientphones(self, PhoneID: int, ClientID: int, PhoneNumber: str) -> Optional[Tuple]:
        """
        Обновление данных телефона клиента в таблице ClientPhones.

        :param PhoneID: Идентификатор телефона.
        :param ClientID: Идентификатор клиента.
        :param PhoneNumber: Новый номер телефона.
        :return: Кортеж с обновленной информацией о телефоне или None.
        """
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE ClientPhones SET ClientID=%s, PhoneNumber=%s
                WHERE ClientID=%s
                RETURNING PhoneID, ClientID, PhoneNumber;
                """, (ClientID, PhoneNumber, PhoneID))
                print(cur.fetchone())
        conn.close()

    def delete_clientphones(self, PhoneID: int) -> None:
        """
        Удаление телефона клиента из таблицы ClientPhones.

        :param PhoneID: Идентификатор телефона.
        """
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                DELETE FROM ClientPhones WHERE PhoneID=%s;
                """, (PhoneID, ))
                conn.commit()
        conn.close()

    def delete_client(self, ClientID: int) -> None:
        """
        Удаление клиента из таблицы Clients.

        :param ClientID: Идентификатор клиента.
        """
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                DELETE FROM Clients WHERE ClientID=%s;
                """, (ClientID, ))
                conn.commit()
        conn.close()

    def find_client(self, Email: Optional[str] = None, PhoneNumber: Optional[str] = None) -> List[Tuple]:
        """
        Поиск клиента по email или номеру телефона.

        :param Email: Email клиента.
        :param PhoneNumber: Номер телефона клиента.
        :return: Список кортежей с информацией о найденных клиентах.
        """
        if Email and not PhoneNumber:
            with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                    SELECT ClientID, FirstName, LastName, Email FROM Clients
                    WHERE Email=%s
                    """, (Email, ))
                    print(*cur.fetchall(), sep='\n')
            conn.close()
        elif not Email and PhoneNumber:
            with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                    SELECT c.ClientID, c.FirstName, c.LastName, cp.PhoneNumber FROM Clients c
                    LEFT JOIN ClientPhones cp ON c.ClientID = cp.ClientID
                    WHERE cp.PhoneNumber=%s
                    """, (PhoneNumber, ))
                    print(*cur.fetchall(), sep='\n')
        conn.close()
