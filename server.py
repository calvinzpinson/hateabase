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
    return render_template('index.html')

@app.route('/hateabase/', methods=['POST', 'GET'])
def hateabase():
    if request.method == 'POST':
        result = request.form['Category']
    else:
        result = ""
    return render_template('base.html', result=result)

def reset():
    db = get_db()
    

def get_db():
    if not hasattr(g, "mysql_db"):
        g.mysql_db = connect()
    return g.mysql_db
        
def connect():
    configParser = configparser.ConfigParser()
    configFilePath = "./dbconf.365"
    configParser.read(configFilePath)

    host = configParser.get("CSLVM",'host')
    user = configParser.get("CSLVM",'userid')
    password = configParser.get("CSLVM",'password')
    database = configParser.get("CSLVM", 'database')

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

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "mysql_db"):
        g.mysql_db.close()    

def main():
    port_num = 5000
    if len(argv) == 2:
        port_num = int(argv[1])
    connect()
    app.run(port=port_num)

if __name__ == '__main__':
    main()