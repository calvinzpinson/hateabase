Team Name: The Balalaika Databassists


Team Members:
1) Calvin Pinson cpinson@calpoly.edu
2) Kent Kawahara kkawahar@calpoly.edu
3) Marina Moore mmoore32@calpoly.edu 


Application Name: Hateabase (pronounced like database, except with an h instead of a d)


Description: 
The Hateabase will be a tool for analyzing hate crimes in the United States, specifically as they occurred in 2014 (should we complete the project for 2014 alone, we may add additional data and analysis for years before and after 2014, but for the time being a single year’s worth of data seems sufficient). 


Data Description: 
The data in the Hateabase will be pulled from the FBI’s reports on hate crimes in the United States for 2014. The data includes information on the crime, the victim, the motivation, and the location. 

-- REVISED SCHEMA -- 

CREATE TABLE Incidents
(
	ORI CHAR(8),
	IncidentNumber INT PRIMARY KEY,
	IncidentDate DATE,
	TotalVictims INT,
	OffenderRaceId CHAR(1),
	TotalOffenders INT,
	FOREIGN KEY (OffenderRaceId) REFERENCES OffenderRace(OffenderRaceId)
);

CREATE TABLE Offenses
(
	ORI CHAR(8),
	IncidentNumber INT,
	Ordinal INT,
	OffenseTypeId CHAR(3),
	NumberOfVictims INT,
	BiasMotivationId INT,
	VictimTypeId CHAR(1),
	PRIMARY KEY (ORI, IncidentNumber, Ordinal),
	FOREIGN KEY (ORI, IncidentNumber) 
	REFERENCES Incidents(ORI, IncidentNumber),
	FOREIGN KEY (OffenseTypeId) REFERENCES OffenseTypes(OffenseTypeId),
	FOREIGN KEY (BiasMotivationId) REFERENCES 
	BiasMotivations(BiasMotivationId),
	FOREIGN KEY (VictimTypeId) REFERENCES VictimTypes(VictimTypeId)
);


CREATE TABLE OffenderRace
(
	OffenderRaceId CHAR(1) PRIMARY KEY,
	Race VARCHAR(60) UNIQUE
);


CREATE TABLE OffenseType
(
	OffenseTypeId CHAR(3) PRIMARY KEY,
	OffenseTypeName VARCHAR(60),
	OffenseTypeGroupId INTEGER,
	FOREIGN KEY (OffenseTypeGroupId) References 
	OffenseTypeGroups(OffenseTypeGroupId)
);

CREATE TABLE OffenseTypeGroups
(
	OffenseTypeGroupId INTEGER PRIMARY KEY,
	OffenseTypeGroup VARCHAR(60)
);

CREATE TABLE BiasMotivations
(
	BiasMotivationId INTEGER PRIMARY KEY,
	BiasMotivation VARCHAR(60),
	BiasMotivationGroupId INTEGER,
	FOREIGN KEY BiasMotivationGroupId REFERENCES 
	BiasMotivationGroups(BiasMotivationGroupId)
);

CREATE TABLE BiasMotivationGroups
(
	BiasMiasMotivationGroupId INTEGER PRIMARY KEY,
	BiasMotivationGroup VARCHAR(60) UNIQUE
);

CREATE TABLE VictimTypes
(
	VictimTypeId CHAR(1) PRIMARY KEY,
	VictimType VARCHAR(30) UNIQUE
);


-- OLDER SCHEMA -- 

CREATE TABLE IdentityCategories
(
    Category VARCHAR(30) PRIMARY KEY,
    Inherited BOOLEAN
);


CREATE TABLE IdentityAspects
(
    Id INT PRIMARY KEY,
    Category VARCHAR(30),
    Aspect VARCHAR(50) UNIQUE,
    FOREIGN KEY (Category) REFERENCES IdentityCategories(Category)
);


CREATE TABLE VictimTypes
(
    Id INT PRIMARY KEY,
    Type VARCHAR(30) UNIQUE
);


CREATE TABLE OffenseTypes
(
    Type VARCHAR(25) UNIQUE,
    Code CHAR(3) PRIMARY KEY
);


CREATE TABLE Incidents
(
    IncidentNumber INT PRIMARY KEY,
    IncidentDate DATE,
    TotalVictims INT,
    TotalOffenders INT,
    OffenderRace INT,
    FOREIGN KEY (OffenderRace) REFERENCES IdentityAspects(Id)
);


CREATE TABLE Offenses
(
    IncidentNumber INT,
    Ordinal INT,
    OffenseCode CHAR(3),
    Location VARCHAR(60),
    Motivation INT,
    VictimType INT,
    PRIMARY KEY (IncidentNumber, Ordinal),
    FOREIGN KEY (IncidentNumber) REFERENCES Incidents(IncidentNumber),
    FOREIGN KEY (OffenseCode) REFERENCES OffenseTypes(Code),
    FOREIGN KEY (Motivation) REFERENCES IdentityAspects(Id),
    FOREIGN KEY (VictimType) REFERENCES VictimTypes(Id)
);
