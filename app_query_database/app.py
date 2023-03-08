import ttkbootstrap as ttk
import pandas as pd
import sqlite3
from pathlib import Path
from ttkbootstrap.constants import *

#  https://drive.google.com/file/d/1zZRnni6zPnHbTkcUNbh-mhxktnEuv0dy/view?usp=share_link
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
        self.label = ttk.Label()
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

        print('Connecting to the database.')

    def disconnect_db(self):
        self.conn.close()
        print('Disconnecting to the database.')

    def select_list(self):

        self.database_data_list.delete(*self.database_data_list.get_children())
        self.connect_db()
        data_list = self.cursor.execute(""" SELECT Placa, Cor, Modelo, Marca, Motorista, Proprietário, Casa 
                                            FROM portaria_bd ORDER BY Data DESC; """)

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

    def read_data(self, event=None):
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

            pesquisa = """ SELECT Placa, Cor, Modelo, Marca, Motorista, Proprietário, Casa 
                           FROM portaria_bd WHERE """

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
            self.cursor.execute(f'{pesquisa} ORDER BY Data DESC')
        else:
            if query.isnumeric() and len(query) <= 2 and 0 < int(query) <= 49:
                self.cursor.execute(f"""
                SELECT Placa, Cor, Modelo, Marca, Motorista, Proprietário, Casa, COUNT(*) as total 
                FROM portaria_bd
                WHERE Casa LIKE '{query}' 
                GROUP BY Motorista
                ORDER BY total ASC """)
            else:
                self.cursor.execute(f"""
                    SELECT Placa, Cor, Modelo, Marca, Motorista, Proprietário, Casa 
                    FROM portaria_bd
                    WHERE 
                         Placa LIKE '%{query}%' OR 
                         Cor LIKE '%{query}%' OR
                         Modelo LIKE '%{query}%' OR
                         Marca LIKE '%{query}%' OR
                         Motorista LIKE '%{query}%' OR
                         Proprietário LIKE '%{query}%'                
                    ORDER BY Data DESC; """)

        searched_data = self.cursor.fetchall()

        if searched_data:
            if self.label.cget("text"):
                self.label.destroy()
            count = 0
            for i in searched_data:
                if count % 2 == 0:
                    self.database_data_list.insert('', ttk.END, values=i, tag=('evenrow',))
                else:
                    self.database_data_list.insert('', ttk.END, values=i, tag=('oddrow',))
                count += 1
        else:
            self.label = ttk.Label(master=self.treeview_frame, bootstyle="inverse", padding=5, anchor=CENTER,
                                   text=f'Sem resultados para: {query}')
            self.label.place(relx=0.5, rely=0.2, relwidth=0.4, anchor=CENTER)

            print(f'Sem resultados para: {query}')

        self.disconnect_db()
        self.query_entry.delete(0, ttk.END)


if __name__ == "__main__":
    app = App()
