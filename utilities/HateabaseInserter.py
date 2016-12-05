#!/usr/bin/env python

def analyzeHCFile(hcFile):
    
    hcInfo = []
    for record in hcFile.readlines():
        recordType = record[0:2]

        if (recordType == "BH"):
            ORI = record[4:13]
        if (recordType == "IR"):
            irRecord = {}
            irRecord["ORI"] = ORI
            irRecord["IncidentNumber"] = record[13:25]
            irRecord["IncidentDate"] = record[25:33]
            irRecord["TotalVictims"] = record[35:38]
            irRecord["TotalOffenders"] = record[40]
            irRecord["OffenderRace"] = record[41]
            irRecord["OffenseCode1"] = record[41:44]
            irRecord["NumberOfVictims1"] = record[44:47]
            irRecord["BiasMotivation1"] = record[49:51]
            irRecord["VictimType1"] = record[51:59]
            irRecord["OffenseCode2"] = record[59:62]
            irRecord["NumberOfVictims2"] = record[62:65]
            irRecord["BiasMotivation2"] = record[67:69]
            irRecord["VictimType2"] = record[69:77]
            irRecord["OffenseCode3"] = record[77:80]
            irRecord["NumberOfVictims3"] = record[80:83]
            irRecord["BiasMotivation3"] = record[85:87]
            irRecord["VictimType3"] = record[87:95]
            irRecord["OffenseCode4"] = record[95:98]
            irRecord["NumberOfVictims4"] = record[98:101]
            irRecord["BiasMotivation4"] = record[103:105]
            irRecord["VictimType4"] = record[105:113]
            irRecord["OffenseCode5"] = record[113:116]
            irRecord["NumberOfVictims5"] = record[116:119]
            irRecord["BiasMotivation5"] = record[121:123]
            irRecord["VictimType5"] = record[123:131]
            irRecord["OffenseCode6"] = record[131:134]
            irRecord["NumberOfVictims6"] = record[134:137]
            irRecord["BiasMotivation6"] = record[139:141]
            irRecord["VictimType6"] = record[141:142]
            irRecord["OffenseCode7"] = record[149:152]
            irRecord["NumberOfVictims7"] = record[152:155]
            irRecord["BiasMotivation7"] = record[157:159]
            irRecord["VictimType7"] = record[159:167]
            irRecord["OffenseCode8"] = record[167:170]
            irRecord["NumberOfVictims8"] = record[170:173]
            irRecord["BiasMotivation8"] = record[175:177]
            irRecord["VictimType8"] = record[177:185]
            irRecord["OffenseCode9"] = record[185:188]
            irRecord["NumberOfVictims9"] = record[188:191]
            irRecord["BiasMotivation9"] = record[193:195]
            irRecord["VictimType9"] = record[195:203]
            irRecord["OffenseCode10"] = record[203:206]
            irRecord["NumberOfVictims10"] = record[206:209]
            irRecord["BiasMotivation10"] = record[211:213]
            irRecord["VictimType10"] = record[213:221]

            hcInfo.append(irRecord)

    return hcInfo

def writeSql(hcInfo):
    try:
        with open("Incidents-INSERT.sql", "w") as incidentSqlFile, \
             open("Offenses-INSERT.sql", "w") as offenseSqlFile:
            incidents = []
            ORIs = []
            for irRecord in hcInfo:
                stripAllWhiteSpace(irRecord)
                writeIncidentSql(incidents, incidentSqlFile, irRecord, ORIs)
                writeOffenseSql(offenseSqlFile, irRecord)
                    
    except IOError:
        print("Unable open files for writing")

def stripAllWhiteSpace(irRecord):
    for key in irRecord:
        irRecord[key] = irRecord[key].strip()

def writeIncidentSql(incidents, incidentSqlFile, irRecord, ORIs):
    if (irRecord["IncidentNumber"] not in incidents or \
        irRecord["ORI"] not in ORIs):
        incidentSqlTemplate = ("INSERT INTO Incidents\n"
                               "VALUES ('{ORI}', '{IncidentNumber}', '{IncidentDate}', "
                                       "'{TotalVictims}', '{TotalOffenders}', "
                                       "'{OffenderRace}');\n")
        incidentSql = generateIncidentSql(incidentSqlTemplate, irRecord)
        incidentSqlFile.write(incidentSql)
        incidents.append(irRecord["IncidentNumber"])
        ORIs.append(irRecord["ORI"])

def generateIncidentSql(incidentSql, irRecord):
    incidentSql = incidentSql.replace("{ORI}", irRecord["ORI"])
    incidentSql = incidentSql.replace("{IncidentNumber}", irRecord["IncidentNumber"])
    incidentSql = incidentSql.replace("{IncidentDate}", irRecord["IncidentDate"])
    incidentSql = incidentSql.replace("{TotalVictims}", irRecord["TotalVictims"])
    incidentSql = incidentSql.replace("{TotalOffenders}", irRecord["TotalOffenders"])
    incidentSql = incidentSql.replace("{OffenderRace}", irRecord["OffenderRace"])

    return incidentSql

def writeOffenseSql(offenseFile, irRecord):
    offenseOrdinal = 1
    offenseSqlTemplate = ("INSERT INTO Offenses\n"
                          "VALUES ('{ORI}', '{IncidentNumber}', '{Ordinal}', "
                                  "'{OffenseCode}', '{NumberOfVictims}', "
                                  "'{BiasMotivation}', '{VictimType}');\n")
    while (offenseOrdinal <= 10):
        offenseCode = "OffenseCode" + str(offenseOrdinal)
        if (irRecord[offenseCode]):
            offenseSql = generateOffenseSql(offenseSqlTemplate, irRecord, str(offenseOrdinal))
            offenseFile.write(offenseSql)
        offenseOrdinal += 1

def generateOffenseSql(offenseSql, irRecord, offenseOrdinal):
    offenseCode = "OffenseCode" + offenseOrdinal
    numberOfVictims = "NumberOfVictims" + offenseOrdinal
    biasMotivation = "BiasMotivation" + offenseOrdinal
    victimType = "VictimType" + offenseOrdinal
    offenseSql = offenseSql.replace("{ORI}", irRecord["ORI"])
    offenseSql = offenseSql.replace("{IncidentNumber}", irRecord["IncidentNumber"])
    offenseSql = offenseSql.replace("{Ordinal}", offenseOrdinal)
    offenseSql = offenseSql.replace("{OffenseCode}", irRecord[offenseCode])
    offenseSql = offenseSql.replace("{NumberOfVictims}", irRecord[numberOfVictims])
    offenseSql = offenseSql.replace("{BiasMotivation}", irRecord[biasMotivation])
    offenseSql = offenseSql.replace("{VictimType}", irRecord[victimType])
    

    return offenseSql
def main():
    try:
        with open("HC 2014 Book Master.TXT") as hcFile:
            hcInfo = analyzeHCFile(hcFile)
            writeSql(hcInfo)

    except IOError:
        print("Unable to find HC 2014 Book Master.TXT. Are you in the right directory?")

if __name__ == "__main__":
    main()