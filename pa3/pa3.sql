﻿/*Question 1: Handlers Exploration
The hhandler table contains registration
forms for hazardous waste handlers.
*/
--  (a) How many forms have been received by the EPA?
SELECT count(epa_handler_id) FROM hhandler; --  2,280,396
--  (b) How many facilities have registered?
--   Hint: use the count(distinct ) function
SELECT count(distinct epa_handler_id) FROM hhandler; --  856,529
--  (c) How many forms were received per year over the last 5 years?
--  Hint: Convert the receive_date to a date using ::date and use a GROUP BY.
SELECT receive_date FROM hhandler limit 10;
--  CREATE TEMP TABLE handler as hhandler;
SELECT count(epa_handler_id)
FROM hhandler
WHERE EXTRACT(YEAR from receive_date) > 2010
GROUP BY EXTRACT(YEAR from receive_date);
/*
2011, 92413
2012, 69795
2013, 128099
2014, 87378
2015, 2844
*/

/*Question 2: Evaluations
The cmecomp3 table contains a list of evaluations (inspections)
of these handlers. See thedata dictionary here.*/
SELECT handler_id, handler_name, evaluation_identifier, evaluation_start_date,
evaluation_agency, evaluation_type, evaluation_type_description from cmecomp3 limit 100;
SELECT count(*) from cmecomp3
GROUP BY handler_id, evaluation_start_date;
evaluation_agency, evaluation_type, evaluation_type_description  limit 100;
SELECT * from cmecomp3 limit 100;
SELECT docket_number from cmecomp3 limit 100;
--  (a) How many evaluations are there?
SELECT count(*) as total from cmecomp3; --  2,061,000
--  (b) How many evaluations found violations?
SELECT count(*) as total_violations, found_violation_flag from cmecomp3
WHERE found_violation_flag='Y'
GROUP BY found_violation_flag; --  1,478,260
--  (c) What proportion of evaluations found violations?
--   1,478,260 / 2,061,000
SELECT count(*) *1.0 / 2061000 as proportion_violations from cmecomp3
WHERE found_violation_flag='Y'
GROUP BY found_violation_flag; --  0.71725376031052886948
--  (d) Which five handler_ids have been found in violation the most times?
SELECT count(*), handler_id, handler_name, found_violation_flag from cmecomp3
WHERE found_violation_flag='Y'
GROUP BY found_violation_flag, handler_id, handler_name
ORDER BY count(*) DESC;
--  How many times?
--  Also find these handlers' site names in the hhandlers table.
/*Hint: Use a GROUP BY and an ORDER BY DESC.*/
/*
2364;"ILD990817991";"KOPPERS INC"
2379;"ILD000714881";"KEYSTONE STEEL & WIRE CO"
2396;"KY0000005785";"DESIGNTEC RECYCLING CENTER"
3481;"ILD006296800";"MUSICK PLATING CO"
4311;"ILD048843809";"CHEMETCO INC"
4772;"KYD053348108";"SAFETY-KLEEN SYSTEMS, INC."
*/


/*Question 3: Industries
The North American Industry Classification System
is a system used by federal agencies to classify a
business according to its industry. The naics table
contains this information as retrieved from here.
Start by skimming this file.*/
/*from the command line now:
psql postgresql://cfpp_student:KERG3O2e@dssgsummer2014postgres.c5faqozfo86k.us-west-2.rds.amazonaws.com:5432/cfpp*/
SELECT naics, naics_description from naics limit 100;
SELECT DISTINCT naics, naics_description from naics limit 100;

--  (a) How many different naics codes are there?
SELECT count(*) FROM naics; --  2016
SELECT count(naics) FROM naics; --  2016
SELECT count(DISTINCT naics) FROM naics; --  2016
SELECT count(naics_description) FROM naics; --  2016
SELECT count(DISTINCT naics_description) FROM naics; --  1393!!
--  Double check that each row is in fact unique in the naics column.
SELECT count(*), naics
FROM naics
GROUP BY naics
ORDER BY count(*) DESC; --  Starts with 1, naics has no duplicate values.
--    Double check that naics_description is the only column with duplicates:
SELECT count(*), naics_description
FROM naics
GROUP BY naics_description
ORDER BY count(*) DESC; --  Starts with 4 | Management of Companies and Enterprises.

--  Since there is no naics_code variable per se, if we presume that
--  naics_description is the better proxy to naics_code, there are
--  1,393 unique codes.

--  How many six-digit industry classifications are there?
/*
SELECT *
FROM naics
WHERE naics LIKE '%9';

SELECT *
FROM naics
WHERE naics LIKE '%[!//]';

SELECT *
FROM naics
WHERE naics LIKE '%[!-//]%';

SELECT *
FROM naics
WHERE naics LIKE '%!-' and WHERE naics LIKE '%!//';

SELECT *
FROM naics
WHERE naics LIKE '[0-9][0-9][0-9][0-9][0-9][0-9]';

SELECT *
FROM naics
WHERE naics NOT LIKE '%/';*/

SELECT count(*)
FROM naics
WHERE naics SIMILAR TO '%(0|1|2|3|4|5|6|7|8|9)';
--  There are 978 six-digit classifications!

--  How many two-digit classifications are there?
SELECT count(*)
FROM naics
WHERE naics SIMILAR TO '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)(-|/)%';
--  There are 20 two-digit classifications!

--  These determine the sectors as described here.
--  (b) The hnaics table contains naics codes for some handlers.
--  How many handlers have naics codes?
SELECT count(*)
FROM hnaics; --  There 3,007,616 rows of epa_handler_id's.

--  How many don't?
SELECT count(hhandler.epa_handler_id)
FROM hhandler
LEFT OUTER JOIN hnaics
  ON (hhandler.epa_handler_id = hnaics.epa_handler_id)
  WHERE hnaics.epa_handler_id IS NULL;

--Double check that these unmatched epa_handler_id's are unique:
SELECT count(DISTINCT hhandler.epa_handler_id)
FROM hhandler
LEFT OUTER JOIN hnaics
  ON (hhandler.epa_handler_id = hnaics.epa_handler_id)
  WHERE hnaics.epa_handler_id IS NULL;
-- 418,498 unique epa_handler_id don't have naics codes.

--  (c) Join the hnaics table with the naics table
--  and use a GROUP BY to determine which the
--  number of facilities in each sector.
SELECT naics_sequence_number, naics_code_owner, naics_code
FROM hnaics limit 100;

CREATE TEMP TABLE nhn AS(
    SELECT *
    FROM naics
    LEFT OUTER JOIN hnaics
      ON (naics.naics = hnaics.naics_code)
);
SELECT naics, naics_description, naics_code
FROM nhn limit 100;

SELECT count(*)
FROM nhn
WHERE naics_code SIMILAR TO '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)(-/)%'
GROUP BY naics_code
ORDER BY count(*) DESC;


--  Which sector has the most hazardous-waste handlers?
--  The least?
--  Hint: You can get the digit naics code from the naics_code
--  using this expression: substring(naics_code for 2) || '--  --  '

--  Hint: group by naics_description to get the description instead of the code.

--  (d) Create a temporary table called hsectors containing
--  unique pairs of handler ids and sector descriptions.
--  Hint: Use a GROUP BY to ensure only unique pairs.
--  Note: We'll discuss creating temporary
--  tables in class on Thursday.

/*(e) Join hsectors to cmecomp3, to determine for each sector,
the number of handlers evaluated, the number of evaluations,
the number of violations, and the proportion of evaluations finding violations.
Which sector has the most violations?*/
--  The highest proportion of evaluations finding violations?
