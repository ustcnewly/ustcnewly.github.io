# Chapter 4: An Applications Building Blocks, Advanced Controls
# Recipe 7: FlatNotebook
#
import wx
import wx.lib
import wx.lib.flatnotebook as FNB

#---- Recipe Code ----#

class MyFlatNotebook(FNB.FlatNotebook):
    def __init__(self, parent):
        mystyle = FNB.FNB_DROPDOWN_TABS_LIST|\
                  FNB.FNB_FF2|\
                  FNB.FNB_SMART_TABS|\
                  FNB.FNB_X_ON_TAB
        super(MyFlatNotebook, self).__init__(parent,
                                             style=mystyle)

        # Attributes
        self._imglst = wx.ImageList(16, 16)

        # Setup
        bmp = wx.Bitmap("text-x-generic.png")
        self._imglst.Add(bmp)
        bmp = wx.Bitmap("text-html.png")
        self._imglst.Add(bmp)
        self.SetImageList(self._imglst)

        # Event Handlers
        self.Bind(FNB.EVT_FLATNOTEBOOK_PAGE_CLOSING, self.OnClosing)

    def OnClosing(self, event):
        """Called when a tab is closing"""
        page = self.GetCurrentPage()
        if page and hasattr(page, "IsModified"):
            if page.IsModified():
                r = wx.MessageBox("Warning unsaved changes will be lost",
                                  "Close Warning",
                                  wx.ICON_WARNING|wx.OK|wx.CANCEL)
                if r == wx.CANCEL:
                    event.Veto()

#---- End Recipe Code ----#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="FlatNotebook", size=(500,350))
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MyFrame, self).__init__(*args, **kwargs)

        # Attributes
        self.panel = MyPanel(self)

        # Setup
        menub = wx.MenuBar()
        fmenu = wx.Menu()
        fmenu.Append(wx.ID_NEW, "New Tab\tCtrl+N")
        menub.Append(fmenu, "File")
        self.SetMenuBar(menub)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # Event Handlers
        self.Bind(wx.EVT_MENU, lambda event: self.panel.NewTab(), id=wx.ID_NEW)
        
class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        # Attributes
        self.nb = MyFlatNotebook(self)

        # Setup / Add pages to notebook
        for x in range(4):
            txt = wx.TextCtrl(self.nb)
            self.nb.AddPage(txt, "Page %d" % x, imageId=x%2)

        # Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def NewTab(self):
        txt = wx.TextCtrl(self.nb)
        num = self.nb.GetPageCount()
        self.nb.AddPage(txt, "Page %d" % num, imageId=num%2)

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
