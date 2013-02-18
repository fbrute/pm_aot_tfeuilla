#-*- coding: iso-8859-1 -*-
"""
On étudie la relation entre PM10 et épaisseur optique, notamment lors
de la présence de poussières, sur une année
"""

import os, sys, string
# utiliser pycrust

from wx.py.shell import ShellFrame
from wx.py.filling import FillingFrame

#from flatten import flatten
#from Numeric import *
from numpy.oldnumeric import *

#naotjours = unique(vaot[:,njour])

#datamois = []
#datamois = mlab.load("ndays.txt",comments="#")
#datamois = ['Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Décembre'] 

# Sélection encore plus fine :
#naotjours  = [184,200,205,207,208,211,214,215,216]

#vaotn = getvaotn(220)
#print vaot[:,njour]
#print vaotn182


class selmat:
    
    """ Renvoyer un extrait de matrice (array) """
    def __init__(self,sourcemat,lstlimits):
        self.sourcemat = sourcemat
        self.lstlimits = lstlimits


# comment out the following to use wx rather than wxagg
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg 

from matplotlib.backends.backend_wx import _load_bitmap
from matplotlib.figure import Figure
#from matplotlib.numerix.mlab import rand, plante le 8/01/2013

import wx
import ConfigParser



# Inspiré de embedding_in_wx4.py
class MyNavigationToolbar(NavigationToolbar2WxAgg):
    """
    Extend the default wx toolbar with your own event handlers
    """
    #ON_CUSTOM = wx.NewId()
    def __init__(self, canvas, cankill):
        NavigationToolbar2WxAgg.__init__(self, canvas)
        self.canvas = canvas
        #setattr(self,'datajours', getattr(canvas.GetParent(),'datajours'))
        for name in dir(canvas.GetParent()):
	    #print "name= :", name
            if name in ["datamois","vg0","vg0_2","year","month","day","nday","pm10","aot1020"]:
                setattr(self,name,getattr(canvas.GetParent(),name))
	
       

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
	
	self.initmois()
        
        self.draw()

    def initmois(self):
        """ Init months  """
	self.dirmois={}

	self.datamois = [1,2,3,4,5,6,7,8,9,10,11,12] 

        for nmois in list(self.datamois):
            self.dirmois[self.get_mois_en_clair(nmois)] = nmois
            
        #print "self.dirmois=", self.dirmois
        keys_sort = self.dirmois.keys()
        keys_sort.sort()

	self.premmois = self.datamois[0]
	self.dermois = self.datamois[len(self.datamois)-1]
        self.nmois = 0 
        self.compteurmois = 0 
 

    def get_jour_en_clair(self,njour):
        # Préparer la liste des jours de données existants 
        from datefromday import datefromday
        string.strip(datefromday(2009,njour).getString())
        return string.strip(datefromday(2009,njour).getString())

    def get_mois_en_clair(self,nmois):
	    """ Renvoyer le mois en texte à partir du n°"""
	    if nmois == 1:
		    return "Janvier"
	    if nmois == 2:
		    return "Fevrier"
	    if nmois == 3:
		    return "Mars"
	    if nmois == 4:
		    return "Avril"
	    if nmois == 5:
		    return "Mai"
	    if nmois == 6:
		    return "Juin"
	    if nmois == 7:
		    return "Juillet"
	    if nmois == 8:
		    return "Aout"
	    if nmois == 9:
		    return "Septembre"
	    if nmois == 10:
		    return "Octobre"
	    if nmois == 11:
		    return "Novembre"
	    if nmois == 12:
		    return "Decembre"



    def get_string_day(self,njour):
        from datefromday import datefromday
	nweekday = datefromday(2009,njour).get_day_of_week()
	return nweekday


    def _on_liste(self, evt):
        """ On choisit le jour à tracer à partir d'une liste """

        #self.datamois = self.canvas.GetParent().datamois
	#print "_on_liste : self.datamois = %s",self.datamois

        dlg = wx.SingleChoiceDialog(
                self, 'Choisir un mois', 'Veuille choisir un mois',
                [str(nmois) for nmois in list(self.datamois)],
                wx.CHOICEDLG_STYLE
                )
        if dlg.ShowModal() == wx.ID_OK:
            #njour = string.atof(dlg.GetStringSelection())
            self.nmois = int(self.dirmois[dlg.GetStringSelection()])
            # Retrouver le rang du jour pour mettre à jour le compteur
            indice = 0
            for mois in self.datamois:
                if mois == self.nmois:
                    self.compteurmois = indice 
                indice +=1
        else:
            return
        dlg.Destroy()
        self.draw()

    def getvg0n(self,nday):
        """Select a day of data """
        return compress(equal(self.vg0[:,self.nday],nday),self.vg0,0)

    def getvg0_month(self,nmonth):
        """Select a month of data """
        return compress(equal(self.vg0[:,self.month],nmonth),self.vg0,0)

    def getvg0_2_month(self,nmonth):
        """Select a month of data """
        return compress(equal(self.vg0_2[:,self.month],nmonth),self.vg0_2,0)

    def draw(self,*args):
        """ Tracer les courbes en fonction de la date choisie """
        #print "draw ..."
	self.vg0 = self.canvas.GetParent().vg0 
        # get the axes
        ax = self.canvas.figure.axes[0]

        #vg0n = self.getvg0_month(self.nmois)
        #vg0n = self.getvg0_month(self.month)

	#self.nmois=5
	#print self.nmois

        #vg0n = self.getvg0_month(self.nmois)
        #vg0n_2 = self.getvg0_2_month(self.nmois)
                
        ax.clear()
        ax.set_xlabel('Jour',fontsize=14)

        ax.set_title('AOT*100 (vert) et PM10 (bleu) - Annee 2009 ' ,fontsize=16)

        # Print PM10 
	if size(self.vg0_2) > 0:
		ax.plot(self.vg0_2[:,self.nday],self.vg0_2[:,self.pm10],color='blue', 
			linestyle='-')

	# Print aot1020
	if size(self.vg0) > 0:
		ax.plot(self.vg0[:,self.nday],self.vg0[:,self.aot1020]*100,color='green',
			linestyle='-')


	ax.grid(b='true', which='major',color='black',linestyle='-',linewidth=0.5)

	#ax.set_xticks(range(32)[1:32])



	#print dir(ax)
        self.canvas.draw()


        
    def _on_previous(self, evt):
        """ Parcourir la liste """
        if self.nmois == self.premmois:
            return
        else:
            self.compteurmois -= 1
            self.nmois = self.datamois[self.compteurmois] 
            self.draw()
        evt.Skip()

    def _on_next(self, evt):
        """ Parcourir la liste """
        if self.nmois == self.dermois:
            return
        else:
            self.compteurmois += 1
            self.nmois = self.datamois[self.compteurmois] 
            self.draw()
        evt.Skip()

    def save(self,evt):
        """ Save figure without prompting for a location """
        dirname = "d:\\dvpt\\pm_aot_tfeuilla\\datav2\\2009\\jan_dec"
        filename = "g" + str(self.njour) + ".png"
        self.canvas.print_figure(os.path.join(dirname,filename))


       

class ParmDialog(wx.Dialog):
    """ Parameters Dialog """
    def __init__(self,selframe):
        self.Config = selframe.Config
        self.InitConfig = selframe.InitConfig
        self.bChangeConfig = selframe.bChangeConfig

        wx.Dialog.__init__(self, None, -1, "Parameters", size = (400,400))

        sizer = wx.FlexGridSizer(rows=6, cols=2, hgap=5, vgap=5)
        sizer.AddGrowableCol(0,proportion=0)
        # Customize border to get oxygene between widgets
        flagvalue = wx.ALL
        bordervalue = 5

        #sizer.Add(wx.StaticText(self,-1,"Date de debut"),border=5)
        sizer.Add(wx.StaticText(self,-1,"First Date"),flag=wx.LEFT,border=bordervalue)
        self.dpcdeb = dpcdeb = wx.DatePickerCtrl(self, size=(120,-1),
            style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        sizer.Add(dpcdeb,flag=flagvalue,border=bordervalue)

        #sizer.Add(wx.StaticText(self,-1,"Date de fin"))
        sizer.Add(wx.StaticText(self,-1,"Last Date"),flag=wx.LEFT,border=bordervalue)
        self.dpcfin = dpcfin =  wx.DatePickerCtrl(self, size=(120,-1),
            style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        sizer.Add(dpcfin,flag=wx.RIGHT,border=bordervalue)


        #sizer.Add(wx.StaticText(self,-1,"Heure de debut"))
        sizer.Add(wx.StaticText(self,-1,"First Hour"),flag=wx.LEFT,border=bordervalue)
        self.spinheuredeb = spinheuredeb =  wx.SpinCtrl(self, -1,"", (50, 30) )
        spinheuredeb.SetRange(6,18)
        sizer.Add(spinheuredeb,flag=wx.RIGHT,border=bordervalue)

        #sizer.Add(wx.StaticText(self,-1,"Heure de fin"))
        sizer.Add(wx.StaticText(self,-1,"Last Hour"),flag=wx.LEFT,border=bordervalue)
        self.spinheurefin = spinheurefin =  wx.SpinCtrl(self, -1,"", (50, 30) )

        spinheurefin.SetRange(6,18)
        sizer.Add(spinheurefin,flag=wx.RIGHT,border=bordervalue)

        # Opérer une séparation
        sizer.Add((0,0))
        sizer.Add((0,0))

        okButton = wx.Button(self,wx.ID_OK, "OK")
        okButton.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.OnOk, okButton)
        sizer.Add(okButton)

        cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel")
        #self.Bind(wx.EVT_BUTTON, self.OnCancel, cancelButton)
        sizer.Add(cancelButton)

        # ON récupère les valeurs en cours
        import string

        d,m,y = [string.atof(value) for value in self.Config.get("dates","datedeb").split("/")]
        dpcdeb.SetValue(wx.DateTimeFromDMY(d,m-1,y))

        d,m,y = [string.atof(value) for value in self.Config.get("dates","datefin").split("/")]
        dpcfin.SetValue(wx.DateTimeFromDMY(d,m-1,y))

        spinheuredeb.SetValue(self.Config.getint("heures","heuredeb"))
        spinheurefin.SetValue(self.Config.getint("heures","heurefin"))

        self.SetSizer(sizer)
        self.Fit()

    def FormatDate(self,date):
        """ Format date correctly """
        lstdate = str(date).split('/')[:3]
        # GetValue does not return century
        return lstdate[1]+ "/" + lstdate[0] + "/" + "20" + lstdate[2][:2]


    def OnCancel(self,evt):
        self.Close(1)

    def OnOk(self,evt):
        """ Confirm parameters """
        self.bChangeConfig = 1
        self.Config.set("dates","datedeb",self.FormatDate(self.dpcdeb.GetValue()))
        self.Config.set("dates","datefin",self.FormatDate(self.dpcfin.GetValue()))

        self.Config.set("heures","heuredeb",self.spinheuredeb.GetValue())
        self.Config.set("heures","heurefin",self.spinheurefin.GetValue())
        self.Config.write(open("params.ini","w"))
        self.InitConfig()
        evt.Skip()

    
class CanvasFrame(wx.Frame):
    """ Classe CanvasFrame """
    
    def __init__(self):
        wx.Frame.__init__(self,None,-1,
                         'CanvasFrame',size=(550,350))

        self.SetBackgroundColour(wx.NamedColor("WHITE"))

        self.figure = Figure(figsize=(5,4), dpi=100)
        self.initdir = "d:\\dvpt\\pm_aot_tfeuilla\\datav2\\2009\\jan_dec"

        # Un petit menu pour pycrust
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        exit = menu1.Append(wx.NewId(), "&Exit", "Quit the program")
        menuBar.Append(menu1, "&File")
        menu2 = wx.Menu()
        menu2.Append(wx.NewId(), "&Copy", "Copy in status bar")
        menu2.Append(wx.NewId(), "C&ut", "")
        menu2.Append(wx.NewId(), "Paste", "")
        menu2.AppendSeparator()
        option = menu2.Append(wx.NewId(), "&Options...", "Display Options")
        menuBar.Append(menu2, "&Edit")

        menu3 = wx.Menu()
        shell = menu3.Append(-1, "&Python shell",
                             "Open Python shell frame")
        filling = menu3.Append(-1, "&Namespace viewer",
                               "Open namespace viewer frame")
        menuBar.Append(menu3, "&Debug")

        self.Bind(wx.EVT_MENU, self.OnShell, shell)
        self.Bind(wx.EVT_MENU, self.OnFilling, filling)
        self.Bind(wx.EVT_MENU, self.OnExit, exit)
        self.Bind(wx.EVT_MENU, self.OnOptions, option)


        self.SetMenuBar(menuBar)

        self.figure.add_subplot(111)

        self.canvas = FigureCanvas(self, -1, self.figure)

        #self.Bind(wx.EVT_LEFT_DOWN,self.OnClicked)
        self.Bind(wx.EVT_MOUSE_EVENTS,self.OnClicked,self.canvas)
        #self.Bind(wx.EVT_IDLE,self.OnClicked)
        #self.Bind(wx.EVT_CHAR, self.OnClicked)
        #self.Bind(wx.EVT_ENTER_WINDOW, self.OnClicked)


        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.TOP | wx.LEFT | wx.EXPAND)

        # Capture the paint message        
        wx.EVT_PAINT(self, self.OnPaint)        

        self.InitConfig()
        self.bChangeConfig = 0 
        # Préparer les données
        self.PrepData()

        # Préparer la barre de navigation
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

    def InitConfig(self):
        # On regarde les paramètres initiaux (fichier pctas.ini)
        self.Config = ConfigParser.ConfigParser()
        self.Config.readfp(open(os.path.join(self.initdir,"params.ini")))


    def unique(self,a):
        """ Renvoie un vecteur contenant les valeurs uniques d'un vecteur  """
        a_unik = []
        for value in a:
            if value not in a_unik:
                a_unik.append(value)
        return array(a_unik)



    def PrepData(self):
        """ Prepare data before plotting """
        dirtoconv = os.path.join("D:\\", "dvpt", "pm_aot_tfeuilla","datav2","2009","jan_dec")
        os.chdir(dirtoconv)
        # On récupère les entêtes (5ème ligne => indice 4)
        #vheaders = aaotlines[4].split(",") 
        # Valeurs des différentes colonnes
        lstdata = """year month day nday aot1020 aot870 aot675 aot440""".split()
        indice=0
        # Chaque colonne reçoit son rang ...
        #print lstdata
        for namevalue in lstdata:
            setattr(self, namevalue ,indice)
            indice+=1

	# meme colonne pour aot1020 et pm10
	self.pm10 = self.aot1020

        from numpy import *
        from pylab import *
        #self.vg0 = vg0 = load("g0.txt",comments="#", delimiter=",") plante le 08/01/2013
        self.vg0 = vg0 = mlab.load("aot_daily_average_2009_v2.txt",comments="#", delimiter=",")
        self.vg0_2 = vg0_2 = mlab.load("pm_daily_average_2009_v2.txt",comments="#", delimiter=",")



        # On récupère les paramètres en cours
        #if self.bChangeConfig : 
        #    self.Config.readfp(open(os.path.join(initdir,"pctas.ini")))
	print sys.path

        from dayfromdate import dayfromdate 
        self.moisdeb = self.Config.get("mois","moisdeb")
        self.moisfin = self.Config.get("mois","moisfin")

        self.vg0 = vg0

    def OnClicked(self,event):
        #print "ruse"
        dlg = wx.MessageDialog(self, str(evt.inaxes),
                               'A Message Box',
                               wx.OK | wx.ICON_INFORMATION
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()
        evt.Skip()


    def OnPaint(self, event):
        self.canvas.draw()
        event.Skip()

    def OnShell(self,event):
        """ Shell pycrust """
        frame = ShellFrame(parent=self)
        frame.Show()

    def OnFilling(self,event):
        """ Browser pycrust """
        frame = FillingFrame(parent=self)
        frame.Show()


    def OnExit(self,event):
        self.Close(1)

    def OnOptions(self,event):
        """ Parameters Dialog Handler """
        self.InitConfig()
        dialog = ParmDialog(self)
        result = dialog.ShowModal()
        if result == wx.ID_OK:
            # Update display
            self.InitConfig()
            self.PrepData()
            self.toolbar.initmois()
            self.toolbar.draw()
        dialog.Destroy()



        
class App(wx.App):
    
    def OnInit(self):
        'Create the main window and insert the custom frame'
        frame = CanvasFrame()
        #frame.Show(true)
        frame.Show(1)

        return True

#app = App(0)
app = App(redirect=False)
app.MainLoop()

