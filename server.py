from sys import argv, exit as die
import pip, configparser

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
    return render_template('base.html', result=result)

def get_db():
    if not hasattr(g, "mysql_db"):
        g.mysql_db = connect()
    return g.mysql_db
        
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
        cursor = db.cursor()
        cursor.execute(SQL)
        return cursor.fetchall()
    except mysql.connector.Error:
        print("Failed to execute query")
    finally:
        cursor.close()

def executeQuery(SQL):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(SQL)
    except mysql.connector.Error:
        print("Failed to execute query")
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
    SQL = "SELECT * FROM  OffenseTypes;"
    return jsonify(read(SQL))

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