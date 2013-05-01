select year,month,day,julian_day,heure,pm10,aot1020 from aot_pm_hourly
where (date between'2012/01/01' and '2012/07/31')
or (date between'2009/03/01' and '2009/07/31')
or (date between'2006/05/01' and '2006/12/31')
or (date between'2007/04/01' and '2007/07/31') 
or (date between'2010/05/01' and '2010/09/30') 
order by date