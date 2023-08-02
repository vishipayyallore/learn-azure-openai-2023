CREATE PROCEDURE [dbo].[usp_insert_country_info]
    @CountryName NVARCHAR(100),
    @CapitalState NVARCHAR(100),
    @CountryBird NVARCHAR(100),
    @CountryPopulation BIGINT,
    @CountryId INT OUTPUT
AS
BEGIN
    
    SET NOCOUNT ON;

    INSERT INTO CountryInfo 
        (CountryName, CapitalState, CountryBird, CountryPopulation)
    VALUES 
        (@CountryName, @CapitalState, @CountryBird, @CountryPopulation);

    SET @CountryId = SCOPE_IDENTITY();
    
END;
