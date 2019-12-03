from abc import ABC, abstractmethod
from tkinter.ttk import Treeview

from db import AbstractDB


class AbstractRepository(ABC):

    @abstractmethod
    def add_records(self, description: str, costs: str, total: str):
        pass

    @abstractmethod
    def update_record(self, description: str, costs: str, total: str):
        pass

    @abstractmethod
    def delete_records(self):
        pass

    @abstractmethod
    def view_records(self):
        pass


class DBRepository(AbstractRepository):

    def __init__(self, db: AbstractDB, tree_view: Treeview):
        self.db = db
        self.tree = tree_view

    def add_records(self, description: str, costs: str, total: str):
        self.db.insert(description, costs, total)
        self.view_records()

    def update_record(self, description: str, costs: str, total: str):
        self.db.update(description, costs, total, self.tree.set(self.tree.selection()[0], '#1'))
        self.view_records()

    def delete_records(self):
        for item in self.tree.selection():
            self.db.delete(self.tree.set(item, '#1'))
        self.view_records()

    def view_records(self):
        self.db.select_all()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.fetch_all()]
