drop table if exists aot_pm_daily_without_selection;
CREATE TABLE aot_pm_daily_without_selection
  (
   year   smallint,
   month  smallint,
   day  smallint,
   julian_day  smallint,
   pm10 smallint,
   aot1020 decimal(7,6)
);  


insert into aot_pm_daily_without_selection (select year, month, day, julian_day,  
avg(pm10) as pm10 , avg(aot1020) as aot1020
from aot_pm_hourly_without_selection
group by year,month,day
order by year,month,day);

select year,month,day,julian_day,pm10,aot1020 from aot_pm_daily_without_selection;