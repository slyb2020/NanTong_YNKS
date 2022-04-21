import wx
import os
from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel
from ID_DEFINE import *
from MakePdfReport import *

class PDFViewerPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        hsizer = wx.BoxSizer( wx.HORIZONTAL )
        vsizer = wx.BoxSizer( wx.VERTICAL )
        self.buttonpanel = pdfButtonPanel(self, wx.ID_ANY,
                                wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.buttonpanel, 0, wx.GROW|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.viewer = pdfViewer( self, wx.ID_ANY, wx.DefaultPosition,
                                wx.DefaultSize, wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)
        vsizer.Add(self.viewer, 1, wx.GROW|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        # loadbutton = wx.Button(self, wx.ID_ANY, "Load PDF file",
        #                         wx.DefaultPosition, wx.DefaultSize, 0 )
        # vsizer.Add(loadbutton, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer.Add(vsizer, 1, wx.GROW|wx.ALL, 5)
        self.SetSizer(hsizer)
        self.SetAutoLayout(True)

        # introduce buttonpanel and viewer to each other
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel

        # self.Bind(wx.EVT_BUTTON, self.OnLoadButton, loadbutton)

    def OnLoadButton(self, event):
        dlg = wx.FileDialog(self, wildcard="*.pdf")
        if dlg.ShowModal() == wx.ID_OK:
            wx.BeginBusyCursor()
            self.viewer.LoadFile(dlg.GetPath())
            wx.EndBusyCursor()
        dlg.Destroy()

class ProductionScheduleDialog(wx.Dialog):
    def __init__(self, parent, log, orderID, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.orderID = orderID
        self.parent = parent
        self.log = log
        # self.log.WriteText("操作员：'%s' 开始执行库存参数设置操作。。。\r\n"%(self.parent.operator_name))
        dirName = scheduleDir + '%s/' % self.orderID
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "排产操作对话框", pos, size, style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, -1, size=(1200, 900))
        hbox = wx.BoxSizer()
        controlPanel = wx.Panel(panel,size=(150,-1))
        hbox.Add(controlPanel,0,wx.EXPAND)
        pdfPanel = wx.Panel(panel,size=(100,-1))
        hbox.Add(pdfPanel,1,wx.EXPAND)
        panel.SetSizer(hbox)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 20))
        hbox = wx.BoxSizer()
        hbox.Add(10, -1)
        hbox.Add(wx.StaticText(panel, label='订单号：'), 0, wx.TOP, 5)
        self.newOrderIDTXT = wx.TextCtrl(panel, size=(50, 25),style=wx.TE_READONLY)
        self.newOrderIDTXT.SetValue('%05d' % int(self.orderID))
        hbox.Add(self.newOrderIDTXT, 1, wx.LEFT | wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.EXPAND)
        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.materialScheduleButton = wx.Button(controlPanel, label="材料出库单", size=(90, 90))
        self.materialScheduleButton.Bind(wx.EVT_BUTTON, self.OnMaterialScheduleBTN)
        hhbox.Add(self.materialScheduleButton, 1, wx.ALL, 5)
        vbox.Add(hhbox,0,wx.EXPAND)
        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.cutScheduleButton = wx.Button(controlPanel, label="裁切计划单", size=(90, 90))
        self.cutScheduleButton.Bind(wx.EVT_BUTTON, self.OnCutScheduleBTN)
        hhbox.Add(self.cutScheduleButton, 1, wx.ALL, 5)
        vbox.Add(hhbox,0,wx.EXPAND)
        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.bendScheduleButton = wx.Button(controlPanel, label="折弯任务单", size=(90, 90))
        self.bendScheduleButton.Bind(wx.EVT_BUTTON, self.OnBendScheduleBTN)
        hhbox.Add(self.bendScheduleButton, 1, wx.ALL, 5)
        vbox.Add(hhbox,0,wx.EXPAND)
        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.hotPressScheduleButton = wx.Button(controlPanel, label="热压任务单", size=(90, 90))
        self.hotPressScheduleButton.Bind(wx.EVT_BUTTON, self.OnOpenFileBTN)
        hhbox.Add(self.hotPressScheduleButton, 1, wx.ALL, 5)
        vbox.Add(hhbox,0,wx.EXPAND)
        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.formingScheduleButton = wx.Button(controlPanel, label="成型任务单", size=(90, 90))
        self.formingScheduleButton.Bind(wx.EVT_BUTTON, self.OnFormingScheduleBTN)
        hhbox.Add(self.formingScheduleButton, 1, wx.ALL, 5)
        vbox.Add(hhbox,0,wx.EXPAND)
        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.punchScheduleButton = wx.Button(controlPanel, label="冲铣任务单", size=(90, 90))
        self.punchScheduleButton.Bind(wx.EVT_BUTTON, self.OnOpenFileBTN)
        hhbox.Add(self.punchScheduleButton, 1, wx.ALL, 5)
        vbox.Add(hhbox,0,wx.EXPAND)
        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.specialScheduleButton = wx.Button(controlPanel, label="特制品任务单", size=(90, 90))
        self.specialScheduleButton.Bind(wx.EVT_BUTTON, self.OnOpenFileBTN)
        hhbox.Add(self.specialScheduleButton, 1, wx.ALL, 5)
        vbox.Add(hhbox,0,wx.EXPAND)
        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.packageScheduleButton = wx.Button(controlPanel, label="打包任务单", size=(90, 90))
        self.packageScheduleButton.Bind(wx.EVT_BUTTON, self.OnOpenFileBTN)
        hhbox.Add(self.packageScheduleButton, 1, wx.ALL, 5)
        vbox.Add(hhbox,0,wx.EXPAND)
        # vbox.Add((-1,10))
        # self.cutScheduleButton = wx.Button(controlPanel, label="裁切计划", size=(100, 100))
        # self.cutScheduleButton.Bind(wx.EVT_BUTTON, self.OnOpenFileBTN)
        # vbox.Add(self.cutScheduleButton, 0, wx.EXPAND | wx.ALL, 10)
        controlPanel.SetSizer(vbox)
        # panel.SetBackgroundColour(wx.Colour(234,219,212))
        sizer.Add(panel, 0, wx.EXPAND)
        line = wx.StaticLine(self, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)
        vbox=wx.BoxSizer(wx.VERTICAL)
        self.pdfViewerPanel = PDFViewerPanel(pdfPanel,self.log)
        vbox.Add(self.pdfViewerPanel,1,wx.EXPAND)
        pdfPanel.SetSizer(vbox)


        btnsizer = wx.BoxSizer()
        bitmap1 = wx.Bitmap("bitmaps/ok3.png", wx.BITMAP_TYPE_PNG)
        bitmap2 = wx.Bitmap("bitmaps/cancel1.png", wx.BITMAP_TYPE_PNG)
        bitmap3 = wx.Bitmap("bitmaps/33.png", wx.BITMAP_TYPE_PNG)
        btn_ok = wx.Button(self, wx.ID_OK, "确  定", size=(200, 40))
        btn_ok.SetBitmap(bitmap1, wx.LEFT)
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "取  消", size=(200, 40))
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

    def OnMaterialScheduleBTN(self, event):
        filename = scheduleDir+'%s/MaterialSchedule.pdf'%self.orderID
        if not os.path.exists(filename):
            print("filename:%sdoes not exist!"%filename)
            MakeMaterialScheduleTemplate(filename)
        else:
            MakeMaterialScheduleTemplate(filename)
        self.pdfViewerPanel.viewer.LoadFile(filename)

    def OnCutScheduleBTN(self, event):
        filename = scheduleDir+'%s/CutSchedule.pdf'%self.orderID
        if not os.path.exists(filename):
            print("filename:%sdoes not exist!"%filename)
            MakeCutScheduleTemplate(self.orderID,filename,self.parent.productionSchedule.cuttingScheduleList)  #这些数据再ProductionScheduleAlgorithm.py文件中
        else:
            MakeCutScheduleTemplate(self.orderID,filename,self.parent.productionSchedule.cuttingScheduleList)
        self.pdfViewerPanel.viewer.LoadFile(filename)

    def OnBendScheduleBTN(self, event):
        filename = scheduleDir+'%s/BendSchedule.pdf'%self.orderID
        if not os.path.exists(filename):
            print("filename:%sdoes not exist!"%filename)
            MakeBendScheduleTemplate(filename)
        else:
            MakeBendScheduleTemplate(filename)
        self.pdfViewerPanel.viewer.LoadFile(filename)

    def OnFormingScheduleBTN(self, event):
        filename = scheduleDir+'%s/FormingSchedule.pdf'%self.orderID
        if not os.path.exists(filename):
            print("filename:%sdoes not exist!"%filename)
            MakeFormingScheduleTemplate(filename)
        else:
            MakeFormingScheduleTemplate(filename)
        self.pdfViewerPanel.viewer.LoadFile(filename)

    def OnOpenFileBTN(self, event):
        self.pdfViewerPanel.viewer.LoadFile("Excel/Stena 生产图纸 2SA.pdf")

    # def OnCancel(self, event):
    #     # self.log.WriteText("操作员：'%s' 取消库存参数设置操作\r\n"%(self.parent.operator_name))
    #     event.Skip()
