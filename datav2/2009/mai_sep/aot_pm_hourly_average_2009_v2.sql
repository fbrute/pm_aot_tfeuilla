select year(date) as year, month(date) as month, day(date) as day,
 floor(julian_day) as julian_day, 
hour(subtime(time,"04:00:00")) as heure,
 pmptp as pmp10,
avg(aot_1020) as avg_aot_1020,
avg(aot_870) as avg_aot_870, 
avg(aot_675) as avg_aot_675,
avg(aot_440) as avg_aot_440
 from aotv20,
(select datetime, pmptp from pm10 
	where hour(datetime) between 8 and 16 
and pmptp > 0 )
 as pm_hour 
where year(date) = 2009 
and date > '2009-05-01'
and date not in (select distinct date from ex_dates_2009_v2)
and (year(date),month(date), day(date),hour(subtime(time,"04:00:00")))
not in (select year,month,day,hour from ex_date_hour_2009_v2)
and date(datetime)=date 
and hour(datetime)=hour(subtime(time,"04:00:00")) 
and subtime(time,"04:00:00") between 8 and 16
and aot_1020 < 1 and aot_870 < 1 and aot_675 < 1 
and aot_440 < 1 
group by date,hour(time)
order by date,hour(time)
