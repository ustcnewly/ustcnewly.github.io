# Chapter 5: Providing Information and Alerting Users
# Recipe 7: About Dialog
#
import wx
import sys

#---- Recipe Code ----#

#---- End Recipe Code ----#

class AboutRecipeApp(wx.App):
    def OnInit(self):
        self.frame = AboutRecipeFrame(None, title="AboutDialog", 
                                      size=(300,200))
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class AboutRecipeFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(AboutRecipeFrame, self).__init__(*args,
                                               **kwargs)

        # Attributes
        self.panel = wx.Panel(self)

        # Setup Menus
        menubar = wx.MenuBar()
        helpmenu = wx.Menu()
        helpmenu.Append(wx.ID_ABOUT, "About")
        menubar.Append(helpmenu, "Help")
        self.SetMenuBar(menubar)

        # Setup StatusBar
        self.CreateStatusBar()
        self.PushStatusText("See About in the Menu")

        # Event Handlers
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)

    def OnAbout(self, event):
        """Show the about dialog"""
        info = wx.AboutDialogInfo()

        # Make a template for the description
        desc = ["\nwxPython Cookbook Chapter 5\n",
                "Platform Info: (%s,%s)",
                "License: Public Domain"]
        desc = "\n".join(desc)

        # Get the platform information
        py_version = [sys.platform,
                      ", python ",
                      sys.version.split()[0]]
        platform = list(wx.PlatformInfo[1:])
        platform[0] += (" " + wx.VERSION_STRING)
        wx_info = ", ".join(platform)

        # Populate with information
        info.SetName("AboutBox Recipe")
        info.SetVersion("1.0")
        info.SetCopyright("Copyright (C) Joe Programmer")
        info.SetDescription(desc % (py_version, wx_info))

        # Create and show the dialog
        wx.AboutBox(info)

if __name__ == "__main__":
    app = AboutRecipeApp(False)
    app.MainLoop()
