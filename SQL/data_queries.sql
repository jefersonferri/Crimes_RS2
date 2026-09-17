-- sum of total crimes by year
SELECT
    year,
    SUM(homicide) AS homicides,
    SUM(theft) AS thefts,
    SUM(robbery) AS robberies,
    SUM(car_theft) AS car_thefts,
    SUM(car_robbery) AS car_robberies,
    SUM(fraud_swindle) AS frauds,
    SUM(narcotics_possession) AS drug_possession,
    SUM(narcotics_traffic) AS drug_traffic
FROM public.crimes_rs
GROUP BY year
ORDER BY year;

--what is the total number of thefts by city?

SELECT
    city,
    SUM(theft) AS total_thefts
FROM public.crimes_rs
GROUP BY city
ORDER BY total_thefts DESC
LIMIT 20;

--what is the total number of homicides by city?
SELECT
    city,
    SUM(homicide) AS total_homicides
FROM public.crimes_rs
GROUP BY city
ORDER BY total_homicides DESC
LIMIT 20;

--what is the total number of robberies by city?
SELECT
    city,
    SUM(robbery) AS total_robberies
FROM public.crimes_rs
GROUP BY city
ORDER BY total_robberies DESC
LIMIT 20;

--what is the total number of homicides by city?
SELECT
    city,
    SUM(homicide) AS total_homicides,
    AVG(population) AS population,
    SUM(homicide) / AVG(population) * 100000 AS homicide_rate
FROM public.crimes_rs
GROUP BY city
ORDER BY homicide_rate DESC;

--what is the year-over-year growth of thefts in the state of Rio Grande do Sul?

WITH yearly AS (

    SELECT
        year,
        SUM(theft) AS total_thefts
    FROM public.crimes_rs
    GROUP BY year

)

SELECT
    year,
    total_thefts,

    LAG(total_thefts) OVER (
        ORDER BY year
    ) AS previous_year,

    ROUND(
        (
            total_thefts -
            LAG(total_thefts) OVER (
                ORDER BY year
            )
        )
        /
        NULLIF(
            LAG(total_thefts) OVER (
                ORDER BY year
            ),
            0
        ) * 100,
        2
    ) AS yoy_growth_pct

FROM yearly
ORDER BY year;