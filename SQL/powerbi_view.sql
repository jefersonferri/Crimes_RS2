CREATE OR REPLACE VIEW public.vw_crimes_powerbi AS

SELECT
    date,
    year,
    month_1,
    month,
    city,
    'Homicide' AS crime,
    homicide AS occurrences,
    population
FROM public.crimes_rs

UNION ALL

SELECT
    date,
    year,
    month_1,
    month,
    city,
    'Homicide Victims' AS crime,
    homicide_victims AS occurrences,
    population
FROM public.crimes_rs

UNION ALL

SELECT
    date,
    year,
    month_1,
    month,
    city,
    'Robbery-Homicide' AS crime,
    robbery_homicide AS occurrences,
    population
FROM public.crimes_rs

UNION ALL

SELECT
    date,
    year,
    month_1,
    month,
    city,
    'Theft' AS crime,
    theft AS occurrences,
    population
FROM public.crimes_rs

UNION ALL

SELECT
    date,
    year,
    month_1,
    month,
    city,
    'Cattle Theft' AS crime,
    cattle_theft AS occurrences,
    population
FROM public.crimes_rs

UNION ALL

SELECT
    date,
    year,
    month_1,
    month,
    city,
    'Car Theft' AS crime,
    car_theft AS occurrences,
    population
FROM public.crimes_rs

UNION ALL

SELECT
    date,
    year,
    month_1,
    month,
    city,
    'Robbery' AS crime,
    robbery AS occurrences,
    population
FROM public.crimes_rs

UNION ALL

SELECT
    date,
    year,
    month_1,
    month,
    city,
    'Car Robbery' AS crime,
    car_robbery AS occurrences,
    population
FROM public.crimes_rs

UNION ALL

SELECT
    date,
    year,
    month_1,
    month,
    city,
    'Fraud' AS crime,
    fraud_swindle AS occurrences,
    population
FROM public.crimes_rs

UNION ALL

SELECT
    date,
    year,
    month_1,
    month,
    city,
    'Weapons and Ammunition' AS crime,
    offenses_related_to_weapons_and_ammunition AS occurrences,
    population
FROM public.crimes_rs

UNION ALL

SELECT
    date,
    year,
    month_1,
    month,
    city,
    'Drug Possession' AS crime,
    narcotics_possession AS occurrences,
    population
FROM public.crimes_rs

UNION ALL

SELECT
    date,
    year,
    month_1,
    month,
    city,
    'Drug Traffic' AS crime,
    narcotics_traffic AS occurrences,
    population
FROM public.crimes_rs;

SELECT *
FROM public.vw_crimes_powerbi
LIMIT 20;

SELECT COUNT(*)
FROM public.vw_crimes_powerbi;