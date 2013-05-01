drop table if exists aot_pm_hourly;

CREATE TABLE aot_pm_hourly
  (
   year   smallint,
   month  smallint,
   day  smallint,
   julian_day  smallint,
   heure  smallint,
   pm10 smallint,
   aot1020 decimal(7,6),
   date date
);   

CREATE INDEX idx_date ON aot_pm_hourly (date);
CREATE INDEX idx_date2 ON aot_pm_hourly (year,month,day);

insert into aot_pm_hourly (select aot.year,aot.month,aot.day, 
aot.julian_day, aot.heure,
 pm.pm10 , aot.aot1020, aot.date 
from aot_hourly_average as aot, pm_hourly_average as pm
where aot.date not in (select distinct date from ex_dates)
and (aot.year,aot.month, aot.day, aot.heure) not in 
(select distinct year, month, day, hour from ex_date_hour)  
and(aot.year,aot.month,aot.day,aot.heure) = 
(pm.year,pm.month,pm.day,pm.heure)
order by aot.year,aot.month,aot.day,aot.heure);