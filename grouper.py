def create_view(name, fields, tables):
    statement = 'CREATE VIEW %s AS (\n' % (name)
    statement += 'SELECT'
    for field in fields:
        statement += ' %s,' % (field)
    statement += ' COUNT(*) AS NumIncidents, __IC__.TotalIncidents, __OC__.TotalOffenses\n'
    statement += 'FROM'
    for table in tables:
        statement += ' %s JOIN' % (table)
    statement = statement[:-5] + ', (SELECT COUNT(*) AS TotalIncidents FROM Incidents) __IC__, (SELECT COUNT(*) AS TotalOffenses FROM Offenses) __OC__\n'
    statement += 'GROUP BY'
    for field in fields:
        statement += ' %s,' % (field)
    statement = statement[:-1] + '\n'
    statement += ');'
    return statement

def main():
    print create_view('test', ['a1','a2','a3'],['table1','table2','table3','table4'])

if __name__ == '__main__':
    main()