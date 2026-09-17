-- pareto, cities with 80% of population 

WITH municipality_population AS (

    SELECT
        city,
        MAX(population) AS population
    FROM public.crimes_rs
    GROUP BY city

),

pareto AS (

    SELECT
        city,
        population,

        SUM(population) OVER (
            ORDER BY population DESC
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ) AS cumulative_population,

        SUM(population) OVER () AS total_population

    FROM municipality_population

)

SELECT
    city,
    population,
    cumulative_population,
    ROUND(
        cumulative_population / total_population * 100,
        2
    ) AS cumulative_population_pct
FROM pareto
WHERE cumulative_population - population
      < total_population * 0.80
ORDER BY population DESC;


--homicide rate by year - the first 10 cities with the highest homicide rate in each year, considering only the cities that make up 80% of the population of the state of Rio Grande do Sul

WITH municipality_population AS (

    SELECT
        city,
        MAX(population) AS population
    FROM public.crimes_rs
    GROUP BY city

),

pareto AS (

    SELECT
        city,
        population,

        SUM(population) OVER (
            ORDER BY population DESC
        ) AS cumulative_population,

        SUM(population) OVER () AS total_population

    FROM municipality_population

),

pareto_80 AS (

    SELECT
        city,
        population
    FROM pareto
    WHERE cumulative_population - population
          < total_population * 0.80

),

annual AS (

    SELECT
        c.year,
        c.city,
        SUM(c.homicide) AS homicides,
        MAX(c.population) AS population

    FROM public.crimes_rs c

    INNER JOIN pareto_80 p
        ON c.city = p.city

    GROUP BY
        c.year,
        c.city

),

ranked AS (

    SELECT
        year,
        city,
        homicides,
        population,

        ROUND(
            homicides::numeric
            / NULLIF(population, 0)
            * 100000,
            2
        ) AS homicide_rate,

        RANK() OVER (
            PARTITION BY year
            ORDER BY
                homicides::numeric
                / NULLIF(population, 0)
                DESC
        ) AS rank

    FROM annual

)

SELECT *
FROM ranked
WHERE rank <= 10
ORDER BY year, rank;

