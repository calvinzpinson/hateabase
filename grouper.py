def create_view(name, fields, tables):
    statement = 'CREATE VIEW %s AS (\n' % (name)
    statement += 'SELECT'
    for field in fields:
        statement += ' %s,' % (field)
    statement += ' COUNT(*) AS NumIncidents, __IC__.TotalIncidents, __OC__.TotalOffenses\n'
    statement += 'FROM'
    for (k,v) in tables.items():
        statement += ' %s %s,' % (v,k)
    statement += ' (SELECT COUNT(*) AS TotalIncidents FROM Incidents) __IC__, (SELECT COUNT(*) AS TotalOffenses FROM Offenses) __OC__\n'
    statement += 'GROUP BY'
    for field in fields:
        statement += ' %s,' % (field)
    statement = statement[:-1] + '\n'
    statement += ');'
    return statement