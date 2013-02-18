select distinct julian_day from 
(select  distinct cast(date_format(date(datetime),'%j') 
as decimal(5,0)) as julian_day from pm10
where year(datetime) = 2009
and date(datetime) >= '2009-05-01'

union select distinct floor(julian_day) from aotv20
where year(date) = 2009
and date >= '2009-05-01'
) as join_aot_pm_dates

order by julian_day
