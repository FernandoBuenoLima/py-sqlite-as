#sqliteas.py
#
#sqlite3 wrapper
#made by Aspire

from contextlib import contextmanager
import sqlite3

class DataBase: #{
    def __init__(self, name="data"): #{
        self.name = name
        self.open = False
        self.connect()
    #}

    def __str__(self): #{
        return "Database[{0}.db, {1}]".format(self.name, "open" if self.open else "closed")
    #}

    def __repr__(self): #{
        return str(self)
    #}

    def connect(self): #{
        if self.open:
            return
        try:
            self.conn = sqlite3.connect(self.name + ".db")
            self.cursor = self.conn.cursor()
            self.open = True
        except sqlite3.Error as error:
            print("Error opening database with name %s" % dbName)
            print(error)
    #}

    @contextmanager
    def openDB(dbName="data"): #{
        db = DataBase(dbName)
        yield db
        db.closeWithoutCommitting()
    #}

    def commit(self): #{
        try:
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
    #}

    def closeWithoutCommitting(self): #{
        if not self.open:
            return

        try:
            self.cursor.close()
            self.conn.close()
            self.open = False
        except sqlite3.Error as error:
            print(error)
    #}

    def close(self): #{
        if not self.open:
            return

        try:
            self.commit()
            self.cursor.close()
            self.conn.close()
            self.open = False
        except sqlite3.Error as error:
            print(error)
    #}

    def execute(self, query): #{
        if len(query) > 0 and self.open:
            try:
                self.cursor.execute(query)
            except sqlite3.Error as error:
                print(error)
        elif not self.open:
            print("Cant query a closed DB")
    #}

    def executeQuery(self, query): #{
        if len(query) > 0 and self.open:
            try:
                self.cursor.execute(query)
                return self.cursor.fetchall()
            except sqlite3.Error as error:
                print(error)
        elif not self.open:
            print("Cant query a closed DB")
    #}

    def createTable(self, name, columns): #{
        query = "CREATE TABLE IF NOT EXISTS {0}({1});".format(name, columns)
        self.execute(query)
    #}

    def dropTable(self, name): #{
        query = "DROP TABLE IF EXISTS {0};".format(name)
        self.execute(query)
    #}

    def select(self, table, columns="*", where="", orderBy="", groupBy=""): #{
        query = "SELECT {0} FROM {1}".format(columns, table)
        if len(where) > 0:
            query += " WHERE " + where
        if len(orderBy) > 0:
            query += " ORDER BY " + orderBy
        if len(groupBy) > 0:
            query += " GROUP BY " + groupBy
        query += ";"
        return self.executeQuery(query)
    #}

    def insert(self, table, data): #{
        query = "INSERT INTO {0} VALUES({1});".format(table, data)
        self.execute(query)
    #}

    def insertIntoColumns(self, table, columns, data): #{
        query = "INSERT INTO {0} ({1}) VALUES({2});".format(table, columns, data)
        self.execute(query)
    #}

    def update(self, table, set, where=""): #{
        query = "UPDATE {0} SET {1}".format(table, set)
        if len(where) > 0:
            query += " WHERE " + set
        query += ";"
        self.execute(query)
    #}

    def delete(self, table, where="1"): #{
        query = "DELETE FROM {0} WHERE ".format(table) + where
        self.execute(query)
    #}

    def truncate(self, table): #{
        self.delete(table)
    #}

    def listTables(self): #{
        return self.select("sqlite_master", "name", "type = 'table'")
    #}

    def listColumns(self, table): #{
        query = "PRAGMA table_info({0});".format(table)
        return self.executeQuery(query)
    #}
#}
