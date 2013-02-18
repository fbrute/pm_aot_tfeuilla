select year, month, day, nday,  avg(pm10) as pm10, 
avg(aot1020) as aot1020 
from aot_pm10_hourly_average
where (year,month,day) not in (select year(date),month(date)
,day(date) from ex_dates)  
and (year,month,day,heure) 
not in (select year,month, day, hour from ex_date_hour)
group by year,month,day
order by year,month,day
