import tkinter as tk
from tkinter import ttk

from db import SQLiteDB
from repository import DBRepository


class MainFrame(tk.Frame):

    BG_COLOR = '#d7d8e0'

    def __init__(self):
        super().__init__(root)
        self.repository = repository
        self.tree = tree_view
        self.init_main()
        self.repository.view_records()

    def init_main(self):
        self.toolbar = tk.Frame(bg=self.BG_COLOR, bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.btn_open_dialog()
        self.btn_edit_dialog()
        self.btn_delete_dialog()

        self.create_tree_column()
        self.create_tree_heading()

        self.tree.pack()

    def btn_open_dialog(self):
        self.add_img = tk.PhotoImage(file='add.gif')
        btn_open_dialog = tk.Button(self.toolbar, text='Добавити', command=self.open_dialog,
                                    bg=self.BG_COLOR, bd=0, compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

    def btn_edit_dialog(self):
        self.update_img = tk.PhotoImage(file='update.gif')
        btn_edit_dialog = tk.Button(self.toolbar, text='Редактировать', command=self.open_update_dialog,
                                    bg=self.BG_COLOR, bd=0, compound=tk.TOP, image=self.update_img)
        btn_edit_dialog.pack(side=tk.LEFT)

    def btn_delete_dialog(self):
        self.delete_img = tk.PhotoImage(file='delete.gif')
        btn_delete_dialog = tk.Button(self.toolbar, text='Видалити', command=self.repository.delete_records,
                                      bg=self.BG_COLOR, bd=0, compound=tk.TOP, image=self.delete_img)
        btn_delete_dialog.pack(side=tk.LEFT)

    def create_tree_column(self):
        self.tree.column(ID, width=30, anchor=tk.CENTER)
        self.tree.column(DESCRIPTION, width=360, anchor=tk.CENTER)
        self.tree.column(COSTS, width=150, anchor=tk.CENTER)
        self.tree.column(TOTAL, width=100, anchor=tk.CENTER)

    def create_tree_heading(self):
        self.tree.heading(ID, text='id')
        self.tree.heading(DESCRIPTION, text='Назва')
        self.tree.heading(COSTS, text='Дохід/Витрати')
        self.tree.heading(TOTAL, text='Сума')

    def open_dialog(self):
        ChildFrame()

    def open_update_dialog(self):
        UpdateFrame()


class ChildFrame(tk.Toplevel):

    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавити дохід/витрати')
        self.geometry('600x420+400+300')
        self.resizable(False, False)

        self.place_label_description()
        self.place_label_select()
        self.place_label_sum()

        self.create_btn_cancel()
        self.create_btn_ok()

        self.grab_set()
        self.focus_set()

    def place_label_description(self):
        (ttk.Label(self, text='Назва:')).place(x=50, y=50)
        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

    def place_label_select(self):
        (ttk.Label(self, text='Доходи/Витрати:')).place(x=50, y=80)
        self.combobox = ttk.Combobox(self, values=['Дохід', 'Витрати'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

    def place_label_sum(self):
        (ttk.Label(self, text='Сума:')).place(x=50, y=110)
        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)

    def create_btn_cancel(self):
        ttk.Button(self, text='Закрити', command=self.destroy).place(x=300, y=170)

    def create_btn_ok(self):
        self.btn_ok = ttk.Button(self, text='Добавити')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>',
                         lambda event:
                         self.view.repository.add_records(
                             self.entry_description.get(),
                             self.entry_money.get(),
                             self.combobox.get())
                         )


class UpdateFrame(ChildFrame):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title('Редагувати')
        self.create_btn_edit()
        self.btn_ok.destroy()

    def create_btn_edit(self):
        btn_edit = ttk.Button(self, text='Редагувати')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>',
                      lambda event:
                      self.view.repository.update_record(
                          self.entry_description.get(),
                          self.combobox.get(),
                          self.entry_money.get())
                      )


if __name__ == '__main__':
    ID = 'ID'
    TOTAL = 'Total'
    COSTS = 'Costs'
    DESCRIPTION = 'Description'

    root = tk.Tk()
    tree_view = ttk.Treeview(column=(ID, DESCRIPTION, COSTS, TOTAL), height=15, show='headings')
    db = SQLiteDB()
    repository = DBRepository(db, tree_view)

    app = MainFrame()
    app.pack()

    root.title('Household finance')
    root.geometry('850x650+300+200')
    root.resizable(False, False)
    root.mainloop()
