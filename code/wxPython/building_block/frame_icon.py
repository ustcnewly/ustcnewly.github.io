# Chapter 1: Getting Started
# Recipe 6: Adding Icons to Windows
#
import os
import wx

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Adding an Icon")
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, idx=wx.ID_ANY, title="", 
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE,
                 name="MyFrame"):
        super(MyFrame, self).__init__(parent, idx, title, pos,
                                      size, style, name)

        # Attributes
        self.panel = wx.Panel(self)

        # Setup
        path = os.path.abspath("./face-monkey.png")
        icon = wx.Icon(path, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
