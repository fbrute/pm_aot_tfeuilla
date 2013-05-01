drop table if exists aot_hourly_average;

/*DELETE FROM aot_hourly_average;*/

CREATE TABLE aot_hourly_average
  (
   year   smallint,
   month  smallint,
   day  smallint,
   julian_day  smallint,
   heure  smallint,
   aot1020 decimal(7,6), 
   aot870 decimal(7,6),
   aot675 decimal(7,6),
   aot440 decimal(7,6),
   date   date 
);   

CREATE INDEX idx_date ON aot_hourly_average (date);
CREATE INDEX idx_date2 ON aot_hourly_average (year,month,day);

insert into aot_hourly_average (select year(date) as year, 
month(date) as month, day(date) as day,
 floor(julian_day) as julian_day, 
hour(subtime(time,"04:00:00")) as heure,
avg(aot_1020) as aot1020,
avg(aot_870) as aot870, 
avg(aot_675) as aot675,
avg(aot_440) as aot440,
date
from aotv15
where not (year(date) = 2010)
and date not in (select distinct date from ex_dates)
and (year(date),month(date),day(date),hour(subtime(time,"04:00:00"))) 
not in (select distinct year,month, day,  hour from ex_date_hour)
and hour(subtime(time,"04:00:00")) between 8 and 16
and aot_1020 < 1 and aot_870 < 1 and aot_675 < 1 
and aot_440 < 1 and aot_1020 > 0 and aot_870 > 0
and aot_675 > 0 and aot_440 > 0 
group by date,hour(time)
order by date,hour(time));

insert into aot_hourly_average (select year(date) as year, 
month(date) as month, day(date) as day,
 floor(julian_day) as julian_day, 
hour(subtime(time,"04:00:00")) as heure,
avg(aot_1020) as aot1020,
avg(aot_870) as aot870, 
avg(aot_675) as aot675,
avg(aot_440) as aot440,
date
from aotv20
where year(date) = 2010
and date not in (select distinct date from ex_dates)
and (year(date),month(date),day(date),hour(subtime(time,"04:00:00"))) 
not in (select distinct year,month, day,  hour from ex_date_hour)
and hour(subtime(time,"04:00:00")) between 8 and 16
and aot_1020 < 1 and aot_870 < 1 and aot_675 < 1 
and aot_440 < 1 and aot_1020 > 0 and aot_870 > 0
and aot_675 > 0 and aot_440 > 0 
group by date,hour(time)
order by date,hour(time));

/*select year, month, day, julian_day,  avg(aot1020) as aot1020 
from aot_hourly_average
group by year,month,day
order by year,month,day*/
