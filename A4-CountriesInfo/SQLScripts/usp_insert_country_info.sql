CREATE PROCEDURE [dbo].[usp_insert_country_info]
    @CountryName NVARCHAR(100),
    @CapitalState NVARCHAR(100),
    @NationalBird NVARCHAR(100),
    @CountryPopulation BIGINT,
    @CountryId INT OUTPUT
AS
BEGIN
    
    SET NOCOUNT ON;

    INSERT INTO CountryInfo 
        (CountryName, CapitalState, NationalBird, CountryPopulation)
    VALUES 
        (@CountryName, @CapitalState, @NationalBird, @CountryPopulation);

    SET @CountryId = SCOPE_IDENTITY();

    SELECT @CountryId AS CountryId;
    
END;
