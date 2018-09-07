# Chapter 3: An Applications Building Blocks, Basic Controls
# Recipe 3: CheckBoxes
#
import wx

class MyApp(wx.App):
    def OnInit(self):
        self.frame = CheckBoxFrame(None, title="CheckBoxes")
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class CheckBoxFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(CheckBoxFrame, self).__init__(*args, **kwargs)

        # Attributes
        self.panel = wx.Panel(self)
        self.checkbox1 = wx.CheckBox(self.panel,
                                     label="2 State CheckBox")
        style = wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER
        self.checkbox2 = wx.CheckBox(self.panel,
                                     label="3 State CheckBox",
                                     style=style)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.checkbox1, 0, wx.ALL, 15)
        sizer.Add(self.checkbox2, 0, wx.ALL, 15)
        self.panel.SetSizer(sizer)
        self.CreateStatusBar()

        # Event Handlers
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck)

    def OnCheck(self, event):
        e_obj = event.GetEventObject()
        if e_obj == self.checkbox1:
            checked = self.checkbox1.GetValue()
            msg = "Two State Clicked: %s" % checked
            self.PushStatusText(msg)
        elif e_obj == self.checkbox2:
            state = self.checkbox2.Get3StateValue()
            msg = "Three State Clicked: %d" % state
            self.PushStatusText(msg)
        else:
            event.Skip()

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
