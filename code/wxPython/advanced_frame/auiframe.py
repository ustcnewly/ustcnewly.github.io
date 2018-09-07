# Chapter 7: Window Layout and Design
# Recipe 8: Sized Controls
#
import wx
import wx.aui as aui

#---- Recipe Code ----#

class AuiBaseFrame(wx.Frame):
    """Frame base class with builtin AUI support"""
    def __init__(self, *args, **kwargs):
        super(AuiBaseFrame, self).__init__(*args, **kwargs)

        # Attributes
        auiFlags = aui.AUI_MGR_DEFAULT
        if wx.Platform == '__WXGTK__' and \
           aui.AUI_MGR_DEFAUL & aui.AUI_MGR_TRANSPARENT_HINT:
            # Use venetian blinds style as transparent can 
            # cause crashes on Linux when desktop compositing
            # is used. (wxAUI bug in 2.8)
            auiFlags -= aui.AUI_MGR_TRANSPARENT_HINT
            auiFlags |= aui.AUI_MGR_VENETIAN_BLINDS_HINT
        self._mgr = aui.AuiManager(self, flags=auiFlags)

        # Event Handlers
        self.Bind(wx.EVT_CLOSE, self.OnAuiBaseClose)

    def OnAuiBaseClose(self, event):
        """Save perspective on exit"""
        appName = wx.GetApp().GetAppName()
        assert appName, "No App Name Set!"
        config = wx.Config(appName)
        perspective = self._mgr.SavePerspective()
        config.Write("perspective", perspective)
        event.Skip() # Allow event to propagate

    def AddPane(self, pane, auiInfo):
        """Add a panel to be managed by this Frame's
        AUI Manager.
        @param pane: wx.Window instance
        @param auiInfo: AuiInfo Object
        """
        # Delegate to AuiManager
        self._mgr.AddPane(pane, auiInfo)
        self._mgr.Update() # Refresh the layout

    def SetCenterPane(self, pane):
        """Set the main center pane of the frame.
        Convenience method for AddPane.
        @param pane: wx.Window instance
        """
        info = aui.AuiPaneInfo()
        info = info.Center().Name("CenterPane")
        info = info.Dockable(False).CaptionVisible(False)
        self._mgr.AddPane(pane, info)

    def LoadDefaultPerspective(self):
        appName = wx.GetApp().GetAppName()
        assert appName, "Must set an AppName!"
        config = wx.Config(appName)
        perspective = config.Read("perspective")
        if perspective:
            self._mgr.LoadPerspective(perspective)

#---- End Recipe Code ----#

# A little test harness to try out our handy new base class

class AuiTestApp(wx.App):
    def OnInit(self):
        self.SetAppName("AuiBaseFrameTestApp")
        self.frame = AuiTestFrame(None,
                                  title="Aui Test")
        self.frame.Show()
        return True

class AuiTestFrame(AuiBaseFrame):
    def __init__(self, *args, **kwargs):
        super(AuiTestFrame, self).__init__(*args, **kwargs)

        # Attributes
        # Create some 'tool' windows
        self.textctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_RICH2)
        self.paneleft = TestPanel(self, "Left Pane", wx.BLUE)
        self.panebottom = TestPanel(self, "Bottom Pane", wx.WHITE)
        self.paneright = TestPanel(self, "Right Pane", wx.RED)

        # Set up some AuiInfo
        info = aui.AuiPaneInfo()
        info = info.Dockable(True).CloseButton(False)
        info = info.MaximizeButton(True).CaptionVisible(True)
        info = info.BestSize((250, 250))

        # Add them to the AuiManager
        self.SetCenterPane(self.textctrl)
        for caption, loc, name in [("Left Pane", "Left", "paneleft"),
                                   ("Right Pane", "Right", "paneright"),
                                   ("Bottom Pane", "Bottom", "panebottom")]:
            info = info.Caption(caption)
            info = info.Name(name)
            # Set the default dock position (i.e info.Bottom())
            info = getattr(info, loc)()
            # Get the window object
            pane = getattr(self, name)
            self.AddPane(pane, info)

        # Restore last session
        self.LoadDefaultPerspective()

class TestPanel(wx.Panel):
    def __init__(self, parent, title, color):
        super(TestPanel, self).__init__(parent)

        # Attributes
        self.label = wx.StaticText(self, label="This is Panel: %s" % title)
        
        # Setup
        self.SetBackgroundColour(color) # make it more visible

        # Layout
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddStretchSpacer()
        hsizer.Add(self.label)
        hsizer.AddStretchSpacer()
        vsizer.AddStretchSpacer()
        vsizer.Add(hsizer, 0, wx.EXPAND)
        vsizer.AddStretchSpacer()
        self.SetSizer(vsizer)


if __name__ == '__main__':
    app = AuiTestApp(False)
    app.MainLoop()
