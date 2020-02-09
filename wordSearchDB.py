import sqlite3


class WordSearchDB:
    
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Word_Collections 
            (id INTEGER PRIMARY KEY, word_collection TEXT UNIQUE)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Words
            (id INTEGER PRIMARY KEY, word_collections_id INTEGER,
            word TEXT, UNIQUE(word_collections_id, word))''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Grid_Maps
            (grid_maps_id INTEGER NOT NULL, cell TEXT, letter TEXT, word_key TEXT,
            UNIQUE(grid_maps_id, cell))''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Collection_Grid
            (word_collections_id INTEGER, grid_maps_id INTEGER UNIQUE, 
            difficulty INTEGER, grid_size INTEGER)''')
        self.conn.commit()
        
    def insert_table(self, table_name, loop = 'last', **kwargs):
        params = '?' + (', ?' * (len(kwargs)-1))
        print(params, kwargs)
        if table_name == 'Word_Collections':
            self.cur.execute('INSERT INTO {} VALUES (NULL, {})'.format(
                table_name, params), 
                (kwargs['word_collection']))
        elif table_name == 'Words':
            self.cur.execute('INSERT INTO {} VALUES (NULL, {})'.format(
                table_name, params),
                (kwargs['word_collections_id'], kwargs['word']))
        elif table_name == 'Grid_Maps':
            self.cur.execute('INSERT INTO {} VALUES ({})'.format(
                table_name, params),
                (kwargs['grid_maps_id'], kwargs['cell'], kwargs['letter'],
                kwargs['word_key']))
        elif table_name == 'Collection_Grid':
            self.cur.execute('INSERT INTO {} VALUES ({})'.format(
                table_name, params),
                (kwargs['word_collections_id'], kwargs['grid_maps_id'],
                kwargs['difficulty'], kwargs['grid_size']))
        else:
            print('Insert failed')
        if loop == 'last':
            self.conn.commit()

    def get_key(self, table_name, **kwargs):
        # global this_key
        if table_name == 'Word_Collections':
            condition = f"{kwargs['identifier']} = \'{kwargs['value']}\'"
            print(condition)
            self.cur.execute("SELECT {} FROM {} WHERE {}".format(
                kwargs['id_'], table_name, condition))
            this_id = self.cur.fetchone()
            print("SELECT {} FROM {} WHERE {}".format(
                kwargs['id_'], table_name, condition))
        elif table_name == 'Grid_Maps':
            self.cur.execute("SELECT {} FROM {}".format(
                kwargs['id_'], table_name))
            this_id = self.cur.fetchall()
            print("SELECT {} FROM {}".format(
                kwargs['id_'], table_name))
        return this_id

    def __del__(self):
        self.conn.close()