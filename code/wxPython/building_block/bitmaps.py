# Chapter 1: Getting Started
# Recipe 5: Bitmaps
#
import os
import wx

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Bitmaps")
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, idx=wx.ID_ANY, title="", 
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE,
                 name="MyFrame"):
        super(MyFrame, self).__init__(parent, idx, title,
                                      pos, size, style, name)

        # Attributes
        self.panel = wx.Panel(self)

        img_path = os.path.abspath("./face-grin.png")
        bitmap = wx.Bitmap(img_path, type=wx.BITMAP_TYPE_PNG)
        self.bitmap = wx.StaticBitmap(self.panel,
                                      bitmap=bitmap)

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()

