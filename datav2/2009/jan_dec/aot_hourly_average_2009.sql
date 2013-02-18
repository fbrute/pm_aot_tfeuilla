drop table if exists aot_hourly_average_2009_v2;

CREATE TABLE aot_hourly_average_2009_v2
  (
   year   smallint,
   month  smallint,
   day  smallint,
   julian_day  smallint,
   heure  smallint,
   aot1020 decimal(7,6), 
   aot870 decimal(7,6),
   aot675 decimal(7,6),
   aot440 decimal(7,6) 
);   

insert into aot_hourly_average_2009_v2 (select year(date) as year, 
month(date) as month, day(date) as day,
 floor(julian_day) as julian_day, 
hour(subtime(time,"04:00:00")) as heure,
avg(aot_1020) as aot1020,
avg(aot_870) as aot870, 
avg(aot_675) as aot675,
avg(aot_440) as aot440
from aotv20
where year(date) = 2009 
and date not in (select distinct date from ex_dates_2009_v2)
and (year(date),month(date),day(date),hour(subtime(time,"04:00:00"))) 
not in (select year,month, day,  hour from ex_date_hour_2009_v2)
and subtime(time,"04:00:00") between 8 and 16
and aot_1020 < 1 and aot_870 < 1 and aot_675 < 1 
and aot_440 < 1 
group by date,hour(time)
order by date,hour(time));

select * from aot_hourly_average_2009_v2 order by year,month,day,heure
