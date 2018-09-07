# Chapter 5: Providing Information and Alerting Users
# Recipe 5: SplashScreen
#
import wx

#---- Recipe Code ----#

class ProgressSplashScreen(wx.SplashScreen):
    def __init__(self, *args, **kwargs):
        super(ProgressSplashScreen, self).__init__(*args,
                                                   **kwargs)

        # Attributes
        self.gauge = wx.Gauge(self, size=(-1, 16))

        # Setup
        rect = self.GetClientRect()
        new_size = (rect.width, 16)
        self.gauge.SetSize(new_size)
        self.SetSize((rect.width, rect.height + 16))
        self.gauge.SetPosition((0, rect.height))

    def SetProgress(self, percent):
        """Set the indicator gauges progress"""
        self.gauge.SetValue(percent)

    def GetProgress(self):
        """Get the current progress of the gauge"""
        return self.gauge.GetValue()

#---- End Recipe Code ----#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="SplashScreen", 
                             size=(300,200))
        self.frame.Center()
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MyFrame, self).__init__(*args, **kwargs)

        # Attributes
        bmp = wx.Bitmap('splash_img.png', wx.BITMAP_TYPE_PNG)
        self.splash = ProgressSplashScreen(bmp,
                                           wx.SPLASH_CENTRE_ON_SCREEN|\
                                           wx.SPLASH_NO_TIMEOUT, -1, self)
        self.splash.Show()
        self.panel = wx.Panel(self)

        # Simulate long startup time
        for x in range(1, 11):
            self.splash.SetProgress(x * 10)
            wx.Sleep(1)
        self.splash.Destroy()

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
