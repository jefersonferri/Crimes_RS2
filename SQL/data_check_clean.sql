--verify nulls

SELECT *
FROM public.crimes_rs
WHERE city IS NULL
   OR TRIM(city) = '';

--check for negatives

SELECT *
FROM public.crimes_rs
WHERE homicide < 0
   OR homicide_victims < 0
   OR robbery_homicide < 0
   OR theft < 0
   OR cattle_theft < 0
   OR car_theft < 0
   OR robbery < 0
   OR car_robbery < 0
   OR fraud_swindle < 0
   OR offenses_related_to_weapons_and_ammunition < 0
   OR narcotics_possession < 0
   OR narcotics_traffic < 0
   OR robbery_homicide_victims < 0
   OR victims_of_bodily_injury < 0
   OR intentional_lethal_violent_crime_victims < 0
   OR total_intentional_lethal_violent_crime_victims < 0
   OR population < 0;

   --verify if all months exist

   SELECT
    date,
    COUNT(DISTINCT city) AS cities
FROM public.crimes_rs
GROUP BY date
ORDER BY date;

--verify duplicates

SELECT
    city,
    date,
    COUNT(*) AS records
FROM public.crimes_rs
GROUP BY city, date
HAVING COUNT(*) > 1
ORDER BY records DESC;