drop table if exists pm_hourly_average;

CREATE TABLE pm_hourly_average
  (
   year   smallint,
   month  smallint,
   day  smallint,
   julian_day  smallint,
   heure  smallint,
   pm10 smallint
);

insert into pm_hourly_average (select year(datetime) as year, 
month(datetime) as month, day(datetime) as day,
 cast(date_format(date(datetime),'%j') as decimal(5,0)) as julian_day , 
hour(datetime) as heure , avg(pmptp) as pm10 
from pm10
where date(datetime) not in (select distinct date from ex_dates)
and (year(datetime),month(datetime),day(datetime),hour(datetime)) 
not in (select year,month, day, hour from ex_date_hour)
and pmptp > 0 
group by date(datetime),hour(datetime)
order by date(datetime),hour(datetime));

select year, month, day, julian_day,  avg(pm10) as pm10 
from pm_hourly_average
group by year,month,day
order by year,month,day
