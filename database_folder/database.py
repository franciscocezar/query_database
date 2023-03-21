import pandas as pd
import sqlite3
from pathlib import Path


class ConnectionDB:

    def connect_db(self):
        way = Path.cwd()
        df = pd.read_csv(way / 'app_query_database/portaria_bd.csv')

        self.conn = sqlite3.connect('banco_de_dados.db')
        self.cursor = self.conn.cursor()
        df.to_sql('portaria_bd', self.conn, if_exists='replace', index=False)

    def disconnect_db(self):
        self.conn.close()


class Query(ConnectionDB):

    def __init__(self):
        self.standard_query = """ SELECT Placa, Cor, Modelo, Marca, Motorista, Proprietário, Casa 
                                   FROM portaria_bd """

    def __driver_or_owner_select(self, valor):
        if '[' in valor:
            self.pessoa = valor
            gente = valor.replace('[', '')
            self.pesquisa += f"(Motorista LIKE '%{gente}%' OR Proprietário LIKE '%{gente}%') AND "

    def __vehicle_color_select(self, valor):
        cores = ['Preto', 'Prata', 'Vermelho', 'Verm',
                 'Branco', 'Cinza', 'Verde', 'Azul',
                 'Vinho', 'Amarelo', 'Marrom', 'Laranja',
                 'Beje', 'Bege', 'Rosa', 'Dourado', 'Roxo']

        if not valor.isnumeric():
            for cor in cores:
                if valor[:-1] == cor[:-1].lower():
                    self.pesquisa += f"Cor LIKE '%{valor[:-1]}%' AND "
                    self.cor = valor
                    break

    def __normal_query(self, valor):
        if valor.isnumeric() and len(valor) <= 2 and 0 < int(valor) <= 49:
            resultado = f"""SELECT Placa, Cor, Modelo, Marca, Motorista, Proprietário, Casa
            FROM portaria_bd WHERE Casa LIKE '{valor}' """
        else:
            if '[' in valor:
                valor = valor.replace('[', '')

            resultado = f"""SELECT Placa, Cor, Modelo, Marca, Motorista, Proprietário, Casa FROM portaria_bd
                                WHERE Placa LIKE '%{valor}%' OR Cor LIKE '%{valor}%' OR Modelo LIKE '%{valor}%' OR
                                Marca LIKE '%{valor}%' OR Motorista LIKE '%{valor}%' OR Proprietário LIKE '%{valor}%'                
                                """
        return resultado

    def __multiple_items(self, lista):
        for i in lista:
            if i.isnumeric() and len(i) <= 2 and 0 < int(i) <= 49:
                self.pesquisa += f"Casa LIKE '{i}' AND "
                lista.remove(i)
                break

        if len(lista) == 2:
            self.pesquisa += f"((Modelo LIKE '%{lista[0]}%' OR  Marca LIKE '%{lista[1]}%') OR " \
                             f"(Marca LIKE '%{lista[0]}%' OR  Modelo LIKE '%{lista[1]}%')) AND "
        elif len(lista) == 1:
            self.pesquisa += f"(Modelo LIKE '%{lista[0]}%' OR  Marca LIKE '%{lista[0]}%') AND "

    def read_data(self, data):
        self.connect_db()
        self.cor = self.pessoa = None

        if '/' in data:
            queries_list = data.split('/')
            queries_list = list(map(lambda x: x.lower(), queries_list))

            self.pesquisa = """ SELECT Placa, Cor, Modelo, Marca, Motorista, Proprietário, Casa 
                                FROM portaria_bd WHERE """

            for query in queries_list:
                self.__driver_or_owner_select(query)
                self.__vehicle_color_select(query)

            if self.pessoa: queries_list.remove(self.pessoa)
            if self.cor: queries_list.remove(self.cor)
            if queries_list: self.__multiple_items(queries_list)

            pesquisa = self.pesquisa[:-4]

        else:
            pesquisa = self.__normal_query(data)

        self.disconnect_db()
        return pesquisa















