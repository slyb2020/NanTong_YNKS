import wx
import os
import images
from ExcelOperation import GetSheetNameListFromExcelFileName,ExcelGridShowPanel

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class ImportOrderFromExcelDialog(wx.Dialog):
    def __init__(self, parent, newOrderID, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.newOrderID = newOrderID
        self.parent = parent
        # self.log.WriteText("操作员：'%s' 开始执行库存参数设置操作。。。\r\n"%(self.parent.operator_name))
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "订单关键信息输入对话框", pos, size, style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, -1, size=(1700, 800))
        mainInformationPanel = wx.Panel(panel,size=(-1,50))
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 20))
        vbox.Add(mainInformationPanel,0,wx.EXPAND)
        hbox = wx.BoxSizer()
        hbox.Add(10, -1)
        hbox.Add(wx.StaticText(mainInformationPanel, label='订单号：'), 0, wx.TOP, 5)
        self.newOrderIDTXT = wx.TextCtrl(mainInformationPanel, size=(50, 25),style=wx.TE_READONLY)
        self.newOrderIDTXT.SetValue('%05d'%self.newOrderID)
        hbox.Add(self.newOrderIDTXT, 1, wx.LEFT | wx.RIGHT, 10)
        mainInformationPanel.SetSizer(hbox)

        self.notebook = wx.Notebook(panel, -1, size=(21, 21), style=
                                    # wx.BK_DEFAULT
                                    # wx.BK_TOP
                                    wx.BK_BOTTOM
                                    # wx.BK_LEFT
                                    # wx.BK_RIGHT
                                    # | wx.NB_MULTILINE
                                    )
        il = wx.ImageList(16, 16)
        idx1 = il.Add(images._rt_smiley.GetBitmap())
        self.total_page_num = 0
        self.notebook.AssignImageList(il)
        idx2 = il.Add(images.GridBG.GetBitmap())
        idx3 = il.Add(images.Smiles.GetBitmap())
        idx4 = il.Add(images._rt_undo.GetBitmap())
        idx5 = il.Add(images._rt_save.GetBitmap())
        idx6 = il.Add(images._rt_redo.GetBitmap())
        vbox.Add(self.notebook,1,wx.EXPAND|wx.LEFT|wx.RIGHT,10)
        panel.SetSizer(vbox)
        # panel.SetBackgroundColour(wx.Colour(234,219,212))
        sizer.Add(panel, 0, wx.EXPAND)
        line = wx.StaticLine(self, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.BoxSizer()
        bitmap1 = wx.Bitmap(bitmapDir+"/ok3.png", wx.BITMAP_TYPE_PNG)
        bitmap2 = wx.Bitmap(bitmapDir+"/cancel1.png", wx.BITMAP_TYPE_PNG)
        bitmap3 = wx.Bitmap(bitmapDir+"/33.png", wx.BITMAP_TYPE_PNG)
        btn_ok = wx.Button(self, wx.ID_OK, "确  定", size=(200, 50))
        btn_ok.SetBitmap(bitmap1, wx.LEFT)
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "取  消", size=(200, 50))
        btn_cancel.SetBitmap(bitmap2, wx.LEFT)
        btnsizer.Add(btn_ok, 0)
        btnsizer.Add((40, -1), 0)
        btnsizer.Add(btn_cancel, 0)
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)

        self.sheetNameList = GetSheetNameListFromExcelFileName(self.parent.excelFileName)
        self.sheetPage=[]
        for sheetName in self.sheetNameList:
            sheetPage = ExcelGridShowPanel(self.notebook,self.parent.excelFileName,sheetName)
            self.notebook.AddPage(sheetPage,sheetName)
            self.sheetPage.append(sheetPage)
        # btn_ok.Bind(wx.EVT_BUTTON, self.OnOk)
        # btn_cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        # manualInputBTN.Bind(wx.EVT_BUTTON, self.OnCancel)

    # def OnOk(self, event):
    #     event.Skip()
    #
    # def OnCancel(self, event):
    #     # self.log.WriteText("操作员：'%s' 取消库存参数设置操作\r\n"%(self.parent.operator_name))
    #     event.Skip()
