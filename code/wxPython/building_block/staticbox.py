# Chapter 3: An Applications Building Blocks, Basic Controls
# Recipe 9: Grouping Controls with a StaticBox
#
import wx

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="StaticBox")
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MyFrame, self).__init__(parent, *args, **kwargs)

        # Attributes
        self.panel = MyPanel(self)

        # Layout
        self.CreateStatusBar()

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        # Layout
        sbox = wx.StaticBox(self, label="Box Label")
        sboxsz = wx.StaticBoxSizer(sbox, wx.VERTICAL)
        
        # Add some controls to the box
        cb = wx.CheckBox(self, label="Enable")
        sboxsz.Add(cb, 0, wx.ALL, 8)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self, label="Value:"))
        sizer.Add((5, 5))
        sizer.Add(wx.TextCtrl(self))
        sboxsz.Add(sizer, 0, wx.ALL, 8)

        msizer = wx.BoxSizer(wx.VERTICAL)
        msizer.Add(sboxsz, 0, wx.EXPAND|wx.ALL, 20)
        self.SetSizer(msizer)

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
