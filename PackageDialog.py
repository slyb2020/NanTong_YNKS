import wx
import os
import wx.lib.scrolledpanel as scrolled
from ID_DEFINE import *
from DBOperation import GetSubOrderPackageState,UpdateSubOrderPackageState,GetSubOrderPanelsForPackage,\
    CreatePackagePanelSheetForOrder,InsertPanelDetailIntoPackageDB,GetSubOrderPanelsForPackageFromPackageDB
import numpy as np
from operator import itemgetter

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
        self.panelTotalAmount=0
        self.panelTotalWeight=0
        self.panelTotalSquare=0
        self.boxTotalAmount=0
        self.boxList = []
        dbName = "p%s"%self.orderID
        from DBOperation import GetTableListFromDB
        _,dbNameList = GetTableListFromDB(self.log,WHICHDB)
        if dbName not in dbNameList:
            CreatePackagePanelSheetForOrder(log,WHICHDB,dbName)
            _, self.panelList = GetSubOrderPanelsForPackage(self.log, WHICHDB, self.orderID)#读取订单中所有子订单数据
            self.data=[]
            for record in self.panelList:
                # print("recor",record)
                # [93, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D40RLA', 1, '1240', '400', '50', 'RAL9010','G', 'None', 'None', '64731-0093', '2.98', '']
                for i in range(int(record[9])):
                    #       `订单号`, `子订单号`, `甲板`,   `区域`,    `房间`,       `图纸`,   `产品类型`,`面板代码`,    `宽度`, `高度`, `厚度`, `X面颜色`, `Y面颜色`, `Z面颜色`, `V面颜色`, `数量`, `面板代码`
                #          [1, 64731, '1'      , '3',      '9',  'Corridor', 'A.2SA.0900', '2SA',  'A5KBWBG',2, '2160'  ,  '550',      '50',     'YC74H',   'YQ73D',   'None',    'None', '64731-0001', '7.13', '']                for i in range(int(record[9])):
                    temp=[record[1],record[2],record[3],record[4],record[5]    ,record[6],record[7],record[8],record[10],record[11],record[12],record[13],record[14],record[15],record[16],record[17],'',record[18],record[17],'',record[19],'']
                    self.data.append(temp)
            InsertPanelDetailIntoPackageDB(self.log,WHICHDB,dbName,self.data)
        _, self.packageState = GetSubOrderPackageState(self.log,WHICHDB,dbName,self.suborderID)
        if self.packageState not in ["按房间打包","按区域打包"]:
            self.packageState = "未打包"
        _, self.panelList = GetSubOrderPanelsForPackageFromPackageDB(self.log,WHICHDB,self.orderID,self.suborderID)
        self.panelTotalAmount = len(self.panelList)
        self.panelList.sort(key=itemgetter(11,9,10), reverse=True)#先将墙板按厚度，长度，宽度排序
        #角墙板怎么打包？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？
        for record in self.panelList:
            print("record=",record)
            # [1, 64731, '1', '3', '9', 'Corridor', 'A.2SA.0900', '2SA', 'A5KBWBG', '2160', '550', '50', 'YC74H', 'YQ73D',
            #  'None', 'None', '64731-0001', '', '7.13', '64731-0001', '', '']
            self.panelTotalWeight+=float(record[18])
            self.panelTotalSquare+= (float(record[9])*float(record[10]))
        self.panelTotalSquare = self.panelTotalSquare/1.E6
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "产品打包操作对话框", pos, size, style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self, -1, size=(1800, 900))
        self.topPanel = wx.Panel(self.panel,size=(100,100))
        self.ReCreateTopPanel()
        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.topPanel,0,wx.EXPAND)
        vbox.Add(wx.StaticLine(self.panel,size=(10,2),style=wx.HORIZONTAL),0,wx.EXPAND)

        self.finishPackagePanel = scrolled.ScrolledPanel(self.panel,size=(100,200))
        vbox.Add(self.finishPackagePanel,1,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,10)
        hhbox = wx.BoxSizer()
        hhbox.Add((10,-1))
        self.leftWorkingPackagePanel = wx.Panel(self.panel,size=(100,400))
        hhbox.Add(self.leftWorkingPackagePanel,1,wx.EXPAND)
        self.middleControlPanel = wx.Panel(self.panel,size=(50,-1))
        self.middleControlPanel.SetBackgroundColour(wx.Colour(220,220,220))
        hhbox.Add(self.middleControlPanel,0,wx.EXPAND)
        self.rightWorkingPackagePanel = wx.Panel(self.panel,size=(100,400))
        hhbox.Add(self.rightWorkingPackagePanel,1,wx.EXPAND)
        hhbox.Add((10,-1))
        vbox.Add(hhbox,0,wx.EXPAND)
        self.bottomPackagePanel = scrolled.ScrolledPanel(self.panel,size=(100,150))
        vbox.Add(self.bottomPackagePanel,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,10)


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



        # self.panel.SetBackgroundColour(wx.Colour(234,219,212))
        self.panel.SetSizer(vbox)
        sizer.Add(self.panel, 0, wx.EXPAND)
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

    def ReCreateTopPanel(self):
        self.topPanel.DestroyChildren()
        hbox = wx.BoxSizer()
        hbox.Add(10, -1)
        vvbox = wx.BoxSizer(wx.VERTICAL)
        vvbox.Add((-1,20))
        hhbox = wx.BoxSizer()
        hbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='订单号：',size=(67,-1)), 0, wx.TOP, 5)
        self.orderIDTXT = wx.TextCtrl(self.topPanel, size=(70, 25), style=wx.TE_READONLY)
        self.orderIDTXT.SetValue('%05d-%03d' % (int(self.orderID),int(self.suborderID)))
        # self.orderIDTXT.SetBackgroundColour(wx.GREEN)
        hhbox.Add(self.orderIDTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='订单名称：',size=(64,-1)), 0, wx.TOP, 5)
        self.orderNameTXT = wx.TextCtrl(self.topPanel, size=(90, 25), style=wx.TE_READONLY)
        self.orderNameTXT.SetValue("需处理")
        self.orderNameTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.orderNameTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='打包状态'), 0, wx.TOP, 5)
        self.packageStateTXT = wx.TextCtrl(self.topPanel, size=(80, 25), style=wx.TE_READONLY)
        self.packageStateTXT.SetValue(self.packageState)
        if self.packageState=='未打包':
            self.packageStateTXT.SetBackgroundColour(wx.RED)
        else:
            self.packageStateTXT.SetBackgroundColour(wx.GREEN)
        hhbox.Add(self.packageStateTXT, 0, wx.LEFT | wx.RIGHT, 10)

        vvbox.Add(hhbox,0,wx.EXPAND)
        hhbox = wx.BoxSizer()
        hbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='面板总数'), 0, wx.TOP, 5)
        self.panelTotlAmountTXT = wx.TextCtrl(self.topPanel, size=(45, 25), style=wx.TE_READONLY)
        self.panelTotlAmountTXT.SetValue(str(self.panelTotalAmount))
        self.panelTotlAmountTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.panelTotlAmountTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='总重量'), 0, wx.TOP, 5)
        self.panelTotlWeightTXT = wx.TextCtrl(self.topPanel, size=(60, 25), style=wx.TE_READONLY)
        self.panelTotlWeightTXT.SetValue("%.2f" % self.panelTotalWeight)
        self.panelTotlWeightTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.panelTotlWeightTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='面板总面积'), 0, wx.TOP, 5)
        self.panelTotalSquareTXT = wx.TextCtrl(self.topPanel, size=(60, 25), style=wx.TE_READONLY)
        self.panelTotalSquareTXT.SetValue("%.2f"%self.panelTotalSquare)
        self.panelTotalSquareTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.panelTotalSquareTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add(wx.StaticText(self.topPanel, label='托盘总数'), 0, wx.TOP, 5)
        self.boxTotalAmountTXT = wx.TextCtrl(self.topPanel, size=(40, 25), style=wx.TE_READONLY)
        self.boxTotalAmountTXT.SetValue(str(self.boxTotalAmount))
        self.boxTotalAmountTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.boxTotalAmountTXT, 0, wx.LEFT | wx.RIGHT, 10)

        vvbox.Add((-1,10))
        vvbox.Add(hhbox,0,wx.EXPAND)

        hbox.Add(vvbox,0)

        hbox.Add(wx.StaticLine(self.topPanel,style=wx.VERTICAL),0,wx.EXPAND|wx.LEFT|wx.RIGHT,10)

        hbox.Add((10,-1))

        vvbox =wx.BoxSizer(wx.VERTICAL)
        hhbox = wx.BoxSizer()
        hhbox.Add(wx.StaticText(self.topPanel, label='当前甲板'), 0, wx.TOP, 5)
        temp=np.array(self.panelList)[:,3]
        choiceList = list(set(temp))
        if len(choiceList)>1:
            choiceList.insert(0,"全部")
        self.deckCOMBO = wx.ComboBox(self.topPanel, value=choiceList[0], size=(40, 25),choices=choiceList, style=wx.TE_READONLY)
        self.deckCOMBO.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.deckCOMBO, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='当前区域'), 0, wx.TOP, 5)
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
        self.zoneCOMBO = wx.ComboBox(self.topPanel, value=choiceList[0], size=(40, 25),choices=choiceList, style=wx.TE_READONLY)
        self.zoneCOMBO.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.zoneCOMBO, 0, wx.LEFT | wx.RIGHT, 10)

        if self.packageState!="按区域打包": #当按区域打包时，不应该显示房间Combobox
            hhbox.Add((10,-1))
            hhbox.Add(wx.StaticText(self.topPanel, label='当前房间'), 0, wx.TOP, 5)
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
                            temp.append(str(record[5]))
            choiceList = list(set(temp))
            if len(choiceList)>1:
                choiceList.insert(0,"全部")
            self.roomCOMBO = wx.ComboBox(self.topPanel, value=choiceList[0], size=(80, 25),choices=choiceList, style=wx.TE_READONLY)
            self.roomCOMBO.SetBackgroundColour(wx.WHITE)
            hhbox.Add(self.roomCOMBO, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='托盘数'), 0, wx.TOP, 5)
        self.currentBoxTotalAmountTXT = wx.TextCtrl(self.topPanel, size=(32, 25), style=wx.TE_READONLY)
        self.currentBoxTotalAmountTXT.SetValue(str(self.boxTotalAmount))
        self.currentBoxTotalAmountTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.currentBoxTotalAmountTXT, 0, wx.LEFT | wx.RIGHT, 10)

        vvbox.Add((-1,20))
        vvbox.Add(hhbox,0,wx.EXPAND)

        hhbox = wx.BoxSizer()
        hhbox.Add(wx.StaticText(self.topPanel, label='当前面板数'), 0, wx.TOP, 5)
        self.currentPanelTotlAmountTXT = wx.TextCtrl(self.topPanel, size=(67, 25), style=wx.TE_READONLY)
        self.currentPanelTotlAmountTXT.SetValue(str(self.panelTotalAmount))
        self.currentPanelTotlAmountTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.currentPanelTotlAmountTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='当前面板重量'), 0, wx.TOP, 5)
        self.currentPanelTotlWeightTXT = wx.TextCtrl(self.topPanel, size=(67, 25), style=wx.TE_READONLY)
        self.currentPanelTotlWeightTXT.SetValue("%.2f"%self.panelTotalWeight)
        self.currentPanelTotlWeightTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.currentPanelTotlWeightTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='当前面板面积'), 0, wx.TOP, 5)
        self.currentPanelTotalSquareTXT = wx.TextCtrl(self.topPanel, size=(67, 25), style=wx.TE_READONLY)
        self.currentPanelTotalSquareTXT.SetValue("")
        self.currentPanelTotalSquareTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.currentPanelTotalSquareTXT, 0, wx.LEFT | wx.RIGHT, 10)
        vvbox.Add((-1,10))
        vvbox.Add(hhbox,0,wx.EXPAND)

        hbox.Add(vvbox,0,wx.EXPAND)

        hbox.Add(wx.StaticLine(self.topPanel,style=wx.VERTICAL),0,wx.EXPAND|wx.LEFT|wx.RIGHT,10)

        vvbox = wx.BoxSizer(wx.VERTICAL)
        hhbox = wx.BoxSizer()
        hhbox.Add(wx.StaticText(self.topPanel, label='选中托盘名称'), 0, wx.TOP, 5)
        self.selectionBoxIDTXT = wx.TextCtrl(self.topPanel, size=(40, 25), style=wx.TE_READONLY)
        self.selectionBoxIDTXT.SetValue("")
        self.selectionBoxIDTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.selectionBoxIDTXT, 0, wx.LEFT | wx.RIGHT, 10)
        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='托盘内面板总数'), 0, wx.TOP, 5)
        self.selectionPanelTotlAmountTXT = wx.TextCtrl(self.topPanel, size=(50, 25), style=wx.TE_READONLY)
        self.selectionPanelTotlAmountTXT.SetValue("")
        self.selectionPanelTotlAmountTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.selectionPanelTotlAmountTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='托盘内面板总重量'), 0, wx.TOP, 5)
        self.selectionPanelTotlWeightTXT = wx.TextCtrl(self.topPanel, size=(70, 25), style=wx.TE_READONLY)
        self.selectionPanelTotlWeightTXT.SetValue("")
        self.selectionPanelTotlWeightTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.selectionPanelTotlWeightTXT, 0, wx.LEFT | wx.RIGHT, 10)

        vvbox.Add((-1,20))
        vvbox.Add(hhbox,0,wx.EXPAND)

        hhbox=wx.BoxSizer()
        hbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='托盘层数'), 0, wx.TOP, 5)
        self.boxLayerNumTXT = wx.TextCtrl(self.topPanel, size=(40, 25), style=wx.TE_READONLY)
        self.boxLayerNumTXT.SetValue(str(10))
        self.boxLayerNumTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.boxLayerNumTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='托盘长'), 0, wx.TOP, 5)
        self.boxLengthTXT = wx.TextCtrl(self.topPanel, size=(50, 25), style=wx.TE_READONLY)
        self.boxLengthTXT.SetValue(str(2345))
        self.boxLengthTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.boxLengthTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='托盘宽'), 0, wx.TOP, 5)
        self.boxWidthTXT = wx.TextCtrl(self.topPanel, size=(50, 25), style=wx.TE_READONLY)
        self.boxWidthTXT.SetValue(str(550))
        self.boxWidthTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.boxWidthTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='托盘高'), 0, wx.TOP, 5)
        self.boxHeightTXT = wx.TextCtrl(self.topPanel, size=(50, 25), style=wx.TE_READONLY)
        self.boxHeightTXT.SetValue(str(1500))
        self.boxHeightTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.boxHeightTXT, 0, wx.LEFT | wx.RIGHT, 10)

        vvbox.Add((-1,10))
        vvbox.Add(hhbox,0,wx.EXPAND)

        hbox.Add(vvbox,0)
        hbox.Add(wx.StaticLine(self.topPanel,style=wx.VERTICAL),0,wx.EXPAND|wx.LEFT,10)

        bitmap = wx.Bitmap("bitmaps/box.jpg", wx.BITMAP_TYPE_JPEG)
        # startAutoPackageBTN.SetFont()
        startAutoPackageBTN = wx.Button(self.topPanel,label="自动打包")
        # startAutoPackageBTN.SetAuthNeeded()
        startAutoPackageBTN.SetBitmap(bitmap, wx.RIGHT)
        # startAutoPackageBTN.SetBitmapMargins(10,10)

        hbox.Add(startAutoPackageBTN,1,wx.EXPAND|wx.ALL,10)
        self.topPanel.SetSizer(hbox)

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
