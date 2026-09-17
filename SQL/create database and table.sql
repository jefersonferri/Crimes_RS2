
--create the database
CREATE DATABASE crimes_rs;

--create the table for the database

CREATE TABLE IF NOT EXISTS crimes_rs (
    date DATE,
    year INTEGER,
    month_1 INTEGER,
    city VARCHAR(150),
    month VARCHAR(30),

    homicide INTEGER,
    homicide_victims INTEGER,
    robbery_homicide INTEGER,
    theft INTEGER,
    cattle_theft INTEGER,
    car_theft INTEGER,
    robbery INTEGER,
    car_robbery INTEGER,
    fraud_swindle INTEGER,
    offenses_related_to_weapons_and_ammunition INTEGER,
    narcotics_possession INTEGER,
    narcotics_traffic INTEGER,
    robbery_homicide_victims INTEGER,
    victims_of_bodily_injury INTEGER,
    intentional_lethal_violent_crime_victims INTEGER,
    total_intentional_lethal_violent_crime_victims INTEGER,

    population BIGINT
);


--tests the  table creation

SELECT *
FROM crimes_rs;


SELECT
    ordinal_position,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'crimes_rs'
ORDER BY ordinal_position;

--coppy data to the table,  i had to copy the folder to a shorter path because the postgre was not accepting one of the special chars i had in the original path, so i copied the file to D:\postgre18\crimes_RS_compilado.csv

copy public.crimes_rs (
    date,
    year,
    month_1,
    city,
    month,
    homicide,
    homicide_victims,
    robbery_homicide,
    theft,
    cattle_theft,
    car_theft,
    robbery,
    car_robbery,
    fraud_swindle,
    offenses_related_to_weapons_and_ammunition,
    narcotics_possession,
    narcotics_traffic,
    robbery_homicide_victims,
    victims_of_bodily_injury,
    intentional_lethal_violent_crime_victims,
    total_intentional_lethal_violent_crime_victims,
    population
)
FROM 'D:\postgre18\crimes_RS_compilado.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ';',
    ENCODING 'UTF8'
);

--data visualization and checking the data

SELECT *
FROM crimes_rs
LIMIT 50;

--checking the number of rows in the table
SELECT COUNT(*) AS total_registros
FROM public.crimes_rs;

--checking max and min dates
SELECT
    COUNT(*) AS total_registros,
    COUNT(DISTINCT city) AS municipios,
    MIN(date) AS primeira_data,
    MAX(date) AS ultima_data
FROM public.crimes_rs;