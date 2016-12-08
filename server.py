from sys import argv, exit as die
import pip, configparser

try:
    import mysql.connector
    from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
except:
    print("Missing requirements\n")
    die(-1)

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
    test()
    return render_template('index.html')

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

def reInitializeDatabase():
    
    db = get_db()
    configData = getConfigData()
    queryFiles = [configData.get("SQL", "destroy"), 
                  configData.get("SQL", "create"), 
                  configData.get("SQL", "insert")]

    for queryFile in queryFiles:
        executeSqlFromFile(queryFile, db)

def executeSqlFromFile(file, db):
    try:
        with open("./queries/" + file, 'r') as fd:
            sqlFile = fd.read()
            queries = sqlFile.split(";")
            cursor = db.cursor()
            for query in queries:
                try:
                    cursor.execute(query)
                except OperationalError:
                    print("Failed to execute sql from file: ")

    except IOError:
        print("Failed to open sql file")
        exit(-1)
    finally:
        cursor.close()

def test():
    SQL = "CREATE TABLE HelloWorld (hello VARCHAR(10), world VARCHAR(10));"
    db = get_db()
    cursor = db.cursor()
    cursor.execute(SQL)

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