import sqlite3
from abc import ABC, abstractmethod


class AbstractDB(ABC):

    @abstractmethod
    def insert(self, description: str, costs: str, total: str):
        pass

    @abstractmethod
    def update(self, description: str, costs: str, total: str, id: str):
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

    @abstractmethod
    def select_all(self):
        pass

    @abstractmethod
    def fetch_all(self):
        pass


class SQLiteDB(AbstractDB):

    def __init__(self):
        self.connection = sqlite3.connect('finance.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS finance (id integer primary key , description text, '
            'costs text, total real)'
        )
        self.connection.commit()

    def insert(self, description: str, costs: str, total: str):
        self.cursor.execute('INSERT INTO finance(description, costs, total) '
                            'VALUES(?, ?, ?)', (description, total, costs))
        self.connection.commit()

    def update(self, description: str, costs: str, total: str, id: str):
        self.cursor.execute('UPDATE finance SET description=?, costs=?, total=? WHERE ID=?',
                            (description, costs, total, id))
        self.connection.commit()

    def delete(self, id: str):
        self.cursor.execute('DELETE FROM finance WHERE ID=?', id)
        self.connection.commit()

    def select_all(self):
        self.cursor.execute('SELECT * FROM finance')

    def fetch_all(self):
        return self.cursor.fetchall()
