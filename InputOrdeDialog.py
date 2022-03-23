import wx
import os
import images
from ExcelOperation import GetSheetNameListFromExcelFileName,ExcelGridShowPanel
from ExcelOperation import GetSheetDataFromExcelFileName
dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class InputNewOrderDialog(wx.Dialog):
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
        self.newOrderIDTXT.SetValue('%05s'%str(self.newOrderID))
        hbox.Add(self.newOrderIDTXT, 1, wx.LEFT | wx.RIGHT, 10)
        vbox.Add(hbox,0,wx.EXPAND)
        mainInformationPanel.SetSizer(vbox)
        sizer.Add(panel,1,wx.EXPAND)
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

        # btn_ok.Bind(wx.EVT_BUTTON, self.OnOk)
        # btn_cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        # manualInputBTN.Bind(wx.EVT_BUTTON, self.OnCancel)

    # def OnOk(self, event):
    #     event.Skip()
    #
    # def OnCancel(self, event):
    #     # self.log.WriteText("操作员：'%s' 取消库存参数设置操作\r\n"%(self.parent.operator_name))
    #     event.Skip()

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
        self.mainInformationPanel = wx.Panel(panel,size=(-1,50))
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 20))
        vbox.Add(self.mainInformationPanel,0,wx.EXPAND)
        hbox = wx.BoxSizer()
        hbox.Add(10, -1)
        hbox.Add(wx.StaticText(self.mainInformationPanel, label='订单号：'), 0, wx.TOP, 5)
        self.newOrderIDTXT = wx.TextCtrl(self.mainInformationPanel, size=(50, 25),style=wx.TE_READONLY)
        self.newOrderIDTXT.SetValue('%05d'%self.newOrderID)
        hbox.Add(self.newOrderIDTXT, 0, wx.LEFT | wx.RIGHT, 10)
        self.mainInformationPanel.SetSizer(hbox)

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
        sheetNameListTemp = []
        for sheetName in self.sheetNameList:
            dataTemp = GetSheetDataFromExcelFileName(self.parent.excelFileName, sheetName)
            if dataTemp.shape[0]>0 and dataTemp.shape[1]>0:
                sheetNameListTemp.append(sheetName)
                sheetPage = ExcelGridShowPanel(self.notebook,self.parent.excelFileName,sheetName)
                self.notebook.AddPage(sheetPage,sheetName)
                self.sheetPage.append(sheetPage)
        self.sheetNameList = sheetNameListTemp

        if len(self.sheetNameList)>0:
            self.newOrderID = self.GetMainOrderID()
            self.newOrderName = self.GetMainOrderName()
            self.subOrderIDList = self.GetSubOrderIDList()
            print(self.GetKeyDataColPosition())
            self.ReCreateMainInformationPanel()
            # btn_ok.Bind(wx.EVT_BUTTON, self.OnOk)
        # btn_cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        # manualInputBTN.Bind(wx.EVT_BUTTON, self.OnCancel)

    # def OnOk(self, event):
    #     event.Skip()
    #
    # def OnCancel(self, event):
    #     # self.log.WriteText("操作员：'%s' 取消库存参数设置操作\r\n"%(self.parent.operator_name))

    def ReCreateMainInformationPanel(self):
        self.mainInformationPanel.DestroyChildren()
        hbox = wx.BoxSizer()
        hbox.Add(10, -1)
        hbox.Add(wx.StaticText(self.mainInformationPanel, label='订单号：', size=(50,-1)), 0, wx.TOP, 5)
        self.newOrderIDTXT = wx.TextCtrl(self.mainInformationPanel, size=(60, -1),style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        self.newOrderIDTXT.SetValue('%05d'%self.newOrderID)
        self.newOrderIDTXT.SetBackgroundColour(wx.RED)
        hbox.Add(self.newOrderIDTXT, 0, wx.RIGHT, 20)

        hbox.Add(wx.StaticText(self.mainInformationPanel, label='订单名称：', size=(60,-1)), 0, wx.TOP, 5)
        self.newOrderNameTXT = wx.TextCtrl(self.mainInformationPanel, size=(100, -1),style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        self.newOrderNameTXT.SetBackgroundColour(wx.YELLOW)
        self.newOrderNameTXT.SetValue(self.newOrderName)
        hbox.Add(self.newOrderNameTXT, 0, wx.RIGHT, 20)



        hbox.Add(wx.StaticText(self.mainInformationPanel, label='子订单：', size=(50,-1)), 0, wx.TOP, 5)
        self.subOrderIDCombo = wx.ComboBox(self.mainInformationPanel, size=(80,25),
                                           choices=self.subOrderIDList, style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        self.subOrderIDCombo.SetBackgroundColour(wx.GREEN)
        self.subOrderIDCombo.SetValue(self.subOrderIDList[0])
        hbox.Add(self.subOrderIDCombo, 0, wx.RIGHT, 20)
        self.mainInformationPanel.SetSizer(hbox)
        self.mainInformationPanel.Layout()
    #     event.Skip()
    def GetMainOrderID(self):
        for i, row in enumerate(self.sheetPage[0].data):
            if "Project" in row:
                row = list(row)
                col = row.index("Project")
                for j,item in enumerate(row[col+1:]):
                    if item:
                        self.sheetPage[0].SetCellBackgroundColour(i,j+col+1,wx.RED)
                        return int(item)
        return -1
    def GetMainOrderName(self):
        for i, row in enumerate(self.sheetPage[0].data):
            if "Project name" in row:
                row = list(row)
                col = row.index("Project name")
                for j, item in enumerate(row[col+1:]):
                    if item:
                        self.sheetPage[0].SetCellBackgroundColour(i,j+col+1,wx.YELLOW)
                        return item
        return ""
    def GetSubOrderIDList(self):
        result = []
        for page in self.sheetPage:
            nextPage = False
            for i, row in enumerate(page.data):
                if nextPage:
                    break
                else:
                    if "SubProject" in row:
                        row = list(row)
                        col = row.index("SubProject")
                        for j, item in enumerate(row[col+1:]):
                            if nextPage:
                                break
                            else:
                                if item:
                                    page.SetCellBackgroundColour(i, j + col + 1, wx.GREEN)
                                    result.append(str(item))
                                    nextPage = True
        return result

    def GetKeyDataColPosition(self):#查找子订单号，甲板，区域，房间所在的列号：
        result = []
        for pageNum, page in enumerate(self.sheetPage):
            for i, row in enumerate(page.data):
                if "SProj" in row and "DECK" in row and "AREA" in row and "ROOM" in row:
                    rowNum = i
                    rowData = list(row)
                    suborderColNum = rowData.index("SProj")
                    deckColNum = rowData.index("DECK")
                    areaColNum = rowData.index("AREA")
                    roomColNum = rowData.index("ROOM")
                    break
            for i, row in enumerate(page.data[rowNum+1:]):
                if row[suborderColNum]==self.subOrderIDList[pageNum]:
                    rowNumStart = i+rowNum+1
                    break
            for i, row in enumerate(page.data[rowNumStart+1:]):
                print(row[suborderColNum], row[deckColNum], row[areaColNum], row[roomColNum])
                if  row[suborderColNum]==None and row[deckColNum]==None and row[areaColNum]==None and row[roomColNum]==None:
                    print("here")
                    rowNumEnd = i+rowNumStart
                    break
            result.append([[rowNumStart,rowNumEnd],[suborderColNum,deckColNum,areaColNum,roomColNum]])
        return result