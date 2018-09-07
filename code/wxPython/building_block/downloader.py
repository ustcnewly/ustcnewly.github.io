# Chapter 5: Providing Information and Alerting Users
# Recipe 6: ProgressDialog
#
import wx
import os
import sys
import urllib2

class DownloaderApp(wx.App):
    def OnInit(self):
        # Create a hidden frame so that the eventloop
        # does not automatically exit before we show
        # the download dialog.
        self.frame = wx.Frame(None)
        self.frame.Hide()
        return True

    def Cleanup(self):
        self.frame.Destroy()

    def DownloadFile(self, url):
        """Downloads the file
        @return: bool (success/fail)
        """
        dialog = None
        try:
            # Open the url to read from and
            # the local file to write the downloaded
            # data to.
            webfile = urllib2.urlopen(url)
            size = int(webfile.info()['Content-Length'])
            dlpath = os.path.abspath(os.getcwd())
            dlfile = url.split('/')[-1]
            dlpath = GetUniqueName(dlpath, dlfile)
            localfile = open(dlpath, 'wb')

            # Create the ProgressDialog
            dlmsg = "Downloading: %s" % dlfile
            style = (wx.PD_APP_MODAL
                     |wx.PD_CAN_ABORT
                     |wx.PD_ELAPSED_TIME
                     |wx.PD_REMAINING_TIME)
            dialog = wx.ProgressDialog("Download Dialog",
                                       dlmsg,
                                       maximum=size,
                                       parent=self.frame,
                                       style=style)

            # Download the file
            blk_sz = 4096
            read = 0
            keep_going = True
            while read < size and keep_going:
                data = webfile.read(blk_sz)
                localfile.write(data)
                read += len(data)
                keep_going, skip = dialog.Update(read)

            localfile.close()
            webfile.close()
        finally:
            # All done so cleanup top level windows
            # to cause the event loop to exit.
            if dialog:
                dialog.Destroy()
            self.Cleanup()

#--- Utility Functions ----#

def GetUniqueName(path, name):
    """Make a file name that will be unique in case a file
    of the same name already exists at that path.
    @param path: Root path to folder of files destination
    @param name: desired file name base
    @return: string
    """
    tmpname = os.path.join(path, name)
    if os.path.exists(tmpname):
        if '.' not in name:
            ext = ''
            fbase = name
        else:
            ext = '.' + name.split('.')[-1]
            fbase = name[:-1 * len(ext)]

        inc = len([x for x in os.listdir(path)
                   if x.startswith(fbase)])
        newname = "%s-%d%s" % (fbase, inc, ext)
        tmpname = os.path.join(path, newname)
        while os.path.exists(tmpname):
            inc = inc + 1
            newname = "%s-%d%s" % (fbase, inc, ext)
            tmpname = os.path.join(path, newname)

    return tmpname

#---- Main Execution ----#
if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        app = DownloaderApp(False)
        # Start with a slight delay so the eventloop
        # can start running, to ensure our dialog gets
        # shown
        wx.CallLater(2000, app.DownloadFile, url)
        app.MainLoop()
    else:
        # Print some help text
        print(("wxPython Cookbook - ProgressDialog\n"
               "usage: downloader url\n"))
