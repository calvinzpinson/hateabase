#!/usr/bin/env python
from __future__ import print_function
import ConfigParser as configparser
from sys import argv, stderr, exit as die
import pip

try:
    import mysql.connector
    from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, render_template, flash
except:
    print("Missing requirements\n", stderr)
    die(-1)

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
    #return test()
    return render_template('index.html')

@app.route('/hateabase/', methods=['POST', 'GET'])
def hateabase():
    if request.method == 'POST':
        if(int(request.form["id"]) == 1):
            race = request.form['Race']
            if race != "Race":
                result = "There were " + str(SelectRaceCount(race)[0]) + " incidents reported where the offender was  " + race + " which is " + str(round(float(SelectRaceCount(race)[0]) * 100/int(SelectTotalIncidents()[0]), 2)) + "%."
            else:
                result = ""
        else:
            result = request.form['Category']
    else:
        result = ""
    races = SelectRaces()
    return render_template('base.html', result=result, races=races)

@app.route('/hateabase/api/v1.0/getoffensebygroup', methods = ["GET"])
def getOffenseByOffenseGroup():
    SQL = ("SELECT COUNT(*) AS NumberOfOffenses, OffenseTypeGroup "
           "FROM Offenses, OffenseTypeGroups, OffenseTypes "
           "WHERE Offenses.OffenseTypeId = OffenseTypes.OffenseTypeId "
           "AND OffenseTypes.OffenseTypeGroupId = OffenseTypeGroups.OffenseTypeGroupId "
           "GROUP BY OffenseTypeGroups.OffenseTypeGroupId")

    return jsonify({"OffenseTypeGroups":read(SQL)})

@app.route('/hateabase/api/v1.0/getoffensebygroupid/<int:offenseTypeGroupId>', methods = ["GET"])
def getOffenseByOffenseGroupId(offenseTypeGroupId):
    SQL = ("SELECT COUNT(*) AS NumberOfOffenses, OffenseTypeGroup "
           "FROM Offenses, OffenseTypeGroups, OffenseTypes "
           "WHERE Offenses.OffenseTypeId = OffenseTypes.OffenseTypeId "
           "AND OffenseTypes.OffenseTypeGroupId = OffenseTypeGroups.OffenseTypeGroupId "
           "AND OffenseTypeGroups.OffenseTypeGroupId = %s")

    params = [offenseTypeGroupId]
    return jsonify({"OffenseTypeGroups":readWithParams(SQL, params)})

@app.route('/hateabase/api/v1.0/getoffensebybiasmotivation', methods = ["GET"])
def getOffenseByBiasMotivation():
    SQL = ("SELECT COUNT(*) AS NumberOfOffenses, BiasMotivation "
           "FROM Offenses, BiasMotivations "
           "WHERE Offenses.BiasMotivationID = BiasMotivations.BiasMotivationId "
           "GROUP BY BiasMotivation")
    return jsonify({"BiasMotivations":read(SQL)})

@app.route('/hateabase/api/v1.0/getincidentsbymonth', methods = ["GET"])
def getIncidentsByMonth():
    SQL = ("SELECT COUNT(*) AS NumberOfIncidents, MONTH(IncidentDate) "
           "FROM Incidents "
           "GROUP BY MONTH(IncidentDate)")
    return jsonify({"Frequencies":read(SQL)})

@app.route('/hateabase/api/v1.0/getincidentsbyoffenderrace', methods = ["GET"])
def getIncidentsByOffenderRace():
    SQL = ("SELECT COUNT(*) AS NumberOfIncidents, Race "
           "FROM Incidents, OffenderRace "
           "WHERE Incidents.OffenderRaceId = OffenderRace.OffenderRaceId "
           "GROUP BY Race")
    return jsonify({"OffenderRace":read(SQL)})

@app.route('/hateabase/api/v1.0/getincidentsbytotaloffenders', methods = ["GET"])
def getIncidentsByTotalOffenders():
    SQL = ("SELECT COUNT(*) AS NumberOfIncidents, TotalOffenders "
           "FROM Incidents "
           "GROUP BY TotalOffenders")
    return jsonify({"NumberOffenders":read(SQL)})

@app.route('/hateabase/api/v1.0/getincidentsbytotalvictims', methods = ["GET"])
def getIncidentsByTotalVictims():
    SQL = ("SELECT COUNT(*) AS NumberOfIncidents, TotalVictims "
           "FROM Incidents "
           "GROUP BY TotalVictims")
    return jsonify({"NumberVictims":read(SQL)})

@app.route('/hateabase/api/v1.0/getoffensesbyvictimtype', methods = ["GET"])
def getOffensesByVictimType():
    SQL = ("SELECT COUNT(*) as NumberVictims, VictimType "
           "FROM Offenses, VictimTypes "
           "WHERE Offenses.VictimTypeId = VictimTypes.VictimTypeId "
           "GROUP BY VictimType")
    return jsonify({"NumberVictims":read(SQL)})

@app.route('/hateabase/api/v1.0/getvictimtypebybiasmotivation/<string:BiasMotivation>', methods = ["GET"])
def getVictimTypeByBiasMotivation(BiasMotivation):
    SQL = ("SELECT COUNT(*) as NumberVictims, VictimType "
           "FROM Offenses, BiasMotivations, VictimTypes "
           "WHERE Offenses.BiasMotivationId = BiasMotivations.BiasMotivationId "
           "AND Offenses.VictimTypeId = VictimTypes.VictimTypeId "
           "AND BiasMotivations.BiasMotivation = %s "
           "GROUP BY VictimType")
    params = [BiasMotivation]
    return jsonify({"NumberVictims":readWithParams(SQL, params)})

@app.route('/hateabase/api/v1.0/getoffensesbyincident', methods = ["GET"])
def getOffensesByIncident():
    SQL = ("SELECT IncidentId, COUNT(*) as NumberOffenses "
           "FROM Offenses "
           "GROUP BY IncidentId")
    return jsonify({"NumberOffenses":read(SQL)})

#everything explodes when this runs
@app.route('/hateabase/api/v1.0/gettotalvictimsbydate', methods = ["GET"])
def getTotalVictimsByDate():
    SQL = ("SELECT SUM(TotalVictims) as NumberVictims, IncidentDate "
           "FROM Incidents "
           "GROUP BY IncidentDate")
    return jsonify({"NumberVictims":read(SQL)})


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
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print("Failed to execute query: " + str(e))
    finally:
        cursor.close()

def SelectTotalIncidents():
    sql = "SELECT COUNT(*) as cnt from Incidents"
    return [ x[u'cnt'] for x in read(sql) ]

def SelectRaceCount(race):
    sql = "SELECT COUNT(*) as cnt FROM Incidents, OffenderRace WHERE Incidents.OffenderRaceId = OffenderRace.OffenderRaceId AND OffenderRace.Race = '" + race + "'"
    return [ x[u'cnt'] for x in read(sql) ]

def SelectRaces():
    sql = "SELECT DISTINCT Race FROM OffenderRace"
    return [ x[u'Race'] for x in (read(sql)) ]
        
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
