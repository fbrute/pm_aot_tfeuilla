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
where (date between'2012/01/01' and '2012/07/31')
or (date between'2009/03/01' and '2009/07/31')
or (date between'2006/05/01' and '2006/12/31')
or (date between'2007/04/01' and '2007/07/31') 
or (date between'2010/05/01' and '2010/09/30') 
group by year,month,day
order by year,month,day);

select year,month,day,julian_day,pm10,aot1020 from aot_pm_daily;