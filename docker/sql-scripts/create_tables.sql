-- General Categories
CREATE TABLE GeneralCategories (
    GeneralCategoryID SERIAL,
    CategoryName VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY (GeneralCategoryID),
    CHECK (CategoryName <> '')
);

-- Material Entity
CREATE TABLE Material (
    MaterialID SERIAL,
    MaterialName VARCHAR(255) NOT NULL UNIQUE,
    GeneralCategoryID INT,
    CreatedAt TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    ElementalComposition TEXT,
    MolecularWeight FLOAT CHECK (MolecularWeight > 0),
    TensileStrength FLOAT CHECK (TensileStrength >= 0),
    Ductility FLOAT CHECK (Ductility >= 0 AND Ductility <= 2000),
    Hardness FLOAT CHECK (Hardness >= 0),
    ThermalConductivity FLOAT CHECK (ThermalConductivity >= 0),
    HeatCapacity FLOAT CHECK (HeatCapacity >= 0),
    MeltingPoint FLOAT CHECK (MeltingPoint >= 0),
    RefractiveIndex FLOAT CHECK (RefractiveIndex > 0),
    Absorbance FLOAT CHECK (Absorbance >= 0 AND Absorbance <= 1),
    Conductivity FLOAT CHECK (Conductivity >= 0),
    Resistivity FLOAT CHECK (Resistivity >= 0),
    PRIMARY KEY (MaterialID),
    FOREIGN KEY (GeneralCategoryID) REFERENCES GeneralCategories(GeneralCategoryID)
);

-- Company
CREATE TABLE Company (
    CompanyID SERIAL,
    CompanyName VARCHAR(255) NOT NULL UNIQUE,
    Location VARCHAR(255) NOT NULL,
    Subsidiary VARCHAR(255),
    PRIMARY KEY (CompanyID),
    CHECK (CompanyName <> '' AND Location <> '')
);

-- Industrial Applications
CREATE TABLE IndustrialApplications (
    ApplicationID SERIAL,
    MaterialID INT,
    ApplicationName VARCHAR(255) NOT NULL,
    Industry VARCHAR(255) NOT NULL,
    PRIMARY KEY (ApplicationID),
    FOREIGN KEY (MaterialID) REFERENCES Material(MaterialID),
    CHECK (ApplicationName <> '')
);

-- Environmental Impact
CREATE TABLE EnvironmentalImpact (
    ImpactID SERIAL,
    MaterialID INT,
    ToxicityLevel FLOAT CHECK (ToxicityLevel >= 0 AND ToxicityLevel <= 10),
    Recyclability BOOLEAN,
    CarbonFootprint FLOAT CHECK (CarbonFootprint >= 0),
    PRIMARY KEY (ImpactID),
    FOREIGN KEY (MaterialID) REFERENCES Material(MaterialID)
);

-- Sold By Relationship (with Price as a descriptive attribute)
CREATE TABLE SoldBy (
    MaterialID INT,
    CompanyID INT,
    BasePrice FLOAT CHECK (BasePrice >= 0),
    Currency VARCHAR(10) NOT NULL,
    PRIMARY KEY (MaterialID, CompanyID),
    FOREIGN KEY (MaterialID) REFERENCES Material(MaterialID),
    FOREIGN KEY (CompanyID) REFERENCES Company(CompanyID)
);

-- HasEffectOnEnvironment Relationship
CREATE TABLE HasEffectOnEnvironment (
    MaterialID INT,
    ImpactID INT,
    PRIMARY KEY (MaterialID, ImpactID),
    FOREIGN KEY (MaterialID) REFERENCES Material(MaterialID),
    FOREIGN KEY (ImpactID) REFERENCES EnvironmentalImpact(ImpactID)
);


-- HasPracticalUses Relationship
CREATE TABLE HasPracticalUses (
    MaterialID INT,
    ApplicationID INT,
    PRIMARY KEY (MaterialID, ApplicationID),
    FOREIGN KEY (MaterialID) REFERENCES Material(MaterialID),
    FOREIGN KEY (ApplicationID) REFERENCES IndustrialApplications(ApplicationID)
);
