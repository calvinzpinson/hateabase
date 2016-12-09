#!/usr/bin/env python
from sys import argv, exit as die
import pip, ConfigParser as configparser

try:
    import mysql.connector
    from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, render_template, flash
except:
    print("Missing requirements\n")
    die(-1)

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
    return test()
    #return render_template('index.html')

@app.route('/hateabase/', methods=['POST', 'GET'])
def hateabase():
    if request.method == 'POST':
        result = request.form['Category']
    else:
        result = ""
    races = SelectRaces()
    return render_template('base.html', result=result, races=races)

@app.route('/hateabase/api/v1.0/getgroup')
def get_db():
    if not hasattr(g, "mysql_db"):
        g.mysql_db = connect()
    return g.mysql_db

def SelectRaces():
    sql = "SELECT DISTINCT Race FROM OffenderRace"
    return [ x[u'Race'] for x in (read(sql)) ]

def read(SQL, parameters):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(SQL, parameters)
        db.commit()
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print("Failed to execute query: " + str(e))
    finally:
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
        return result
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

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "mysql_db"):
        g.mysql_db.close()    

def main():
    port_num = 5000
    if len(argv) == 2:
        port_num = int(argv[1])
    app.run(port=port_num)

if __name__ == '__main__':
    main()
