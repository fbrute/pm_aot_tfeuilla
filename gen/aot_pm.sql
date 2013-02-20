drop table if exists aot_pm_hourly;
CREATE TABLE aot_pm_hourly
  (
   year   smallint,
   month  smallint,
   day  smallint,
   julian_day  smallint,
   heure  smallint,
   pm10 smallint,
   aot1020 decimal(7,6)
);   


insert into aot_pm_hourly (select aot.year,aot.month,aot.day, 
aot.julian_day, aot.heure,
 pm.pm10 , aot.aot1020 from aot_hourly_average as aot, pm_hourly_average as pm
where (aot.year,aot.month,aot.day) 
not in (select year,month,day from ex_dates)
and (aot.year,aot.month, aot.day, aot.heure) not in 
(select year, month, day, hour from ex_date_hour)
and(aot.year,aot.month,aot.day,aot.heure) = 
(pm.year,pm.month,pm.day,pm.heure)
order by aot.year,aot.month,aot.day,aot.heure);

drop table if exists aot_pm_daily;
CREATE TABLE aot_pm_daily
  (
   year   smallint,
   month  smallint,
   day  smallint,
   julian_day  smallint,
   pm10 smallint,
   aot1020 decimal(7,6)
);  

insert into aot_pm_daily (select year, month, day, julian_day,  
avg(pm10) as pm10 , avg(aot1020) as aot1020
from aot_pm_hourly
group by year,month,day
order by year,month,day)
