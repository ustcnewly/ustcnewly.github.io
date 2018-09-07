# Chapter 4: An Applications Building Blocks, Advanced Controls
# Recipe 3: Virtual List Box
#
import wx

#---- Recipe Code ----#

class UserListBox(wx.VListBox):
    """Simple List Box control to show a list of users"""
    def __init__(self, parent, users):
        """@param users: list of user names"""
        super(UserListBox, self).__init__(parent)

        # Attributes
        self.bmp = wx.Bitmap("system-users.png",
                             wx.BITMAP_TYPE_PNG)
        self.bh = self.bmp.GetHeight()
        self.users = users

        # Setup
        self.SetItemCount(len(self.users))

    def OnMeasureItem(self, index):
        """Called to get an items height"""
        # All our items are the same so index is ignored
        return self.bh + 4

    def OnDrawSeparator(self, dc, rect, index):
        """Called to draw the item separator"""
        oldpen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.DrawLine(rect.x, rect.y,
                    rect.x + rect.width,
                    rect.y)
        rect.Deflate(0, 2)
        dc.SetPen(oldpen)

    def OnDrawItem(self, dc, rect, index):
        """Called to draw the item"""
        # Draw the bitmap
        dc.DrawBitmap(self.bmp, rect.x + 2,
                      ((rect.height - self.bh) / 2) + rect.y)
        # Draw the label to the right of the bitmap
        textx = rect.x + 2 + self.bh + 2
        lblrect = wx.Rect(textx, rect.y,
                          rect.width - textx,
                          rect.height)
        dc.DrawLabel(self.users[index], lblrect,
                     wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)

#---- End Recipe Code ----#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Virtual List Box", size=(300,200))
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MyFrame, self).__init__(*args, **kwargs)

        # Attributes
        self.panel = MyPanel(self)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.CreateStatusBar()

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        # Attributes
        users = ["Steve", "James", "Mary", "Yuya",
                 "Yukiyo", "Ankur", "Saiyam", "Vadim",
                 "Andrea", "Ana" ]
        users.sort()
        self.lst = UserListBox(self, users)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.lst, 1, wx.EXPAND)
        self.SetSizer(sizer)

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
