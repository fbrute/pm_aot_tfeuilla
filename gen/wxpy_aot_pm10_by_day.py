#-*- coding: iso-8859-1 -*-
"""
On cherche à obtenir des données horaire d'épaisseur optiques 
que nous pourrons comparer avec les courbes de rayonnement obtenues par le
traitement des données obtenues par l'inra

"""

import os, sys, string
# utiliser pycrust

from wx.py.shell import ShellFrame
from wx.py.filling import FillingFrame

#from flatten import flatten
#from Numeric import *
from numpy.oldnumeric import *

from datefromday import datefromday

#naotjours = unique(vaot[:,njour])

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
            if name in ["nyear","Config","datajours","vg0","year","month","day","nday","heure","pm10","aot1020"]:
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

	cid = self.canvas.mpl_connect('button_press_event', self.onclick)
	cid = self.canvas.mpl_connect('key_press_event', self.onkey)

	import MySQLdb

	#self.db = MySQLdb.connect("calamar.univ-ag.fr","dbmeteodb","dbmeteodb","dbmeteodb")
	self.db = MySQLdb.connect("localhost","dbmeteodb","dbmeteodb","dbmeteodb")

	self.cursor = self.db.cursor()

        self.initjour()

        self.draw()

    def initjour(self):
        """ Init days  """
        self.nyear = self.Config.getint("anneesv15","anneedeb")
        self.datajours = self.canvas.GetParent().datajours
	#print "def initjour"
	#print "self.datajours =",self.datajours
        self.dirjours ={}

        for jour in self.datajours:
            # pour retrouver le jour à partir de la date en clair 
            self.dirjours[string.strip(datefromday(self.nyear,jour).getString())] = jour
            #self.dirjours[self.get_jour_en_clair(njour)] = njour
            
        #print "initjour :: self.dirjours",self.dirjours
        keys_sort = self.dirjours.keys()
        keys_sort.sort()
        #self.premjour = self.dirjours[keys_sort[0]]
        #self.nyear = self.Config.getint("annee","annee")

        self.premjour = self.datajours[0]
        #self.derjour = self.dirjours[keys_sort[len(keys_sort)-1]]
        self.derjour = self.datajours[len(self.datajours)-1] 
        #self.derjour = 365 
        self.njour = self.premjour 
        self.compteurjour = 0 
 

    def get_jour_en_clair(self,njour):
        # Préparer la liste des jours de données existants 
        from datefromday import datefromday
        string.strip(datefromday(self.nyear,njour).getString())
        return string.strip(datefromday(self.nyear,njour).getString())

    def get_string_day(self,njour):
        from datefromday import datefromday
	nweekday = datefromday(self.nyear,njour).get_day_of_week()
	return nweekday




    def _on_liste(self, evt):
        """ On choisit le jour à tracer à partir d'une liste """

        self.datajours = self.canvas.GetParent().datajours

        dlg = wx.SingleChoiceDialog(
                self, 'Choisir un jour', 'Veuille choisir un jour',
                [self.get_jour_en_clair(njour) for njour in list(self.datajours)],
                wx.CHOICEDLG_STYLE
                )
        if dlg.ShowModal() == wx.ID_OK:
            #njour = string.atof(dlg.GetStringSelection())
            self.njour = self.dirjours[dlg.GetStringSelection()]
            self.date_en_clair = dlg.GetStringSelection()
            # Retrouver le rang du jour pour mettre à jour le compteur
            indice = 0
            for jour in self.datajours:
                if jour == self.njour:
                    self.compteurjour = indice 
                indice +=1
        else:
            return
        dlg.Destroy()
        self.draw()

    def getvg0n(self,nday):
        """Select a day of data """
        return compress(equal(self.vg0[:,self.nday],nday),self.vg0,0)

    def draw(self,*args):
        """ Tracer les courbes en fonction de la date choisie """
        #print "draw ..."
	self.vg0 = self.canvas.GetParent().vg0 
	self.date_en_clair = self.get_jour_en_clair(self.njour) 
	jour_en_clair = self.get_string_day(self.njour)
	#jour_en_clair = " a definir" 
	print "jour en clair =", jour_en_clair
        # get the axes
        ax = self.canvas.figure.axes[0]

	#print "draw::self.njour"
	#print self.njour
        vg0n = self.getvg0n(self.njour)
	#print "draw::vg0n"
	#print vg0n

        #print "draw::vg0"
	#print self.vg0
               
        ax.clear()
        #ax2.set_title("Clair(bleu)/Moyen(magenta)/Pollue(rouge)/G0(noir) , le %s " % date_en_clair,fontsize=8)
        ax.set_xlabel('Heure locale',fontsize=14)
        #ax.set_xlabel('local hour',fontsize=14)
        #ax2.set_ylabel('Rayonnement global',fontsize=8)
        #ax.set_title('Rayonnement global (W/m2), le %s (jour %d)' % (self.date_en_clair, self.njour),fontsize=8)
        #ax.set_title('Rayonnement global (W/m2), le %s ' % self.date_en_clair,fontsize=16)

        #ax.set_title('AOT*100 (vert) et PM10 (bleu) le %s (jour %d, %s)' % (self.date_en_clair,self.njour,jour_en_clair),fontsize=16)

        #ax.set_title('AOT*100 (vert) et PM10 (bleu) le %s (jour %d, %s)' % ("jour","jour"),fontsize=16)
        #ax.set_title('AOT*100 (vert) et PM10 (bleu) le %s (jour %s, %s)' % ("jour","jour","jour"),fontsize=16)

        #ax.set_title('AOT*100 (vert) et PM10 (bleu) le %s (jour %d, %s)' % (self.date_en_clair,self.njour,jour_en_clair),fontsize=16)
	self.date = "%02d/%02d/%04d" % (int(vg0n[0,self.day]) , int(vg0n[0,self.month]) , int(vg0n[0,self.year]))
	#self.date=  str(int(vg0n[0,self.day])) + '/' +  str(int(vg0n[0,self.month])) + '/' +  str(int(vg0n[0,self.year]))

        ax.set_title('AOT*100 (vert) et PM10 (bleu) le %s (jour %d, %s)' % (self.date,self.njour,jour_en_clair),fontsize=16)

        # Print aot1020 
        #ax.plot(vg0n[:,self.heure],vg0n[:,self.aot1020]*100,'g+')
        #self.mpl_connect('button_press_event', onclick)
	#if size(vg0n) > 0 :
        ax.plot(vg0n[:,self.heure],vg0n[:,self.aot1020]*100,color='green', marker='o', markersize=12,linestyle='none')


        #ax2.plot(vg0n[:,g0heure],vg0n[:,globM3tl2],'-g')
        #ax2.plot(vg0n[:,g0heure],vg0n[:,globM3tl4],'-m')
        #ax2.plot(vg0n[:,g0heure],vg0n[:,globM3tl6],'-r')
        #ax2.plot(vg0n[:,g0heure],vg0n[:,globM1],'-k')

        #ax.plot(vg0n[:,g0heure],vg0n[:,globM5tl2],'-m')
        #ax2.plot(vg0n[:,g0tsv],vg0n[:,globM4tl2],'-g')
        #ax2.plot(vg0n[:,g0heure],vg0n[:,globM5tl2],'-m')
        #ax2.plot(vg0n[:,g0tsv],vg0n[:,globM5tl2],'-m')

        # Print PM10 
	#if size(vg0n) > 0 :
        ax.plot(vg0n[:,self.heure],vg0n[:,self.pm10],color='blue', marker='o',
			markersize=12,linestyle='none')

        #ax.text(10,290,'-', fontsize=16,color='k')
        #ax.text(10.2,280,'G0', fontsize=12,color='k')
        #ax.text(10.2,280,'out of atmosphere global radiation', fontsize=12,color='k')

        #ax.text(10.2,240,'Mesure', fontsize=12,color='b')
        #ax.text(10,250,'-', fontsize=16,color='k')
        #ax.text(10.2,240,'direct radiation (measurements)', fontsize=12,color='b')

        #ax.text(10,210,'-', fontsize=16,color='g')
        #ax.text(10.2,200,'Modele ciel clair Hottel', fontsize=12,color='g')
        #ax.text(10.2,200,'direct radiation for a clear day  (Hottel model)', fontsize=12,color='g')

        #ax.text(10,170,'-', fontsize=16,color='m')
        #ax.text(10.2,160,'global AOT*1000', fontsize=12,color='m')
	#cid = self.canvas.mpl_connect('button_press_event', self.onclick)
        self.canvas.draw()

    def onclick(self,event):
	""" Ajouter et retirer la date et l'heure à ex_date_hour 
	    double click gauche pour ajouter, double click droit pour supprimer"""
	if event.dblclick :
	    date = self.date
	    heure = round(event.xdata)
	    annee = int(str(date[6:]))
	    mois = int(str(date[3:][:2]))
	    jour = int(str(date[0:][:2]))
	    success_message = ''
	    sql = ''
	    if event.button == 1:	
	        sql = "INSERT INTO ex_date_hour VALUES (%d,%d,%d,%d)" % (annee, mois, jour, heure) 
	        success_message = "Date du %s a %dh ajoutee a ex_date_hour" % (date, heure)

	    if event.button == 3:	
	        sql = "DELETE FROM ex_date_hour WHERE (year,month,day,hour) = (%d,%d,%d,%d)" % (annee, mois, jour, heure) 
	        success_message = "Date du %s a %dh supprimee de ex_date_hour" % (date, heure)

	    try:
	        self.cursor.execute(sql)
		self.db.commit()
	        print success_message 
	    except e:
		db.lrollback()
		print e
		#print "requete non executee"


    def onkey(self,event):
	""" Ajouter ou supprimer la date à la table ex_dates """
	#print dir(event)
	evt = event.key
	if evt == 'ctrl+d' or evt == 'ctrl+s':
	    date = self.date
	    date_mysql = str(date[6:]) + '-' + str(date[3:][:2])+ '-' +str(date[0:][:2])
	    print date_mysql
	    success_message = ''

            if evt == 'ctrl+d':	
	        sql = "INSERT INTO ex_dates VALUES ('%s')" % date_mysql
	        success_message = "Date du %s ajoutee a ex_dates" % date
	    if evt == 'ctrl+s' :
	        sql = "DELETE FROM ex_dates WHERE date = '%s'" % date_mysql
	        success_message = "Date du %s supprimee de ex_dates" % date

	    try:
	        self.cursor.execute(sql)
		self.db.commit()
	        print success_message 
	    except e:
		db.rollback()
		print e
		#print "requete non executee"


        
    def _on_previous(self, evt):
        """ Parcourir la liste """
        if self.njour == self.premjour:
            return
        else:
            #self.njour -= 1
            self.compteurjour -= 1
            self.njour = self.datajours[self.compteurjour] 
            self.draw()
        evt.Skip()

    def _on_next(self, evt):
        """ Parcourir la liste """
        if self.njour == self.derjour:
            return
        else:
            #self.njour += 1
            self.compteurjour += 1
            self.njour = self.datajours[self.compteurjour] 
            self.draw()
        evt.Skip()

    def save(self,evt):
        """ Save figure without prompting for a location """
        dirname = "d:\\dvpt\\pm_aot_tfeuilla\\gen"
        filename = "g" + str(self.njour) + ".png"
        self.canvas.print_figure(os.path.join(dirname,filename))


       

class ParmDialog(wx.Dialog):
    """ Parameters Dialog """
    def __init__(self,selframe):
        self.Config = selframe.Config
        self.ReadConfig = selframe.ReadConfig
        #self.nyear = selframe.nyear
        self.bChangeConfig = selframe.bChangeConfig

        wx.Dialog.__init__(self, None, -1, "Parameters", size = (400,400))

        sizer = wx.FlexGridSizer(rows=6, cols=2, hgap=5, vgap=5)
        sizer.AddGrowableCol(0,proportion=0)
        # Customize border to get oxygene between widgets
        flagvalue = wx.ALL
        bordervalue = 5

	sizer.Add(wx.StaticText(self,-1,"Select year"),flag=wx.LEFT,border=bordervalue)
        self.dpcdeb = dpcdeb = wx.SpinCtrl(self, -1,"", (50, 30) )
        dpcdeb.SetRange(2005,2012)
	sizer.Add(dpcdeb,flag=wx.RIGHT,border=bordervalue)

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

        dpcdeb.SetValue(self.Config.getint("anneesv15","anneedeb"))

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
        self.Config.set("anneesv15","anneedeb",self.dpcdeb.GetValue())
        self.Config.write(open("params.ini","w"))
        evt.Skip()

    
class CanvasFrame(wx.Frame):
    """ Classe CanvasFrame """
    
    def __init__(self):
        wx.Frame.__init__(self,None,-1,
                         'wxpy_aot_pm10_by_day.py',size=(550,350))

        self.SetBackgroundColour(wx.NamedColor("WHITE"))

        self.figure = Figure(figsize=(5,4), dpi=100)
        self.initdir = "d:\\dvpt\\pm_aot_tfeuilla\\gen"

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

        #self.mpl_connect('button_press_event', onclick)
        #self.Bind(wx.EVT_BUTTON, self.OnOk, okButton)


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
	print "CanvasFrame::init::call self.InitConfig()"
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
	self.ReadConfig()

    def ReadConfig(self):
	""" Gestion des paramètres """
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

        self.nyear = self.Config.getint("anneesv15","anneedeb")
	print "PrepData"
	print self.nyear

        # On crée une matrice avec les données déjà traitées par g0ascci.py
        dirtoconv = os.path.join("D:\\", "dvpt", "pm_aot_tfeuilla","gen")
        os.chdir(dirtoconv)
        # On récupère les entêtes (5ème ligne => indice 4)
        #vheaders = aaotlines[4].split(",") 
        # Valeurs des différentes colonnes
        lstdata = """year month day nday heure pm10 aot1020 aot870 aot675 aot440""".split()
        indice=0
        # Chaque colonne reçoit son rang ...
        #print lstdata
        for namevalue in lstdata:
            setattr(self, namevalue ,indice)
            indice+=1

        from numpy import *
        from pylab import *
        #self.vg0 = vg0 = load("g0.txt",comments="#", delimiter=",") plante le 08/01/2013
        self.vg0 = vg0 = mlab.load("aot_pm_hourly.txt",comments="#", delimiter=",")

        # On récupère les paramètres en cours
        #if self.bChangeConfig : 
        #    self.Config.readfp(open(os.path.join(initdir,"pctas.ini")))

        from dayfromdate import dayfromdate 
        self.datedeb = self.Config.get("dates","datedeb")+'/'+str(self.nyear)
	"print self.datedeb,self.datefin"
	print self.datedeb

        d,m,y= [int(value) for value in self.datedeb.split('/')]
        self.jourdeb = dayfromdate(y,m,d).getnDay() 

        self.datefin = self.Config.get("dates","datefin")+'/'+str(self.nyear)
	print self.datefin

        d,m,y= [int(value) for value in self.datefin.split('/')]
        self.jourfin = dayfromdate(y,m,d).getnDay() 


        # On limite les données à l'année choisie
        vg0 = compress(equal(vg0[:,self.year],self.nyear),vg0,0)
	# récupérer les numéros de jours 
        #self.datajours = self.unique(self.vg0[:,self.nday])
        self.datajours = self.unique(vg0[:,self.nday])
	#print "self.datajours, apres self.unique"
	#print self.datajours
	#print "len", len(self.datajours)
        self.datajours = [njour for njour in self.datajours if njour >= self.jourdeb
			and njour <= self.jourfin ]
	self.datajours.sort()
        # On limite les données aux jours choisis
        print "self.jourdeb", self.jourdeb
        print "self.jourfin", self.jourfin
        vg0 = compress(greater(vg0[:,self.nday],self.jourdeb-1),vg0,0)
        vg0 = compress(less(vg0[:,self.nday],self.jourfin+1),vg0,0)

        #self.datajours = mlab.load("ndays.txt",comments="#")
        #self.datajours = {} 
        #self.datajours = range (self.jourdeb, self.jourfin + 1)
	print "self.datajours"
	#print self.datajours

        self.heuredeb = self.Config.getint("heures","heuredeb")
        self.heurefin = self.Config.getint("heures","heurefin")

        
        # On limite les données aux heures choisies, déjà fait dans la requête sql
	#vg0 = compress(greater(vg0[:,self.g0tsv],self.heuredeb),vg0,0)
        #vg0 = compress(less(vg0[:,self.g0tsv],self.heurefin),vg0,0)

        self.vg0 = vg0
	#print "PrepData::vg0"
	#print vg0

        # On exécute g0ascii qui prépare les données de l'inra
        #if self.bChangeDates:
        #    print "exécuter g0ascii.py"
        #    os.chdir('c:\\pctas_tools')
        #    os.system('g0ascii.py')


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
        dialog = ParmDialog(self)
        result = dialog.ShowModal()
        if result == wx.ID_OK:
            # Update display
            self.ReadConfig()
            self.PrepData()
            self.toolbar.initjour()
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

