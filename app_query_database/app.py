import ttkbootstrap as ttk
import pandas as pd
import sqlite3
from pathlib import Path
from ttkbootstrap.constants import *


class App:
    def __init__(self):
        self.root = ttk.Window(themename="cyborg")
        self.root.title("PORTARIA [BANCO DE DADOS]")
        self.label = None
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
        self.query_entry_frame = ttk.Frame(master=self.root, bootstyle="cyborg")

        self.query_entry_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.15)

        self.treeview_frame = ttk.Frame(master=self.root, bootstyle="cyborg")
        self.treeview_frame.place(relx=0.02, rely=0.2, relwidth=0.96, relheight=0.78)

    def treeview(self):
        treeview = ttk.Treeview(master=self.treeview_frame, columns=[1, 2, 3, 4, 5, 6, 7], show='headings',
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

        self.database_data_list.tag_configure('oddrow', background='gray20')
        self.database_data_list.tag_configure('evenrow', background='gray10')

        frame_new_window_scrollbar = ttk.Scrollbar(self.treeview_frame, bootstyle=DARK)

        frame_new_window_scrollbar.place(relx=0.98, rely=0.01, relwidth=0.017, relheight=0.98)

        self.database_data_list.configure(yscrollcommand=frame_new_window_scrollbar.set)

    def widgets(self):
        self.query_entry = ttk.Entry(master=self.query_entry_frame,
                                     width=120, )
        self.query_entry.place(relx=0.5, rely=0.4, relwidth=0.33, anchor=CENTER)
        self.query_entry.bind('<Return>', self.read_data)
        self.insert()

        self.style = ttk.Style()
        self.style.configure('dark.TButton', font=('Arial', 10),
                             width=10, foreground='gray50', hover='black20')

        self.how_button = ttk.Button(master=self.query_entry_frame,
                                     text='Como buscar', style='dark.TButton', command=self.showing_info)
        self.how_button.place(relx=0.336, rely=0.65)

    def showing_info(self):
        if self.how_button:
            texto = """        Use ' / ' para mais de um item: 
        Ex.: modelo/cor/casa   ⇾  gol/prata/7

        Com nome da pessoa use ' [ ' antes do nome:
        Ex.: [motorista/modelo/casa   ⇾   [ana/uno/47"""
            self.info = ttk.Label(master=self.query_entry_frame, text=texto, font=("Helvetica", 12),
                                  foreground='white', bootstyle="cyborg", anchor=NW)
            self.info.place(relx=0, rely=0, relwidth=0.31, relheight=1)
            self.how_button.configure(text="Ocultar", command=self.hiding_info)

    def hiding_info(self):
        if self.how_button:
            self.info.destroy()
            self.how_button.configure(text="Como buscar", command=self.showing_info)

    def remove(self, event=None):
        self.query_entry.delete(0, END)
        self.query_entry.configure(foreground='white')

    def insert(self, event=None):
        self.query_entry.insert(0, 'Busque')
        self.query_entry.configure(foreground='gray30')

    def connect_db(self):
        way = Path.cwd()
        df = pd.read_csv(way / 'portaria_bd.csv')

        self.conn = sqlite3.connect('banco_de_dados.db')
        self.cursor = self.conn.cursor()
        df.to_sql('portaria_bd', self.conn, if_exists='replace', index=False)

    def disconnect_db(self):
        self.conn.close()

    def select_list(self):

        self.database_data_list.delete(*self.database_data_list.get_children())
        self.connect_db()
        data_list = self.cursor.execute(""" SELECT Placa, Cor, Modelo, Marca, Motorista, Proprietário, Casa 
                                            FROM portaria_bd ORDER BY Data DESC; """)

        for i, data in enumerate(data_list):
            if i % 2 == 0:
                self.database_data_list.insert(
                    '', ttk.END, values=(data[0], data[1], data[2], data[3], data[4],
                                         data[5], data[6]), iid=i, tag=('evenrow',))
            else:
                self.database_data_list.insert(
                    '', ttk.END, values=(data[0], data[1], data[2], data[3], data[4],
                                         data[5], data[6]), iid=i, tag=('oddrow',))

        self.disconnect_db()

    def person(self, valor):
        if '[' in valor:
            self.pessoa = valor
            gente = valor.replace('[', '')
            self.pesquisa += f"(Motorista LIKE '%{gente}%' OR Proprietário LIKE '%{gente}%') AND "

    def vehicle_color(self, valor):
        cores = ['Preto', 'Prata', 'Vermelho', 'Verm', 'Branco', 'Cinza', 'Verde', 'Azul', 'Vinho', 'Amarelo',
                 'Marrom', 'Laranja', 'Beje', 'Bege', 'Rosa', 'Dourado', 'Roxo']
        if not valor.isnumeric():
            for cor in cores:
                if valor[:-1] == cor[:-1].lower():
                    self.pesquisa += f"Cor LIKE '%{valor[:-1]}%' AND "
                    self.cor = valor
                    break

    def normal_query(self, valor):
        if valor.isnumeric() and len(valor) <= 2 and 0 < int(valor) <= 49:
            self.cursor.execute(f"""
            SELECT Placa, Cor, Modelo, Marca, Motorista, Proprietário, Casa
            FROM portaria_bd WHERE Casa LIKE '{valor}' 
            ORDER BY Motorista """)
        else:
            self.cursor.execute(f"""
                SELECT Placa, Cor, Modelo, Marca, Motorista, Proprietário, Casa FROM portaria_bd
                WHERE 
                     Placa LIKE '%{valor}%' OR Cor LIKE '%{valor}%' OR Modelo LIKE '%{valor}%' OR
                     Marca LIKE '%{valor}%' OR Motorista LIKE '%{valor}%' OR Proprietário LIKE '%{valor}%'                
                ORDER BY Data DESC; """)

    def multiple_items(self, lista):
        for i in lista:
            if i.isnumeric() and len(i) <= 2 and 0 < int(i) <= 49:
                self.pesquisa += f"Casa LIKE '{i}' AND "
                lista.remove(i)
                break
        if len(lista) == 2:
            self.modelo, self.marca = lista[0], lista[1]
            self.pesquisa += f"((Modelo LIKE '%{self.modelo}%' OR  Marca LIKE '%{self.marca}%') OR " \
                             f"(Marca LIKE '%{self.modelo}%' OR  Modelo LIKE '%{self.marca}%')) AND "
        elif len(lista) == 1:
            self.pesquisa += f"(Modelo LIKE '%{lista[0]}%' OR  Marca LIKE '%{lista[0]}%') AND "

    def read_data(self, event=None):
        self.connect_db()
        self.database_data_list.delete(*self.database_data_list.get_children())
        query = self.query_entry.get()
        self.cor = self.pessoa = self.modelo = self.marca = self.casa = None

        if '/' in query:
            values = query.split('/')
            values = list(map(lambda x: x.lower(), values))

            self.pesquisa = """ SELECT Placa, Cor, Modelo, Marca, Motorista, Proprietário, Casa 
                                FROM portaria_bd WHERE """

            for valor in values:
                self.person(valor)
                self.vehicle_color(valor)
            if self.pessoa:
                values.remove(self.pessoa)
            if self.cor:
                values.remove(self.cor)
            if values:
                self.multiple_items(values)

            pesquisa = self.pesquisa[:-4]
            self.cursor.execute(f'{pesquisa} ORDER BY Data DESC')
        else:
            self.normal_query(query)

        searched_data = self.cursor.fetchall()
        if self.label: self.label.destroy()

        if searched_data:
            for i, v in enumerate(searched_data):
                if i % 2 == 0:
                    self.database_data_list.insert('', ttk.END, values=v, tag=('evenrow',))
                else:
                    self.database_data_list.insert('', ttk.END, values=v, tag=('oddrow',))

        else:
            self.label = ttk.Label(master=self.treeview_frame, bootstyle="inverse", padding=5,
                                   anchor=CENTER, text=f'Sem resultados para: {query}')
            self.label.place(relx=0.5, rely=0.2, relwidth=0.4, anchor=CENTER)

        self.disconnect_db()
        self.query_entry.delete(0, ttk.END)


if __name__ == "__main__":
    app = App()
