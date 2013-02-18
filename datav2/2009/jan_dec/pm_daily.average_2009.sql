select year, month, day, julian_day,  avg(pm10) as pm10 
from pm_hourly_average_2009_v2
group by year,month,day
order by year,month,day
