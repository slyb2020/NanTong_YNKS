import wx
import os
import wx.lib.scrolledpanel as scrolled
from ID_DEFINE import *
from DBOperation import GetSubOrderPackageState,UpdateSubOrderPackageState,GetSubOrderPanelsForPackage
import numpy as np

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')

class TopViewPanel(wx.Panel):
    def __init__(self,parent,data=[],size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, size=size)
        self.parent = parent
        self.data = [
                        [(800,200),(500,200),(400,200)],
                        [(1000,200),(500,200),(500,200)],
                        [(1800,200),(1000,200)]
                    ]
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.nameTXT = wx.TextCtrl(self,size=(10,40))
        vbox.Add(self.nameTXT,0,wx.EXPAND)
        totalRow = len(self.data)
        if totalRow>0:
            for row in range(totalRow):
                hbox = wx.BoxSizer()
                for col in range(len(self.data[row])):
                    button = wx.Button(self,label="%sX%s"%(self.data[row][col]),size=(1,1),name="%s,%s"%(row,col))
                    button.SetBackgroundColour(wx.Colour(210,210,210))
                    print("totalRow,row,col=",totalRow,row,col)
                    hbox.Add(button,self.data[row][col][0],wx.EXPAND)
                vbox.Add(hbox,self.data[row][0][1],wx.EXPAND)
        self.SetSizer(vbox)

class FrontViewPanel(wx.Panel):
    def __init__(self,parent,data=[],size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, size=size)
        self.parent = parent
        self.state=""
        self.data = [
                        [
                            25,[
                                    [(800,200),(500,200)],
                                    [(800,200),(500,200)],
                               ]
                        ],
                        [25,[[(800,200),(500,200)]],[[(800,200),(500,200)]]],
                        [50,[[(800,200),(500,200)]],[[(800,200),(500,200)]]],
                        [25,[[(800,200),(500,200)]],[[(800,200),(500,200)]]],
                        [25,[[(800,200),(500,200)]],[[(800,200),(500,200)]]],
                        [50,[[(800,200),(500,200)]],[[(800,200),(500,200)]]],
                    ]
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.nameTXT = wx.TextCtrl(self,size=(10,40))
        vbox.Add(self.nameTXT,0,wx.EXPAND)
        totalLayer = len(self.data)
        if totalLayer>0:
            for i in range(totalLayer):
                button = wx.Button(self,label="第%d层"%(totalLayer-i),size=(10,-1),name="%s"%(totalLayer-i-1))
                button.SetForegroundColour(wx.YELLOW)
                button.SetBackgroundColour(wx.Colour(111,123,245))
                vbox.Add(button,self.data[i][0],wx.EXPAND)
        self.SetSizer(vbox)

class PackagePanel(wx.Panel):
    def __init__(self,parent,master,data,name=""):
        self.master = master
        self.name=name
        self.size = (120,120)
        wx.Panel.__init__(self, parent, size=self.size)
        self.data = data
        self.frame = wx.StaticBox(self,label=data[0],size=(10,10))
        hbox =wx.BoxSizer()
        hbox.Add(self.frame,1,wx.EXPAND|wx.ALL,2)
        self.SetSizer(hbox)
        self.frame.SetBackgroundColour(wx.Colour(240,240,240))
        self.Bind(wx.EVT_LEFT_DOWN,self.OnLeftClick)
        self.state = ""

    def GetName(self):
        return self.name

    def OnLeftClick(self,event):
        obj = event.GetEventObject()
        name = obj.GetName()
        for i,box in enumerate(self.master.boxList):
            if box.GetName()==name:
                if box.state=="":
                    if self.master.leftFrontViewPanel.state != "占用" or self.master.rightFrontViewPanel.state != "占用":
                        box.frame.SetBackgroundColour(wx.Colour(124,234,233))
                        self.master.boxList[i].state='选定'
                    if self.master.leftFrontViewPanel.state != "占用":
                        self.master.leftTopDownloadBTN.Enable(True)
                    if self.master.rightFrontViewPanel.state != "占用":
                        self.master.rightTopDownloadBTN.Enable(True)
            elif box.state=="选定":
                self.master.boxList[i].state=""
                box.frame.SetBackgroundColour(wx.Colour(240,240,240))
            box.frame.Refresh()
        # self.frame.SetBackgroundColour(wx.GREEN)
        # self.frame.Refresh()
        event.Skip()

class PackageDialog(wx.Dialog):
    def __init__(self, parent, log, data, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        print("data=",data)
        self.orderID = data[0]
        self.suborderID = data[8]
        self.log = log
        self.parent = parent
        self.panelTotlAmount=0
        self.panelTotlWeight=0
        self.boxTotalAmount=0
        self.boxList = []
        # self.log.WriteText("操作员：'%s' 开始执行库存参数设置操作。。。\r\n"%(self.parent.operator_name))
        _, self.packageState = GetSubOrderPackageState(self.log,WHICHDB,self.orderID,self.suborderID)
        if self.packageState not in ["按房间打包","按区域打包"]:
            self.packageState = "未打包"
        # if state == "":
        #     self.CalculateSubOrderPackage()
            # UpdateSubOrderPackageState(self.log, WHICHDB, self.orderID, self.suborderID, state)
        # else:
        #     state = ""
        #     UpdateSubOrderPackageState(self.log,WHICHDB,self.orderID,self.suborderID,state)
        _, self.panelList = GetSubOrderPanelsForPackage(self.log,WHICHDB,self.orderID,self.suborderID)
        for panel in self.panelList:
            self.panelTotlAmount+=panel[9]
            self.panelTotlWeight+=(float(panel[9])*float(panel[18]))
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "产品打包操作对话框", pos, size, style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, -1, size=(1800, 900))
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 10))
        hbox = wx.BoxSizer()
        hbox.Add(10, -1)
        vvbox = wx.BoxSizer(wx.VERTICAL)
        hhbox = wx.BoxSizer()
        hhbox.Add(wx.StaticText(panel, label='订单号：'), 0, wx.TOP, 5)
        self.orderIDTXT = wx.TextCtrl(panel, size=(70, 25), style=wx.TE_READONLY)
        self.orderIDTXT.SetValue('%05d-%03d' % (int(self.orderID),int(self.suborderID)))
        self.orderIDTXT.SetBackgroundColour(wx.GREEN)
        hhbox.Add(self.orderIDTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(panel, label='当前打包状态：'), 0, wx.TOP, 5)
        self.packageStateTXT = wx.TextCtrl(panel, size=(70, 25), style=wx.TE_READONLY)
        self.packageStateTXT.SetValue(self.packageState)
        self.packageStateTXT.SetBackgroundColour(wx.YELLOW)
        hhbox.Add(self.packageStateTXT, 0, wx.LEFT | wx.RIGHT, 10)
        vvbox.Add(hhbox,0,wx.EXPAND)
        hhbox = wx.BoxSizer()
        hhbox.Add(wx.StaticText(panel, label='面板总数(Pcs)：'), 0, wx.TOP, 5)
        self.panelTotlAmountTXT = wx.TextCtrl(panel, size=(50, 25), style=wx.TE_READONLY)
        self.panelTotlAmountTXT.SetValue(str(self.panelTotlAmount))
        self.panelTotlAmountTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.panelTotlAmountTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(panel, label='面板总重量(Kg)：'), 0, wx.TOP, 5)
        self.panelTotlWeightTXT = wx.TextCtrl(panel, size=(70, 25), style=wx.TE_READONLY)
        self.panelTotlWeightTXT.SetValue(str(self.panelTotlWeight))
        self.panelTotlWeightTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.panelTotlWeightTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(panel, label='托盘总数：'), 0, wx.TOP, 5)
        self.boxTotalAmountTXT = wx.TextCtrl(panel, size=(40, 25), style=wx.TE_READONLY)
        self.boxTotalAmountTXT.SetValue(str(self.boxTotalAmount))
        self.boxTotalAmountTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.boxTotalAmountTXT, 0, wx.LEFT | wx.RIGHT, 10)
        vvbox.Add((-1,10))
        vvbox.Add(hhbox,0,wx.EXPAND)
        hbox.Add(vvbox,0)

        hbox.Add(wx.StaticLine(panel,style=wx.VERTICAL),0,wx.EXPAND|wx.LEFT|wx.RIGHT,10)

        hbox.Add((10,-1))

        vvbox =wx.BoxSizer(wx.VERTICAL)
        hhbox = wx.BoxSizer()
        hhbox.Add(wx.StaticText(panel, label='甲板：'), 0, wx.TOP, 5)
        temp=np.array(self.panelList)[:,3]
        choiceList = list(set(temp))
        if len(choiceList)>1:
            choiceList.insert(0,"全部")
        self.deckCOMBO = wx.ComboBox(panel, value=choiceList[0], size=(40, 25),choices=choiceList, style=wx.TE_READONLY)
        self.deckCOMBO.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.deckCOMBO, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(panel, label='区域：'), 0, wx.TOP, 5)
        deck = self.deckCOMBO.GetValue()
        if deck == "全部":
            temp = np.array(self.panelList)[:, 4]
        else:
            temp = []
            for record in self.panelList:
                if str(record[3])==deck:
                    temp.append(str(record[4]))
        choiceList = list(set(temp))
        if len(choiceList)>1:
            choiceList.insert(0,"全部")
        self.zoneCOMBO = wx.ComboBox(panel, value=choiceList[0], size=(40, 25),choices=choiceList, style=wx.TE_READONLY)
        self.zoneCOMBO.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.zoneCOMBO, 0, wx.LEFT | wx.RIGHT, 10)

        if self.packageState!="按区域打包": #当按区域打包时，不应该显示房间Combobox
            hhbox.Add((10,-1))
            hhbox.Add(wx.StaticText(panel, label='房间：'), 0, wx.TOP, 5)
            deck = self.deckCOMBO.GetValue()
            zone = self.zoneCOMBO.GetValue()
            temp=[]
            if deck == "全部":
                if zone == "全部":
                    temp = np.array(self.panelList)[:, 5]
                else:
                    for record in self.panelList:
                        if str(record[4])==zone:
                            temp.append(str(record[5]))
            else:
                if zone == "全部":
                    for record in self.panelList:
                        if str(record[3])==deck:
                            temp.append(str(record[5]))
                else:
                    for record in self.panelList:
                        if str(record[4])==zone and str(record[3])==deck:
                            print("record=",record)
                            temp.append(str(record[5]))
            print("temp=",temp)
            choiceList = list(set(temp))
            if len(choiceList)>1:
                choiceList.insert(0,"全部")
            self.roomCOMBO = wx.ComboBox(panel, value=choiceList[0], size=(100, 25),choices=choiceList, style=wx.TE_READONLY)
            self.roomCOMBO.SetBackgroundColour(wx.WHITE)
            hhbox.Add(self.roomCOMBO, 0, wx.LEFT | wx.RIGHT, 10)
        vvbox.Add((-1,20))
        vvbox.Add(hhbox,0,wx.EXPAND)
        hbox.Add(vvbox,0,wx.EXPAND)

        vvbox = wx.BoxSizer(wx.VERTICAL)
        hhbox = wx.BoxSizer()
        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(panel, label='当前面板总数(Pcs)：'), 0, wx.TOP, 5)
        self.currentPanelTotlAmountTXT = wx.TextCtrl(panel, size=(50, 25), style=wx.TE_READONLY)
        self.currentPanelTotlAmountTXT.SetValue(str(self.panelTotlAmount))
        self.currentPanelTotlAmountTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.currentPanelTotlAmountTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(panel, label='当前面板总重量(Kg)：'), 0, wx.TOP, 5)
        self.currentPanelTotlWeightTXT = wx.TextCtrl(panel, size=(70, 25), style=wx.TE_READONLY)
        self.currentPanelTotlWeightTXT.SetValue(str(self.panelTotlWeight))
        self.currentPanelTotlWeightTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.currentPanelTotlWeightTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(panel, label='当前托盘总数：'), 0, wx.TOP, 5)
        self.currentBoxTotalAmountTXT = wx.TextCtrl(panel, size=(40, 25), style=wx.TE_READONLY)
        self.currentBoxTotalAmountTXT.SetValue(str(self.boxTotalAmount))
        self.currentBoxTotalAmountTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.currentBoxTotalAmountTXT, 0, wx.LEFT | wx.RIGHT, 10)
        vvbox.Add((-1,10))
        vvbox.Add(hhbox,0,wx.EXPAND)

        hhbox = wx.BoxSizer()
        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(panel, label='选中面板总数(Pcs)：'), 0, wx.TOP, 5)
        self.selectionPanelTotlAmountTXT = wx.TextCtrl(panel, size=(50, 25), style=wx.TE_READONLY)
        self.selectionPanelTotlAmountTXT.SetValue("")
        self.selectionPanelTotlAmountTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.selectionPanelTotlAmountTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(panel, label='选中面板总重量(Kg)：'), 0, wx.TOP, 5)
        self.selectionPanelTotlWeightTXT = wx.TextCtrl(panel, size=(70, 25), style=wx.TE_READONLY)
        self.selectionPanelTotlWeightTXT.SetValue("")
        self.selectionPanelTotlWeightTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.selectionPanelTotlWeightTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(panel, label='选中托盘名称：'), 0, wx.TOP, 5)
        self.selectionBoxIDTXT = wx.TextCtrl(panel, size=(40, 25), style=wx.TE_READONLY)
        self.selectionBoxIDTXT.SetValue("")
        self.selectionBoxIDTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.selectionBoxIDTXT, 0, wx.LEFT | wx.RIGHT, 10)
        vvbox.Add((-1,10))
        vvbox.Add(hhbox,0,wx.EXPAND)
        hbox.Add(vvbox,0)


        vbox.Add(hbox, 0, wx.EXPAND)
        vbox.Add(wx.StaticLine(panel,size=(10,2),style=wx.HORIZONTAL),0,wx.EXPAND|wx.TOP,10)

        self.finishPackagePanel = scrolled.ScrolledPanel(panel,size=(100,200))
        vbox.Add(self.finishPackagePanel,1,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,10)
        hhbox = wx.BoxSizer()
        hhbox.Add((10,-1))
        self.leftWorkingPackagePanel = wx.Panel(panel,size=(100,400))
        hhbox.Add(self.leftWorkingPackagePanel,1,wx.EXPAND)
        self.middleControlPanel = wx.Panel(panel,size=(50,-1))
        self.middleControlPanel.SetBackgroundColour(wx.Colour(220,220,220))
        hhbox.Add(self.middleControlPanel,0,wx.EXPAND)
        self.rightWorkingPackagePanel = wx.Panel(panel,size=(100,400))
        hhbox.Add(self.rightWorkingPackagePanel,1,wx.EXPAND)
        hhbox.Add((10,-1))
        vbox.Add(hhbox,0,wx.EXPAND)
        self.bottomPackagePanel = scrolled.ScrolledPanel(panel,size=(100,150))
        vbox.Add(self.bottomPackagePanel,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,10)
        panel.SetSizer(vbox)

        vvbox=wx.BoxSizer(wx.VERTICAL)
        hhbox = wx.BoxSizer()
        self.leftTopDownloadBTN = wx.Button(self.leftWorkingPackagePanel,label="▼ 将选定托盘下载到左侧工作区",size=(100,50))
        self.leftTopDownloadBTN.Bind(wx.EVT_BUTTON, self.OnLeftTopDownloadBTN)
        self.leftTopDownloadBTN.Enable(False)
        self.leftTopUploadBTN = wx.Button(self.leftWorkingPackagePanel,label="▲ 将左侧工作区中的托盘上传到完成区",size=(100,50))
        self.leftTopUploadBTN.Enable(False)
        hhbox.Add(self.leftTopDownloadBTN,1)
        hhbox.Add(self.leftTopUploadBTN,1)
        vvbox.Add(hhbox,0,wx.EXPAND)
        hhbox = wx.BoxSizer()
        self.leftFrontViewPanel = FrontViewPanel(self.leftWorkingPackagePanel,size=(100,100))
        self.leftTopViewPanel = TopViewPanel(self.leftWorkingPackagePanel,size=(100,100))
        hhbox.Add(self.leftFrontViewPanel,1,wx.EXPAND)
        hhbox.Add(self.leftTopViewPanel,1,wx.EXPAND)
        vvbox.Add(hhbox,1,wx.EXPAND)
        hhbox = wx.BoxSizer()
        self.leftBottomDownloadBTN = wx.Button(self.leftWorkingPackagePanel,label="▼",size=(100,50))
        self.leftBottonUploadBTN = wx.Button(self.leftWorkingPackagePanel,label="▲",size=(100,50))
        hhbox.Add(self.leftBottomDownloadBTN,1)
        hhbox.Add(self.leftBottonUploadBTN,1)
        vvbox.Add(hhbox,0,wx.EXPAND)
        self.leftWorkingPackagePanel.SetSizer(vvbox)

        vvbox=wx.BoxSizer(wx.VERTICAL)
        hhbox = wx.BoxSizer()
        self.rightTopDownloadBTN = wx.Button(self.rightWorkingPackagePanel,label="▼",size=(100,50))
        self.rightTopDownloadBTN.Bind(wx.EVT_BUTTON, self.OnRightTopDownloadBTN)
        self.rightTopUploadBTN = wx.Button(self.rightWorkingPackagePanel,label="▲",size=(100,50))
        self.rightTopDownloadBTN.Enable(False)
        self.rightTopUploadBTN.Enable(False)
        hhbox.Add(self.rightTopDownloadBTN,1)
        hhbox.Add(self.rightTopUploadBTN,1)
        vvbox.Add(hhbox,0,wx.EXPAND)
        hhbox = wx.BoxSizer()
        self.rightFrontViewPanel = FrontViewPanel(self.rightWorkingPackagePanel,size=(100,100))
        self.rightTopViewPanel = TopViewPanel(self.rightWorkingPackagePanel,size=(100,100))
        hhbox.Add(self.rightTopViewPanel,1,wx.EXPAND)
        hhbox.Add(self.rightFrontViewPanel,1,wx.EXPAND)
        vvbox.Add(hhbox,1,wx.EXPAND)
        hhbox = wx.BoxSizer()
        self.rightBottomDownloadBTN = wx.Button(self.rightWorkingPackagePanel,label="▼",size=(100,50))
        self.rightBottonUploadBTN = wx.Button(self.rightWorkingPackagePanel,label="▲",size=(100,50))
        hhbox.Add(self.rightBottomDownloadBTN,1)
        hhbox.Add(self.rightBottonUploadBTN,1)
        vvbox.Add(hhbox,0,wx.EXPAND)
        self.rightWorkingPackagePanel.SetSizer(vvbox)

        self.middleLeftAddBTN = wx.Button(self.middleControlPanel,label="<<+",size=(10,50))
        self.middleRightAddBTN = wx.Button(self.middleControlPanel,label="+>>",size=(10,50))
        self.middleLeftBTN = wx.Button(self.middleControlPanel,label=">>",size=(10,20))
        self.middleRightBTN = wx.Button(self.middleControlPanel,label="<<",size=(10,20))
        vvbox = wx.BoxSizer(wx.VERTICAL)
        vvbox.Add(self.middleLeftAddBTN,0,wx.EXPAND)
        vvbox.Add(self.middleRightBTN,1,wx.EXPAND)
        vvbox.Add(self.middleLeftBTN,1,wx.EXPAND)
        vvbox.Add(self.middleRightAddBTN,0,wx.EXPAND)
        self.middleControlPanel.SetSizer(vvbox)


        hbox=wx.BoxSizer()
        for i in range(20):
            package = PackagePanel(self.finishPackagePanel,self,["货盘%s"%i],name=str(i))
            self.boxList.append(package)
            hbox.Add(package)
        self.finishPackagePanel.SetSizer(hbox)
        self.finishPackagePanel.SetAutoLayout(1)
        self.finishPackagePanel.SetupScrolling()



        # panel.SetBackgroundColour(wx.Colour(234,219,212))
        sizer.Add(panel, 0, wx.EXPAND)
        line = wx.StaticLine(self, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.BoxSizer()
        bitmap1 = wx.Bitmap("bitmaps/ok3.png", wx.BITMAP_TYPE_PNG)
        bitmap2 = wx.Bitmap("bitmaps/cancel1.png", wx.BITMAP_TYPE_PNG)
        bitmap3 = wx.Bitmap("bitmaps/33.png", wx.BITMAP_TYPE_PNG)
        btn_repack = wx.Button(self, label="全部重新打包", size=(200, 50))
        btn_repack.SetBitmap(bitmap1, wx.LEFT)
        btn_save = wx.Button(self, label="保存 (Save)", size=(200, 50))
        btn_save.SetBitmap(bitmap2, wx.LEFT)
        btn_ok = wx.Button(self, wx.ID_OK, "确  定", size=(200, 50))
        btn_ok.SetBitmap(bitmap1, wx.LEFT)
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "取  消", size=(200, 50))
        btn_cancel.SetBitmap(bitmap2, wx.LEFT)
        btnsizer.Add(btn_repack, 0)
        btnsizer.Add((40, -1), 0)
        btnsizer.Add(btn_save, 0)
        btnsizer.Add((40, -1), 0)
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

    def CalculateSubOrderPackage(self):
        _,self.panelList=GetSubOrderPanelsForPackage(self.log,WHICHDB,self.orderID,self.suborderID)
        for panel in self.panelList:
            print("panel=",panel)

    def OnLeftTopDownloadBTN(self, event):
        error=True
        for i, box in enumerate(self.boxList):
            if box.state=='选定':
                error=False
                box.frame.SetBackgroundColour(wx.Colour(234,124,233))
                self.leftFrontViewPanel.state="占用"
                self.boxList[i].state="左"
                box.frame.Refresh()
                self.leftTopDownloadBTN.Enable(False)
                self.leftTopUploadBTN.Enable(True)
        if error:
            wx.MessageBox("您还没有选择要移入左侧工作区的托盘！")
        # self.frame.SetBackgroundColour(wx.GREEN)
        # self.frame.Refresh()
        event.Skip()
    def OnRightTopDownloadBTN(self, event):
        error=True
        for i, box in enumerate(self.boxList):
            if box.state=='选定':
                error=False
                box.frame.SetBackgroundColour(wx.Colour(189,174,233))
                self.rightFrontViewPanel.state="占用"
                self.boxList[i].state="右"
                box.frame.Refresh()
                self.rightTopDownloadBTN.Enable(False)
                self.rightTopUploadBTN.Enable(True)
        if error:
            wx.MessageBox("您还没有选择要移入左侧工作区的托盘！")
        # self.frame.SetBackgroundColour(wx.GREEN)
        # self.frame.Refresh()
        event.Skip()
