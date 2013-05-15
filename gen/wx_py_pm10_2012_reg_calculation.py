#-*- coding: iso-8859-1 -*-
"""
On cherche à obtenir des données horaire d'épaisseur optiques 
que nous pourrons comparer avec les courbes de rayonnement obtenues par le
traitement des données obtenues par l'inra

"""

import os, sys, string
#from flatten import flatten
#from Numeric import *
from numpy import *
dirtoconv = os.path.join("D:\\", "dvpt", "pm_aot_tfeuilla","gen")
os.chdir(dirtoconv)

# Valeurs des différentes colonnes
nblignes = 18
g0annee, g0mois, g0jour, g0numjour, g0heure, g0tsv, g0rayglob, g0raydif, g0G0, globM1, globM2, globM3tl2,globM3tl4, globM3tl6, globM4tl2, globM5tl2, gAOT,g0IR = range(nblignes)

class selmat:
    """ Renvoyer un extrait de matrice (array) """
    def __init__(self,sourcemat,lstlimits):
        self.sourcemat = sourcemat
        self.lstlimits = lstlimits


# Les données du photomètre doivent exister pour pouvoir les comparer
# ce sont donc ces jours seulement que nous considérerons
datayears = range(2005,2013) 

from numpy import *
from pylab import *

# comment out the following to use wx rather than wxagg
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg 

from matplotlib.backends.backend_wx import _load_bitmap
from matplotlib.figure import Figure
#from matplotlib.numerix.mlab import rand (plante le 08/01/2013)
import wx



# Inspiré de embedding_in_wx4.py
class MyNavigationToolbar(NavigationToolbar2WxAgg):
    """
    Extend the default wx toolbar with your own event handlers
    """
    #ON_CUSTOM = wx.NewId()
    def __init__(self, canvas, cankill):
        NavigationToolbar2WxAgg.__init__(self, canvas)

        # for simplicity I'm going to reuse a bitmap from wx, you'll
        # probably want to add your own.
        self.ON_PREVIOUS = wx.NewId()
        self.ON_NEXT = wx.NewId()
        self.ON_LISTE = wx.NewId()

        self.AddSimpleTool(self.ON_PREVIOUS, _load_bitmap('stock_left.xpm'), 'Courbe precedente', 'Courbe precedente')
        self.AddSimpleTool(self.ON_NEXT, _load_bitmap('stock_right.xpm'), 'Courbe suivante', 'Courbe suivante')
        self.AddSimpleTool(self.ON_LISTE, _load_bitmap('stock_up.xpm'), 'Liste par date', 'Liste par date')

        wx.EVT_TOOL(self, self.ON_PREVIOUS, self._on_previous)
        wx.EVT_TOOL(self, self.ON_NEXT, self._on_next)
        wx.EVT_TOOL(self, self.ON_LISTE, self._on_liste)

        self.diryears = datayears

        print self.diryears
        #keys_sort = self.diryears.keys()
        #keys_sort.sort()
        #self.premyear = self.diryears[keys_sort[0]]
        #self.premyear = datayears[0]
        self.premyear = 2005
        #self.deryear = self.diryears[keys_sort[len(keys_sort)-1]]
        #self.deryear = datayears[len(datayears)-1] 
        self.deryear = 2012 
        self.njour = self.premyear 
        self.compteuryear = 0 

        self.prepdata()
        self.draw()

    def get_tranche(self,asource,heuredeb,heurefin):
        """ Récupérer une tranche de données """
        #print "heuredeb:", heuredeb
        #print "heurefin:", heurefin
        res_array = compress(greater_equal(asource[:,heure],float(heuredeb)), asource,0) 
        res_array = compress(less_equal(res_array[:,heure],float(heurefin)), res_array,0) 
        #print "res_array", res_array
        return res_array



    def prepdata(self):
        """ Préparer un tableau avec tous les jours de données pour la
        synthèse finale """
        # Pour sauvegarder les données ultimes présentées
        tot_array_data3 = array([])
        # Colonnes du tableau, tot_array_data
        self.ntyear, self.ntmonth, self.ntday,self.ntjul_day, self.ntpm10,self.ntaot1020 = range(6) 
        self.tot_array_data3 = mlab.load("aot_pm_daily_2012.txt",comments="#", delimiter=",")
	# Année à garder
	self.nyear = 2012
	# Mois à garder : mars à juillet
	self.nt_month_deb = 1
	self.nt_month_fin = 12 


    def get_jour_en_clair(self,njour):
        # Préparer la liste des jours de données existants 
        from datefromday import datefromday
        return string.strip(datefromday(self.nyear,njour).getString())


    def _on_liste(self, evt):
        """ On choisit le jour à tracer à partir d'une liste """

        dlg = wx.SingleChoiceDialog(
                self, 'Choisir une année', 'Veuille choisir une année',
                datayears,
                wx.CHOICEDLG_STYLE
                )
        if dlg.ShowModal() == wx.ID_OK:
            #njour = string.atof(dlg.GetStringSelection())
            self.nyear = self.diryears[dlg.GetStringSelection()]
        else:
            return
        dlg.Destroy()
        self.draw()

    def get_aot_pm_year_months(self,vector,nyear):
        """Select a year of data, and months between 03 ant 07 """
	colyear = self.ntyear 
	colmonth = self.ntmonth 
	moisdeb = self.nt_month_deb
	moisfin = self.nt_month_fin
        vect_tmp = compress(equal(vector[:,colyear],nyear),vector,0)
        vect_tmp = compress(greater_equal(vect_tmp[:,colmonth],float(moisdeb)), vect_tmp,0) 
        vect_tmp = compress(less_equal(vect_tmp[:,colmonth],float(moisfin)), vect_tmp,0) 

	return vect_tmp


    def draw(self,*args):
        """ Tracer les courbes en fonction de la date choisie """
       	# On sélectionne les données pour une année
	self.aot_pm = []
        self.aot_pm = self.get_aot_pm_year_months(self.tot_array_data3,self.nyear)
        # On trace l'AOT global en fonction de l'AOT1020
        vaot1020 = self.vaot1020 = self.aot_pm[:,self.ntaot1020]
        vpm10 = self.vpm10 = self.aot_pm[:,self.ntpm10]
	print "size(vpm10)=",size(vpm10)

	from scipy import stats
        svaot1020 = sort(vaot1020)
	svpm10 = -sort(-vpm10)
        pente, origine, coeffreg = stats.linregress(vaot1020,vpm10)[:3]

        interlinear = self.interlinear = pente*svaot1020 + origine

	from numpy import mean, median
	print "moyenne de vaot1020 calcule :", mean(interlinear)
	print "mediane de vaot1020 calcule :", median(interlinear)
	print "mode de vaot1020 calcule :", stats.mode(interlinear)

        #ax.plot(svaot1020,interlinear,'-b')
        #ax.plot(svaot1020,interlinear,'*m')

        #pente = pente * 100.0
	#ax.text(ax.x,30,("pente = %f" % pente))
        #ax.set_title("PM10 fonction de l' AOT1020*100 (%d,v15 apres selection)" % self.nyear,fontsize=8)
	print "pente=%f" % pente
	print "coeff=%f" % coeffreg 
	print "origine=%f" % origine 
	#self.draw_bar_distribution()
	self.draw_bar_frequency()

    def draw_bar_frequency(self, *args):
	vpm10= self.interlinear
        import pylab as plt
	#gaussian_numbers = normal(size=1000)
	#print gaussian_numbers
	bins_values = range(0,105,5)
	print "bins_values=",bins_values
	#bins_values = [0,5],[5,10],[10,15],[15,20],[20,25],[25,30],[30,35],[35,40],[40,45],[45,50],[50,55],[55,60],
	#[60,65],[65,70],[70,75],[75,80],[80,85],[85,90],[95,100]
        #plt.hist(vpm10,bins=bins_values,normed=1,histtype='bar')
        #plt.hist(vpm10,bins=bins_values)
        #n,bins,patches = plt.hist(vpm10,bins=bins_values)
	n,xout,patches = plt.hist(vpm10,bins=bins_values)
	#n,xout,patches = plt.hist(vpm10,bins=20)
	print "n=" ,n, "sum=",sum(n), "len(n)=", len(n)
	print "xout=" ,xout, "len(xout)=", len(xout)
        print [float(number)/sum(n) for number in n]
	plt.figure()
	plt.bar(xout[:20],[float(number)/sum(n) for number in n],width=5)
	#plt.bar(bins_values,[float(number)/sum(n) for number in n],width=5)
	#print "patches =" , [patch for patch in patches]
        plt.title("Histogramme PM10 Calcul - 2012")
        plt.xlabel("Valeur")
        plt.ylabel("Frequence")
        plt.show()

    def draw_bar_distribution(self, *args):
	vpm10 = self.interlinear
        import pylab as plt
        from numpy.random import normal
	#gaussian_numbers = normal(size=1000)
	#print gaussian_numbers
	bins_values = range(0,105,5)
        #plt.hist(vpm10,bins=bins_values,normed=1,histtype='bar')
        #plt.hist(vpm10,bins=bins_values)
        #n,bins,patches = plt.hist(vpm10,bins=bins_values)
	plt.figure()
	n,xout,patches = plt.hist(vpm10,bins=bins_values)
	#n,xout,patches = plt.hist(vpm10,bins=20)
	print "n=" ,n, "sum=",sum(n), "len(n)=", len(n)
	print "xout=" ,xout, "len(xout)=", len(xout)
        print [float(number)/sum(n) for number in n]
        plt.title("Histogramme PM10 - 2012")
        plt.xlabel("Valeur")
        plt.ylabel("Nombre de valeurs par intervalle")
        plt.show()


        
        
    def _on_previous(self, evt):
        """ Parcourir la liste """
        if self.nyear == self.premyear:
            return
        else:
            self.compteuryear -= 1
            self.nyear = datayears[self.compteuryear] 
            self.draw()
        evt.Skip()

    def _on_next(self, evt):
        """ Parcourir la liste """
        if self.nyear == self.deryear:
            return
        else:
            #self.njour += 1
            self.compteuryear += 1
            print "self.compteuryear=", self.compteuryear
            print "datayears=", datayears 
            self.nyear = datayears[self.compteuryear] 
            self.draw()
        evt.Skip()


       
        
    
class CanvasFrame(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self,None,-1,
                         'wx_py_aot_pm10_cmp',size=(550,350))

        self.SetBackgroundColour(wx.NamedColor("WHITE"))

        self.figure = Figure(figsize=(5,4), dpi=100)
        #self.figure.clf()
        # une ligne, 2 colonnes (121 et 122)
        #self.axes = self.figure.add_subplot(121)
        #self.figure.add_subplot(122)
        # trois lignes, 1 colonne (311 , 312, 313)

        self.axes = self.figure.add_subplot(111)
        ###self.figure.add_subplot(132)
        ###self.figure.add_subplot(133)

        #print dir(self.figure)
        t = arange(0.0,3.0,0.01)
        s = sin(2*pi*t)
        
        #self.axes.plot(t,s)

        self.canvas = FigureCanvas(self, -1, self.figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.TOP | wx.LEFT | wx.EXPAND)
        # Capture the paint message        
        wx.EVT_PAINT(self, self.OnPaint)        

        self.toolbar = MyNavigationToolbar(self.canvas, True)
        self.toolbar.Realize()
        if wx.Platform == '__WXMAC__':
            # Mac platform (OSX 10.3, MacPython) does not seem to cope with
            # having a toolbar in a sizer. This work-around gets the buttons
            # back, but at the expense of having the toolbar at the top
            self.SetToolBar(self.toolbar)
        else:
            # On Windows platform, default window size is incorrect, so set
            # toolbar width to figure width.
            tw, th = self.toolbar.GetSizeTuple()
            fw, fh = self.canvas.GetSizeTuple()
            # By adding toolbar in sizer, we are able to put it at the bottom
            # of the frame - so appearance is closer to GTK version.
            # As noted above, doesn't work for Mac.
            self.toolbar.SetSize(wx.Size(fw, th))
            self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)

        # update the axes menu on the toolbar
        self.toolbar.update()  
        self.SetSizer(self.sizer)
        self.Fit()


    def OnPaint(self, event):
        self.canvas.draw()
        event.Skip()
        
class App(wx.App):
    
    def OnInit(self):
        'Create the main window and insert the custom frame'
        frame = CanvasFrame()
        #frame.Show(true)
        frame.Show(1)

        return True

app = App(0)
app.MainLoop()

def interact(): 
    # Manière interactive
    import matplotlib
    matplotlib.interactive(True)
    matplotlib.use('WX')
    from matplotlib.pylab import *
    #plot(vaotn[:,heure],vaotn[:,moy],'b+') 
    import time
    for jour in datayears:
        vaotn = getvaotn(jour)
        plot(vaotn[:,heure],vaotn[:,moyaot],'r+') 
        #plot(vaotn[:,heure],vaotn[:,aot675],'b+') 
        xlabel('heure')
        ylabel('AOT')
        time.sleep(5)
        clf()
#plot(vaotn182[:,heure], vaotn182[:,moy],"b+")
#xlabel('hi tinotte')
#print size(vaotn182[:,moy])
