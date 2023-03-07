import ttkbootstrap as ttk
import pandas as pd
import sqlite3
from pathlib import Path
from ttkbootstrap.constants import *


class App:
    def __init__(self):
        self.root = ttk.Window(themename="cyborg")
        self.root.title("PORTARIA [BANCO DE DADOS]")
        self.center()
        self.frame()
        self.widgets()
        self.treeview()
        self.select_list()
        self.query_entry.bind('<FocusOut>', self.insert)
        self.query_entry.bind('<FocusIn>', self.remove)
        self.root.mainloop()

    def center(self):

        APP_WIDTH = 950
        APP_HEIGHT = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        app_center_coordinate_x = (screen_width / 2) - (APP_WIDTH / 2)
        app_center_coordinate_y = (screen_height / 2) - (APP_HEIGHT / 2)

        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{int(app_center_coordinate_x)}+{int(app_center_coordinate_y)}")

    def frame(self):
        self.frame_query_button = ttk.Frame(master=self.root, bootstyle="cyborg")

        self.frame_query_button.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.15)

        self.frame_new_window = ttk.Frame(master=self.root, bootstyle="cyborg")
        self.frame_new_window.place(relx=0.02, rely=0.2, relwidth=0.96, relheight=0.78)

    def treeview(self):
        treeview = ttk.Treeview(master=self.frame_new_window, columns=[1, 2, 3, 4, 5, 6, 7], show='headings',
                                style='cyborg.Treeview')
        style = ttk.Style()
        style.map(
            'Treeview',
            background=[('selected', 'white')],
            foreground=[('selected', 'black')],
        )
        self.database_data_list = treeview
        self.database_data_list.heading('#1', text='Placa')
        self.database_data_list.heading('#2', text='Cor')
        self.database_data_list.heading('#3', text='Modelo')
        self.database_data_list.heading('#4', text='Marca')
        self.database_data_list.heading('#5', text='Motorista')
        self.database_data_list.heading('#6', text='Proprietário')
        self.database_data_list.heading('#7', text='Casa')

        self.database_data_list.column('#1', width=50, anchor='center')
        self.database_data_list.column('#2', width=40, anchor='center')
        self.database_data_list.column('#3', width=70, anchor='center')
        self.database_data_list.column('#4', width=70, anchor='center')
        self.database_data_list.column('#5', width=140, anchor='center')
        self.database_data_list.column('#6', width=270, anchor='center')
        self.database_data_list.column('#7', width=15, anchor='center')

        self.database_data_list.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.97)

        # lines color without selecting them
        self.database_data_list.tag_configure('oddrow', background='gray20')
        self.database_data_list.tag_configure('evenrow', background='gray10')

        self.database_data_list.bind("<Double-1>")

        # create CTk scrollbar
        frame_new_window_scrollbar = ttk.Scrollbar(self.frame_new_window, bootstyle=DARK)

        frame_new_window_scrollbar.place(relx=0.98, rely=0.01, relwidth=0.017, relheight=0.98)

        self.database_data_list.configure(yscrollcommand=frame_new_window_scrollbar.set)

    def widgets(self):
        self.button_query = ttk.Button(master=self.frame_query_button,
                                       text="Buscar", command=self.buscar_button, bootstyle=DARK)
        self.button_query.place(relx=0.32, rely=0.5, relwidth=0.2, anchor=CENTER)

        self.query_entry = ttk.Entry(master=self.frame_query_button,
                                     width=120)
        self.query_entry.place(relx=0.62, rely=0.5, relwidth=0.33, anchor=CENTER)
        self.query_entry.bind('<Return>', self.buscar_button)
        self.insert()
        self.label = ttk.Label()

    def remove(self, event=None):
        self.query_entry.delete(0, END)
        self.query_entry.configure(foreground='white')

    def insert(self, event=None):
        self.query_entry.insert(0, 'Ex.: joao silva ou gol/prata/[joao/7')
        self.query_entry.configure(foreground='gray30')

    def buscar_button(self, event=None):
        self.read_data()
        if self.button_query:
            self.button_query.configure(text='Voltar')
            self.button_query.configure(bootstyle=[SECONDARY, OUTLINE])
            self.button_query.configure(command=self.voltar_button)

    def voltar_button(self):
        self.select_list()
        if self.button_query:
            self.button_query.configure(text='Buscar')
            self.button_query.configure(bootstyle=DARK)
            self.button_query.configure(command=self.buscar_button)

    def connect_db(self):
        way = Path.cwd()
        df = pd.read_csv(way / 'portaria_bd.csv')

        self.conn = sqlite3.connect('banco_de_dados.db')
        self.cursor = self.conn.cursor()
        df.to_sql('portaria_bd', self.conn, if_exists='replace', index=False)

        print('Connecting to the database.')

    def disconnect_db(self):
        self.conn.close()
        print('Disconnecting to the database.')

    def select_list(self):

        self.database_data_list.delete(*self.database_data_list.get_children())
        self.connect_db()
        data_list = self.cursor.execute(""" SELECT * FROM portaria_bd ORDER BY rowid LIMIT 200; """)

        count = 0
        for data in data_list:
            if count % 2 == 0:
                self.database_data_list.insert(
                    '', ttk.END, values=(data[0], data[1], data[2], data[3], data[4],
                                         data[5], data[6]), iid=count, tag=('evenrow',))
            else:
                self.database_data_list.insert(
                    '', ttk.END, values=(data[0], data[1], data[2], data[3], data[4],
                                         data[5], data[6]), iid=count, tag=('oddrow',))
            count += 1

        self.disconnect_db()

    def read_data(self):
        self.connect_db()
        self.database_data_list.delete(*self.database_data_list.get_children())
        query = self.query_entry.get()
        cor = modelo = marca = casa = pessoa = None

        if '/' in query:
            cores = ['Azul', 'Vinho', 'Vermelho', 'Verm', 'Preto', 'Prata', 'Cinza', 'Verde', 'Branco', 'Beje', 'Marrom',
                     'Amarelo', 'Laranja', 'Bege', 'Rosa', 'Dourado', 'Roxo']
            cores = list(map(lambda x: x.lower(), cores))

            values = query.split('/')
            values = list(map(lambda x: x.lower(), values))

            print(values)
            pesquisa = "SELECT * FROM portaria_bd WHERE "

            for valor in values:
                if '[' in valor:
                    pessoa = valor
                    gente = pessoa.replace('[', '')
                    pesquisa += f"(Motorista LIKE '%{gente}%' OR Proprietário LIKE '%{gente}%') AND "

                if not valor.isnumeric():
                    for cour in cores:
                        if valor[:-1] == cour[:-1]:
                            pesquisa += f"Cor LIKE '%{valor[:-1]}%' AND "
                            cor = valor
                            break

            if pessoa: values.remove(pessoa)
            if cor: values.remove(cor)

            if values:
                for i in values:
                    if i.isnumeric() and len(i) <= 2 and 0 < int(i) <= 49:
                        pesquisa += f"Casa LIKE '{i}' AND "
                        print(i)
                        values.remove(i)
                        break
                if len(values) == 2:
                    marca = values[1]
                    modelo = values[0]
                    pesquisa += f"((Modelo LIKE '%{modelo}%' OR  Marca LIKE '%{marca}%') OR " \
                                f"(Marca LIKE '%{modelo}%' OR  Modelo LIKE '%{marca}%')) AND "
                elif len(values) == 1:
                    pesquisa += f"(Modelo LIKE '%{values[0]}%' OR  Marca LIKE '%{values[0]}%') AND "

            print(pesquisa)
            pesquisa = pesquisa[:-4]
            self.cursor.execute(pesquisa)
        else:
            if query.isnumeric() and len(query) <= 2 and 0 < int(query) <= 49:
                self.cursor.execute(f"""
                SELECT *
                FROM portaria_bd
                WHERE Casa LIKE '%{query}%'""")
            else:
                self.cursor.execute(f"""
                    SELECT *, rowid
                    FROM portaria_bd
                    WHERE 
                         Placa LIKE '%{query}%' OR 
                         Cor LIKE '%{query}%' OR
                         Modelo LIKE '%{query}%' OR
                         Marca LIKE '%{query}%' OR
                         Motorista LIKE '%{query}%' OR
                         Proprietário LIKE '%{query}%'                
                    ORDER BY rowid; """)

        searched_data = self.cursor.fetchall()

        if searched_data:
            if self.label:
                self.label.destroy()
            count = 0
            for i in searched_data:
                if count % 2 == 0:
                    self.database_data_list.insert('', ttk.END, values=i, tag=('evenrow',))
                else:
                    self.database_data_list.insert('', ttk.END, values=i, tag=('oddrow',))
                count += 1
        else:
            self.label = ttk.Label(master=self.frame_new_window, bootstyle="inverse", padding=5, anchor=CENTER,
                                    text=f'Sem resultados para: {query}')
            self.label.place(relx=0.5, rely=0.2, relwidth=0.4, anchor=CENTER)

            print(f'Sem resultados para: {query}')

        self.disconnect_db()
        self.query_entry.delete(0, ttk.END)


if __name__ == "__main__":
    app = App()
