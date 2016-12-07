from sys import argv, exit as die
import pip, configparser

try:
    #from mysql.connector import connect
    import mysql.connector
    from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
except:
    print("Missing requirements\n")
    #try:
        #pip.main(['install','-r','requirements.pip'])
        #from mysql.connector import connect
        #from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
    #except:
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

def connect():
    configParser = configparser.ConfigParser()
    configFilePath = "./dbconf.365"
    configParser.read(configFilePath)

    host = configParser.get("Hateabase",'host')
    user = configParser.get("Hateabase",'userid')
    password = configParser.get("Hateabase",'password')
    database = configParser.get("Hateabase", 'database')

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
    
def main():
    port_num = 5000
    if len(argv) == 2:
        port_num = int(argv[1])
    conn = connect()
    app.run(port=port_num)

if __name__ == '__main__':
    main()
