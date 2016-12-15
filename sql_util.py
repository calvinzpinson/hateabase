from flask import g
import ConfigParser as configparser
import mysql.connector
from decimal import Decimal
from sanitize import sanitize

def get_db():
    if not hasattr(g, "mysql_db"):
        g.mysql_db = connect()
    return g.mysql_db

def readWithParams(SQL, parameters):
    try:
        db = get_db()
        cursor = db.cursor(buffered = True, dictionary = True)
        cursor.execute(SQL, parameters)
        db.commit()
        result = cursor.fetchall()
        print(result)
        return sanitize(result, (lambda val: float(val) if type(val) == Decimal else val))
    except mysql.connector.Error as e:
        print("Failed to execute query: " + str(e))
    finally:
        cursor.close()

def executeWithParams(SQL, parameters):
    cursor = None
    try:
        db = get_db()
        cursor = db.cursor(buffered = True, dictionary = True)
        cursor.execute(SQL, parameters)
        db.commit()
    except mysql.connector.Error as e:
        print("Failed to execute query: " + str(e))
    finally:
        if cursor:
            cursor.close()


def connect():
    configData = getConfigData()

    host = configData.get("DigitalOcean", 'host')
    user = configData.get("DigitalOcean", 'userid')
    password = configData.get("DigitalOcean", 'password')
    database = configData.get("DigitalOcean", 'database')

    try:
        conn = mysql.connector.connect(
                user = user,
                password = password,
                host = host,
                database = database)
    except mysql.connector.ProgrammingError:
        print("Unable to connect to the database")
        exit(-1)

    return conn

def getConfigData():
    configParser = configparser.ConfigParser()
    configFilePath = "./dbconf.365"
    configParser.read(configFilePath)

    return configParser

def insertValues():
    configData = getConfigData()
    queryFiles = [configData.get("SQL", "insert")]

    for queryFile in queryFiles:
        executeSqlFromFile(queryFile)

def initializeDatabase():

    configData = getConfigData()
    queryFiles = [configData.get("SQL", "create"), 
                  configData.get("SQL", "insert")]

    for queryFile in queryFiles:
        executeSqlFromFile(queryFile)

def createTables():

    configData = getConfigData()
    queryFiles = [configData.get("SQL", "create")]

    for queryFile in queryFiles:
        executeSqlFromFile(queryFile)

def destroyDatabase():
    configData = getConfigData()
    queryFiles = [configData.get("SQL", "destroy")]

    for queryFile in queryFiles:
        executeSqlFromFile(queryFile)

def testInsert():
    SQL = "INSERT INTO VictimTypes VALUES ('B', 'po')"
    return jsonify(executeQuery(SQL))


def reInitializeDatabase():

    configData = getConfigData()
    queryFiles = [configData.get("SQL", "destroy"), 
                  configData.get("SQL", "create"), 
                  configData.get("SQL", "insert")]

    for queryFile in queryFiles:
        executeSqlFromFile(queryFile)

def read(SQL):
    try:
        db = get_db()
        cursor = db.cursor(buffered=True, dictionary=True)
        cursor.execute(SQL)
        db.commit()
        result = cursor.fetchall()
        return sanitize(result, (lambda val: float(val) if type(val) == Decimal else val))
    except mysql.connector.Error as e:
        print("Failed to execute query: " + str(e))
    finally:
        cursor.close()

def executeQuery(SQL):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(SQL)
        db.commit()
    except mysql.connector.Error as e:
        print("Failed to execute query: " + str(e))
    finally:
        cursor.close()

def executeSqlFromFile(file):
    try:
        with open(file, 'r') as fd:
            sqlFile = fd.read()
            queries = sqlFile.split(";")
            for query in queries:
                executeQuery(query)

    except IOError:
        print("Failed to open sql file")
        exit(-1)

def test():
    SQL = "SELECT * FROM  OffenseTypes"
    return jsonify({"OffenseTypes":read(SQL)})

def test2():
    configData = getConfigData()
    queryFiles = [configData.get("SQL", "victimInsert")]

    for queryFile in queryFiles:
        executeSqlFromFile(queryFile)

def createQuery(components):
    query = ''
    for clause in ['select', 'from', 'where', 'group', 'having', 'order']:
        if components.has_key(clause):
            query += components[clause]
    return query
