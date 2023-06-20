drop table if exists Adolescent_fertility_rate;
CREATE TABLE Adolescent_fertility_rate (
  Id varchar(255),
  Year DATE,
  CountryID INT,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(10, 2),
  CategoryId INT,
  RegionId INT
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);

INSERT INTO Adolescent_fertility_rate (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[Adolescent fertility rate (births per 1,000 women ages 15-19)],c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE Adolescent_fertility_rate 
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE Adolescent_fertility_rate
SET indicatorId = 12,
    CategoryId = 1;



drop table if exists Healthy_life_expectancy_female;
CREATE TABLE Healthy_life_expectancy_female (
  Id varchar(255),
  Year DATE,
  CountryId INT,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(10, 2),
  CategoryId INT,
  RegionId INT,
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);
INSERT INTO Healthy_life_expectancy_female (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[Healthy life expectancy, female (years)],c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE Healthy_life_expectancy_female 
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE Healthy_life_expectancy_female
SET indicatorId = 1,
    CategoryId = 1;


drop table if exists Healthy_life_expectancy_male;
CREATE TABLE Healthy_life_expectancy_male (
  Id varchar(255),
  Year DATE,
  CountryId INT,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(10, 2),
  CategoryId INT,
  RegionId INT,
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);
INSERT INTO Healthy_life_expectancy_male (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[Healthy life expectancy, male (years)],c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE Healthy_life_expectancy_male 
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE Healthy_life_expectancy_male
SET indicatorId = 2,
    CategoryId = 1;


drop table if exists Birth_rate_crude;
CREATE TABLE Birth_rate_crude (
  Id varchar(255),
  Year DATE,
  CountryId INT,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(10, 2),
  CategoryId INT,
  RegionId INT,
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);
INSERT INTO Birth_rate_crude (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[Birth rate, crude (per 1,000 people)],c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE Birth_rate_crude 
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE Birth_rate_crude
SET	indicatorId = 3,
    CategoryId = 1;


drop table if exists Life_expectancy_at_birth_female;
CREATE TABLE Life_expectancy_at_birth_female(
  Id varchar(255),
  Year DATE,
  CountryId int,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(10, 2),
  CategoryId INT,
  RegionId INT,
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);
INSERT INTO Life_expectancy_at_birth_female (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[Life expectancy at birth, female (years)],c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE Life_expectancy_at_birth_female 
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE Life_expectancy_at_birth_female
SET indicatorId = 4,
    CategoryId = 1;


drop table if exists Life_expectancy_at_birth_male;
CREATE TABLE Life_expectancy_at_birth_male(
  Id varchar(255),
  Year DATE,
  CountryId INT,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(10, 2),
  CategoryId INT,
  RegionId INT,
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);
INSERT INTO Life_expectancy_at_birth_male (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[Life expectancy at birth, male (years)],c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE Life_expectancy_at_birth_male 
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE Life_expectancy_at_birth_male
SET indicatorId = 5,
    CategoryId = 1;


drop table if exists Life_expectancy_at_birth_total;
CREATE TABLE Life_expectancy_at_birth_total(
  Id varchar(255),
  Year DATE,
  CountryId int,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(10, 2),
  CategoryId INT,
  RegionId INT,
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);
INSERT INTO Life_expectancy_at_birth_total (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[Life expectancy at birth, total (years)],c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE Life_expectancy_at_birth_total 
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE Life_expectancy_at_birth_total
SET indicatorId = 6,
    CategoryId = 1;



drop table if exists Mortality_rate_infant_total;
CREATE TABLE Mortality_rate_infant_total(
  Id varchar(255),
  Year DATE,
  CountryId INT,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(10, 2),
  CategoryId INT,
  RegionId INT,
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);
INSERT INTO Mortality_rate_infant_total (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[Mortality rate, infant (per 1,000 live births)],c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE Mortality_rate_infant_total 
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE Mortality_rate_infant_total
SET indicatorId = 7,
    CategoryId = 1;



drop table if exists Mortality_rate_infant_female;
CREATE TABLE Mortality_rate_infant_female(
  Id varchar(255),
  Year DATE,
  CountryId INT,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(10, 2),
  CategoryId INT,
  RegionId INT,
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);
INSERT INTO Mortality_rate_infant_female (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[Mortality rate, infant, female (per 1,000 live births)],c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE Mortality_rate_infant_female 
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE Mortality_rate_infant_female
SET indicatorId = 8,
    CategoryId = 1;


drop table if exists Mortality_rate_infant_male;
CREATE TABLE Mortality_rate_infant_male(
  Id varchar(255),
  Year DATE,
  CountryId INT,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(10, 2),
  CategoryId INT,
  RegionId INT,
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);
INSERT INTO Mortality_rate_infant_male (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[Mortality rate, infant, male (per 1,000 live births)]
,c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE Mortality_rate_infant_male 
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE Mortality_rate_infant_male
SET indicatorId = 9,
    CategoryId = 1;



drop table if exists Number_of_infant_deaths;
CREATE TABLE Number_of_infant_deaths(
  Id varchar(255),
  Year DATE,
  CountryId INT,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(10, 2),
  CategoryId INT,
  RegionId INT,
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);
INSERT INTO Number_of_infant_deaths (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[Number of infant deaths]
,c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE Number_of_infant_deaths
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE Number_of_infant_deaths
SET indicatorId = 10,
    CategoryId = 1;


drop table if exists Number_of_neonatal_deaths;
CREATE TABLE Number_of_neonatal_deaths(
  Id varchar(255),
  Year DATE,
  CountryId INT,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(10, 2),
  CategoryId INT,
  RegionId INT,
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);
INSERT INTO Number_of_neonatal_deaths (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[Number of neonatal deaths]
,c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE Number_of_neonatal_deaths
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE Number_of_neonatal_deaths
SET indicatorId = 11,
    CategoryId = 1;


drop table if exists Immunization_DPT_ages_12_23_months;
CREATE TABLE Immunization_DPT_ages_12_23_months(
  Id varchar(255),
  Year DATE,
  CountryId INT,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(10, 2),
  CategoryId INT,
  RegionId INT,
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);
INSERT INTO Immunization_DPT_ages_12_23_months (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[Immunization, DPT (% of children ages 12-23 months)],c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE Immunization_DPT_ages_12_23_months
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE Immunization_DPT_ages_12_23_months
SET indicatorId = 14,
    CategoryId = 3;



drop table if exists gdp_current_USD;
CREATE TABLE gdp_current_USD(
  Id varchar(255),
  Year DATE,
  CountryId INT,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(20, 1),
  CategoryId INT,
  RegionId INT,
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);
INSERT INTO gdp_current_USD (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[GDP (current US$)],c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE gdp_current_USD
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE gdp_current_USD
SET indicatorId = 13,
    CategoryId = 2;


drop table if exists Immunization_measles_ages_12_23_months;
CREATE TABLE Immunization_measles_ages_12_23_months(
  Id varchar(255),
  Year DATE,
  CountryId INT,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(10, 2),
  CategoryId INT,
  RegionId INT,
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);
INSERT INTO Immunization_measles_ages_12_23_months (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[Immunization, measles (% of children ages 12-23 months)],c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE Immunization_measles_ages_12_23_months
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE Immunization_measles_ages_12_23_months
SET indicatorId = 15,
    CategoryId = 3;



drop table if exists Healthy_life_expectancy_total;
CREATE TABLE Healthy_life_expectancy_total(
  Id varchar(255),
  Year DATE,
  CountryId INT,
  CountryCode VARCHAR(255),
  indicatorId INT,
  Value DECIMAL(10, 2),
  CategoryId INT,
  RegionId INT,
  FOREIGN KEY (indicatorId) REFERENCES indicator(indicatorId),
  FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
  FOREIGN KEY (RegionId) REFERENCES region(RegionId),
  FOREIGN KEY (CountryId) REFERENCES country(CountryID)
);
INSERT INTO Healthy_life_expectancy_total (Year,CountryId, CountryCode, Value, RegionId)
SELECT	d.Time,c.CountryID, c.CountryCode, d.[Healthy life expectancy, total (years)],c.RegionId
FROM [Data-Bank] as d
INNER JOIN country c ON d.[Country Name]= c.CountryName;
UPDATE Healthy_life_expectancy_total
SET id = CountryCode + RIGHT(CONVERT(VARCHAR(4), Year), 2);
UPDATE Healthy_life_expectancy_total
SET indicatorId = 16,
    CategoryId = 1;