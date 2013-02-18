select distinct julian_day from 
(select  distinct cast(date_format(date(datetime),'%j') 
as decimal(5,0)) as julian_day from pm10
where year(datetime) = 2009

union select distinct floor(julian_day) from aotv20
where year(date) = 2009
) as join_aot_pm_dates

order by julian_day
