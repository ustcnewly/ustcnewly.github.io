# Chapter 4: An Applications Building Blocks, Advanced Controls
# Recipe 9: FoldPanelBar
#
import wx
import wx.lib.foldpanelbar as foldpanel
import wx.lib.colourselect as colourselect

#---- Recipe Code ----#

class FoldPanelMgr(foldpanel.FoldPanelBar):
    """Fold panel that manages a collection of Panels"""
    def __init__(self, parent, *args, **kwargs):
        super(FoldPanelMgr, self).__init__(parent,
                                           *args,
                                           **kwargs)

    def AddPanel(self, pclass, title=u"", collapsed=False):
        """Add a panel to the manager
        @param pclass: Class constructor (callable)
        @keyword title: foldpanel title
        @keyword collapsed: start with it collapsed
        @return: pclass instance
        """
        fpitem = self.AddFoldPanel(title, collapsed=collapsed)
        wnd = pclass(fpitem)
        best = wnd.GetBestSize()
        wnd.SetSize(best)
        self.AddFoldPanelWindow(fpitem, wnd)
        return wnd

#---- End Recipe Code ----#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="FoldPanelBar", size=(500, 500))
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MyFrame, self).__init__(parent, *args, **kwargs)

        # Attributes
        self.panel = MyMainPanel(self)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
class MyMainPanel(wx.Panel):
    def __init__(self, parent):
        super(MyMainPanel, self).__init__(parent)

        # Attributes
        self.fpb = FoldPanelMgr(self)

        # Setup
        self.fpb.AddPanel(PalletPanel, "Pallet")
        files = self.fpb.AddPanel(FilesPanel, "Files", True)
        spaths = wx.StandardPaths.Get()
        files.ExpandPath(spaths.GetDocumentsDir())
        files.SetSize((-1, 300))
        self.fpb.AddPanel(OptionPanel, "Options")

        # Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fpb.SetSize((250, -1))
        sizer.Add(self.fpb, 0, wx.EXPAND)
        tctrl = wx.TextCtrl(self, value="Main content area",
                            style=wx.TE_MULTILINE)
        sizer.Add(tctrl, 1, wx.EXPAND)
        self.SetSizer(sizer)

class OptionPanel(wx.Panel):
    def __init__(self, parent):
        super(OptionPanel, self).__init__(parent)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        for cb in range(6):
            cbox = wx.CheckBox(self, label="Option %d" % cb)
            sizer.Add(cbox, 0, wx.TOP, 5)
        self.SetSizer(sizer)

class FilesPanel(wx.GenericDirCtrl):
    def __init__(self, parent):
        super(FilesPanel, self).__init__(parent)

class PalletPanel(wx.Panel):
    def __init__(self, parent):
        super(PalletPanel, self).__init__(parent)

        # Layout
        gsizer = wx.GridSizer(4, 3, 2, 2)
        for colour in ("red", "green", "blue", "yellow",
                       "purple", "black", "white", "pink",
                       "orange", "grey", "navy", "cyan"):
            cobj = wx.NamedColour(colour)
            cs = colourselect.ColourSelect(self, colour=cobj, size=(20, 20))
            gsizer.Add(cs)
        self.SetSizer(gsizer)

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
