import wx
import wx.grid as gridlib
from DBOperation import GetAllBluPrintList, GetRGBWithRalID,GetAllColor
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
        self.CreateGrid(self.master.dataArray.shape[0]+30, len(self.master.colLabelValueList))  # , gridlib.Grid.SelectRows)
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
            print(data)
            for j, item in enumerate(data):
                # self.SetCellBackgroundColour(i,j,wx.Colour(250, 250, 250))
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.SetCellValue(i, j, str(item))

        # self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
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
        print("input data",data)
        result = list(data[:4])
        process = ''
        if data[4]=='Y':
            process += self.master.processList[0]
            process += '/'
        if data[5]=='Y':
            process += self.master.processList[1]
            process += '/'
        if data[6]=='Y':
            process += self.master.processList[2]
            process += '/'
        if data[7]=='Y':
            process += self.master.processList[3]
            process += '/'
        if data[8]=='Y':
            process += self.master.processList[4]
            process += '/'
        if data[9]=='Y':
            process += self.master.processList[5]
            process += '/'
        if data[10]=='Y':
            process += self.master.processList[6]
            process += '/'
        if data[11]=='Y':
            process += self.master.processList[7]
        process=process+'\r\n'+process
        result.append(process)
        result.append(data[12])
        return result

    def ReCreate(self):
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
            self.SetRowSize(i, 25)
            data = self.Translate(temp)
            for j, item in enumerate(data):
                # self.SetCellBackgroundColour(i,j,wx.Colour(250, 250, 250))
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)
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

    def Recreate(self,filename):
        self.filename = filename
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

class SpecificBluePrintManagementPanel(wx.Panel):
    def __init__(self, parent, master, log, type,state='在用'):
        wx.Panel.__init__(self, parent)
        self.master = master
        self.log = log
        self.type = type
        self.state = state
        self.processList=self.master.processList
        self.colWidthList = [80, 65, 65, 65, 150, 90,]
        self.colLabelValueList = ['图纸号', '面板增量', '中板增量', '背板增量', '所需工序','状态']
        _, dataList = GetAllBluPrintList(self.log, 1, self.type,state=self.state)
        self.dataArray = np.array(dataList)
        self.bluePrintIDSearch = ''
        self.middleLengthDeltaSearch = ''
        self.middleWidthDeltaSearch = ''
        self.rearLengthSearch = ''
        self.rearWidthSearch=''
        self.workProcessSearch=''
        self.editBluePrintOccupied = False
        hbox = wx.BoxSizer()
        self.leftPanel = wx.Panel(self, size=(583, -1))
        hbox.Add(self.leftPanel, 0, wx.EXPAND)
        self.rightPanel = wx.Panel(self, size=(360, -1))
        hbox.Add(self.rightPanel, 1, wx.EXPAND)
        self.SetSizer(hbox)
        self.CreateLeftPanel()
        self.CreateRightPanel()
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)

    def OnCellLeftClick(self, evt):
        row = evt.GetRow()
        data = self.dataArray[row]
        filename = './bitmaps/' + data[0].split('.')[1]+'.jpg'
        self.picPanel.Recreate(filename)
        self.ReCreateBasicInfoPanel(self.type,data)
        self.ReCreateBottomPanel(self.type,data)
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


    def CreateRightPanel(self):
        vvbox = wx.BoxSizer(wx.VERTICAL)
        self.topPanel = wx.Panel(self.rightPanel,size=(-1,450))
        vvbox.Add(self.topPanel, 1, wx.EXPAND)
        self.bottomPanel = wx.Panel(self.rightPanel,size=(-1,100))
        vvbox.Add(self.bottomPanel,0, wx.EXPAND)
        self.rightPanel.SetSizer(vvbox)

        hhbox = wx.BoxSizer()
        self.picPanel = BluePrintShowPanel(self.topPanel, size=(550, 450))
        hhbox.Add(self.picPanel,1)
        self.basicInfoPanel = wx.Panel(self.topPanel,size=(230,100))
        hhbox.Add(self.basicInfoPanel, 0, wx.EXPAND)
        self.topPanel.SetSizer(hhbox)
        # self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)

    # def OnCellLeftDClick(self, evt):
    #     row = evt.GetRow()
    #     col = evt.GetCol()
    #     if col == 9:
    #         if self.editBoardPanelOccupied == False:
    #             self.editBoardPanelOccupied=True
    #             self.ReCreateBasicInfoPanel(self.boardType, state='编辑')
    #         else:
    #             wx.MessageBox("请先结束当前编辑工作后，再进行新的编辑操作！","信息提示")
    #     # evt.Skip()
    def ReCreateBottomPanel(self,type,data=[], state='编辑'):
        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1,10))
        hbox = wx.BoxSizer()
        hbox.Add((20,-1))
        hbox.Add(wx.StaticText(self.bottomPanel, label='面板工序：',size=(70,-1)),0,wx.TOP,5)
        hbox.Add((20,-1))
        vvbox = wx.BoxSizer(wx.VERTICAL)
        self.process505Check = wx.CheckBox(self.bottomPanel,label='剪板505')
        vvbox.Add(self.process505Check,0)
        hbox.Add(vvbox,0,wx.EXPAND)
        vbox.Add(hbox,0,wx.EXPAND)
        self.bottomPanel.SetSizer(vbox)


    def ReCreateBasicInfoPanel(self, type, data=[], state='编辑'):
        self.basicInfoPanel.Freeze()
        self.basicInfoPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1,10))
        hhbox = wx.BoxSizer()
        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.basicInfoPanel,label='图纸类别：',size=(90,-1)),0,wx.TOP,5)
        bluePrintTypeDict = {'2SF':"25mm墙板","2SA":'50mm墙板','2SG':'25mm墙角板','2SD':'50mm墙角板','2SH':'25mmT型墙板','2SE':'50mmT型墙板','2SM':'高隔音墙板','2SL':'100mm墙板'}
        choices=[]
        if type=="墙板":
            choices=["25mm墙板",'50mm墙板','25mm墙角板','25mmT型墙板','50mmT型墙板','高隔音墙板','100mm墙板']
        self.bluePrintTypeCombo = wx.ComboBox(self.basicInfoPanel,choices=choices,size=(120,30),style=wx.TE_PROCESS_ENTER)
        if len(data)!=0:
            key = data[0].split('.')[1]
            self.bluePrintTypeCombo.SetValue(bluePrintTypeDict[key])
        self.bluePrintTypeCombo.Bind(wx.EVT_COMBOBOX, self.OnBluePrintTypeChanged)
        hhbox.Add(self.bluePrintTypeCombo,1,wx.RIGHT,20)
        vbox.Add(hhbox,0,wx.EXPAND)

        # hhbox = wx.BoxSizer()
        # hhbox.Add((70,-1))
        # hhbox.Add(wx.StaticText(self.basicInfoPanel,label="   长度方向",size=(70,-1)),1)
        # hhbox.Add((5,-1))
        # hhbox.Add(wx.StaticText(self.basicInfoPanel,label="   宽度方向",size=(70,-1)),1)
        # vbox.Add(hhbox,0)
        #
        hhbox = wx.BoxSizer()
        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.basicInfoPanel,label='面板长度增量:',size=(90,-1)),0,wx.TOP,5)
        self.frontLengthDeltaCtrl=wx.TextCtrl(self.basicInfoPanel,size=(60,-1))
        hhbox.Add(self.frontLengthDeltaCtrl,1,wx.RIGHT,20)
        vbox.Add(hhbox,0,wx.EXPAND)
        vbox.Add((-1,5))

        hhbox = wx.BoxSizer()
        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.basicInfoPanel,label='面板宽度增量:',size=(90,-1)),0,wx.TOP,5)
        self.frontWidthDeltaCtrl=wx.TextCtrl(self.basicInfoPanel,size=(60,-1))
        hhbox.Add(self.frontWidthDeltaCtrl,1,wx.RIGHT,20)
        vbox.Add(hhbox,0,wx.EXPAND)
        vbox.Add((-1,5))

        if self.bluePrintTypeCombo.GetValue() in ["50mm墙板"]:
            hhbox = wx.BoxSizer()
            hhbox.Add((20,-1))
            hhbox.Add(wx.StaticText(self.basicInfoPanel,label='中板长度增量:',size=(90,-1)),0,wx.TOP,5)
            self.middleLengthDeltaCtrl=wx.TextCtrl(self.basicInfoPanel,size=(60,-1))
            hhbox.Add(self.middleLengthDeltaCtrl,1,wx.RIGHT,20)
            vbox.Add(hhbox,0,wx.EXPAND)

            hhbox = wx.BoxSizer()
            hhbox.Add((20,-1))
            hhbox.Add(wx.StaticText(self.basicInfoPanel,label='中板宽度增量:',size=(90,-1)),0,wx.TOP,5)
            self.middleWidthDeltaCtrl=wx.TextCtrl(self.basicInfoPanel,size=(60,-1))
            hhbox.Add(self.middleWidthDeltaCtrl,1,wx.RIGHT,20)
            vbox.Add(hhbox,0,wx.EXPAND|wx.TOP,5)
            vbox.Add((-1,5))

        hhbox = wx.BoxSizer()
        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.basicInfoPanel,label='背板长度增量:',size=(90,-1)),0,wx.TOP,5)
        self.rearLengthDeltaCtrl=wx.TextCtrl(self.basicInfoPanel,size=(60,-1))
        hhbox.Add(self.rearLengthDeltaCtrl,1,wx.RIGHT,20)
        vbox.Add(hhbox,0,wx.EXPAND)
        vbox.Add((-1,5))

        hhbox = wx.BoxSizer()
        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.basicInfoPanel,label='背板宽度增量:',size=(90,-1)),0,wx.TOP,5)
        self.rearWidthDeltaCtrl=wx.TextCtrl(self.basicInfoPanel,size=(60,-1))
        hhbox.Add(self.rearWidthDeltaCtrl,1,wx.RIGHT,20)
        vbox.Add(hhbox,0,wx.EXPAND)
        vbox.Add((-1,5))

        if state == '编辑':
            self.bluePrintTypeCombo.Enable(False)
            temp = data[1].split(',')
            self.frontLengthDelta = temp[0]
            self.frontWidthDelta = temp[1]
            self.frontLengthDeltaCtrl.SetValue(self.frontLengthDelta)
            self.frontWidthDeltaCtrl.SetValue(self.frontWidthDelta)
            if self.bluePrintTypeCombo.GetValue() in ["50mm墙板"]:
                temp = data[2].split(',')
                self.middleLengthDelta = temp[0]
                self.middleWidthDelta = temp[1]
                self.middleLengthDeltaCtrl.SetValue(self.middleLengthDelta)
                self.middleWidthDeltaCtrl.SetValue(self.middleWidthDelta)
            temp = data[3].split(',')
            self.rearLengthDelta = temp[0]
            self.rearWidthDelta = temp[1]
            self.rearLengthDeltaCtrl.SetValue(self.rearLengthDelta)
            self.rearWidthDeltaCtrl.SetValue(self.rearWidthDelta)

        # self.frontWidthDeltaCtrl=wx.TextCtrl(self.basicInfoPanel,size=(50,-1))
        # hhbox.Add((5,-1))
        # hhbox.Add(self.frontWidthDeltaCtrl,1)
        # self.btn = wx.Button(self.basicInfoPanel,label="change",size=(100,30))
        # self.btn.Bind(wx.EVT_BUTTON, self.OnChangeBluePrintBTN)
        # hbox=wx.BoxSizer()
        # hbox.Add(self.btn)
        self.basicInfoPanel.SetSizer(vbox)
        self.basicInfoPanel.Refresh()
        self.basicInfoPanel.Layout()
        self.basicInfoPanel.Thaw()

    def OnBluePrintTypeChanged(self,event):
        self.bluePrintType = self.bluePrintTypeCombo.GetValue()
        if self.bluePrintType == '25mm墙板':
            self.picPanel.Recreate('bitmaps/2SA.JPG')
        elif self.bluePrintType == '25mm墙角板':
            self.picPanel.Recreate('bitmaps/2SG.JPG')


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
        if self.editBluePrintOccupied == False:
            self.editBluePrintOccupied = True
            self.ReCreateBasicInfoPanel(self.type,)
        else:
            wx.MessageBox("请先结束当前编辑工作后，再进行新的编辑操作！", "信息提示")
        # hhbox = wx.BoxSizer()
        # self.finishNewBoardBTN = wx.Button(self.editBoardPanel)
        # self.finishNewBoardBTN.Bind(wx.EVT_BUTTON,self.OnFinishNewBoard)
        # hhbox.Add(self.finishNewBoardBTN,0)
        # self.editBoardPanel.SetSizer(hhbox)
        # self.editBoardPanel.Layout()
        # self.colorPalettePanel.ReCreate()

    # def OnFinishNewBoard(self,event):
    #     self.colorPalettePanel.DestroyChildren()
    #     self.editBoardPanel.DestroyChildren()
    #     self.editBoardPanelOccupied = False

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
