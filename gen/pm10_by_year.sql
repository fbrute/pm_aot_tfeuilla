drop table if exists pm10_year_horaire;
set @year=2011;
CREATE TABLE pm10_year_horaire LIKE pm10_2012;
INSERT pm10_year_horaire SELECT datetime, jour, pmptp as pm10 FROM pm10 
where (year(datetime) = @year or year(datetime) = (@year+1)) 
and pm10.pmptp > 0;

/* Enlever une minute au données de 00h qui correspondent à 24h du jour précédent */
update pm10_year_horaire set datetime = subtime(datetime,'0 0:1:0') 
where hour(datetime) = 0;

select date(datetime) as date, cast(date_format(date(datetime),'%j') as decimal(5,0)) as julian_day,
avg(pm10) as pm10 from pm10_year_horaire 
where year(datetime) = @year
group by julian_day
order by julian_day;

/*select * from pm10_year_horaire  where year(datetime) = 9999
order by datetime;*/