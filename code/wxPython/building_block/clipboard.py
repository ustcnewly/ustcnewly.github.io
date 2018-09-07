# Chapter 1: Getting Started
# Recipe 8: The Clipboard
#
import wx

#-----------------------------------------------------------------------------#
# Recipe Code for clipboard access
# For usage see OnCopy and OnPaste below

def SetClipboardText(text):
    """Put text in the clipboard
    @param text: string
    """
    data_o = wx.TextDataObject()
    data_o.SetText(text)
    if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
        wx.TheClipboard.SetData(data_o)
        wx.TheClipboard.Close()

def GetClipboardText():
    """Get text from the clipboard
    @return: string
    """
    text_obj = wx.TextDataObject()
    rtext = ""
    if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
        if wx.TheClipboard.GetData(text_obj):
            rtext = text_obj.GetText()
        wx.TheClipboard.Close()
    return rtext

#-----------------------------------------------------------------------------#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Clipboard")
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, idx=wx.ID_ANY, title="", 
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name="MyFrame"):
        wx.Frame.__init__(self, parent, idx, title, pos, size, style, name)

        # Attributes
        self.panel = wx.Panel(self)
        self.copy_from = wx.TextCtrl(self.panel, value="Put text to copy here")
        self.paste_to = wx.TextCtrl(self.panel, value="Values will be pasted here")

        # Setup
        self.CreateStatusBar()
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnCopy, id=wx.ID_COPY)
        self.Bind(wx.EVT_BUTTON, self.OnPaste, id=wx.ID_PASTE)

    def __DoLayout(self):
        """Layout the window"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        copy_btn = wx.Button(self.panel, wx.ID_COPY)
        paste_btn = wx.Button(self.panel, wx.ID_PASTE)

        # Layout the controls using a sizer
        sizer.AddMany([((10, 10), 0),
                       (self.copy_from, 0, wx.EXPAND),
                       (copy_btn, 0, wx.ALIGN_CENTER),
                       ((10, 10), 0),
                       (self.paste_to, 0, wx.EXPAND),
                       (paste_btn, 0, wx.ALIGN_CENTER)])
        self.panel.SetSizer(sizer)
        
        msizer = wx.BoxSizer()
        msizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(msizer)
        self.SetInitialSize(size=(300, 200))

    def OnCopy(self, evt):
        """Copy the text to the clipboard"""
        text = self.copy_from.GetValue()
        SetClipboardText(text)
        self.PushStatusText("'%s' copied to clipboard" % text)

    def OnPaste(self, evt):
        """Paste the text from the clipboard"""
        text = GetClipboardText()
        self.paste_to.SetValue(text)
        self.PushStatusText("'%s' retrieved from the clipboard" % text)

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
