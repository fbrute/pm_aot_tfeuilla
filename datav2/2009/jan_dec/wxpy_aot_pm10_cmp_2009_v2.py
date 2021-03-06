#-*- coding: iso-8859-1 -*-
"""
On cherche � obtenir des donn�es horaire d'�paisseur optiques 
que nous pourrons comparer avec les courbes de rayonnement obtenues par le
traitement des donn�es obtenues par l'inra

"""

import os, sys, string
#from flatten import flatten
#from Numeric import *
from numpy import *
#dirtoconv = os.path.join("C:\\", "pctas_data", "aot_join_pm10_selection_dates",'datav15')
dirtoconv = os.path.join("D:\\", "dvpt", "pm_aot_tfeuilla","datav2","2009","mai_sep")
os.chdir(dirtoconv)

# Valeurs des diff�rentes colonnes
nblignes = 18
g0annee, g0mois, g0jour, g0numjour, g0heure, g0tsv, g0rayglob, g0raydif, g0G0, globM1, globM2, globM3tl2,globM3tl4, globM3tl6, globM4tl2, globM5tl2, gAOT,g0IR = range(nblignes)

class selmat:
    """ Renvoyer un extrait de matrice (array) """
    def __init__(self,sourcemat,lstlimits):
        self.sourcemat = sourcemat
        self.lstlimits = lstlimits


# Les donn�es du photom�tre doivent exister pour pouvoir les comparer
# ce sont donc ces jours seulement que nous consid�rerons
datajours = []

from numpy import *
from pylab import *

datajours = mlab.load("ndays_2009_v2.txt",comments="#")

# comment out the following to use wx rather than wxagg
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg 

from matplotlib.backends.backend_wx import _load_bitmap
from matplotlib.figure import Figure
#from matplotlib.numerix.mlab import rand (plante le 08/01/2013)
import wx



# Inspir� de embedding_in_wx4.py
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

        self.dirjours ={}

        for njour in list(datajours):
            # pour retrouver le jour � partir de la date en clair 
            #self.dirjours[string.strip(datefromday(2005,jour).getString())] = jour
            self.dirjours[self.get_jour_en_clair(njour)] = njour
            
        print self.dirjours
        keys_sort = self.dirjours.keys()
        keys_sort.sort()
        #self.premjour = self.dirjours[keys_sort[0]]
        self.premjour = datajours[0]
        #self.derjour = self.dirjours[keys_sort[len(keys_sort)-1]]
        self.derjour = datajours[len(datajours)-1] 
        self.njour = self.premjour 
        self.compteurjour = 0 

        self.prepdata()
        self.draw()

    def get_tranche(self,asource,heuredeb,heurefin):
        """ R�cup�rer une tranche de donn�es """
        #print "heuredeb:", heuredeb
        #print "heurefin:", heurefin
        res_array = compress(greater_equal(asource[:,heure],float(heuredeb)), asource,0) 
        res_array = compress(less_equal(res_array[:,heure],float(heurefin)), res_array,0) 
        #print "res_array", res_array
        return res_array



    def prepdata(self):
        """ Pr�parer un tableau avec tous les jours de donn�es pour la
        synth�se finale """
        # Pour sauvegarder les donn�es ultimes pr�sent�es
        tot_array_data3 = array([])
        # Colonnes du tableau, tot_array_data
        self.ntyear, self.ntmonth, self.ntday,self.ntjul_day, self.ntpm10,self.ntaot1020 = range(6) 
        self.tot_array_data3 = mlab.load("aot_pm10_daily_average_2009_v2.txt",comments="#", delimiter=",")


    def get_jour_en_clair(self,njour):
        # Pr�parer la liste des jours de donn�es existants 
        from datefromday import datefromday
        return string.strip(datefromday(2005,njour).getString())


    def _on_liste(self, evt):
        """ On choisit le jour � tracer � partir d'une liste """

        dlg = wx.SingleChoiceDialog(
                self, 'Choisir un jour', 'Veuille choisir un jour',
                [self.get_jour_en_clair(njour) for njour in list(datajours)],
                wx.CHOICEDLG_STYLE
                )
        if dlg.ShowModal() == wx.ID_OK:
            #njour = string.atof(dlg.GetStringSelection())
            self.njour = self.dirjours[dlg.GetStringSelection()]
            self.date_en_clair = dlg.GetStringSelection()
        else:
            return
        dlg.Destroy()
        self.draw()

    def draw(self,*args):
        """ Tracer les courbes en fonction de la date choisie """
        self.date_en_clair = self.get_jour_en_clair(self.njour) 
        # get the axes
        ax = self.canvas.figure.axes[0]
        #print dir(ax)
        #ax.set_title("Moyenne AOT (Angstrom) et Global Infrarouge (kW/m2)",fontsize=8)
        # 2�me figure
        #ax2 = self.canvas.figure.axes[1]
        # 3�me figure
        #ax3 = self.canvas.figure.axes[2]


        #self.canvas.figure.clf()
        ax.clear()
        # On trace l'AOT global en fonction de l'AOT1020
        vaot1020 = self.tot_array_data3[:,self.ntaot1020]*100
        vpm10 = self.tot_array_data3[:,self.ntpm10]
        #ax.plot(self.tot_array_data3[:,self.ntaot1020]*100,self.tot_array_data3[:,self.ntpm10],'m.')
	ax.plot(vaot1020,vpm10,'m.')
	print "size(self.tot.array_data3))", len(self.tot_array_data3[:,self.ntaot1020])

	from scipy import stats
        svaot1020 = sort(vaot1020)
	svpm10 = -sort(-vpm10)
        pente, origine, coeffreg = stats.linregress(vaot1020,vpm10)[:3]
	ax.text(40,40,("nombre de points = %d" % len(vaot1020)))
	ax.text(40,30,("pente = %f" % pente))
	ax.text(40,20,("origine = %f" % origine))
	ax.text(40,10,("coeffreg = %f" % coeffreg))

        interlinear = pente*svaot1020 + origine
        ax.plot(svaot1020,interlinear,'-b')

        ax.set_title("PM10 fonction de l' AOT1020*100 (2010,v2 avant selection)",fontsize=8)


        # 2�me figure
        #ax2.clear()

        #ax3.clear()

        self.canvas.draw()

        
    def _on_previous(self, evt):
        """ Parcourir la liste """
        if self.njour == self.premjour:
            return
        else:
            #self.njour -= 1
            self.compteurjour -= 1
            self.njour = datajours[self.compteurjour] 
            self.draw()
        evt.Skip()

    def _on_next(self, evt):
        """ Parcourir la liste """
        if self.njour == self.derjour:
            return
        else:
            #self.njour += 1
            self.compteurjour += 1
            self.njour = datajours[self.compteurjour] 
            self.draw()
        evt.Skip()


       
        
    
class CanvasFrame(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self,None,-1,
                         'CanvasFrame',size=(550,350))

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
    # Mani�re interactive
    import matplotlib
    matplotlib.interactive(True)
    matplotlib.use('WX')
    from matplotlib.pylab import *
    #plot(vaotn[:,heure],vaotn[:,moy],'b+') 
    import time
    for jour in datajours:
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
