# Chapter 3: An Applications Building Blocks, Basic Controls
# Recipe 8: How to use PopupMenus
#
import wx

# Menu ID's
ID_RED = wx.NewId()
ID_GREEN = wx.NewId()
ID_BLUE = wx.NewId()

# Recipe code
class PopupMenuMixin(object):
    def __init__(self):
        super(PopupMenuMixin, self).__init__()

        # Attributes
        self._menu = None

        # Event Handlers
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)

    def OnContextMenu(self, event):
        """Creates and shows the Menu"""
        if self._menu is not None:
            self._menu.Destroy()

        self._menu = wx.Menu()
        self.CreateContextMenu(self._menu)
        self.PopupMenu(self._menu)

    def CreateContextMenu(self, menu):
        """Override in subclass to create the menu"""
        raise NotImplementedError

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="PopupMenus")
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MyFrame, self).__init__(*args, **kwargs)

        # Attributes
        self.panel = PanelWithMenu(self)

        # Layout
        self.CreateStatusBar() # To show help text

class PanelWithMenu(wx.Panel, PopupMenuMixin):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        PopupMenuMixin.__init__(self)

        # Layout
        sizer = wx.BoxSizer()
        sizer.Add(wx.StaticText(self, label="Right Click Panel"),
                  0, wx.ALL, 15)
        self.SetSizer(sizer)

        # Event Handlers
        self.Bind(wx.EVT_MENU, self.OnMenu)

    def OnMenu(self, event):
        """Handle menu events from the popup menu"""
        evt_id = event.GetId()
        colour_map = {ID_RED : wx.RED,
                      ID_GREEN : wx.GREEN,
                      ID_BLUE : wx.BLUE}
        if evt_id in colour_map:
            colour = colour_map.get(evt_id)
            self.SetBackgroundColour(colour)
            self.Refresh()
        else:
            event.Skip()

    def CreateContextMenu(self, menu):
        """Overrides PopupMenuMixin.CreateContextMenu"""
        menu.Append(ID_RED, "Red",
                    "Change background to Red")
        menu.Append(ID_GREEN, "Green",
                    "Change background to Green")
        menu.Append(ID_BLUE, "Blue",
                    "Change background to Blue")

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
