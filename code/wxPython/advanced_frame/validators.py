# Chapter 2: Responding to Events
# Recipe 8: Validators
#
import sys
import wx

#------- Begin Recipe Code -------#

class IntRangeValidator(wx.PyValidator):
    """An integer range validator for a TextCtrl"""
    def __init__(self, min_=0, max_=sys.maxint):
        """Initialize the validator
        @keyword min: min value to accept
        @keyword max: max value to accept

        """
        super(IntRangeValidator, self).__init__()
        assert min_ >= 0, "Minimum Value must be >= 0"
        self._min = min_
        self._max = max_

        # Event managment
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        """Required override"""
        return IntRangeValidator(self._min, self._max)

    def Validate(self, win):
        """Override called to validate the window's value.
        @return: bool
        """
        txtCtrl = self.GetWindow()
        val = txtCtrl.GetValue()
        isValid = False
        if val.isdigit():
            digit = int(val)
            if digit >= self._min and digit <= self._max:
                isValid = True

        if not isValid:
            # Notify the user of the invalid value
            msg = "Value must be between %d and %d" % \
                  (self._min, self._max)
            wx.MessageBox(msg,
                          "Invalid Value",
                          style=wx.OK|wx.ICON_ERROR)

        return isValid

    def OnChar(self, event):
        txtCtrl = self.GetWindow()
        key = event.GetKeyCode()
        isDigit = False
        if key < 256:
            isDigit = chr(key).isdigit()

        if key in (wx.WXK_RETURN,
                   wx.WXK_DELETE,
                   wx.WXK_BACK) or \
           key > 255 or isDigit:
            if isDigit:
                # Check if in range
                val = txtCtrl.GetValue()
                digit = chr(key)
                pos = txtCtrl.GetInsertionPoint()
                if pos == len(val):
                    val += digit
                else:
                    val = val[:pos] + digit + val[pos:]

                val = int(val)
                if val < self._min or val > self._max:
                    if not wx.Validator_IsSilent():
                        wx.Bell()
                    return
                
            event.Skip()
            return

        if not wx.Validator_IsSilent():
            # Beep to warn about invalid input
            wx.Bell()

        return

    def TransferToWindow(self):
        """Overridden to skip data transfer"""
        return True

    def TransferFromWindow(self):
        """Overridden to skip data transfer"""
        return True 

#------ End Recipe Code -------#

#------ Begin Test Application -------#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Validators")
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        wx.Frame.__init__(self, parent, *args, **kwargs)

        # Attributes
        self.panel = wx.Panel(self)

        # Layout
        sizer = wx.BoxSizer()
        btn = wx.Button(self.panel, label="Show Dialog")
        sizer.Add(btn, 0, wx.ALL|wx.ALIGN_CENTER, 20)
        self.panel.SetSizer(sizer)
        self.CreateStatusBar()
        self.SetInitialSize((300,300))

        self.Bind(wx.EVT_BUTTON, self.OnShowDialog, btn)

    def OnShowDialog(self, event):
        dlg = MyDialog(self, title="Test Validator")
        if dlg.ShowModal() == wx.ID_OK:
            self.PushStatusText("Got Value: %d" % dlg.GetValue())
        else:
            self.PushStatusText("")
        dlg.Destroy()

class MyDialog(wx.Dialog):
    def __init__(self, parent, *args, **kwargs):
        wx.Dialog.__init__(self, parent, *args, **kwargs)

        # Attributes
        self.txt = wx.TextCtrl(self, validator=IntRangeValidator(0, 100))

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self,
                              label="Enter a value (0-100): ")
        hsizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        hsizer.Add(self.txt, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(hsizer, 0, wx.EXPAND|wx.ALL, 20)

        # Add some buttons to the dialog
        okb = wx.Button(self, wx.ID_OK)
        cancelb = wx.Button(self, wx.ID_CANCEL)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(okb)
        btnsizer.AddButton(cancelb)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALL|wx.ALIGN_RIGHT, 8)
        self.SetSizer(sizer)
        self.SetInitialSize()

    def GetValue(self):
        return int(self.txt.GetValue())

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
