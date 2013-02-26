# -*- coding: iso-8859-1 -*-
# Le but du jeu est de renvoyer la date en fonction du rang du jour dans
# l'année
import os,sys, time
sys.path.append("c:\\pydev")
#from boj.guimixin import GuiMixin
class datefromday:

    def __init__(self,year,njour):
        self.year = year
        self.njour = njour 
        # On connait le nombre de jours de tous les mois sauf du mois de fevrier.
        # Si nous sommes une année bissextile on ajuste le mois de février
        # selon wiképédia.fr, l'année est divisible par 4, pas par 100, mais par
        # 400.
        if ((self.year % 4 == 0 and not self.year % 100 == 0 ) or self.year % 400 == 0) :
            day_feb = 29
            months_days = [31,day_feb,31,30,31,30,31,31,30,31,30,31]
        else :
            day_feb = 28
            months_days = [31,day_feb,31,30,31,30,31,31,30,31,30,31]

        #print months_days
        # On cherche à quel mois appartient ce jour
        cumuldays=0
        for month in range(12):
            cumuldays += months_days[month] 
            if njour <= cumuldays : 
                resmonth = month
                break
        
        # on considère le cumul sans le mois en cours du jour considéré
        resday = njour - (cumuldays - months_days[month]) 
        self.resday = resday
        self.resmonth = resmonth + 1

    def getStringYear(self):
        return str(self.year)

    def getStringMonth(self):
        return str(self.resmonth)

    def getStringDay(self):
        return str(self.resday)

    def get_day_of_week(self):
        y,m,d =  int(self.year),int(self.resmonth),int(self.resday)
	import datetime
	nweekday = datetime.date(y,m,d).weekday()
	
	if nweekday == 0:
		return "Lundi"
	if nweekday == 1:
		return "Mardi"
	if nweekday == 2:
		return "Mercredi"
	if nweekday == 3:
		return "Jeudi"
	if nweekday == 4:
		return "Vendredi"
	if nweekday == 5:
		return "Samedi"
	if nweekday == 6:
		return "Dimanche"


    def getArray(self):
        #return [self.resday,self.resmonth,self.year]
        return int(self.year),int(self.resmonth),int(self.resday)

    def getString(self):
        #return "%2d/%2d/%4d" % (self.resday,self.resmonth,self.year)
        return "%d/%d/%4d" % (self.resday,self.resmonth,self.year)


if __name__ == "__main__":
    day = 182 
    year = 2005
    dd = datefromday(year,day)
    print dd.getStringYear()
    print dd.getStringMonth()
    print dd.getStringDay()
    print dd.getArray()
