drop table indicator;
CREATE TABLE indicator (
  IndicatorId INT IDENTITY(1,1) PRIMARY KEY,
  indicatorName VARCHAR(255) NOT NULL,
  CategoryId int
);

CREATE TABLE Category (
  CategoryId INT PRIMARY KEY,
  CategoryName VARCHAR(255)
);

INSERT INTO Category(CategoryId, CategoryName) VALUES (1, 'Demográficos');
INSERT INTO Category (CategoryId, CategoryName) VALUES (2, 'Económicos');
INSERT INTO Category (CategoryId, CategoryName) VALUES (3, 'Salud');

INSERT INTO indicator (indicatorName, CategoryId) VALUES ('Healthy_life_expectancy_total', 1);
INSERT INTO indicator (indicatorName, CategoryId) VALUES ('Healthy_life_expectancy_female', 1);
INSERT INTO indicator (indicatorName, CategoryId) VALUES ('Healthy_life_expectancy_male', 1);
INSERT INTO indicator (indicatorName, CategoryId) VALUES ('Birth_rate_crude', 1);
INSERT INTO indicator (indicatorName, CategoryId) VALUES ('Life_expectancy_at_birth_female', 1);
INSERT INTO indicator (indicatorName, CategoryId) VALUES ('Life_expectancy_at_birth_male', 1);
INSERT INTO indicator (indicatorName, CategoryId) VALUES ('Life_expectancy_at_birth_total', 1);
INSERT INTO indicator (indicatorName, CategoryId) VALUES ('Mortality_rate_infant_total', 1);
INSERT INTO indicator (indicatorName, CategoryId) VALUES ('Mortality_rate_infant_female', 1);
INSERT INTO indicator (indicatorName, CategoryId) VALUES ('Mortality_rate_infant_male', 1);
INSERT INTO indicator (indicatorName, CategoryId) VALUES ('Number_of_infant_deaths', 1);
INSERT INTO indicator (indicatorName, CategoryId) VALUES ('Number_of_neonatal_deaths', 1);
INSERT INTO indicator (indicatorName, CategoryId) VALUES ('Adolescent_fertility_rate', 1);
INSERT INTO indicator (indicatorName, CategoryId) VALUES ('gdp_current_USD', 2);
INSERT INTO indicator (indicatorName, CategoryId) VALUES ('Immunization_DPT_ages_12_23_months', 3);
INSERT INTO indicator (indicatorName, CategoryId) VALUES ('Immunization_measles_ages_12_23_months', 3);
