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