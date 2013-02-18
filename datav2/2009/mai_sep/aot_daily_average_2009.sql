select year, month, day, julian_day,  avg(aot1020) as aot1020 
from aot_hourly_average_2009_v2
group by year,month,day
order by year,month,day
