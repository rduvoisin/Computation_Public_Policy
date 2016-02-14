/*Question 1: Handlers Exploration
The hhandler table contains registration 
forms for hazardous waste handlers. 
*/
--(a) How many forms have been received by the EPA?
SELECT count(epa_handler_id) FROM hhandler; --2,280,396
--(b) How many facilities have registered? 
-- Hint: use the count(distinct ) function
SELECT count(distinct epa_handler_id) FROM hhandler; --856,529
--(c) How many forms were received per year over the last 5 years?
--Hint: Convert the receive_date to a date using ::date and use a GROUP BY.
SELECT receive_date FROM hhandler limit 10;
--CREATE TEMP TABLE handler as hhandler;
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
--(a) How many evaluations are there?
SELECT count(*) from cmecomp3; --2061000
--(b) How many evaluations found violations?
SELECT count(*), found_violation_flag from cmecomp3 
GROUP BY found_violation_flag; --1478260
/*(c) What proportion of evaluations found violations?

(d) Which five handler_ids have been found in violation the most times? How many times? 
Also find these handlers' site names in the hhandlers table.
Hint: Use a GROUP BY and an ORDER BY DESC.*/