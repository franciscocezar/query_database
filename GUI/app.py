import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database_folder import Query


class App(Query):

    def __init__(self):
        super().__init__()
        self.root = ttk.Window(themename="cyborg")
        self.root.title("PORTARIA [BANCO DE DADOS]")
        self.error_label = None
        self.controle = False
        self.button_voltar = None
        self.prop = ['None', 'ANDREW G. MACDONALD  ( Aratoca )',
                     'DOMINIQUE WORMS  ( 110 Degraus )',
                     'ELIZABETH M. de OLIVEIRA  ( Auguri )',
                     'MARALICE + JOEL  ( Xilos )', 'JORGE LUIZ CONTI  ( Stock Yard )',
                     'MARCIO MURAD  ( Vila Caajara )', 'HENRIQUE DEGEN  ( Vila Lobos )',
                     'SILVIA BARRETO ( Rancho Tranquilo )',
                     'Marcio Botrel / Nancy Botrel  ( Caty )',
                     'IMOB. DELFINA  ( V. Fernando Monteiro )',
                     'I. MACKENZIE  (  COLONIA )', 'I. MACKENZIE  ( ORIPABA )',
                     'I. MACKENZIE  ( Erasmo Braga )', 'I. MACKENZIE  ( Acampamento )',
                     'ABILIO BENEDITO DE FREITAS  ( Aruã )',
                     'Prof. J. R. Moura ( Sans Souci )',
                     'JOSÉ ROBERTO T. PINTO ( Xodó/Tari )',
                     'JOAQUIM BAUCH  ( Recanto da Natureza )',
                     'RENATO e KAREN  ( Recanto dos Alpes )',
                     'MARIA HELENA SCHERB  ( Rancho Pôr-do-Sol )',
                     'Tatiana Vieira ( Casa Ypê )',
                     'SYLVIA M. CRIVELLI ( Hermitage/Tangará )',
                     'LAURESTO C. ESHER  ( Esher )',
                     'PROF. MARCEL MENDES  ( Four Seasons )',
                     'KARIN  BAUMERGGER  ( Chalé da Floresta )',
                     'EVELYN GANSL  ( Clair Soleil )', 'THEODOR  SCHUEPP  ( Manacá )',
                     'VICTORYA W. KIMBALL  ( Green Crest )',
                     'WILLIAM CONCEIÇÃO HERING  ( Tabapoan )', 'ERNESTO COPPO RAUTER',
                     'LUIZ RICARDO GIFFONI', 'FERNANDO GUSTAVO L. de FRANÇA ( Nanuk )',
                     'Jose Augusto Acciaris Junior', 'Celso  e Tanya Jatene',
                     'Wagner Mariano', 'MARIANA TEIXEIRA', 'Wagner Mariano Carlos',
                     'Danilo e Daniela', 'Wagner Mariano Carlos', 'Walter Hipólito',
                     'Julio Cesar Acciares', 'Assoc', 'Igreja Metodista',
                     'Ralph de Carvalho', 'D. Sônia', 'Elias Nochese Skaf',
                     'Laercio Aparecido da Silva', 'Silvia Fuchs',
                     'Pedro Paulo Kimashi', 'João Leandro Garcia',
                     'Murilo Guerra de Oliveira', 'Mario Pirondi e Walemar Pirondi',
                     'Rene Claudio Gansl', 'Camilo Aschar Junior', 'Sr Evelina']
        self.center()
        self.frames()
        self.widgets()
        self.treeview()
        self.data_list_select(self.standard_query)
        self.query_entry.bind('<FocusOut>', self.insert_placeholder)
        self.query_entry.bind('<FocusIn>', self.remove_placeholder)
        self.insert_placeholder()
        self.root.mainloop()

    def center(self):
        APP_WIDTH = 950
        APP_HEIGHT = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        app_center_coordinate_x = (screen_width / 2) - (APP_WIDTH / 2)
        app_center_coordinate_y = (screen_height / 2) - (APP_HEIGHT / 2)

        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{int(app_center_coordinate_x)}+{int(app_center_coordinate_y)}")

    def frames(self):
        self.query_entry_frame = ttk.Frame(master=self.root, bootstyle="cyborg")
        self.query_entry_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.15)

        self.treeview_frame = ttk.Frame(master=self.root, bootstyle="cyborg")
        self.treeview_frame.place(relx=0.02, rely=0.2, relwidth=0.96, relheight=0.78)

    def treeview(self):
        treeview = ttk.Treeview(master=self.treeview_frame, columns=[1, 2, 3, 4, 5, 6, 7],
                                show='headings', style='cyborg.Treeview')
        style = ttk.Style()
        style.map('Treeview', background=[('selected', 'white')], foreground=[('selected', 'black')], )

        self.treeview_data = treeview
        self.treeview_data.heading('#1', text='Placa')
        self.treeview_data.heading('#2', text='Cor')
        self.treeview_data.heading('#3', text='Modelo')
        self.treeview_data.heading('#4', text='Marca')
        self.treeview_data.heading('#5', text='Motorista')
        self.treeview_data.heading('#6', text='Proprietário')
        self.treeview_data.heading('#7', text='Casa')

        self.treeview_data.column('#1', width=50, anchor='center')
        self.treeview_data.column('#2', width=40, anchor='center')
        self.treeview_data.column('#3', width=140, anchor='center')
        self.treeview_data.column('#4', width=70, anchor='center')
        self.treeview_data.column('#5', width=130, anchor='center')
        self.treeview_data.column('#6', width=170, anchor='center')
        self.treeview_data.column('#7', width=15, anchor='center')

        self.treeview_data.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.97)
        self.treeview_data.tag_configure('oddrow', background='gray20')
        self.treeview_data.tag_configure('evenrow', background='gray10')

        self.treeview_data.bind("<Double-1>", self.OnDoubleClick)

        scrollbar = ttk.Scrollbar(self.treeview_frame, bootstyle=DARK)
        scrollbar.place(relx=0.98, rely=0.01, relwidth=0.017, relheight=0.98)
        self.treeview_data.configure(yscrollcommand=scrollbar.set)

    def widgets(self):
        self.query_entry = ttk.Entry(master=self.query_entry_frame, width=120)
        self.query_entry.place(relx=0.5, rely=0.4, relwidth=0.33, anchor=CENTER)
        self.query_entry.bind('<Return>',
                              lambda x: self.data_list_select(self.read_data(
                                  self.query_entry.get())) if self.query_entry.get() else self.data_list_select(
                                  self.standard_query))

        style = ttk.Style()
        style.configure('dark.TButton', font=('Arial', 10), width=10, foreground='gray50', hover='black20')

        self.info_button = ttk.Button(master=self.query_entry_frame, text='Como buscar',
                                      style='dark.TButton', command=self.show_info)
        self.info_button.place(relx=0.336, rely=0.65)

        self.data_create_button = ttk.Button(master=self.query_entry_frame, text='Cadastrar',
                                             style='dark.TButton', command=self.reconfigure_frame)
        self.data_create_button.place(relx=0.575, rely=0.65)

    def data_list_select(self, query, event=None):
        self.treeview_data.delete(*self.treeview_data.get_children())
        self.connect_db()
        self.cursor.execute(f"{query}")

        query_results_list = self.cursor.fetchall()
        self.remove_error_label()

        if query_results_list:
            for i, data in enumerate(query_results_list):
                if i % 2 == 0:
                    self.treeview_data.insert(
                        '', ttk.END, values=(data[1], data[2], data[3], data[4],
                                             data[5], data[6], data[7], data[0]), iid=i, tag=('evenrow',))
                else:
                    self.treeview_data.insert(
                        '', ttk.END, values=(data[1], data[2], data[3], data[4],
                                             data[5], data[6], data[7], data[0]), iid=i, tag=('oddrow',))
        else:
            self.no_answer(self.query_entry.get())

        self.query_entry.delete(0, ttk.END)
        self.disconnect_db()

    def OnDoubleClick(self, event):
        # self.reconfigure_frame()
        # Função Duplo Clique na lista mostrada na tela.
        self.reconfigure_frame()

        # Seleciona o item clicado e os insere de volta nos campos Entry.
        for n in self.treeview_data.selection():
            # Desempacota a lista.
            col1, col2, col3, col4, col5, col6, col7, col0 = self.treeview_data.item(n, 'values')
            # Insere cada item em sua respectiva variável entry.
            self.plate_entry.insert(END, col1)
            self.cor_entry.insert(END, col2)
            self.marca_entry.insert(END, col4)
            self.motorista_entry.insert(END, col5)
            self.casa_entry.insert(END, col7)
            self.id_entry.insert(END, col0)

    def remove_error_label(self):
        if self.error_label:
            self.error_label.destroy()

    def show_info(self):
        if self.info_button:
            info_text = """        Use ' / ' para mais de um item: 
        Ex.: modelo/cor/casa   ⇾  gol/prata/7

        Com nome da pessoa use ' [ ' antes do nome:
        Ex.: [motorista/modelo/casa   ⇾   [ana/uno/47"""
            self.info = ttk.Label(master=self.query_entry_frame, text=info_text, font=("Helvetica", 12),
                                  foreground='white', bootstyle="cyborg", anchor=NW)
            self.info.place(relx=0, rely=0, relwidth=0.31, relheight=1)
            self.info_button.configure(text="Ocultar", command=self.hide_info)

    def hide_info(self):
        if self.info_button:
            self.info.destroy()
            self.info_button.configure(text="Como buscar", command=self.show_info)

    def remove_placeholder(self, event=None):
        self.query_entry.delete(0, END)
        self.query_entry.configure(foreground='white')

    def insert_placeholder(self, event=None):
        self.query_entry.insert(0, 'Busque')
        self.query_entry.configure(foreground='gray30')

    def no_answer(self, query):
        self.error_label = ttk.Label(master=self.treeview_frame, padding=5, anchor=CENTER,
                                     text=f'Sem resultados para: {query}', bootstyle=INVERSE)
        self.error_label.place(relx=0.5, rely=0.2, relwidth=0.4, anchor=CENTER)

    def widgets2(self):
        # Placa cor modelo marca motorista proprietário casa
        self.id_entry = ttk.Entry(master=self.query_entry_frame, width=120)

        self.plate_label = ttk.Label(master=self.query_entry_frame, text="Placa")
        self.plate_label.place(relx=0.03, rely=0.0)
        self.plate_entry = ttk.Entry(master=self.query_entry_frame, width=120)
        self.plate_entry.place(relx=0.13, rely=0.45, relwidth=0.2, anchor=ttk.CENTER)

        self.cor_label = ttk.Label(master=self.query_entry_frame, text="Cor")
        self.cor_label.place(relx=0.24, rely=0.0)
        self.cor_entry = ttk.Entry(master=self.query_entry_frame, width=120)
        self.cor_entry.place(relx=0.34, rely=0.45, relwidth=0.2, anchor=ttk.CENTER)

        self.marca_label = ttk.Label(master=self.query_entry_frame, text="Marca")
        self.marca_label.place(relx=0.45, rely=0.0)
        self.marca_entry = ttk.Entry(master=self.query_entry_frame, width=120)
        self.marca_entry.place(relx=0.55, rely=0.45, relwidth=0.2, anchor=ttk.CENTER)

        self.motorista_label = ttk.Label(master=self.query_entry_frame, text="Motorista")
        self.motorista_label.place(relx=0.66, rely=0)
        self.motorista_entry = ttk.Entry(master=self.query_entry_frame, width=120)
        self.motorista_entry.place(relx=0.76, rely=0.45, relwidth=0.2, anchor=ttk.CENTER)

        self.casa_label = ttk.Label(master=self.query_entry_frame, text="Casa")
        self.casa_label.place(relx=0.874, rely=0)
        self.casa_entry = ttk.Entry(master=self.query_entry_frame, width=120)
        self.casa_entry.place(relx=0.9, rely=0.45, relwidth=0.05, anchor=ttk.CENTER)

        self.button_query = ttk.Button(master=self.query_entry_frame, text="Novo",
                                       style='dark.TButton', command=self.create_data)
        self.button_query.place(relx=0.34, rely=0.68)

        self.button_alter = ttk.Button(master=self.query_entry_frame, text="Editar",
                                       style='dark.TButton', command=self.update_data)
        self.button_alter.place(relx=0.45, rely=0.68)

        self.button_voltar = ttk.Button(master=self.query_entry_frame, text="Voltar",
                                        style='dark.TButton',
                                        command=lambda: (self.cleans_entries(), self.reconfigure_frame()))
        self.button_voltar.place(relx=0.55, rely=0.68)

    def create_data(self):
        motorista = self.motorista_entry.get().title()
        plate = self.plate_entry.get().upper()
        casa = int(self.casa_entry.get())
        cor = self.cor_entry.get().title()
        marca = self.marca_entry.get().title()

        self.connect_db()

        self.cursor.execute(
            """INSERT INTO portaria_banco (Placa, Cor, Modelo, Marca, Motorista, Proprietário, Casa) 
               VALUES (?, ?, '-', ?, ?, ?, ?)""", (plate, cor, marca, motorista, self.prop[casa], casa)
        )
        self.conn.commit()
        self.disconnect_db()
        self.cleans_entries()
        self.select_list()
        self.reconfigure_frame()

    def update_data(self):
        motorista = self.motorista_entry.get().title()
        plate = self.plate_entry.get().upper()
        casa = int(self.casa_entry.get())
        cor = self.cor_entry.get().title()
        marca = self.marca_entry.get().title()
        iid = self.id_entry.get()
        print(iid)

        self.connect_db()
        self.cursor.execute("""
                        UPDATE portaria_banco
                        SET Placa = ?, Cor = ?, Marca = ?, Motorista = ?, Proprietário = ?, casa = ?
                        WHERE id = ? """, (plate, cor, marca, motorista, self.prop[casa], casa, iid))

        self.conn.commit()
        self.disconnect_db()
        self.cleans_entries()
        self.select_list()
        self.reconfigure_frame()

    def cleans_entries(self):

        self.motorista_entry.delete(0, END)
        self.plate_entry.delete(0, END)
        self.casa_entry.delete(0, END)
        self.cor_entry.delete(0, END)
        self.marca_entry.delete(0, END)
        self.id_entry.delete(0, END)
        self.controle = True

    def reconfigure_frame(self):
        for widgets in self.query_entry_frame.winfo_children():
            widgets.destroy()

        if self.controle:
            self.widgets()
            self.controle = False
            self.insert_placeholder()
            self.query_entry.bind('<FocusOut>', self.insert_placeholder)
            self.query_entry.bind('<FocusIn>', self.remove_placeholder)
        else:
            self.widgets2()
            self.controle = True

    def select_list(self):
        # Shows database data on the screen.

        # Deletes all the data shown on the screen to update the list.
        self.treeview_data.delete(*self.treeview_data.get_children())

        # Connect to database and gets data
        self.connect_db()
        data_list = self.cursor.execute(
            """ SELECT *
                FROM portaria_banco; """
        )

        # Gets selected data and shows it on the screen

        for i, data in enumerate(data_list):
            if i % 2 == 0:
                self.treeview_data.insert(
                    '', END, values=(data[1], data[2], data[3], data[4],
                                     data[5], data[6], data[7], data[0]), iid=i, tag=('evenrow',)
                )
            else:
                self.treeview_data.insert(
                    '', END, values=(data[1], data[2], data[3], data[4],
                                     data[5], data[6], data[7], data[0]), iid=i, tag=('oddrow',)
                )

        self.disconnect_db()
