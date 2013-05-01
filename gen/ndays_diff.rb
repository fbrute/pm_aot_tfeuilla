new_ndays = File.open('aot_pm_hourly_julian_day.txt').collect {|line| line.chomp}
new_ndays.shift
old_ndays = File.open('ndays_85.txt').collect {|line| line.chomp}
old_ndays.shift
puts old_ndays - new_ndays
puts new_ndays - old_ndays
