import wx;

class TPToolBar(wx.ToolBar):  
    """ transparent toolbar """  
    def __init__(self, parent, idx = wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,style=wx.BORDER_NONE|wx.TB_HORIZONTAL,name='PyToolBarNameStr' ):  
        style |= wx.CLIP_CHILDREN | wx.TRANSPARENT_WINDOW   
        wx.ToolBar.__init__(self, parent, idx, pos, size, style, name)  
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)  
  
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)  
      
    def OnEraseBackground(self, evt):  
        pass  
#---------------------------------------------  
class TPCheckBox(wx.CheckBox):  
    """ transparent checkbox  
        Important: The parent window must have wx.TRANSPARENT_WINDOW flag!!!! 
    """  
    def __init__(self, parent, idx = wx.ID_ANY, label=wx.EmptyString,   
        pos = wx.DefaultPosition, size = wx.DefaultSize,style=0,   
            validator = wx.DefaultValidator,name = wx.CheckBoxNameStr):          
        style |= wx.CLIP_CHILDREN | wx.TRANSPARENT_WINDOW   
        wx.CheckBox.__init__(self, parent, id=idx, label=label, pos = pos,   
                size = size, style = style, validator = validator, name = name)  
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)  
        self._spacing = 3  
          
        self.Bind(wx.EVT_PAINT,self.OnPaint)  
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)  
      
    def OnEraseBackground(self, evt):  
        pass  
  
    def Draw(self, dc):  
        dc.SetBackground(wx.TRANSPARENT_BRUSH )  
        dc.Clear()  
          
        render = wx.RendererNative.Get()  
          
        label = self.GetLabel()  
        spacing = self._spacing  
          
        width, height = self.GetClientSize()   
          
        textWidth, textHeight = dc.GetTextExtent(label)  
        cboxWidth, cboxHeight = 16, 16          
        cboxXpos = 0  
        cboxYpos = (height - textHeight)/2  
          
        textXpos = cboxWidth + spacing  
        textYpos = (height - textHeight)/2  
        if not self.IsChecked():  
            render.DrawCheckBox(self, dc, (cboxXpos, cboxYpos, cboxWidth, cboxHeight))  
        else:  
            render.DrawCheckBox(self, dc, (cboxXpos, cboxYpos, cboxWidth, cboxHeight), wx.CONTROL_CHECKED)  
              
        dc.SetFont(self.GetFont())  
        dc.DrawText(label, textXpos, textYpos)   
  
    def OnPaint(self, event):  
        dc = wx.GCDC(wx.PaintDC(self))  
        self.Draw(dc)  
          
          
#-----------------------------                  
class TPStaticText(wx.StaticText):  
    """ transparent StaticText """  
    def __init__(self,parent,idx,label='',  
                 pos=wx.DefaultPosition,  
                 size=wx.DefaultSize,  
                 style=0,  
                 name = 'TPStaticText'):  
        style |= wx.CLIP_CHILDREN | wx.TRANSPARENT_WINDOW   
        wx.StaticText.__init__(self,parent,idx,label,pos,size,style = style)  
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)  
        self.Bind(wx.EVT_PAINT,self.OnPaint)  
          
    def OnPaint(self,event):  
        event.Skip()  
        dc = wx.GCDC(wx.PaintDC(self) )  
        dc.SetFont(self.GetFont())                  
        dc.DrawText(self.GetLabel(), 0, 0)  