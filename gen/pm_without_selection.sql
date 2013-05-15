/*CREATE INDEX idx_date ON pm10 (datetime);*/

drop table if exists pm_hourly_average_without_selection;

/*delete from pm_hourly_average_without_selection;*/

CREATE TABLE pm_hourly_average_without_selection
  (
   year   smallint,
   month  smallint,
   day  smallint,
   julian_day  smallint,
   heure  smallint,
   pm10 smallint,
   date date
);

CREATE INDEX idx_date  ON pm_hourly_average_without_selection (date);
CREATE INDEX idx_date2 ON pm_hourly_average_without_selection (year,month,day);

insert into pm_hourly_average_without_selection (select year(datetime) as year, 
month(datetime) as month, day(datetime) as day,
 cast(date_format(date(datetime),'%j') as decimal(5,0)) as julian_day , 
hour(datetime) as heure ,  avg(pmptp) as pm10 ,date(datetime)
from pm10
where  pmptp > 0 
group by date(datetime),hour(datetime)
order by date(datetime),hour(datetime));

/*select year, month, day, julian_day,  avg(pm10) as pm10 
from pm_hourly_average_without_selection
group by year,month,day
order by year,month,day*/
