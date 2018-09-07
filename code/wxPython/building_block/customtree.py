# Chapter 4: An Applications Building Blocks, Advanced Controls
# Recipe 2: CustomTreeCtrl
#
import os
import wx
import wx.lib.customtreectrl as customtree

#---- Recipe Code ----#

class FileBrowser(customtree.CustomTreeCtrl):
    FOLDER, \
    ERROR, \
    FILE = range(3)
    def __init__(self, parent, rootdir, *args, **kwargs):
        super(FileBrowser, self).__init__(parent,
                                          *args,
                                          **kwargs)
        assert os.path.exists(rootdir),\
               "Invalid Root Directory!"
        assert os.path.isdir(rootdir),\
               "rootdir must be a Directory!"

        # Attributes
        self._il = wx.ImageList(16, 16)
        self._root = rootdir
        self._rnode = None

        # Setup
        for art in (wx.ART_FOLDER, wx.ART_ERROR,
                    wx.ART_NORMAL_FILE):
            bmp = wx.ArtProvider.GetBitmap(art, size=(16,16))
            self._il.Add(bmp)
        self.SetImageList(self._il)
        self._rnode = self.AddRoot(os.path.basename(rootdir),
                                   image=FileBrowser.FOLDER,
                                   data=self._root)
        self.SetItemHasChildren(self._rnode, True)
        # Use Windows Vista style selections
        self.EnableSelectionVista(True)

        # Event Handlers
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpanding)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnCollapsed)

    def _GetFiles(self, path):
        try:
            files = [fname for fname in os.listdir(path)
                     if fname not in ('.', '..')]
        except OSError:
            files = None
        return files

    def OnCollapsed(self, event):
        item = event.GetItem()
        self.DeleteChildren(item)

    def OnExpanding(self, event):
        item = event.GetItem()
        path = self.GetPyData(item)
        files = self._GetFiles(path)

        # Handle Access Errors
        if files is None:
            self.SetItemImage(item, FileBrowser.ERROR)
            self.SetItemHasChildren(item, False)
            return

        for fname in files:
            fullpath = os.path.join(path, fname)
            if os.path.isdir(fullpath):
                self.AppendDir(item, fullpath)
            else:
                self.AppendFile(item, fullpath)

    def AppendDir(self, item, path):
        """Add a directory node"""
        assert os.path.isdir(path), "Not a valid directory!"
        name = os.path.basename(path)
        nitem = self.AppendItem(item, name,
                                image=FileBrowser.FOLDER,
                                data=path)
        self.SetItemHasChildren(nitem, True)

    def AppendFile(self, item, path):
        """Add a file to a node"""
        assert os.path.isfile(path), "Not a valid file!"
        name = os.path.basename(path)
        self.AppendItem(item, name,
                        image=FileBrowser.FILE,
                        data=path)

    def GetSelectedPath(self):
        """Get the selected path"""
        sel = self.GetSelection()
        path = self.GetItemPyData(sel)
        return path

    def GetSelectedPaths(self):
        """Get a list of selected paths"""
        sels = self.GetSelections()
        paths = [self.GetItemPyData(sel)
                 for sel in sels ]
        return paths

#---- End Recipe Code ----#

#---- Sample Application ----#

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="CustomTreeCtrl", size=(300,200))
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(MyFrame, self).__init__(parent, *args, **kwargs)

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
        self.browser = FileBrowser(self, wx.GetHomeDir())

        # Setup

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.browser, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # Event Handlers
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated)

    def OnItemActivated(self, event):
        path = self.browser.GetSelectedPath()
        self.GetTopLevelParent().PushStatusText(path)

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
