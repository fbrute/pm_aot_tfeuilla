drop table if exists pm10_2012_horaire;
CREATE TABLE pm10_2012_horaire LIKE pm10_2012;
INSERT pm10_2012_horaire SELECT * FROM pm10_2012 where pm10_2012.pm10 > 0;

/* Enlever une minute au données de 00h qui correspondent à 24h du jour précédent */
update pm10_2012_horaire set datetime = subtime(datetime,'0 0:1:0') where hour(datetime) = 0;
select year(datetime) as year, month(datetime) as month, day(datetime) as day,
cast(date_format(date(datetime),'%j') as decimal(5,0)) as julian_day,
avg(pm10) as pm10 from pm10_2012_horaire 
group by date(datetime)
order by date(datetime)