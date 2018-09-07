# Chapter 2: Responding to Events
# Recipe 7: Managing Events with EventStack
#
# This is the sample application that uses the recipe
# presented in the topic "Managing Events with EventStack"
#

import wx
import wx.lib.eventStack as eventStack

class EventMgrApp(wx.App, eventStack.AppEventHandlerMixin):
    """Application object base class that
    event handler managment.
    """
    def __init__(self, *args, **kwargs):
        eventStack.AppEventHandlerMixin.__init__(self)
        wx.App.__init__(self, *args, **kwargs)

class EventMgrFrame(wx.Frame):
    """Frame base class that provides event
    handler managment.
    """
    def __init__(self, parent, *args, **kwargs):
        super(EventMgrFrame, self).__init__(parent,
                                            *args,
                                            **kwargs)

        # Attributes
        self._menu_handlers = []
        self._ui_handlers = []

        # Event Handlers
        self.Bind(wx.EVT_ACTIVATE, self._OnActivate)

    def _OnActivate(self, event):
        """Pushes/Pops event handlers"""
        app = wx.GetApp()
        active = event.GetActive()
        if active:
            mode = wx.UPDATE_UI_PROCESS_SPECIFIED
            wx.UpdateUIEvent.SetMode(mode)
            self.SetExtraStyle(wx.WS_EX_PROCESS_UI_UPDATES)

            # Push this instances handlers
            for handler in self._menu_handlers:
                app.AddHandlerForID(*handler)

            for handler in self._ui_handlers:
                app.AddUIHandlerForID(*handler)
        else:
            self.SetExtraStyle(0)
            wx.UpdateUIEvent.SetMode(wx.UPDATE_UI_PROCESS_ALL)
            # Pop this instances handlers
            for handler in self._menu_handlers:
                app.RemoveHandlerForID(handler[0])

            for handler in self._ui_handlers:
                app.RemoveUIHandlerForID(handler[0])

    def RegisterMenuHandler(self, event_id, handler):
        """Register a MenuEventHandler
        @param event_id: MenuItem ID
        @param handler: Event handler function
        """
        self._menu_handlers.append((event_id, handler))

    def RegisterUpdateUIHandler(self, event_id, handler):
        """Register a controls UpdateUI handler
        @param event_id: Control ID
        @param handler: Event handler function
        """
        self._ui_handlers.append((event_id, handler))


class MyApp(EventMgrApp):
    def OnInit(self):
        self.frame = MyFrame(None, title="EventStackApp")
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(EventMgrFrame):
    def __init__(self, parent, *args, **kwargs):
        EventMgrFrame.__init__(self, parent,
                                         *args, **kwargs)

        # Attributes
        self.panel = wx.Panel(self)
        self.txt = wx.TextCtrl(self.panel,
                               value="Hello World",
                               style=wx.TE_MULTILINE)

        # Add a MenuBar
        menub = wx.MenuBar()
        filem = wx.Menu()
        filem.Append(wx.ID_NEW, "New\tCtrl+N")
        menub.Append(filem, "File")
        editm = wx.Menu()
        editm.Append(wx.ID_CUT, "Cut\tCtrl+X")
        editm.Append(wx.ID_COPY, "Copy\tCtrl+C")
        editm.Append(wx.ID_PASTE, "Paste\tCtrl+P")
        editm.Append(wx.ID_SELECTALL, "Select All\tCtrl+A")
        menub.Append(editm, "Edit")
        self.SetMenuBar(menub)

        # Add a ToolBar
        toolb = wx.ToolBar(self)
        for itemid, bmpid in [(wx.ID_CUT, wx.ART_CUT),
                              (wx.ID_COPY, wx.ART_COPY),
                              (wx.ID_PASTE, wx.ART_PASTE)]:
            bmp = wx.ArtProvider.GetBitmap(bmpid, wx.ART_TOOLBAR)
            toolb.AddTool(itemid, bmp)
        toolb.Realize()
        self.SetToolBar(toolb)

        # Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.txt, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        self.CreateStatusBar()

        # Event Handlers
        # Use the base classes Register* methods instead
        # of the usual Bind.
        self.RegisterMenuHandler(wx.ID_NEW, self.OnNewWindow)
        self.RegisterMenuHandler(wx.ID_CUT, self.OnCut)
        self.RegisterMenuHandler(wx.ID_COPY, self.OnCopy)
        self.RegisterMenuHandler(wx.ID_PASTE, self.OnPaste)
        self.RegisterMenuHandler(wx.ID_SELECTALL, self.OnSelectAll)
        self.RegisterUpdateUIHandler(wx.ID_CUT, self.OnUpdateCut)
        self.RegisterUpdateUIHandler(wx.ID_COPY, self.OnUpdateCopy)
        self.RegisterUpdateUIHandler(wx.ID_PASTE, self.OnUpdatePaste)
        self.RegisterUpdateUIHandler(wx.ID_SELECTALL, self.OnUpdateSelectAll)

    def OnCut(self, event):
        self.txt.Cut()

    def OnCopy(self, event):
        self.txt.Copy()

    def OnPaste(self, event):
        self.txt.Paste()

    def OnSelectAll(self, event):
        self.txt.SelectAll()

    def OnUpdateCut(self, event):
        event.Enable(self.txt.CanCopy())

    def OnNewWindow(self, event):
        """Create a new window"""
        num = len(wx.GetTopLevelWindows())
        win = MyFrame(None, title="Frame %d" % num)
        win.Show()

    def OnUpdateCopy(self, event):
        event.Enable(self.txt.CanCopy())

    def OnUpdatePaste(self, event):
        event.Enable(self.txt.CanPaste())

    def OnUpdateSelectAll(self, event):
        """Only enable SelectAll if there is text in the control"""
        event.Enable(bool(self.txt.GetValue()))

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
