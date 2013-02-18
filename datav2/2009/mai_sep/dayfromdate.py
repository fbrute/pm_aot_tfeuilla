#-*- coding: iso-8859-1 -*-
# dayfromdate

import datetime

class dayfromdate:
    """ Trouver le num�ro du jour � partir de la date en clair """
    def __init__(self,year,month,day):
        """Get day number from date """
        self.date = datetime.datetime(year,month,day)

    def getnDay(self):
        """R�ucp�rer le num�ro du jour """ 
        return self.date.timetuple()[7]


if __name__ == '__main__':
    date = dayfromdate(2005,7,1)
    print date.getnDay()


