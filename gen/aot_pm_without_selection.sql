drop table if exists aot_pm_hourly_without_selection;

CREATE TABLE aot_pm_hourly_without_selection
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

CREATE INDEX idx_date ON aot_pm_hourly_without_selection (date);
CREATE INDEX idx_date2 ON aot_pm_hourly_without_selection (year,month,day);

insert into aot_pm_hourly_without_selection (select aot.year,aot.month,aot.day, 
aot.julian_day, aot.heure,
 pm.pm10 , aot.aot1020, aot.date 
from aot_hourly_average_without_selection as aot, pm_hourly_average_without_selection as pm
where (aot.year,aot.month,aot.day,aot.heure) = 
(pm.year,pm.month,pm.day,pm.heure)
order by aot.year,aot.month,aot.day,aot.heure);