# Chapter 1: Getting Started
# Recipe 1: The Application Object
#
import wx

class MyApp(wx.App):
    def OnInit(self):
        wx.MessageBox("Hello wxPython", "wxApp")
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
