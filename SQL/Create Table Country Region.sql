drop table country;
CREATE TABLE country (
  CountryID INT IDENTITY(1,1) PRIMARY KEY,
  CountryName VARCHAR(255),
  CountryCode varchar(255)
);
INSERT INTO country (CountryName, CountryCode)
SELECT DISTINCT[Country Name], [Country Code] FROM dbo.DATA;


drop table region;
CREATE TABLE region (
  RegionId INT IDENTITY(1,1) PRIMARY KEY,
  RegionName VARCHAR(255)
);
INSERT INTO region (RegionName) VALUES ('North America');
INSERT INTO region (RegionName) VALUES ('Central América');
INSERT INTO region (RegionName) VALUES ('South America');
INSERT INTO region (RegionName) VALUES ('Oceania');

ALTER TABLE country
ADD RegionId INT,
FOREIGN KEY (RegionId) REFERENCES region(RegionId);
UPDATE country
SET RegionId = (
  SELECT RegionId
  FROM region
  WHERE RegionName = 'North America'
)
WHERE CountryName IN ('Canada', 'United States');
UPDATE country
SET RegionId = (
  SELECT RegionId
  FROM region
  WHERE RegionName = 'Central América'
)
WHERE CountryName IN ('Belize', 'Costa Rica', 'El Salvador', 'Guatemala', 'Honduras', 'Mexico', 'Nicaragua', 'Panama','Cuba', 'Haiti');
UPDATE country
SET RegionId = (
  SELECT RegionId
  FROM region
  WHERE RegionName = 'South America'
)
WHERE CountryName IN ('Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela');
UPDATE country
SET RegionId = (
  SELECT RegionId
  FROM region
  WHERE RegionName = 'Oceania'
)
WHERE CountryName IN ('Australia', 'Fiji', 'Kiribati', 'Marshall Islands', 'Micronesia, Fed. Sts.', 'Nauru', 'New Zealand', 'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu');
