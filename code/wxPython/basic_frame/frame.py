# Chapter 1: Getting Started
# Recipe 2: The Main Frame
#
import wx

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="The Main Frame")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, idx=wx.ID_ANY, title="", 
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE,
                 name="MyFrame"):
        super(MyFrame, self).__init__(parent, id, title,
                                      pos, size, style, name)

        # Attributes
        self.panel = wx.Panel(self)

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()

