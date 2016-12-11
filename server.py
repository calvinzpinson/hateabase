#!/usr/bin/env python
from __future__ import print_function
from sys import argv, stderr, exit as die
import pip
import json

try:
    from sql_util import read, readWithParams, executeQuery, executeWithParams, createQuery
    import mysql.connector
    from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, render_template, flash
except:
    print("Missing requirements\n", stderr)
    die(-1)

app = Flask(__name__)
app.config.from_object(__name__)
apiJsonObject = None
queryJsonObject = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hateabase/api/v1.0/insert/', methods=["POST"])
def insertOffenses():
    params = request.form.getlist('params', type = str)
    SQL = ("INSERT INTO OFFENSES "
           "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    try:
        executeWithParams(SQL, params)
        return 201
    except Exception as e:
        return "Invalid request:" + e, 400

@app.route('/hateabase/', methods=['GET'])
def hateabase():
    global apiJsonObject
    with open('public.api.json', 'r') as f:
        apiJsonObject = json.load(f)
    return render_template('search.html', api=apiJsonObject)

@app.route('/hateabase/api/v1.0/<string:get>/<string:by>/query', methods=["GET"])
def getQueryBy(get, by):
    if not app.debug:
        abort(404)
    global queryJsonObject
    if app.debug:
        with open('queries/api.json', 'r') as f:
            queryJsonObject = json.load(f)
    try:
        target = queryJsonObject[get][by]
        query = createQuery(target['query'])
        return jsonify({'query':query})
    except Exception as e:
        return ("", 400, "")

@app.route('/hateabase/api/v1.0/<string:get>/<string:by>', methods=["GET"])
def getBy(get, by):
    global queryJsonObject
    if not queryJsonObject or app.debug:
        with open('queries/api.json', 'r') as f:
            queryJsonObject = json.load(f)
    try:
        args = request.args
        target = queryJsonObject[get][by]
        query = createQuery(target['query'])
        params = []
        for param in target['params']:
            params.append(args[param])
        return jsonify({'data':readWithParams(query, params),'keys':target['key']})
    except Exception as e:
        return ("", 400, "")

@app.errorhandler(400)
def badRequest(error):
    return render_template('error.html', code=400)

@app.route('/hateabase/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        params = [request.form['ORI'], request.form['IncidentId'], request.form['IncidentDate'], request.form['TotalVictims'], request.form['TotalOffenders'], request.form['OffenderRace']]
        addIncident(params)

        for i in range(1, 4):
            if request.form['Ordinal' + str(i)]:
                offenseparams = [request.form['ORI'], request.form['IndicentId'], request.form['Ordinal' + i], getOffenseTypeId(request.form['OffenseType']), request.form['NumberOfVictims'], getBiasMotivationId(request.form['BiasMotivationId']), getVictimTypeId(request.form['VictimType'])]

    return render_template('insert.html')


def addIncident(params):
    SQL = ("INSERT INTO Incidents "
           "VALUES "
           "(%s, %s, %s, %s, %s, %s)")
    executeWithParams(SQL, params)

def addOffense(params):
    SQL = ("INSERT INTO Offenses "
           "VALUES "
           "(%s, %s, %s, %s, %s, %s, %s)")
    executeWithParams(SQL, params)

def getOffenseTypeId(params):
    SQL = ("SELECT OffenseTypeId "
           "FROM OffenseTypes "
           "WHERE OffenseTypeName = %s")
    return [x[u'OffenseTypeId'] for x in readWithParams(SQL, params)][0]

def getBiasMotivationId(params):
    SQL = ("SELECT BiasMotivationId "
           "FROM BiasMotivations "
           "WHERE BiasMotivationName = %s")
    return [x[u'BiasMotivationId'] for x in readWithParams(SQL, params)][0]

def getVictimTypeId(params):
    SQL = ("SELECT VictimTypeId "
           "FROM VictimTypes "
           "WHERE VictimTypeName = %s")
    return [x[u'VictimTypeId'] for x in readWithParams(SQL, params)][0]

@app.errorhandler(404)
def notFound(error):
    return render_template('error.html', code=404)

@app.errorhandler(500)
def internal(error):
    return render_template('error.html', code=500)

def SelectTotalIncidents():
    sql = "SELECT COUNT(*) as cnt from Incidents"
    return [ x[u'cnt'] for x in read(sql) ]

def SelectRaceCount(race):
    sql = "SELECT COUNT(*) as cnt FROM Incidents, OffenderRace WHERE Incidents.OffenderRaceId = OffenderRace.OffenderRaceId AND OffenderRace.Race = '" + race + "'"
    return [ x[u'cnt'] for x in read(sql) ]

def SelectRaces():
    sql = "SELECT DISTINCT Race FROM OffenderRace"
    return [ x[u'Race'] for x in (read(sql)) ]

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "mysql_db"):
        g.mysql_db.close()    

def main():
    global apiJsonObject
    with open('public.api.json', 'r') as f:
        apiJsonObject = json.load(f)
    port_num = 5000
    if len(argv) == 2:
        port_num = int(argv[1])
    app.debug = True
    app.run(port=port_num)

if __name__ == '__main__':
    main()
