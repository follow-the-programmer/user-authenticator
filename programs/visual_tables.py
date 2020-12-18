#I dont know why i called it this way but a least it works

class SqlHelper:
    def __init__(self, db_name, table_name, **kwargs):
        self.db_name = db_name  # name of the database
        self.table_name = table_name  # name of the table used
        self.connection = sqlite3.connect(self.db_name)  # connector
        self.cursor = self.connection.cursor()   # cursor, used to navigate thru the file
        self.column_name = ""  # used in a function
        self.keys = kwargs  # keys for ease

    def create(self):
        import io
        try:
            table = f"""CREATE TABLE {self.table_name}(\n """  # first line of a SQL carry
            for key, value in self.keys.items():  # for every item in the kwargs
                if value == "id":
                    table += f"        {key} INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT"
                elif value == "txt":
                    table += f",\n        {key} TEXT"
                elif value == "txtn":
                    table += f",\n        {key} TEXT NOT NULL"
                elif value == "int":
                    table += f",\n        {key} INTEGER"
                elif value == "txtn":
                    table += f",\n        {key} INTEGER NOT NULL"
            table += "\n);"
            self.cursor.execute(table)
            with io.open(f'{self.db_name}.sql', 'w') as f:
                for line in self.connection.iterdump():
                    f.write(f'{line}')  # writes to te .sql file

        except sqlite3.OperationalError:
            pass


    def get_columns_from_table(self, column, cond=None):
        if cond is None: #if there isn't a condition
            self.cursor.execute(f"""SELECT {column} FROM {self.table_name};""") # kind of sql code
        else:
            self.cursor.execute(f"SELECT {column} FROM {self.table_name} WHERE {cond};") # other kind of sql code, I dont remember exacly how it works but it does

        tabela = [i for i in [list(j) for j in self.cursor.fetchall()]]
        for i, j in enumerate(tabela):
            for k, l in enumerate(j):
                tabela[i][k] = str(tabela[i][k])

        return tabela #returns a list of the table, with lists with specified columns and all of the values are strings. 

    def update_db(self, data, ide):
        data.append(ide)
        data = tuple(data)
        self.cursor.execute(f"""UPDATE {self.table_name} SET {' = ?, '.join(self.keys)} = ? WHERE id = ?""", data)

    def write_db(self, data):
        self.cursor.execute(f"""INSERT INTO {self.table_name} ({', '.join(self.get_table_title(True))}) VALUES (?{',?' * (len(data)- 1)}); """, data)

    def commit(self):
        self.connection.commit()

    def save_db(self):
        import io
        with io.open(f'{self.db_name}.sql', 'w') as f:
            for linha in self.connection.iterdump():
                f.write(f'{linha}')

    def get_db(self):
        import io
        with io.open(f'{self.db_name}.sql', 'r') as f:
            seql = f.read()
            self.cursor.executescript(seql)

    def get_all_table(self, table_name):

        self.cursor.execute(f"""SELECT * FROM {table_name};""")

        tabela = [i for i in [list(j) for j in self.cursor.fetchall()]]
        for i, j in enumerate(tabela):
            for k, l in enumerate(j):
                tabela[i][k] = str(tabela[i][k])

        return tabela

    def get_table_title(self, remove_id=False):
        self.cursor.execute(f'PRAGMA table_info({self.table_name});')
        if not remove_id:
            return [str(tupla[1]) for tupla in self.cursor.fetchall()]
        else:
            lista = [str(tupla[1]) for tupla in self.cursor.fetchall()]
            lista.pop(0)
            return lista

    def delete_by_id(self, eid):
        self.cursor.execute(f"""DELETE FROM pessoas WHERE id = ?;""", (eid,))

    def get_any_of(self, column):
        if type(column) is str:
            self.column_name = column
        elif type(column) is int:
            if column < 0:
                raise Exception(f'columns can not be smaller than index 0. (given {column})')
            else:
                self.column_name = self.get_table_title()[column]

        self.cursor.execute(f"SELECT {self.column_name} FROM {self.table_name};")
        return [i[0] for i in self.cursor.fetchall()]

    def has_in(self, string, column):
        columne = self.get_any_of(column)

        if string in columne:
            return True
        return False

    def get_row(self, id_value):
        self.cursor.execute(f"""SELECT id FROM {self.table_name} WHERE id = {id_value}""")
        return [i[0] for i in self.cursor.fetchall()]

    def get_first_of(self, column):
        return self.get_any_of(column)[0]

    def close_db(self):
        self.connection.close()
