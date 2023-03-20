import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database_folder.database import Query


class App(Query):

    def __init__(self):
        super().__init__()
        self.root = ttk.Window(themename="cyborg")
        self.root.title("PORTARIA [BANCO DE DADOS]")
        self.error_label = None
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
        self.treeview_data.column('#3', width=70, anchor='center')
        self.treeview_data.column('#4', width=70, anchor='center')
        self.treeview_data.column('#5', width=140, anchor='center')
        self.treeview_data.column('#6', width=270, anchor='center')
        self.treeview_data.column('#7', width=15, anchor='center')

        self.treeview_data.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.97)
        self.treeview_data.tag_configure('oddrow', background='gray20')
        self.treeview_data.tag_configure('evenrow', background='gray10')

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

    def data_list_select(self, query, event=None):
        self.treeview_data.delete(*self.treeview_data.get_children())
        self.connect_db()
        self.cursor.execute(f'{query} ORDER BY Data DESC')

        query_results_list = self.cursor.fetchall()
        self.remove_error_label()

        if query_results_list:
            for i, data in enumerate(query_results_list):
                if i % 2 == 0:
                    self.treeview_data.insert(
                        '', ttk.END, values=(data[0], data[1], data[2], data[3], data[4],
                                             data[5], data[6]), iid=i, tag=('evenrow',))
                else:
                    self.treeview_data.insert(
                        '', ttk.END, values=(data[0], data[1], data[2], data[3], data[4],
                                             data[5], data[6]), iid=i, tag=('oddrow',))
        else:
            self.no_answer(self.query_entry.get())

        self.query_entry.delete(0, ttk.END)
        self.disconnect_db()

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












