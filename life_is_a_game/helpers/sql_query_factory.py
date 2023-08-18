class SqlQueryFactory:

    def insert(self, table, columns, values):
        return '''INSERT INTO {} ({}) VALUES {}'''.format(table, columns, values)
    
    def insert_returning(self, table, columns, values, returning):
        return '''INSERT INTO {} ({}) VALUES {} RETURNING {}'''.format(table, columns, values, returning)
    
    def select_where(self, table, columns, where):
        return '''SELECT {} FROM {} WHERE {}'''.format(columns, table, where)
    
    def update_where(self, table, columns, where):
        return '''UPDATE {} SET {} WHERE {}'''.format(table, columns, where)
    
    def select(self, table, columns):
        return '''SELECT {} FROM {}'''.format(columns, table)
    

        