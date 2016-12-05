CREATE TABLE VictimTypes
(
	VictimTypeId CHAR(1) PRIMARY KEY,
	VictimType VARCHAR(30) UNIQUE
);

CREATE TABLE BiasMotivationGroups
(
	BiasMotivationGroupId INTEGER PRIMARY KEY,
	BiasMotivationGroup VARCHAR(60) UNIQUE
);

CREATE TABLE BiasMotivations
(
	BiasMotivationId INTEGER PRIMARY KEY,
	BiasMotivation VARCHAR(60),
	BiasMotivationGroupId INTEGER,
	FOREIGN KEY (BiasMotivationGroupId) REFERENCES 
	BiasMotivationGroups(BiasMotivationGroupId)
);

CREATE TABLE OffenseTypeGroups (
    OffenseTypeGroupId INTEGER PRIMARY KEY,
    OffenseTypeGroup VARCHAR(60)
);

CREATE TABLE OffenseTypes
(
	OffenseTypeId CHAR(3) PRIMARY KEY,
	OffenseTypeName VARCHAR(60),
	OffenseTypeGroupId INTEGER,
	FOREIGN KEY (OffenseTypeGroupId) REFERENCES
	OffenseTypeGroups(OffenseTypeGroupId)
);

CREATE TABLE OffenderRace
(
	OffenderRaceId CHAR(1) PRIMARY KEY,
	Race VARCHAR(60) UNIQUE
);

CREATE TABLE Incidents
(
	ORI CHAR(9),
	IncidentId VARCHAR(30),
	IncidentDate DATE,
	TotalVictims INT,
	OffenderRaceId CHAR(1),
	TotalOffenders INT,
	FOREIGN KEY (OffenderRaceId) REFERENCES OffenderRace(OffenderRaceId),
    CONSTRAINT pk_ORIAndIncidentId PRIMARY KEY (ORI, IncidentId)
);

CREATE TABLE Offenses
(
	ORI CHAR(9),
	IncidentId VARCHAR(30),
	Ordinal INT,
	OffenseTypeId CHAR(3),
	NumberOfVictims INT,
	BiasMotivationId INT,
	VictimTypeId CHAR(1),
	CONSTRAINT pk_ORIAndIncidentIdAndOrdinal PRIMARY KEY (ORI, IncidentId, Ordinal),
	FOREIGN KEY (ORI, IncidentId) 
	REFERENCES Incidents(ORI, IncidentId),
	FOREIGN KEY (OffenseTypeId) REFERENCES OffenseTypes(OffenseTypeId),
	FOREIGN KEY (BiasMotivationId) REFERENCES 
	BiasMotivations(BiasMotivationId),
	FOREIGN KEY (VictimTypeId) REFERENCES VictimTypes(VictimTypeId)
);