# Chapter 3: An Applications Building Blocks, Basic Controls
# Recipe 5: Choice Control
#
import wx

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Choice Control")
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MyFrame, self).__init__(*args, **kwargs)

        # Attributes
        self.panel = ChoicePanel(self)

        # Layout
        self.CreateStatusBar()

class ChoicePanel(wx.Panel):
    def __init__(self, parent):
        super(ChoicePanel, self).__init__(parent)

        # Attributes
        items = ["item 1", "item 2", "item 3"]
        self.choice = wx.Choice(self, choices=items)
        self.choice.SetSelection(0)

        # Layout
        sizer = wx.BoxSizer()
        sizer.Add(self.choice, 1,
                  wx.EXPAND|wx.ALL, 20)
        self.SetSizer(sizer)

        # Event Handlers
        self.Bind(wx.EVT_CHOICE, self.OnChoice)

    def OnChoice(self, event):
        selection = self.choice.GetStringSelection()
        index = self.choice.GetSelection()
        print "Selected Item: %d '%s'" % (index, selection)

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
