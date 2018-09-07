# Chapter 1: Getting Started
# Recipe 4: Referencing Controls
#
import wx

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Hierarchy")
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, idx=wx.ID_ANY, title="", 
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE,
                 name="MyFrame"):
        super(MyFrame, self).__init__(parent, idx, title,
                                      pos, size, style, name)

        # Attributes
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.BLACK)
        button = wx.Button(self.panel,
                           label="Get Children",
                           pos=(50, 50))
        self.btnId = button.GetId()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton, button)

    def OnButton(self, event):
        """Called when the Button is clicked"""
        print "\nFrame GetChildren:"
        for child in self.GetChildren():
            print "%s" % repr(child)

        print "\nPanel FindWindowById:"
        button = self.panel.FindWindowById(self.btnId)
        print "%s" % repr(button)
        # Change the Button's label
        button.SetLabel("Changed Label")

        print "\nButton GetParent:"
        panel = button.GetParent()
        print "%s" % repr(panel)

        print "\nGet the Application Object:"
        app = wx.GetApp()
        print "%s" % repr(app)

        print "\nGet the Frame from the App:"
        frame = app.GetTopWindow()
        print "%s" % repr(frame)

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
