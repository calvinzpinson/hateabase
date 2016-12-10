#!/usr/bin/env python
from __future__ import print_function
from sys import argv, stderr, exit as die
import pip

try:
    from sql_util import read, readWithParams
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
    return render_template('search.html', result=result, races=races)

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
    SQL = ("(SELECT SUM(TotalVictims) as NumberVictims, IncidentDate "
           "FROM Incidents "
           "GROUP BY IncidentDate)")
    return jsonify({"NumberVictims":read(SQL)})

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
    port_num = 5000
    if len(argv) == 2:
        port_num = int(argv[1])
    app.run(port=port_num)

if __name__ == '__main__':
    main()
