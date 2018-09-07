# Chapter 3: An Applications Building Blocks, Basic Controls
# Recipe 3: CheckBoxes
#
import wx

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="TextCtrls")
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MyFrame, self).__init__(*args, **kwargs)

        # Attributes
        self.panel = wx.Panel(self)
        self.label = wx.StaticText(self.panel)

        # Setup
        font = self.label.GetFont()
        font.SetPointSize(20)
        self.label.SetFont(font)

        # Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.label, 0, wx.ALIGN_CENTER)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.AddStretchSpacer()
        vsizer.Add(sizer, 0, wx.ALIGN_CENTER)
        vsizer.AddStretchSpacer()
        self.panel.SetSizer(vsizer)

    def Show(self, show=True):
        
        login = LoginDialog(self, title="Login")
        loggedIn = False
        while not loggedIn:
            rval = login.ShowModal()
            if rval == wx.ID_OK:
                uname = login.GetUsername()
                passwd = login.GetPassword()
                if (uname, passwd) == ("Foo", "Bar"):
                    loggedIn = True

            if not loggedIn:
                wx.MessageBox("Login Failed! (try Foo Bar)",
                              "Incorrect Login",
                              wx.ICON_ASTERISK|wx.OK)
                self.label.SetLabel("Login Failed!!")
                self.panel.SendSizeEvent()
                
        super(MyFrame, self).Show(show)
        self.label.SetLabel("Login Succeeded")
        self.panel.SendSizeEvent()

#------- Begin Recipe Code -----------#

class LoginDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(LoginDialog, self).__init__(*args, **kwargs)

        # Attributes
        self.panel = LoginPanel(self)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize()

    def GetUsername(self):
        return self.panel.GetUsername()

    def GetPassword(self):
        return self.panel.GetPassword()

class LoginPanel(wx.Panel):
    def __init__(self, parent):
        super(LoginPanel, self).__init__(parent)

        # Attributes
        self._username = wx.TextCtrl(self)
        self._passwd = wx.TextCtrl(self, style=wx.TE_PASSWORD)

        # Layout
        sizer = wx.FlexGridSizer(2, 2, 8, 8)
        sizer.Add(wx.StaticText(self, label="Username:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self._username, 0, wx.EXPAND)
        sizer.Add(wx.StaticText(self, label="Password:"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self._passwd, 0, wx.EXPAND)
        msizer = wx.BoxSizer(wx.VERTICAL)
        msizer.Add(sizer, 1, wx.EXPAND|wx.ALL, 20)
        btnszr = wx.StdDialogButtonSizer()
        button = wx.Button(self, wx.ID_OK)
        button.SetDefault()
        btnszr.AddButton(button)
        msizer.Add(btnszr, 0, wx.ALIGN_CENTER|wx.ALL, 12)
        btnszr.Realize()

        self.SetSizer(msizer)

    def GetUsername(self):
        return self._username.GetValue()

    def GetPassword(self):
        return self._passwd.GetValue()

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
