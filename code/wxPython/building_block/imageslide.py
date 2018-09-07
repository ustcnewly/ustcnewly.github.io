# Chapter 8: Drawing to the Screen, Using Device Contexts
# Recipe 1: Screen Drawing
#
import os
import wx

class SlideShowApp(wx.App):
    def OnInit(self):
        self.frame = SlideShowFrame(None,
                                    title="Screen Drawing")
        self.frame.Show()
        return True

class SlideShowFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(SlideShowFrame, self).__init__(*args, **kwargs)

        # Attributes
        self.panel = SlideShowPanel(self)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize()

class SlideShowPanel(wx.Panel):
    def __init__(self, parent):
        super(SlideShowPanel, self).__init__(parent)

        # Attributes
        self.canvas = ImageCanvas(self)
        self.next = wx.Button(self, label="Next >>")
        self.pre = wx.Button(self, label="<< Previous")

        # Setup
        # Use local image directory
        imgpath = os.path.abspath('./images')
        self.canvas.SetImageDir(imgpath)

        # Layout
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def __DoLayout(self):
        msizer = wx.BoxSizer(wx.VERTICAL)
        msizer.Add(self.canvas, 1, wx.EXPAND)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddStretchSpacer()
        hsizer.Add(self.pre)
        hsizer.AddSpacer(10)
        hsizer.Add(self.next)
        hsizer.AddStretchSpacer()
        msizer.Add(hsizer, 0, wx.EXPAND|wx.ALIGN_CENTER)

        self.SetSizer(msizer)

    def OnButton(self, event):
        """Change the image"""
        evt_obj = event.GetEventObject()
        if evt_obj == self.next:
            self.canvas.Next()
        elif evt_obj == self.pre:
            self.canvas.Previous()
        else:
            event.Skip()

class ImageCanvas(wx.PyPanel):
    def __init__(self, parent):
        super(ImageCanvas, self).__init__(parent)

        # Attributes
        self.idx = 0 # Current index in image list
        self.images = list() # list of images found to display

        # Event Handlers
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def DoGetBestSize(self):
        """Virtual override for PyPanel"""
        newsize = wx.Size(0, 0)
        if len(self.images):
            imgpath = self.images[self.idx]
            bmp = wx.Bitmap(imgpath)
            newsize = bmp.GetSize()
            newsize = newsize + (20, 20) # some padding
        else:
            tsize = self.GetTextExtent("No Image!")
            newsize = tsize + (20, 20)

        # Ensure new size is at least 300x300
        return wx.Size(max(300, newsize[0]),
                       max(300, newsize[1]))

    def OnPaint(self, event):
        """Draw the image on to the panel"""
        dc = wx.PaintDC(self) # Must create a PaintDC

        # Get the working rectangle
        rect = self.GetClientRect()

        # Setup the DC
        dc.SetTextForeground(wx.BLACK)

        # Do the drawing
        if len(self.images):
            # Draw the current image
            imgpath = self.images[self.idx]
            bmp = wx.Bitmap(imgpath)
            bsize = bmp.GetSize()
            # Try and center the image
            # Note: assumes image is smaller than canvas
            xpos = (rect.width - bsize[0]) / 2
            ypos = (rect.height - bsize[1]) / 2
            dc.DrawBitmap(bmp, xpos, ypos)
            # Draw a label under the image saying what
            # number in the set it is.
            number = "%d / %d" % (self.idx, len(self.images))
            tsize = dc.GetTextExtent(number)
            xpos = (rect.width - tsize[0]) / 2
            ypos = ypos + bsize[1] + 5 # 5px below image
            dc.DrawText(number, xpos, ypos)
        else:
            # Display that there are no images
            font = self.GetFont()
            font.SetWeight(wx.FONTWEIGHT_BOLD)
            dc.SetFont(font)
            dc.DrawLabel("No Images!", rect, wx.ALIGN_CENTER)

    def Next(self):
        """Goto next image"""
        self.idx += 1
        if self.idx >= len(self.images):
            self.idx = 0 # Go back to zero
        self.Refresh() # Causes a repaint

    def Previous(self):
        """Goto previous image"""
        self.idx -= 1
        if self.idx < 0:
            self.idx = len(self.images) - 1 # Goto end
        self.Refresh() # Causes a repaint

    def SetImageDir(self, imgpath):
        """Set the path to where the images are"""
        assert os.path.exists(imgpath)
        # Find all the images in the directory
        self.images = [ os.path.join(imgpath, img)
                        for img in os.listdir(imgpath)
                        if img.lower().endswith('.png') or
                           img.lower().endswith('.jpg') ]
        self.idx = 0

if __name__ == '__main__':
    app = SlideShowApp(False)
    app.MainLoop()
