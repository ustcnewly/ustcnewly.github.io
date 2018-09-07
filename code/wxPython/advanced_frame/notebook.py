# Chapter 4: An Applications Building Blocks, Advanced Controls
# Recipe 6: Notebook
#
import wx

#---- Recipe Code ----#

class MyNotebook(wx.Notebook):
    def __init__(self, parent):
        super(MyNotebook, self).__init__(parent)

        # Attributes
        self.textctrl = wx.TextCtrl(self, value="edit me",
                                    style=wx.TE_MULTILINE)
        self.blue = wx.Panel(self)
        self.blue.SetBackgroundColour(wx.BLUE)
        self.fbrowser = wx.GenericDirCtrl(self)

        # Setup
        self.AddPage(self.textctrl, "Text Editor")
        self.AddPage(self.blue, "Blue Panel")
        self.AddPage(self.fbrowser, "File Browser")

#---- End Recipe Code ----#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="wxNotebook", size=(400,500))
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MyFrame, self).__init__(*args, **kwargs)

        # Attributes
        self.panel = MyPanel(self)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Attributes
        self.nb = MyNotebook(self)

        # Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
