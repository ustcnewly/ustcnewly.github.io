# Chapter 3: An Applications Building Blocks, Basic Controls
# Recipe 2: Buttons, Buttons, and More Buttons
#
import wx
import wx.lib.platebtn as pbtn
import wx.lib.agw.gradientbutton as gbtn

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Buttons")
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", 
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE,
                 name="MyFrame"):
        super(MyFrame, self).__init__(parent, id, title,
                                      pos, size, style, name)

        # Attributes
        self.panel = ButtonTestPanel(self)

        # Layout
        sizer = wx.BoxSizer()
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize()
        
class ButtonTestPanel(wx.Panel):
    def __init__(self, parent):
        super(ButtonTestPanel, self).__init__(parent)

        # Attributes
        # Make a ToggleButton
        self.toggle = wx.ToggleButton(self,
                                      label="Toggle Button")

        # Make a BitmapButton
        bmp = wx.Bitmap("./face-monkey.png",
                        wx.BITMAP_TYPE_PNG)
        self.bmpbtn = wx.BitmapButton(self, bitmap=bmp)

        # Make a few PlateButton variants
        self.pbtn1 = pbtn.PlateButton(self,
                                      label="PlateButton")
        self.pbtn2 = pbtn.PlateButton(self, 
                                      label="PlateBmp",
                                      bmp=bmp)
        style = pbtn.PB_STYLE_SQUARE
        self.pbtn3 = pbtn.PlateButton(self,
                                      label="Square Plate",
                                      bmp=bmp,
                                      style=style)
        self.pbtn4 = pbtn.PlateButton(self,
                                      label="PlateMenu")
        menu = wx.Menu()
        menu.Append(wx.NewId(), text="Hello World")
        self.pbtn4.SetMenu(menu)

        # Gradient Buttons
        self.gbtn1 = gbtn.GradientButton(self,
                                         label="GradientBtn")
        self.gbtn2 = gbtn.GradientButton(self,
                                         label="GradientBmp",
                                         bitmap=bmp)

        # Layout
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.toggle, 0, wx.ALL, 12)
        vsizer.Add(self.bmpbtn, 0, wx.ALL, 12)
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.AddMany([(self.pbtn1, 0, wx.ALL, 5),
                        (self.pbtn2, 0, wx.ALL, 5),
                        (self.pbtn3, 0, wx.ALL, 5),
                        (self.pbtn4, 0, wx.ALL, 5)])
        vsizer.Add(hsizer1, 0, wx.ALL, 12)
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2.AddMany([(self.gbtn1, 0, wx.ALL, 5),
                         (self.gbtn2, 0, wx.ALL, 5)])
        vsizer.Add(hsizer2, 0, wx.ALL, 12)
        self.SetSizer(vsizer)

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
