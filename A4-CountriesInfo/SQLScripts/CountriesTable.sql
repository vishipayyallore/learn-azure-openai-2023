CREATE TABLE CountryInfo (
    [CountryId] INT IDENTITY (1, 1) NOT NULL PRIMARY KEY,
    CountryName NVARCHAR(100),
    CapitalState NVARCHAR(100),
    NationalBird NVARCHAR(100),
    CountryPopulation BIGINT
);