# Chapter 10: Creating Components and Extending Functionality
# Recipe 4: Creating a SearchBar
#
import wx

#---- Recipe Code ----#

class SearchBar(wx.Panel):
    def __init__(self, parent):
        style = wx.BORDER_RAISED
        super(SearchBar, self).__init__(parent,
                                        style=style)

        # Attributes
        self.search = wx.SearchCtrl(self,
                                    size=(250, -1),
                                    style=wx.TE_PROCESS_ENTER)
        self.lastfind = ''

        # Layout
        self.__DoLayout()

        # Event Handlers
        if wx.Platform in ['__WXMSW__', '__WXGTK__']:
            # Workaround for compound control on msw/gtk
            for child in self.search.GetChildren():
                if isinstance(child, wx.TextCtrl):
                    child.Bind(wx.EVT_KEY_UP, self.OnEnter)
                    break
        else:
            self.search.Bind(wx.EVT_KEY_UP, self.OnEnter)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancel)

    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.search, 0, wx.ALL, 2)
        self.SetSizer(sizer)

    def OnCancel(self, event):
        self.search.SetValue("")
        self.search.ShowCancelButton(False)

    def OnEnter(self, event):
        """Send a search event"""
        code = event.GetKeyCode()
        val = self.search.GetValue()
        if code == wx.WXK_RETURN and val:
            if val == self.lastfind:
                etype = wx.wxEVT_COMMAND_FIND
            else:
                etype = wx.wxEVT_COMMAND_FIND_NEXT
            fevent = wx.FindDialogEvent(etype)
            fevent.SetFindString(val)
            self.ProcessEvent(fevent)
            self.lastfind = val
        else:
            show = bool(val)
            self.search.ShowCancelButton(show)

#---- End Recipe Code ----#

#---- Example Application to test the SearchBar ----#

class SearchBarApp(wx.App):
    def OnInit(self):
        self.frame = SearchBarFrame(None,
                                    title="SearchBar")
        self.frame.Show()
        return True

class SearchBarFrame(wx.Frame):
    """Main application window"""
    def __init__(self, *args, **kwargs):
        super(SearchBarFrame, self).__init__(*args, **kwargs)

        # Attributes
        self.txt = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.search = SearchBar(self)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.txt, 1, wx.EXPAND)
        sizer.Add(self.search, 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize((300, 150))

        # Event Handlers
        self.Bind(wx.EVT_FIND, self.OnFind)
        self.Bind(wx.EVT_FIND_NEXT, self.OnFind)

    def OnFind(self, event):
        print "Find action requested!"
        # Search in the TextCtrl for a match
        query = event.GetFindString().lower() # case insensitive search
        cpos = self.txt.GetInsertionPoint() # Current cursor position
        txt = self.txt.GetValue().lower() # Contents of control
        spos = txt.find(query, cpos)
        if spos != -1:
            self.txt.SetSelection(spos, spos+len(query))
            self.txt.SetFocus()
        else:
            wx.Bell() # Beep when nothing found

if __name__ == '__main__':
    app = SearchBarApp(False)
    app.MainLoop()
