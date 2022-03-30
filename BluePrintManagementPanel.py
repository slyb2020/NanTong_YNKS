import os

import wx
import wx.grid as gridlib
from DBOperation import GetAllBluPrintList, GetRGBWithRalID,GetAllColor,SaveBluePrintInDB,UpdateBluePrintInDB
import wx.grid as gridlib
import numpy as np
import images
import wx.lib.scrolledpanel as scrolled

class BluePrintGrid(gridlib.Grid):  ##, mixins.GridAutoEditMixin):
    def __init__(self, parent, master, log):
        gridlib.Grid.__init__(self, parent, -1)
        self.log = log
        self.master = master
        self.moveTo = None

        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.CreateGrid(self.master.dataArray.shape[0], len(self.master.colLabelValueList))  # , gridlib.Grid.SelectRows)
        self.EnableEditing(False)

        self.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)

        self.SetRowLabelSize(50)
        self.SetColLabelSize(25)

        for i, title in enumerate(self.master.colLabelValueList):
            self.SetColLabelValue(i,title)
        for i, width in enumerate(self.master.colWidthList):
            self.SetColSize(i, width)

        for i, temp in enumerate(self.master.dataArray):
            self.SetRowSize(i, 50)
            data = self.Translate(temp)
            for j, item in enumerate(data):
                # self.SetCellBackgroundColour(i,j,wx.Colour(250, 250, 250))
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.SetCellValue(i, j, str(item))

        # self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)
        # self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_DCLICK, self.OnCellRightDClick)

        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelLeftDClick)
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_DCLICK, self.OnLabelRightDClick)

        self.Bind(gridlib.EVT_GRID_COL_SORT, self.OnGridColSort)

        self.Bind(gridlib.EVT_GRID_ROW_SIZE, self.OnRowSize)
        self.Bind(gridlib.EVT_GRID_COL_SIZE, self.OnColSize)

        self.Bind(gridlib.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.OnCellChange)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)

        self.Bind(gridlib.EVT_GRID_EDITOR_SHOWN, self.OnEditorShown)
        self.Bind(gridlib.EVT_GRID_EDITOR_HIDDEN, self.OnEditorHidden)
        self.Bind(gridlib.EVT_GRID_EDITOR_CREATED, self.OnEditorCreated)

    def Translate(self, data):
        result = list(data[:4])
        processFront = ''
        processMiddle=''
        processRear=''
        processList=["505",'405','409','406','652','100','306','9000']
        for i,process in enumerate(processList):
            if 'F' in data[i+4]:
                processFront += process
                if i<7:
                    processFront += '/'
            if 'R' in data[i+4]:
                processRear += process
                if i<7:
                    processRear += '/'
            if 'M' in data[i+4]:
                processMiddle += process
                if i<7:
                    processMiddle += '/'
        if processMiddle=='':
            process = '面板:'+processFront + '\r\n' + '背板:'+processRear
        else:
            process='面板:'+processFront+'\r\n'+ '中板:'+ processMiddle+'\r\n' + '背板:'+processRear
        result.append(process)
        result.append(data[12])
        return result

    def ReCreate(self):
        if self.GetNumberRows()<self.master.dataArray.shape[0]:
            self.InsertRows(numRows=self.master.dataArray.shape[0]-self.GetNumberRows())
        self.ClearGrid()
        self.EnableEditing(False)
        self.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)

        self.SetRowLabelSize(50)
        self.SetColLabelSize(25)

        for i, title in enumerate(self.master.colLabelValueList):
            self.SetColLabelValue(i,title)
        for i, width in enumerate(self.master.colWidthList):
            self.SetColSize(i, width)

        for i, temp in enumerate(self.master.dataArray):
            self.SetRowSize(i, 50)
            data = self.Translate(temp)
            for j, item in enumerate(data):
                # self.SetCellBackgroundColour(i,j,wx.Colour(250, 250, 250))
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.SetCellValue(i, j, str(item))

    # def OnCellLeftClick(self, evt):
    #     self.log.write("OnCellLeftClick: (%d,%d) %s\n" %
    #                    (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
    #     evt.Skip()

    def OnCellRightClick(self, evt):
        self.log.write("OnCellRightClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnCellLeftDClick(self, evt):
        self.log.write("OnCellLeftDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnCellRightDClick(self, evt):
        self.log.write("OnCellRightDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelLeftClick(self, evt):
        self.log.write("OnLabelLeftClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelRightClick(self, evt):
        self.log.write("OnLabelRightClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelLeftDClick(self, evt):
        self.log.write("OnLabelLeftDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelRightDClick(self, evt):
        self.log.write("OnLabelRightDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnGridColSort(self, evt):
        self.log.write("OnGridColSort: %s %s" % (evt.GetCol(), self.GetSortingColumn()))
        self.SetSortingColumn(evt.GetCol())

    def OnRowSize(self, evt):
        self.log.write("OnRowSize: row %d, %s\n" %
                       (evt.GetRowOrCol(), evt.GetPosition()))
        evt.Skip()

    def OnColSize(self, evt):
        self.log.write("OnColSize: col %d, %s\n" %
                       (evt.GetRowOrCol(), evt.GetPosition()))
        evt.Skip()

    def OnRangeSelect(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        self.log.write("OnRangeSelect: %s  top-left %s, bottom-right %s\n" %
                       (msg, evt.GetTopLeftCoords(), evt.GetBottomRightCoords()))
        evt.Skip()

    def OnCellChange(self, evt):
        self.log.write("OnCellChange: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))

        # Show how to stay in a cell that has bad data.  We can't just
        # call SetGridCursor here since we are nested inside one so it
        # won't have any effect.  Instead, set coordinates to move to in
        # idle time.
        value = self.GetCellValue(evt.GetRow(), evt.GetCol())

        if value == 'no good':
            self.moveTo = evt.GetRow(), evt.GetCol()

    def OnIdle(self, evt):
        if self.moveTo is not None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None

        evt.Skip()

    def OnSelectCell(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        self.log.write("OnSelectCell: %s (%d,%d) %s\n" %
                       (msg, evt.GetRow(), evt.GetCol(), evt.GetPosition()))

        # Another way to stay in a cell that has a bad value...
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()

        if self.IsCellEditControlEnabled():
            self.HideCellEditControl()
            self.DisableCellEditControl()

        value = self.GetCellValue(row, col)

        if value == 'no good 2':
            return  # cancels the cell selection

        evt.Skip()

    def OnEditorShown(self, evt):
        if evt.GetRow() == 6 and evt.GetCol() == 3 and \
                wx.MessageBox("Are you sure you wish to edit this cell?",
                              "Checking", wx.YES_NO) == wx.NO:
            evt.Veto()
            return

        self.log.write("OnEditorShown: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnEditorHidden(self, evt):
        if evt.GetRow() == 6 and evt.GetCol() == 3 and \
                wx.MessageBox("Are you sure you wish to  finish editing this cell?",
                              "Checking", wx.YES_NO) == wx.NO:
            evt.Veto()
            return

        self.log.write("OnEditorHidden: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnEditorCreated(self, evt):
        self.log.write("OnEditorCreated: (%d, %d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetControl()))

class BluePrintShowPanel(wx.Panel):
    def __init__(self, parent,size):
        wx.Panel.__init__(self, parent, size=size)
        self.filename = ''
        self.SetAutoLayout(True)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def Recreate(self,filename,state='查看'):
        self.filename = filename
        print(state)
        if state!='查看':
            self.pageUpBTN = wx.Button(self,label="▲",size=(30,30),name='pageUp')
            self.pageDownBTN = wx.Button(self,label="▼",size=(30,30),name='pageDown')
            hbox = wx.BoxSizer(wx.VERTICAL)
            hbox.Add(self.pageUpBTN,0)
            hbox.Add(self.pageDownBTN,0)
            self.SetSizer(hbox)
            self.Layout()
        self.Refresh()

    def OnResize(self, evt):
        self.Refresh()

    def OnPaint(self, evt):
        if self.filename:
            dc = wx.PaintDC(self)
            dc.SetBackground(wx.Brush("WHITE"))
            dc.Clear()
            x,y = self.GetClientSize()
            bmp = wx.Image(self.filename).Scale(width=x, height=y,
                                                      quality=wx.IMAGE_QUALITY_BOX_AVERAGE).ConvertToBitmap()
            dc.DrawBitmap(bmp, 0, 0, True)
        evt.Skip()
# class BluePrintShowPanel(wx.Panel):
#     def __init__(self, parent,size):
#         wx.Panel.__init__(self, parent, size=size)
#         self.filename = ''
#         self.SetAutoLayout(True)
#         self.Bind(wx.EVT_PAINT, self.OnPaint)
#         self.Bind(wx.EVT_SIZE, self.OnResize)
#
#     def Recreate(self,filename,state='查看'):
#         self.filename = filename
#         print(state)
#         if state!='查看':
#             self.pageUpBTN = wx.Button(self,label="▲",size=(30,30),name='pageUp')
#             self.pageDownBTN = wx.Button(self,label="▼",size=(30,30),name='pageDown')
#             hbox = wx.BoxSizer(wx.VERTICAL)
#             hbox.Add(self.pageUpBTN,0)
#             hbox.Add(self.pageDownBTN,0)
#             self.SetSizer(hbox)
#             self.Layout()
#         self.Refresh()
#
#     def OnResize(self, evt):
#         self.Refresh()
#
#     def OnPaint(self, evt):
#         if self.filename:
#             dc = wx.PaintDC(self)
#             dc.SetBackground(wx.Brush("WHITE"))
#             dc.Clear()
#             x,y = self.GetClientSize()
#             bmp = wx.Image(self.filename).Scale(width=x, height=y,
#                                                       quality=wx.IMAGE_QUALITY_BOX_AVERAGE).ConvertToBitmap()
#             dc.DrawBitmap(bmp, 0, 0, True)
#         evt.Skip()

class SpecificBluePrintManagementPanel(wx.Panel):
    def __init__(self, parent, master, log, type,state='在用'):
        wx.Panel.__init__(self, parent)
        self.master = master
        self.log = log
        self.type = type
        self.state = state
        self.busy = False
        self.pageNo = 1
        self.editState = '查看'
        self.editState = '查看'
        self.data = []
        self.processList=self.master.processList
        self.colWidthList = [80, 65, 65, 65, 170, 70,47]
        self.colLabelValueList = ['图纸号', '面板增量', '中板增量', '背板增量', '所需工序','状态','']
        _, dataList = GetAllBluPrintList(self.log, 1, self.type,state=self.state)
        self.dataArray = np.array(dataList)
        self.bluePrintIDSearch = ''
        self.middleLengthDeltaSearch = ''
        self.middleWidthDeltaSearch = ''
        self.rearLengthSearch = ''
        self.rearWidthSearch=''
        self.workProcessSearch=''
        self.busy = False
        hbox = wx.BoxSizer()
        self.leftPanel = wx.Panel(self, size=(630, -1))
        hbox.Add(self.leftPanel, 0, wx.EXPAND)
        self.middlePanel=wx.Panel(self, size=(300, -1))
        hbox.Add(self.middlePanel, 0, wx.EXPAND)
        self.rightPanel = wx.Panel(self, size=(550, 450))
        hbox.Add(self.rightPanel, 1, wx.EXPAND)
        self.SetSizer(hbox)
        self.CreateLeftPanel()
        # self.CreateRightPanel()
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self,event):
        obj = event.GetEventObject()
        if obj.GetName()=='pageUp':
            self.pageNo=int(self.data[17])
            if self.pageNo>1:
                self.pageNo -=1
            else:
                self.pageNo = len(os.listdir('图纸/%s/'%self.bluePrintIndexCtrl.GetValue()))
            self.data[17]=str(self.pageNo)
            print("page=",self.data[17])
            filename = '图纸/%s/%s.jpg' % (self.bluePrintIndexCtrl.GetValue(), self.data[17])
            print(filename)
            # self.bluePrintShowPanel.Recreate(filename, self.editState)
        event.Skip()

    def OnCellLeftDClick(self, evt):
        if self.busy == False:
            col=evt.GetCol()
            if col == 6:
                    self.busy = True
                    row = evt.GetRow()
                    self.data = self.dataArray[row]
                    self.pageNo = self.data[17]
                    index = self.data[0].split('.')[1]
                    filename = '图纸/%s/%s.jpg'%(index,self.pageNo)
                    self.editState = '编辑'
                    self.ReCreateMiddlePanel(self.type, self.editState)
                    # self.ReCreateRightPanel()
                    # self.bluePrintShowPanel.Recreate(filename, self.editState)
        evt.Skip()

    def OnCellLeftClick(self, evt):
        if self.busy == False:
            row = evt.GetRow()
            self.bluePrintGrid.SetSelectionMode(wx.grid.Grid.GridSelectRows)
            self.bluePrintGrid.SelectRow(row)
            self.data = self.dataArray[row]
            self.pageNo = self.data[17]
            index = self.data[0].split('.')[1]
            filename = '图纸/%s/%s.jpg' % (index, self.pageNo)
            self.editState = '查看'
            self.ReCreateMiddlePanel(self.type, self.editState)
            self.ReCreateRightPanel()
            # self.bluePrintShowPanel.Recreate(filename)
        evt.Skip()

    def CreateLeftPanel(self):
        vvbox = wx.BoxSizer(wx.VERTICAL)
        self.bluePrintGrid = BluePrintGrid(self.leftPanel, self, self.log)
        vvbox.Add(self.bluePrintGrid, 1, wx.EXPAND)
        hhbox = wx.BoxSizer()
        searchPanel = wx.Panel(self.leftPanel, size=(-1, 30), style=wx.BORDER_DOUBLE)
        vvbox.Add(searchPanel, 0, wx.EXPAND)
        self.searchResetBTN = wx.Button(searchPanel, label='Rest', size=(48, -1))
        self.searchResetBTN.Bind(wx.EVT_BUTTON, self.OnResetSearchItem)
        hhbox.Add(self.searchResetBTN, 0, wx.EXPAND)

        self.bluePrintIDSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[0], -1), style=wx.TE_PROCESS_ENTER)
        self.bluePrintIDSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnBluePrintIDSearch)
        hhbox.Add(self.bluePrintIDSearchCtrl, 0, wx.EXPAND)

        self.middleLengthDeltaSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[1], -1),
                                                       style=wx.TE_PROCESS_ENTER)
        self.middleLengthDeltaSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnMiddleLengthDeltaSearch)
        hhbox.Add(self.middleLengthDeltaSearchCtrl, 0, wx.EXPAND)

        self.middleWidthDeltaSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[2], -1),
                                                       style=wx.TE_PROCESS_ENTER)
        self.middleWidthDeltaSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnMiddleWidthDeltaSearch)
        hhbox.Add(self.middleWidthDeltaSearchCtrl, 0, wx.EXPAND)

        self.rearLengthDeltaSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[3], -1),
                                                       style=wx.TE_PROCESS_ENTER)
        self.rearLengthDeltaSearchCtrl.Bind(wx.EVT_COMBOBOX, self.OnRearLengthDeltaSearch)
        hhbox.Add(self.rearLengthDeltaSearchCtrl, 0, wx.EXPAND)

        self.rearWidthDeltaSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[4], -1),
                                                       style=wx.TE_PROCESS_ENTER)
        self.rearWidthDeltaSearchCtrl.Bind(wx.EVT_COMBOBOX, self.OnRearWidthDeltaSearch)
        hhbox.Add(self.rearWidthDeltaSearchCtrl, 0, wx.EXPAND)

        self.createNewBluPrintBTN = wx.Button(searchPanel, label='新建%s图纸' % self.type)
        self.createNewBluPrintBTN.SetBackgroundColour(wx.Colour(22, 211, 111))
        self.createNewBluPrintBTN.Bind(wx.EVT_BUTTON, self.OnCreateNewBluePrint)
        hhbox.Add(self.createNewBluPrintBTN, 1, wx.EXPAND | wx.RIGHT | wx.LEFT, 1)

        self.changeStateBTN = wx.Button(searchPanel, size=(15,-1))
        self.changeStateBTN.Bind(wx.EVT_BUTTON, self.OnChangeState)
        if self.state == '在用':
            self.changeStateBTN.SetBackgroundColour(wx.GREEN)
        else:
            self.changeStateBTN.SetBackgroundColour(wx.RED)
        hhbox.Add(self.changeStateBTN,0,wx.EXPAND)
        searchPanel.SetSizer(hhbox)
        self.leftPanel.SetSizer(vvbox)

    def Translate(self, data):
        result = list(data[:4])
        processFront = ''
        processMiddle=''
        processRear=''
        processList=["505",'405','409','406','652','100','306','9000']
        for i,process in enumerate(processList):
            if 'F' in data[i+4]:
                processFront += process
                if i<7:
                    processFront += '/'
            if 'R' in data[i+4]:
                processRear += process
                if i<7:
                    processRear += '/'
            if 'M' in data[i+4]:
                processMiddle += process
                if i<7:
                    processMiddle += '/'
        return [processFront,processMiddle,processRear]

    def ReCreateRightPanel(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        # self.bluePrintShowPanel = BluePrintShowPanel(self.rightPanel, size=(550, 450))
        from ProductionScheduleDialog import PDFViewerPanel
        self.bluePrintShowPanel = PDFViewerPanel(self.rightPanel, self.log,False)
        self.bluePrintShowPanel.viewer.LoadFile("Stena 生产图纸/Stena 生产图纸 2SA/Stena 生产图纸 2SA_页面_01.pdf")
        vbox.Add(self.bluePrintShowPanel, 1, wx.EXPAND)
        self.rightPanel.SetSizer(vbox)
        self.rightPanel.Layout()

    def ReCreateMiddlePanel(self, type, state='查看'):
        if len(self.data)>0:
            procedure, processMiddle, processRear = self.Translate(self.data)
        self.middlePanel.Freeze()
        self.middlePanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1,10))
        hhbox = wx.BoxSizer()
        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.middlePanel, label='图纸类别：', size=(60, -1)), 0, wx.TOP, 5)
        self.bluePrintTypeDict = {'2SF':"25mm墙板","2SA":'50mm墙板','2SG':'25mm墙角板','2SD':'50mm墙角板','2SH':'25mmT型墙板','2SE':'50mmT型墙板','2SM':'高隔音墙板','2SL':'100mm墙板'}
        self.typeBluePrintDict = dict(zip(self.bluePrintTypeDict.values(), self.bluePrintTypeDict.keys()))
        choices=[]
        if type=="墙板":
            choices=["25mm墙板",'50mm墙板','25mm墙角板','25mmT型墙板','50mmT型墙板','高隔音墙板','100mm墙板']
        self.bluePrintTypeCombo = wx.ComboBox(self.middlePanel, choices=choices, size=(90, 30), style=wx.TE_PROCESS_ENTER)
        if len(self.data)!=0:
            key = self.data[0].split('.')[1]
            self.bluePrintTypeCombo.SetValue(self.bluePrintTypeDict[key])
        self.bluePrintTypeCombo.Bind(wx.EVT_COMBOBOX, self.OnBluePrintTypeChanged)
        self.bluePrintIndexCtrl=wx.TextCtrl(self.middlePanel,size=(40,-1),style=wx.TE_READONLY)
        self.bluePrintIndexCtrl.SetValue(key)
        if state=='新建':
            hhbox.Add(self.bluePrintTypeCombo, 1)
            self.bluePrintNoSpin = wx.SpinCtrl(self.middlePanel,size=(55,-1))
            self.bluePrintNoSpin.SetMin(1)
            self.bluePrintNoSpin.SetMax(9999)
            self.bluePrintNoSpin.SetValue(2)
            hhbox.Add(self.bluePrintIndexCtrl, 0)
            hhbox.Add(self.bluePrintNoSpin,0,wx.RIGHT,20)
        else:
            self.bluePrintNoTXT = wx.TextCtrl(self.middlePanel,size=(45,-1),style=wx.TE_READONLY)
            self.bluePrintNoTXT.SetValue(self.data[0].split('.')[2])
            hhbox.Add(self.bluePrintTypeCombo, 1, wx.RIGHT, 10)
            hhbox.Add(self.bluePrintIndexCtrl, 0)
            hhbox.Add(self.bluePrintNoTXT, 0, wx.RIGHT,20)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((20,-1))
        # if state=='新建':
        #     self.middleEnableCheck = wx.CheckBox(self.middlePanel,label='有中板',size=(60,-1),style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        #     # self.middleEnableCheck.SetValue(True if self.data[14]=='Y' else False)
        #     self.middleEnableCheck.Bind(wx.EVT_CHECKBOX, self.OnMiddleEnableCheck)
        #     hhbox.Add(20,-1)
        #     hhbox.Add(self.middleEnableCheck,0)
        # else:
        #     hhbox.Add((70,-1))
        self.middleNumberSPIN = wx.SpinCtrl(self.middlePanel, size=(60, -1), style=wx.TE_READONLY)
        self.middleNumberSPIN.SetRange(0, 2)
        self.middleNumberSPIN.SetValue(int(self.data[14]))
        hhbox.Add(self.middleNumberSPIN, 0)

        if state == '查看':
            self.middleNumberSPIN.Show(False)
            hhbox.Add((60,-1))
        hhbox.Add(wx.StaticText(self.middlePanel, label = '长度方向', size=(70,-1), style=wx.ALIGN_CENTRE),1,wx.TOP,5)
        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.middlePanel, label = '宽度方向', size=(70,-1), style=wx.ALIGN_CENTRE),1,wx.TOP,5)
        vbox.Add(hhbox,0,wx.EXPAND|wx.RIGHT,20)
        vbox.Add((-1,5))

        hhbox = wx.BoxSizer()
        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.middlePanel, label='面板增量:', size=(60, -1)), 0, wx.TOP, 5)
        self.frontLengthDeltaCtrl=wx.SpinCtrl(self.middlePanel, -1, "", (70, 50))
        self.frontLengthDeltaCtrl.SetRange(-100,100)
        hhbox.Add(self.frontLengthDeltaCtrl,1,wx.RIGHT,10)
        # hhbox.Add((10,-1))
        self.frontWidthDeltaCtrl=wx.SpinCtrl(self.middlePanel, -1, "", (70, 50))
        self.frontWidthDeltaCtrl.SetRange(-100,100)
        hhbox.Add(self.frontWidthDeltaCtrl,1,wx.RIGHT,20)
        vbox.Add(hhbox,0,wx.EXPAND)
        vbox.Add((-1,5))

        if int(self.data[14])>0:
            for i in range(int(self.data[14])):
                hhbox = wx.BoxSizer()
                hhbox.Add((20,-1))
                hhbox.Add(wx.StaticText(self.middlePanel, label='中板增量%d:'%i, size=(60, -1)), 0, wx.TOP, 5)
                self.middleLengthDeltaCtrl=wx.SpinCtrl(self.middlePanel, -1, "", (70, 50))
                self.middleLengthDeltaCtrl.SetRange(-100, 100)
                hhbox.Add(self.middleLengthDeltaCtrl,1,wx.RIGHT,10)
                # hhbox.Add((10,-1))
                self.middleWidthDeltaCtrl=wx.SpinCtrl(self.middlePanel, -1, "", (70, 50))
                self.middleWidthDeltaCtrl.SetRange(-100, 100)
                hhbox.Add(self.middleWidthDeltaCtrl,1,wx.RIGHT,20)
                vbox.Add(hhbox,0,wx.EXPAND)
                vbox.Add((-1,5))

        hhbox = wx.BoxSizer()
        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.middlePanel, label='背板增量:', size=(60, -1)), 0, wx.TOP, 5)
        self.rearLengthDeltaCtrl=wx.SpinCtrl(self.middlePanel, -1, "", (70, 50))
        self.rearLengthDeltaCtrl.SetRange(-100, 100)
        hhbox.Add(self.rearLengthDeltaCtrl,1,wx.RIGHT,10)
        # hhbox.Add((10,-1))
        self.rearWidthDeltaCtrl=wx.SpinCtrl(self.middlePanel, -1, "", (70, 50))
        self.rearWidthDeltaCtrl.SetRange(-100, 100)
        hhbox.Add(self.rearWidthDeltaCtrl,1,wx.RIGHT,20)
        vbox.Add(hhbox,0,wx.EXPAND)
        vbox.Add((-1,10))


        if state == "查看":
            print(self.data)
            if self.data[18]=='Y':
                hhbox = wx.BoxSizer()
                hhbox.Add(20,-1)
                # hhbox.Add(wx.CheckBox(self.middlePanel),0,wx.TOP,5)
                hhbox.Add(wx.StaticText(self.middlePanel,label="a: "),0,wx.TOP,5)
                self.aSPIN = wx.SpinCtrl(self.middlePanel, size=(35, -1), style=wx.TE_READONLY)
                self.aSPIN.SetRange(0, 4000)
                self.aSPIN.SetValue(int(self.data[19]))
                self.aSPIN.Enable(False)
                hhbox.Add(self.aSPIN,1)
                vbox.Add(hhbox,0,wx.EXPAND|wx.RIGHT,20)
                vbox.Add((-1,5))

            if self.data[20]=='Y':
                hhbox = wx.BoxSizer()
                hhbox.Add(20,-1)
                # hhbox.Add(wx.CheckBox(self.middlePanel),0,wx.TOP,5)
                hhbox.Add(wx.StaticText(self.middlePanel,label="b: "),0,wx.TOP,5)
                self.bSPIN = wx.SpinCtrl(self.middlePanel, size=(35, -1), style=wx.TE_READONLY)
                self.bSPIN.SetRange(0, 4000)
                self.bSPIN.SetValue(int(self.data[21]))
                self.bSPIN.Enable(False)
                hhbox.Add(self.bSPIN,1)
                vbox.Add(hhbox,0,wx.EXPAND|wx.RIGHT,20)
                vbox.Add((-1,5))

            if self.data[22]=='Y':
                hhbox = wx.BoxSizer()
                hhbox.Add(20,-1)
                # hhbox.Add(wx.CheckBox(self.middlePanel),0,wx.TOP,5)
                hhbox.Add(wx.StaticText(self.middlePanel,label="c: "),0,wx.TOP,5)
                self.cSPIN = wx.SpinCtrl(self.middlePanel, size=(35, -1), style=wx.TE_READONLY)
                self.cSPIN.SetRange(0, 4000)
                self.cSPIN.SetValue(int(self.data[23]))
                self.cSPIN.Enable(False)
                hhbox.Add(self.cSPIN,1)
                vbox.Add(hhbox,0,wx.EXPAND|wx.RIGHT,20)
                vbox.Add((-1,5))

            if self.data[24]=='Y':
                hhbox = wx.BoxSizer()
                hhbox.Add(20,-1)
                # hhbox.Add(wx.CheckBox(self.middlePanel),0,wx.TOP,5)
                hhbox.Add(wx.StaticText(self.middlePanel,label="d: "),0,wx.TOP,5)
                self.dSPIN = wx.SpinCtrl(self.middlePanel, size=(35, -1), style=wx.TE_READONLY)
                self.dSPIN.SetRange(0, 4000)
                self.dSPIN.SetValue(int(self.data[25]))
                self.dSPIN.Enable(False)
                hhbox.Add(self.dSPIN,1)
                vbox.Add(hhbox,0,wx.EXPAND|wx.RIGHT,20)
                vbox.Add((-1,5))

            if self.data[26]=='Y':
                hhbox = wx.BoxSizer()
                hhbox.Add(20,-1)
                hhbox.Add(wx.CheckBox(self.middlePanel),0,wx.TOP,5)
                hhbox.Add(wx.StaticText(self.middlePanel,label="e: "),0,wx.TOP,5)
                self.eSPIN = wx.SpinCtrl(self.middlePanel, size=(35, -1), style=wx.TE_READONLY)
                self.eSPIN.SetRange(0, 4000)
                self.eSPIN.SetValue(int(self.data[27]))
                self.eSPIN.Enable(False)
                hhbox.Add(self.eSPIN,1)
                vbox.Add(hhbox,0,wx.EXPAND|wx.RIGHT,20)
                vbox.Add((-1,5))

            if self.data[28]=='Y':
                hhbox = wx.BoxSizer()
                hhbox.Add(20,-1)
                # hhbox.Add(wx.CheckBox(self.middlePanel),0,wx.TOP,5)
                hhbox.Add(wx.StaticText(self.middlePanel,label="f: "),0,wx.TOP,5)
                self.fSPIN = wx.SpinCtrl(self.middlePanel, size=(35, -1), style=wx.TE_READONLY)
                self.fSPIN.SetRange(0, 4000)
                self.fSPIN.SetValue(int(self.data[29]))
                self.fSPIN.Enable(False)
                hhbox.Add(self.fSPIN,1)
                vbox.Add(hhbox,0,wx.EXPAND|wx.RIGHT,20)
                vbox.Add((-1,5))

            if self.data[30]=='Y':
                hhbox = wx.BoxSizer()
                hhbox.Add(20,-1)
                hhbox.Add(wx.CheckBox(self.middlePanel),0,wx.TOP,5)
                # hhbox.Add(wx.StaticText(self.middlePanel,label="CY: "),0,wx.TOP,5)
                self.cYSPIN = wx.SpinCtrl(self.middlePanel, size=(35, -1), style=wx.TE_READONLY)
                self.cYSPIN.SetRange(0, 4000)
                self.cYSPIN.SetValue(int(self.data[31]))
                self.cYSPIN.Enable(False)
                hhbox.Add(self.cYSPIN,1)
                vbox.Add(hhbox,0,wx.EXPAND|wx.RIGHT,20)
        else:
            hhbox = wx.BoxSizer()
            hhbox.Add(20, -1)
            self.aCheckCtrl = wx.CheckBox(self.middlePanel)
            hhbox.Add(self.aCheckCtrl, 0, wx.TOP, 5)
            hhbox.Add(wx.StaticText(self.middlePanel, label="a: "), 0, wx.TOP, 5)
            self.aSPIN = wx.SpinCtrl(self.middlePanel, size=(35, -1), style=wx.TE_READONLY)
            self.aSPIN.SetRange(0, 4000)
            self.aSPIN.SetValue(self.data[19])
            if self.data[18]=='Y':
                self.aCheckCtrl.SetValue(True)
                self.aSPIN.Enable(True)
            else:
                self.aCheckCtrl.SetValue(False)
                self.aSPIN.Enable(False)
            hhbox.Add(self.aSPIN, 1)
            vbox.Add(hhbox, 0, wx.EXPAND | wx.RIGHT, 20)
            vbox.Add((-1, 5))

            hhbox = wx.BoxSizer()
            hhbox.Add(20, -1)
            self.bCheckCtrl = wx.CheckBox(self.middlePanel)
            hhbox.Add(self.bCheckCtrl, 0, wx.TOP, 5)
            hhbox.Add(wx.StaticText(self.middlePanel, label="b: "), 0, wx.TOP, 5)
            self.bSPIN = wx.SpinCtrl(self.middlePanel, size=(35, -1), style=wx.TE_READONLY)
            self.bSPIN.SetRange(0, 4000)
            self.bSPIN.SetValue(self.data[21])
            if self.data[20]=='Y':
                self.bCheckCtrl.SetValue(True)
                self.bSPIN.Enable(True)
            else:
                self.bCheckCtrl.SetValue(False)
                self.bSPIN.Enable(False)
            hhbox.Add(self.bSPIN, 1)
            vbox.Add(hhbox, 0, wx.EXPAND | wx.RIGHT, 20)
            vbox.Add((-1, 5))

            hhbox = wx.BoxSizer()
            hhbox.Add(20, -1)
            self.cCheckCtrl = wx.CheckBox(self.middlePanel)
            hhbox.Add(self.cCheckCtrl, 0, wx.TOP, 5)
            hhbox.Add(wx.StaticText(self.middlePanel, label="c: "), 0, wx.TOP, 5)
            self.cSPIN = wx.SpinCtrl(self.middlePanel, size=(35, -1), style=wx.TE_READONLY)
            self.cSPIN.SetRange(0, 4000)
            self.cSPIN.SetValue(self.data[23])
            if self.data[22]=='Y':
                self.cCheckCtrl.SetValue(True)
                self.cSPIN.Enable(True)
            else:
                self.cCheckCtrl.SetValue(False)
                self.cSPIN.Enable(False)
            hhbox.Add(self.cSPIN, 1)
            vbox.Add(hhbox, 0, wx.EXPAND | wx.RIGHT, 20)
            vbox.Add((-1, 5))

            hhbox = wx.BoxSizer()
            hhbox.Add(20, -1)
            self.dCheckCtrl = wx.CheckBox(self.middlePanel)
            hhbox.Add(self.dCheckCtrl, 0, wx.TOP, 5)
            hhbox.Add(wx.StaticText(self.middlePanel, label="d: "), 0, wx.TOP, 5)
            self.dSPIN = wx.SpinCtrl(self.middlePanel, size=(35, -1), style=wx.TE_READONLY)
            self.dSPIN.SetRange(0, 4000)
            self.dSPIN.SetValue(self.data[25])
            if self.data[24]=='Y':
                self.dCheckCtrl.SetValue(True)
                self.dSPIN.Enable(True)
            else:
                self.dCheckCtrl.SetValue(False)
                self.dSPIN.Enable(False)
            hhbox.Add(self.dSPIN, 1)
            vbox.Add(hhbox, 0, wx.EXPAND | wx.RIGHT, 20)
            vbox.Add((-1, 5))

            hhbox = wx.BoxSizer()
            hhbox.Add(20, -1)
            self.eCheckCtrl = wx.CheckBox(self.middlePanel)
            hhbox.Add(self.eCheckCtrl, 0, wx.TOP, 5)
            hhbox.Add(wx.StaticText(self.middlePanel, label="e: "), 0, wx.TOP, 5)
            self.eSPIN = wx.SpinCtrl(self.middlePanel, size=(35, -1), style=wx.TE_READONLY)
            self.eSPIN.SetRange(0, 4000)
            self.eSPIN.SetValue(self.data[27])
            if self.data[26]=='Y':
                self.eCheckCtrl.SetValue(True)
                self.eSPIN.Enable(True)
            else:
                self.eCheckCtrl.SetValue(False)
                self.eSPIN.Enable(False)
            hhbox.Add(self.eSPIN, 1)
            vbox.Add(hhbox, 0, wx.EXPAND | wx.RIGHT, 20)
            vbox.Add((-1, 5))

            hhbox = wx.BoxSizer()
            hhbox.Add(20, -1)
            self.fCheckCtrl = wx.CheckBox(self.middlePanel)
            hhbox.Add(self.fCheckCtrl, 0, wx.TOP, 5)
            hhbox.Add(wx.StaticText(self.middlePanel, label="f: "), 0, wx.TOP, 5)
            self.fSPIN = wx.SpinCtrl(self.middlePanel, size=(35, -1), style=wx.TE_READONLY)
            self.fSPIN.SetRange(0, 4000)
            self.fSPIN.SetValue(self.data[29])
            if self.data[28]=='Y':
                self.fCheckCtrl.SetValue(True)
                self.fSPIN.Enable(True)
            else:
                self.fCheckCtrl.SetValue(False)
                self.fSPIN.Enable(False)
            hhbox.Add(self.fSPIN, 1)
            vbox.Add(hhbox, 0, wx.EXPAND | wx.RIGHT, 20)
            vbox.Add((-1, 5))

            hhbox = wx.BoxSizer()
            hhbox.Add(20, -1)
            self.cYCheckCtrl = wx.CheckBox(self.middlePanel)
            hhbox.Add(self.cYCheckCtrl, 0, wx.TOP, 5)
            hhbox.Add(wx.StaticText(self.middlePanel, label="cY: "), 0, wx.TOP, 5)
            self.cYSPIN = wx.SpinCtrl(self.middlePanel, size=(35, -1), style=wx.TE_READONLY)
            self.cYSPIN.SetRange(0, 4000)
            self.cYSPIN.SetValue(self.data[31])
            if self.data[30]=='Y':
                self.cYCheckCtrl.SetValue(True)
                self.cYSPIN.Enable(True)
            else:
                self.cYCheckCtrl.SetValue(False)
                self.cYSPIN.Enable(False)
            hhbox.Add(self.cYSPIN, 1)
            vbox.Add(hhbox, 0, wx.EXPAND | wx.RIGHT, 20)
            vbox.Add((-1, 5))

        vbox.Add((-1,20))

        procudureFrame = wx.StaticBox(self.middlePanel,label='生产工序:',size=(100,80))
        vbox.Add(procudureFrame,0,wx.EXPAND|wx.LEFT|wx.RIGHT,7)
        topBorder, otherBorder = procudureFrame.GetBordersForSizer()
        bsizer=wx.BoxSizer(wx.VERTICAL)
        bsizer.AddSpacer(topBorder+5)
        hhbox = wx.BoxSizer()
        hhbox.AddSpacer(otherBorder+2)

        vvbox = wx.BoxSizer(wx.VERTICAL)
        self.shapeprocess405Check = wx.CheckBox(procudureFrame,label='成型405')
        if self.data[5]=='Y':
            self.shapeprocess405Check.SetValue(True)
        vvbox.Add(self.shapeprocess405Check,0)
        self.shapeprocess406Check = wx.CheckBox(procudureFrame,label='成型406')
        if self.data[7]=='Y':
            self.shapeprocess406Check.SetValue(True)
        vvbox.Add(self.shapeprocess406Check,0)
        # self.shapeprocess409Check = wx.CheckBox(procudureFrame,label='成型409')
        # if self.data[6]=='Y':
        #     self.shapeprocess409Check.SetValue(True)
        # vvbox.Add(self.shapeprocess409Check,0)
        hhbox.Add(vvbox,1)

        vvbox = wx.BoxSizer(wx.VERTICAL)
        self.bowprocess652Check = wx.CheckBox(procudureFrame,label='折弯652')
        if self.data[8]=='Y':
            self.bowprocess652Check.SetValue(True)
        vvbox.Add(self.bowprocess652Check,0)
        hhbox.Add(vvbox,1)

        vvbox = wx.BoxSizer(wx.VERTICAL)
        self.hotpressprocess100Check = wx.CheckBox(procudureFrame,label='热压100')
        if self.data[9]=='Y':
            self.hotpressprocess100Check.SetValue(True)
        vvbox.Add(self.hotpressprocess100Check,0)
        self.hotpressprocess306Check = wx.CheckBox(procudureFrame,label='特制品306')
        if self.data[10]=='Y':
            self.hotpressprocess306Check.SetValue(True)
        vvbox.Add(self.hotpressprocess306Check,0)
        hhbox.Add(vvbox,1)

        # vvbox = wx.BoxSizer(wx.VERTICAL)
        # self.holeprocess9000Check = wx.CheckBox(procudureFrame,label='冲铣xxx')
        # if '9000' in procedure:
        #     self.holeprocess9000Check.SetValue(True)
        # vvbox.Add(self.holeprocess9000Check,0)
        # hhbox.Add(vvbox)
        bsizer.Add(hhbox,1,wx.EXPAND)
        procudureFrame.SetSizer(bsizer)




        temp = self.data[1].split(',')
        self.frontLengthDelta = temp[0]
        self.frontWidthDelta = temp[1]
        self.frontLengthDeltaCtrl.SetValue(self.frontLengthDelta)
        self.frontWidthDeltaCtrl.SetValue(self.frontWidthDelta)
        if self.data[14]=='Y':
            temp = self.data[2].split(',')
            self.middleLengthDelta = temp[0]
            self.middleWidthDelta = temp[1]
            self.middleLengthDeltaCtrl.SetValue(self.middleLengthDelta)
            self.middleWidthDeltaCtrl.SetValue(self.middleWidthDelta)
            # self.middleWidthDeltaCtrl.SetEditable(False)
        temp = self.data[3].split(',')
        self.rearLengthDelta = temp[0]
        self.rearWidthDelta = temp[1]
        self.rearLengthDeltaCtrl.SetValue(self.rearLengthDelta)
        self.rearWidthDeltaCtrl.SetValue(self.rearWidthDelta)

        if state != '查看':
            if state == '编辑':
                self.bluePrintTypeCombo.Enable(False)
            vbox.Add(wx.Panel(self.middlePanel, size=(10, 10)), 1, wx.EXPAND)
            hhbox=wx.BoxSizer()
            hhbox.Add((10,-1))
            self.editCancelButton=wx.Button(self.middlePanel, label='取消', size=(50, 35))
            self.editCancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
            self.editCancelButton.SetBackgroundColour(wx.RED)
            self.editOkButton=wx.Button(self.middlePanel, label='确定', size=(50, 35))
            self.editOkButton.Bind(wx.EVT_BUTTON,self.OnEditOkBTN)
            self.editOkButton.SetBackgroundColour(wx.GREEN)
            hhbox.Add(self.editCancelButton,1,wx.EXPAND|wx.RIGHT,10)
            hhbox.Add((10,-1))
            hhbox.Add(self.editOkButton,1,wx.EXPAND|wx.RIGHT,10)
            vbox.Add(hhbox,0,wx.EXPAND|wx.BOTTOM,5)
            vbox.Add(wx.StaticLine(self.middlePanel, style=wx.HORIZONTAL), 0, wx.EXPAND)
        else:
            self.bluePrintTypeCombo.Enable(False)
            self.frontLengthDeltaCtrl.Enable(False)
            self.frontWidthDeltaCtrl.Enable(False)
            self.rearLengthDeltaCtrl.Enable(False)
            self.rearWidthDeltaCtrl.Enable(False)
            # self.shapeprocess405Check.Enable(False)
            # self.shapeprocess406Check.Enable(False)
            # self.shapeprocess409Check.Enable(False)
            # self.bowprocess652Check.Enable(False)
            # self.hotpressprocess100Check.Enable(False)
            # self.hotpressprocess306Check.Enable(False)
            # self.holeprocess9000Check.Enable(False)
            # self.shapeprocess405RearCheck.Enable(False)
            # self.shapeprocess406RearCheck.Enable(False)
            # self.shapeprocess409RearCheck.Enable(False)
            # self.bowprocess652RearCheck.Enable(False)
            # self.hotpressprocess100RearCheck.Enable(False)
            # self.hotpressprocess306RearCheck.Enable(False)
            # self.holeprocess9000RearCheck.Enable(False)
            if self.data[14]=='Y':
                self.middleLengthDeltaCtrl.Enable(False)
                self.middleWidthDeltaCtrl.Enable(False)
                # self.shapeprocess405MiddleCheck.Enable(False)
                # self.shapeprocess406MiddleCheck.Enable(False)
                # self.shapeprocess409MiddleCheck.Enable(False)
                # self.bowprocess652MiddleCheck.Enable(False)
                # self.hotpressprocess100MiddleCheck.Enable(False)
                # self.hotpressprocess306MiddleCheck.Enable(False)
                # self.holeprocess9000MiddleCheck.Enable(False)

        self.middlePanel.SetSizer(vbox)
        self.middlePanel.Refresh()
        self.middlePanel.Layout()
        self.middlePanel.Thaw()

    def OnMiddleEnableCheck(self, event):
        # self.data[14]='Y' if self.middleEnableCheck.GetValue() else 'N'
        self.ReCreateMiddlePanel(self.type, '新建')
        event.Skip()

    def OnEditOkBTN(self,event):
        if self.editState == '新建':
            dlg = wx.TextEntryDialog(
                    self, '请输入图纸编号,目前显示的是系统为您建议的图纸号：',
                    '信息提示', '')
            string = "N.%s.%04d"%(self.bluePrintIndexCtrl.GetValue(),self.bluePrintNoSpin.GetValue())
            dlg.SetValue(string)
            if dlg.ShowModal() == wx.ID_OK:
                self.CombineData(dlg.GetValue())
                SaveBluePrintInDB(self.log, 1, self.data)
                self.busy = False
                self.middlePanel.DestroyChildren()
                self.rightPanel.DestroyChildren()
                _, dataList = GetAllBluPrintList(self.log, 1, self.type, state=self.state)
                self.dataArray = np.array(dataList)
                self.bluePrintGrid.ReCreate()
            dlg.Destroy()
        else:
            self.CombineData(self.data[0])
            UpdateBluePrintInDB(self.log, 1, self.data)
            self.busy = False
            self.middlePanel.DestroyChildren()
            self.rightPanel.DestroyChildren()
            _, dataList = GetAllBluPrintList(self.log, 1, self.type, state=self.state)
            self.dataArray = np.array(dataList)
            self.bluePrintGrid.ReCreate()

    def CombineData(self,bluePrintNo):
        self.data[0] = bluePrintNo
        self.data[1] = '%s,%s'%(self.frontLengthDeltaCtrl.GetValue(),self.frontWidthDeltaCtrl.GetValue())
        if self.data[14]=='Y':
            self.data[2] = '%s,%s'%(self.middleLengthDeltaCtrl.GetValue(),self.middleWidthDeltaCtrl.GetValue())
        else:
            self.data[2] = '0,0'
        self.data[3] = '%s,%s'%(self.rearLengthDeltaCtrl.GetValue(),self.rearWidthDeltaCtrl.GetValue())
        self.data[4] = 'FR' if self.data[14]=='N' else 'FMR'
        self.data[5] = ''#成型405工序
        if self.shapeprocess405Check.GetValue():
            self.data[5] += 'F'
        if self.data[14] == 'Y':
            if self.shapeprocess405MiddleCheck.GetValue():
                self.data[5] += 'M'
        if self.shapeprocess405RearCheck.GetValue():
            self.data[5] += 'R'

        self.data[6] = ''#成型409工序
        if self.shapeprocess409Check.GetValue():
            self.data[6] += 'F'
        if self.data[14] == 'Y':
            if self.shapeprocess409MiddleCheck.GetValue():
                self.data[6] += 'M'
        if self.shapeprocess409RearCheck.GetValue():
            self.data[6] += 'R'

        self.data[7] = ''#成型406工序
        if self.shapeprocess406Check.GetValue():
            self.data[7] += 'F'
        if self.data[14] == 'Y':
            if self.shapeprocess406MiddleCheck.GetValue():
                self.data[7] += 'M'
        if self.shapeprocess406RearCheck.GetValue():
            self.data[7] += 'R'

        self.data[8] = ''#折弯652工序
        if self.bowprocess652Check.GetValue():
            self.data[8] += 'F'
        if self.data[14] == 'Y':
            if self.bowprocess652MiddleCheck.GetValue():
                self.data[8] += 'M'
        if self.bowprocess652RearCheck.GetValue():
            self.data[8] += 'R'

        self.data[9] = ''#热压100工序
        if self.hotpressprocess100Check.GetValue():
            self.data[9] += 'F'
        if self.data[14] == 'Y':
            if self.hotpressprocess100MiddleCheck.GetValue():
                self.data[9] += 'M'
        if self.hotpressprocess100RearCheck.GetValue():
            self.data[9] += 'R'

        self.data[10] = ''#特制品306工序
        if self.hotpressprocess306Check.GetValue():
            self.data[10] += 'F'
        if self.data[14] == 'Y':
            if self.hotpressprocess306MiddleCheck.GetValue():
                self.data[10] += 'M'
        if self.hotpressprocess306RearCheck.GetValue():
            self.data[10] += 'R'

        # self.data[11] = ''#冲洗xxx工序
        # if self.holeprocess9000Check.GetValue():
        #     self.data[11] += 'F'
        # if self.data[14] == 'Y':
        #     if self.holeprocess9000MiddleCheck.GetValue():
        #         self.data[11] += 'M'
        # if self.holeprocess9000RearCheck.GetValue():
        #     self.data[11] += 'R'

        self.data[12]='在用'
        self.data[13]='%s'%self.master.master.master.operatorID
        self.data[15] = 'FR' if self.data[14]=='N' else 'FMR'
        self.data[16] = '%s'%self.type
        # self.data[17] = str(self.pageNo)

    def OnCancel(self,event):
        self.busy = False
        self.middlePanel.DestroyChildren()
        self.rightPanel.DestroyChildren()

    def OnBluePrintTypeChanged(self,event):
        self.bluePrintType = self.bluePrintTypeCombo.GetValue()
        key=self.typeBluePrintDict[self.bluePrintType]
        # self.bluePrintShowPanel.Recreate('bitmaps/%s.JPG' % key)
        self.bluePrintIndexCtrl.SetValue(key)
        # if self.bluePrintType == '25mm墙板':
        #     self.picPanel.Recreate('bitmaps/2SA.JPG')
        # elif self.bluePrintType == '25mm墙角板':
        #     self.picPanel.Recreate('bitmaps/2SG.JPG')


    # def OnChangeBluePrintBTN(self,event):
    #     self.picPanel.Recreate('bitmaps/2SG.JPG')

    def OnChangeState(self,event):
        if self.state == '在用':
            self.state = '停用'
            self.changeStateBTN.SetBackgroundColour(wx.RED)
        elif self.state == '停用':
            self.state = '全部'
            self.changeStateBTN.SetBackgroundColour(wx.YELLOW)
        else:
            self.state = '在用'
            self.changeStateBTN.SetBackgroundColour(wx.GREEN)
        _, dataList = GetAllBluPrintList(self.log, 1, self.type,state=self.state)
        self.dataArray = np.array(dataList)
        self.bluePrintGrid.ReCreate()
        # self.bluePrintGrid.Render()

    def OnCreateNewBluePrint(self, event):
        if self.busy == False:
            self.busy = True
            if len(self.data)==0:
                if len(self.dataArray)==0:
                    self.data = ['']*18
                else:
                    self.data = self.dataArray[0]
            self.data[14]='0'
            self.editState = '新建'
            self.ReCreateMiddlePanel(self.type,state=self.editState)
            self.ReCreateRightPanel()
            filename = '图纸/%s/%s.jpg' % (self.bluePrintIndexCtrl.GetValue(), self.pageNo)
            # self.bluePrintShowPanel.Recreate(filename, '新建')
        else:
            wx.MessageBox("请先结束当前编辑工作后，再进行新的编辑操作！", "信息提示")

    def OnBluePrintIDSearch(self, event):
        self.bluePrintIDSearch = self.bluePrintIDSearchCtrl.GetValue()
        self.ReSearch()

    def OnMiddleLengthDeltaSearch(self, event):
        self.middleLengthDeltaSearch = self.middleLengthDeltaSearchCtrl.GetValue()
        self.ReSearch()

    def OnMiddleWidthDeltaSearch(self, event):
        self.middleWidthDeltaSearch = self.middleWidthDeltaSearchCtrl.GetValue()
        self.ReSearch()

    def OnRearLengthDeltaSearch(self, event):
        self.rearLengthDeltaSearch = self.rearLengthDeltaSearchCtrl.GetValue()
        self.ReSearch()

    def OnRearWidthDeltaSearch(self, event):
        self.rearWidthDeltaSearch = self.rearWidthDeltaSearchCtrl.GetValue()
        self.ReSearch()

    def OnBoardSupportComponentSearch(self,event):
        self.boardSupportComponentSearch = self.boardSupportComponentSearchCtrl.GetValue()
        self.ReSearch()

    def OnBoardSupportWidthSearch(self,event):
        self.boardSupportWidthSearch = self.boardSupportWidthSearchCtrl.GetValue()
        self.ReSearch()

    def ReSearch(self):
        _, dataList = GetAllBluPrintList(self.log, 1, self.type,state=self.state)
        self.dataArray = np.array(dataList)
        if self.bluePrintIDSearch != '':
            bluePrintList = []
            for item in self.dataArray:
                if self.bluePrintIDSearch in str(item[0]):
                    bluePrintList.append(board)
            self.dataArray = np.array(bluePrintList)
        # if self.boardMaterialSearch != '':
        #     bluePrintList = []
        #     for board in self.boardArray:
        #         if self.boardMaterialSearch in board[2]:
        #             bluePrintList.append(board)
        #     self.boardArray = np.array(bluePrintList)
        # if self.boardDensitySearch != '':
        #     bluePrintList = []
        #     for board in self.boardArray:
        #         if self.boardDensitySearch in str(board[3]):
        #             bluePrintList.append(board)
        #     self.boardArray = np.array(bluePrintList)
        # if self.boardSupportComponentSearch != '':
        #     bluePrintList = []
        #     for board in self.boardArray:
        #         if self.boardSupportComponentSearch in str(board[4]):
        #             bluePrintList.append(board)
        #     self.boardArray = np.array(bluePrintList)
        # if self.boardSupportWidthSearch != '':
        #     bluePrintList = []
        #     for board in self.boardArray:
        #         if self.boardSupportWidthSearch == str(board[5]):
        #             bluePrintList.append(board)
        #     self.boardArray = np.array(bluePrintList)
        # if self.boardRALIDSearch != '':
        #     bluePrintList = []
        #     for board in self.boardArray:
        #         if self.boardRALIDSearch in str(board[6]):
        #             bluePrintList.append(board)
        #     self.boardArray = np.array(bluePrintList)
        self.bluePrintGrid.ReCreate()
        # self.bluePrintGrid.Render()

    def OnResetSearchItem(self, event):
        self.bluePrintIDSearch = ''
        self.bluePrintIDSearchCtrl.SetValue('')
        self.middleLengthDeltaSearch = ''
        self.middleLengthDeltaSearchCtrl.SetValue('')
        self.middleWidthDeltaSearch = ''
        self.middleWidthDeltaSearchCtrl.SetValue('')
        self.rearLengthSearch = ''
        self.rearLengthDeltaSearchCtrl.SetValue('')
        self.rearWidthSearch = ''
        self.rearWidthDeltaSearchCtrl.SetValue('')
        self.ReSearch()

class BluePrintManagementPanel(wx.Panel):
    def __init__(self, parent, master, log):
        wx.Panel.__init__(self, parent, -1)
        self.master = master
        self.log = log
        self.processList=["505","405","409","406","652","100","306","9000"]
        self.notebook = wx.Notebook(self, -1, size=(21, 21), style=
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
        hbox = wx.BoxSizer()
        hbox.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(hbox)
        self.wallBluePrintManagementPanel = SpecificBluePrintManagementPanel(self.notebook, self, self.log, '墙板')
        self.notebook.AddPage(self.wallBluePrintManagementPanel, "墙板图纸管理")
        self.galvanizedSheetManagmentPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.galvanizedSheetManagmentPanel, "天花板图纸管理")
        self.colorCoatManagementPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.colorCoatManagementPanel, "构件图纸管理")
        self.stainlessSheetManagmentPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.stainlessSheetManagmentPanel, "检修门图纸管理")
        self.sparyBoardManagementPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.sparyBoardManagementPanel, "检修口图纸管理")
        self.notebook.SetSelection(0)
