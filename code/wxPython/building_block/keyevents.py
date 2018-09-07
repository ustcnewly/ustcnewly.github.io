# Chapter 2: Responding to Events
# Recipe 3: Handling KeyEvents
#
import wx

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Handling KeyEvents")
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MyFrame, self).__init__(parent, *args, **kwargs)

        # Attributes
        self.panel = wx.Panel(self)
        self.txtctrl = wx.TextCtrl(self.panel,
                                   style=wx.TE_MULTILINE)

        # Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.txtctrl, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        self.CreateStatusBar() # For output display

        # Event Handlers
        self.txtctrl.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.txtctrl.Bind(wx.EVT_CHAR, self.OnChar)
        self.txtctrl.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

    def OnKeyDown(self, event):
        """KeyDown event is sent first"""
        print "OnKeyDown Called"
        # Get information about the event and log it to
        # the StatusBar for display.
        key_code = event.GetKeyCode()
        raw_code = event.GetRawKeyCode()
        modifiers = event.GetModifiers()
        msg = "key:%d,raw:%d,modifers:%d" % \
              (key_code, raw_code, modifiers)
        self.PushStatusText("KeyDown: " + msg)

        # Must Skip the event to allow OnChar to be called
        event.Skip()

    def OnChar(self, event):
        """The Char event comes second and is
        where the character associated with the
        key is put into the control.
        """
        print "OnChar Called"
        modifiers = event.GetModifiers()
        key_code = event.GetKeyCode()
        # Beep at the user if the Shift key is down
        # and disallow input.
        if modifiers & wx.MOD_SHIFT:
            wx.Bell()
        elif chr(key_code) in "aeiou":
            # When a vowel is pressed append a
            # question mark to the end.
            self.txtctrl.AppendText("?")
        else:
            # Let the text go in to the buffer
            event.Skip()

    def OnKeyUp(self, event):
        """KeyUp comes last"""
        print "OnKeyUp Called"
        event.Skip()

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()

