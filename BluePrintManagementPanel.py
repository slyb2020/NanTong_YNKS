import os

import wx
import wx.grid as gridlib
from DBOperation import GetAllBluPrintList, GetRGBWithRalID,GetAllColor,SaveBluePrintInDB,UpdateBluePrintInDB,GetAllConstructionList,SaveConstructionInDB
import wx.grid as gridlib
import numpy as np
import images
import wx.lib.scrolledpanel as scrolled
from ID_DEFINE import *
from ProductionScheduleDialog import PDFViewerPanel
import datetime


class BluePrintShowPanel(PDFViewerPanel):
    def __init__(self, parent, log,filename=""):
        super(BluePrintShowPanel, self).__init__(parent, log)
        if filename!="":
            self.filename = filename
            self.viewer.LoadFile(self.filename)


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
            self.SetRowSize(i, 25)
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
        processList=["505",'405','409','406','652','100','306']
        for i,process in enumerate(processList):
            if 'Y' == data[i+4]:
                processFront += process
                processFront += '/'
        processFront += '9000'
        result.append(processFront)
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
            self.SetRowSize(i, 25)
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
class ConstructionGrid(gridlib.Grid):  ##, mixins.GridAutoEditMixin):
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

        for i, data in enumerate(self.master.dataArray):
            self.SetRowSize(i, 25)
            for j, item in enumerate(data[:-2]):
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

        for i, data in enumerate(self.master.dataArray):
            self.SetRowSize(i, 25)
            for j, item in enumerate(data[:-1]):
                # self.SetCellBackgroundColour(i,j,wx.Colour(250, 250, 250))
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.SetCellValue(i, j, str(item))

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

class SpecificBluePrintManagementPanel(wx.Panel):
    def __init__(self, parent, master, log, type,state='在用'):
        wx.Panel.__init__(self, parent)
        self.master = master
        self.log = log
        self.type = type
        self.state = state
        self.busy = False
        self.editState = '查看'
        self.data = []
        self.processList=self.master.processList
        self.colWidthList = [80, 65, 65, 65, 150, 50,47]
        self.colLabelValueList = ['图纸号', '面板增量', '中板增量', '背板增量', '所需工序','状态','']
        _, dataList = GetAllBluPrintList(self.log, 1, self.type,state=self.state)
        self.dataArray = np.array(dataList)
        self.bluePrintIDSearch = ''
        self.frontDeltaSearch = ''
        self.middleDeltaSearch = ''
        self.rearDeltaSearch = ''
        self.procedureSearch=''
        self.busy = False
        hbox = wx.BoxSizer()
        self.leftPanel = wx.Panel(self, size=(590, -1))
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

    def OnCellLeftDClick(self, evt):
        if self.busy == False:
            col=evt.GetCol()
            if col == 6:
                    self.busy = True
                    row = evt.GetRow()
                    self.data = self.dataArray[row]
                    index = self.data[0].split('.')[1]
                    filename = bluePrintDir + 'Stena 生产图纸 %s/' % index + self.data[32] + '.pdf'
                    self.editState = '编辑'
                    self.ReCreateMiddlePanel(self.type, self.editState)
                    self.ReCreateRightPanel(filename)
            evt.Skip()
        else:
            wx.MessageBox("请先结束当前编辑工作后，再进行新的编辑操作！", "信息提示")


    def OnCellLeftClick(self, evt):
        if self.busy == False:
            row = evt.GetRow()
            self.bluePrintGrid.SetSelectionMode(wx.grid.Grid.GridSelectRows)
            self.bluePrintGrid.SelectRow(row)
            self.data = self.dataArray[row]
            index = self.data[0].split('.')[1]
            filename = bluePrintDir+'Stena 生产图纸 %s/'%index+self.data[32]+'.pdf'
            self.editState = '查看'
            self.ReCreateMiddlePanel(self.type, self.editState)
            self.ReCreateRightPanel(filename)
            evt.Skip()
        else:
            wx.MessageBox("请先结束当前编辑工作后，再进行新的编辑操作！", "信息提示")



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

        self.frontDeltaSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[1], -1),
                                                style=wx.TE_PROCESS_ENTER)
        self.frontDeltaSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnFrontDeltaSearch)
        hhbox.Add(self.frontDeltaSearchCtrl, 0, wx.EXPAND)

        self.middleDeltaSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[2], -1),
                                                 style=wx.TE_PROCESS_ENTER)
        self.middleDeltaSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnMiddleDeltaSearch)
        hhbox.Add(self.middleDeltaSearchCtrl, 0, wx.EXPAND)

        self.rearDeltaSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[3], -1),
                                               style=wx.TE_PROCESS_ENTER)
        self.rearDeltaSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnRearDeltaSearch)
        hhbox.Add(self.rearDeltaSearchCtrl, 0, wx.EXPAND)

        self.procedureSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[4], -1),
                                                       style=wx.TE_PROCESS_ENTER)
        self.procedureSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnProcedureSearch)
        hhbox.Add(self.procedureSearchCtrl, 0, wx.EXPAND)

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

    def ReCreateRightPanel(self,filename=""):
        self.rightPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.bluePrintShowPanel = BluePrintShowPanel(self.rightPanel, self.log,filename)
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
                # hhbox.Add(wx.CheckBox(self.middlePanel),0,wx.TOP,5)
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
        hhbox.Add(vvbox,1)

        vvbox = wx.BoxSizer(wx.VERTICAL)
        self.bendprocess652Check = wx.CheckBox(procudureFrame, label='折弯652')
        if self.data[8]=='Y':
            self.bendprocess652Check.SetValue(True)
        vvbox.Add(self.bendprocess652Check, 0)
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
            self.shapeprocess405Check.Enable(False)
            self.shapeprocess406Check.Enable(False)
            # self.shapeprocess409Check.Enable(False)
            self.bendprocess652Check.Enable(False)
            self.hotpressprocess100Check.Enable(False)
            self.hotpressprocess306Check.Enable(False)
            if self.data[14]=='Y':
                self.middleLengthDeltaCtrl.Enable(False)
                self.middleWidthDeltaCtrl.Enable(False)

        self.middlePanel.SetSizer(vbox)
        self.middlePanel.Refresh()
        self.middlePanel.Layout()
        self.middlePanel.Thaw()

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
        """"`图纸号`, `面板增量`, `中板增量`, `背板增量`, `剪板505`, `成型405`, `成型409`, `成型406`, `折弯652`, `热压100`,
        `热压306`, `冲铣`, `图纸状态`, `创建人`, `中板`, '打包9000', `创建时间`, `备注`, `a使能`, `a`,
        `b使能`, `b`, `c使能`, `c`, `d使能`, `d`, `e使能`, `e`, `f使能`, `f`,
        `CY使能`, `CY`, `图纸名`
        from `图纸信息`"""
        self.data[0] = bluePrintNo
        self.data[1] = '%s,%s'%(self.frontLengthDeltaCtrl.GetValue(),self.frontWidthDeltaCtrl.GetValue())
        if self.data[14]=='1':
            self.data[2] = '%s,%s,0,0'%(self.middleLengthDeltaCtrl.GetValue(),self.middleWidthDeltaCtrl.GetValue())
        elif self.data[14]=='2':
            self.data[2] = '0,0,0,0'
        self.data[3] = '%s,%s'%(self.rearLengthDeltaCtrl.GetValue(),self.rearWidthDeltaCtrl.GetValue())
        self.data[4] = 'Y'
        self.data[5] = 'Y' if self.shapeprocess405Check.GetValue() else 'N'#成型405工序
        self.data[7] = 'Y' if self.shapeprocess406Check.GetValue() else 'N'#成型406工序
        self.data[8] = 'Y' if self.bendprocess652Check.GetValue() else 'N'#折弯652工序
        self.data[9] = 'Y' if self.hotpressprocess100Check.GetValue() else 'N'#热压100工序
        self.data[10] = 'Y' if self.hotpressprocess306Check.GetValue() else 'N'#特制品306工序
        self.data[12]='在用'
        self.data[13]='%s'%self.master.master.master.operatorID
        self.data[15] = 'Y'
        self.data[16] = '%s'%str(datetime.date.today())
        if self.aCheckCtrl.GetValue():
            self.data[18]='Y'
            self.data[19]=str(self.aSPIN.GetValue())
        else:
            self.data[18]='N'
            self.data[19]='0'

        if self.bCheckCtrl.GetValue():
            self.data[20]='Y'
            self.data[21]=str(self.bSPIN.GetValue())
        else:
            self.data[20]='N'
            self.data[21]='0'

        if self.cCheckCtrl.GetValue():
            self.data[22]='Y'
            self.data[23]=str(self.cSPIN.GetValue())
        else:
            self.data[22]='N'
            self.data[23]='0'

        if self.dCheckCtrl.GetValue():
            self.data[24]='Y'
            self.data[25]=str(self.dSPIN.GetValue())
        else:
            self.data[24]='N'
            self.data[25]='0'

        if self.eCheckCtrl.GetValue():
            self.data[26]='Y'
            self.data[27]=str(self.eSPIN.GetValue())
        else:
            self.data[26]='N'
            self.data[27]='0'

        if self.fCheckCtrl.GetValue():
            self.data[28]='Y'
            self.data[29]=str(self.fSPIN.GetValue())
        else:
            self.data[28]='N'
            self.data[29]='0'

        if self.cYCheckCtrl.GetValue():
            self.data[30]='Y'
            self.data[31]=str(self.cYSPIN.GetValue())
        else:
            self.data[30]='N'
            self.data[31]='0'

    def OnCancel(self,event):
        self.busy = False
        self.middlePanel.DestroyChildren()
        self.rightPanel.DestroyChildren()

    def OnBluePrintTypeChanged(self,event):
        self.bluePrintType = self.bluePrintTypeCombo.GetValue()
        key=self.typeBluePrintDict[self.bluePrintType]
        self.bluePrintIndexCtrl.SetValue(key)

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
                    self.data = ['']*32
                else:
                    self.data = self.dataArray[0]
            self.data[14]='0'
            self.editState = '新建'
            self.ReCreateMiddlePanel(self.type,state=self.editState)
            self.ReCreateRightPanel()
        else:
            wx.MessageBox("请先结束当前编辑工作后，再进行新的编辑操作！", "信息提示")

    def OnBluePrintIDSearch(self, event):
        self.bluePrintIDSearch = self.bluePrintIDSearchCtrl.GetValue()
        self.ReSearch()

    def OnFrontDeltaSearch(self, event):
        self.frontDeltaSearch = self.frontDeltaSearchCtrl.GetValue()
        self.ReSearch()

    def OnMiddleDeltaSearch(self, event):
        self.middleDeltaSearch = self.middleDeltaSearchCtrl.GetValue()
        self.ReSearch()

    def OnRearDeltaSearch(self, event):
        self.rearDeltaSearch = self.rearDeltaSearchCtrl.GetValue()
        self.ReSearch()

    def OnProcedureSearch(self, event):
        self.procedureSearch = self.procedureSearchCtrl.GetValue()
        self.ReSearch()

    def ReSearch(self):
        _, dataList = GetAllBluPrintList(self.log, 1, self.type,state=self.state)
        self.dataArray = np.array(dataList)
        if self.bluePrintIDSearch != '':
            bluePrintList = []
            for item in self.dataArray:
                if self.bluePrintIDSearch in str(item[0]):
                    bluePrintList.append(item)
            self.dataArray = np.array(bluePrintList)
        if self.frontDeltaSearch != '':
            bluePrintList = []
            for item in self.dataArray:
                if self.frontDeltaSearch in str(item[1]):
                    bluePrintList.append(item)
            self.dataArray = np.array(bluePrintList)
        if self.middleDeltaSearch != '':
            bluePrintList = []
            for item in self.dataArray:
                if self.middleDeltaSearch in str(item[2]):
                    bluePrintList.append(item)
            self.dataArray = np.array(bluePrintList)
        if self.rearDeltaSearch != '':
            bluePrintList = []
            for item in self.dataArray:
                if self.rearDeltaSearch in str(item[3]):
                    bluePrintList.append(item)
            self.dataArray = np.array(bluePrintList)
        if self.procedureSearch != '':
            bluePrintList = []
            for item in self.dataArray:
                if self.procedureSearch in str(item[4]):
                    bluePrintList.append(item)
            self.dataArray = np.array(bluePrintList)
        self.bluePrintGrid.ReCreate()
        # self.bluePrintGrid.Render()

    def OnResetSearchItem(self, event):
        self.bluePrintIDSearch = ''
        self.bluePrintIDSearchCtrl.SetValue('')
        self.frontDeltaSearch = ''
        self.frontDeltaSearchCtrl.SetValue('')
        self.middleDeltaSearch = ''
        self.middleDeltaSearchCtrl.SetValue('')
        self.rearDeltaSearch = ''
        self.rearDeltaSearchCtrl.SetValue('')
        self.procedureSearch = ''
        self.procedureSearchCtrl.SetValue('')
        self.ReSearch()
class ConstructionManagementPanel(wx.Panel):
    def __init__(self, parent, master, log, type,state='在用'):
        wx.Panel.__init__(self, parent)
        self.master = master
        self.log = log
        self.type = type
        self.state = state
        self.busy = False
        self.editState = '查看'
        self.data = []
        self.processList=self.master.processList
        self.colWidthList = [80, 65, 65, 65, 50,100]
        self.colLabelValueList = ['图纸号', '构件宽度', '构件厚度', '重量','状态','']
        _, dataList = GetAllConstructionList(self.log, 1, self.type,state=self.state)
        self.dataArray = np.array(dataList)
        self.constructionIDSearch = ''
        self.widthSearch = ''
        self.thicknessSearch = ''
        self.weightSearch = ''
        hbox = wx.BoxSizer()
        self.leftPanel = wx.Panel(self, size=(490, -1))
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

    def OnCellLeftDClick(self, evt):
        if self.busy == False:
            col=evt.GetCol()
            if col == 5:
                    self.busy = True
                    row = evt.GetRow()
                    self.data = self.dataArray[row]
                    self.data[5] = "Stena 生产图纸 构件_页面_001"
                    filename = bluePrintDir + 'Stena 生产图纸 %s/' % self.data[6] + "Stena 生产图纸 构件_页面_001.pdf"
                    self.editState = '编辑'
                    self.ReCreateMiddlePanel(self.type, self.editState)
                    self.ReCreateRightPanel(filename)
            evt.Skip()
        else:
            wx.MessageBox("请先结束当前编辑工作后，再进行新的编辑操作！", "信息提示")


    def OnCellLeftClick(self, evt):
        if self.busy == False:
            row = evt.GetRow()
            self.constructionGrid.SetSelectionMode(wx.grid.Grid.GridSelectRows)
            self.constructionGrid.SelectRow(row)
            self.data = self.dataArray[row]
            self.editState = '查看'
            self.ReCreateMiddlePanel(self.type, self.editState)
            self.data[5] = "Stena 生产图纸 构件_页面_001"
            filename = bluePrintDir+'Stena 生产图纸 %s/'%self.data[6] + "Stena 生产图纸 构件_页面_001.pdf"
            self.ReCreateRightPanel(filename)
            evt.Skip()
        else:
            wx.MessageBox("请先结束当前编辑工作后，再进行新的编辑操作！", "信息提示")

    def ReCreateMiddlePanel(self, type, state='查看'):
        self.middlePanel.Freeze()
        self.middlePanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1,10))
        hhbox = wx.BoxSizer()
        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.middlePanel, label='图纸类别：', size=(60, -1)), 0, wx.TOP, 5)
        self.constructionTypeTXT = wx.TextCtrl(self.middlePanel, size=(70, 25), style=wx.TE_PROCESS_ENTER)
        self.constructionTypeTXT.SetValue("构件")
        self.constructionTypeTXT.Enable(False)
        self.constructionIndexCtrl=wx.TextCtrl(self.middlePanel,size=(60,-1))
        if state=='新建':
            self.constructionIndexCtrl.Enable(True)
            hhbox.Add(self.constructionTypeTXT, 1)
            self.constructionNoSpin = wx.SpinCtrl(self.middlePanel,size=(55,-1))
            self.constructionNoSpin.SetMin(1)
            self.constructionNoSpin.SetMax(9999)
            self.constructionNoSpin.SetValue(2)
            hhbox.Add(self.constructionIndexCtrl, 0)
            hhbox.Add(self.constructionNoSpin,0,wx.RIGHT,20)
        else:
            self.constructionIndexCtrl.Enable(False)
            self.constructionNoTXT = wx.TextCtrl(self.middlePanel,size=(45,-1),style=wx.TE_READONLY)
            self.constructionNoTXT.SetValue(self.data[0].split('.')[2])
            hhbox.Add(self.constructionTypeTXT, 1, wx.RIGHT, 10)
            hhbox.Add(self.constructionIndexCtrl, 0)
            hhbox.Add(self.constructionNoTXT, 0, wx.RIGHT,20)
        index = self.data[0].split('.')[0]+'.'+self.data[0].split('.')[1]
        self.constructionIndexCtrl.SetValue(index)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))
        hhbox = wx.BoxSizer()
        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.middlePanel,label="构件板材宽度:",size=(80,-1)),0,wx.TOP,5)
        self.constructionWidthTXT=wx.TextCtrl(self.middlePanel,size=(50,25))
        self.constructionWidthTXT.SetValue(self.data[1])
        hhbox.Add(self.constructionWidthTXT,1,wx.RIGHT,20)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))
        hhbox = wx.BoxSizer()
        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.middlePanel,label="构件板材厚度:",size=(80,-1)),0,wx.TOP,5)
        self.constructionThicknessTXT=wx.TextCtrl(self.middlePanel,size=(50,25))
        self.constructionThicknessTXT.SetValue(self.data[2])
        hhbox.Add(self.constructionThicknessTXT,1,wx.RIGHT,20)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))
        hhbox = wx.BoxSizer()
        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.middlePanel,label="构件板材重量:",size=(80,-1)),0,wx.TOP,5)
        self.constructionWeightTXT=wx.TextCtrl(self.middlePanel,size=(50,25))
        self.constructionWeightTXT.SetValue(self.data[3])
        hhbox.Add(self.constructionWeightTXT,1,wx.RIGHT,20)
        vbox.Add(hhbox,0,wx.EXPAND)

        if state != '查看':
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

        self.middlePanel.SetSizer(vbox)
        self.middlePanel.Refresh()
        self.middlePanel.Layout()
        self.middlePanel.Thaw()


    def CreateLeftPanel(self):
        vvbox = wx.BoxSizer(wx.VERTICAL)
        self.constructionGrid = ConstructionGrid(self.leftPanel, self, self.log)
        vvbox.Add(self.constructionGrid, 1, wx.EXPAND)
        hhbox = wx.BoxSizer()
        searchPanel = wx.Panel(self.leftPanel, size=(-1, 30), style=wx.BORDER_DOUBLE)
        vvbox.Add(searchPanel, 0, wx.EXPAND)
        self.searchResetBTN = wx.Button(searchPanel, label='Rest', size=(48, -1))
        self.searchResetBTN.Bind(wx.EVT_BUTTON, self.OnResetSearchItem)
        hhbox.Add(self.searchResetBTN, 0, wx.EXPAND)

        self.bluePrintIDSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[0], -1), style=wx.TE_PROCESS_ENTER)
        self.bluePrintIDSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnBluePrintIDSearch)
        hhbox.Add(self.bluePrintIDSearchCtrl, 0, wx.EXPAND)

        self.frontDeltaSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[1], -1),
                                                style=wx.TE_PROCESS_ENTER)
        self.frontDeltaSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnFrontDeltaSearch)
        hhbox.Add(self.frontDeltaSearchCtrl, 0, wx.EXPAND)

        self.middleDeltaSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[2], -1),
                                                 style=wx.TE_PROCESS_ENTER)
        self.middleDeltaSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnMiddleDeltaSearch)
        hhbox.Add(self.middleDeltaSearchCtrl, 0, wx.EXPAND)

        self.rearDeltaSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[3], -1),
                                               style=wx.TE_PROCESS_ENTER)
        self.rearDeltaSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnRearDeltaSearch)
        hhbox.Add(self.rearDeltaSearchCtrl, 0, wx.EXPAND)

        self.procedureSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[4], -1),
                                                       style=wx.TE_PROCESS_ENTER)
        self.procedureSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnProcedureSearch)
        hhbox.Add(self.procedureSearchCtrl, 0, wx.EXPAND)

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

    def ReCreateRightPanel(self,filename=""):
        self.rightPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.bluePrintShowPanel = BluePrintShowPanel(self.rightPanel, self.log,filename)
        vbox.Add(self.bluePrintShowPanel, 1, wx.EXPAND)
        self.rightPanel.SetSizer(vbox)
        self.rightPanel.Layout()

    def OnEditOkBTN(self,event):
        if self.editState == '新建':
            dlg = wx.TextEntryDialog(
                    self, '请输入图纸编号,目前显示的是系统为您建议的图纸号：',
                    '信息提示', '')
            string = "%s.%04d"%(self.constructionIndexCtrl.GetValue(),self.constructionNoSpin.GetValue())
            dlg.SetValue(string)
            if dlg.ShowModal() == wx.ID_OK:
                self.CombineData(dlg.GetValue())
                SaveConstructionInDB(self.log, 1, self.data)
                self.busy = False
                self.middlePanel.DestroyChildren()
                self.rightPanel.DestroyChildren()
                _, dataList = GetAllConstructionList(self.log, 1, self.type, state=self.state)
                self.dataArray = np.array(dataList)
                self.constructionGrid.ReCreate()
            dlg.Destroy()
        else:
            self.CombineData(self.data[0])
            # UpdateBluePrintInDB(self.log, 1, self.data)
            self.busy = False
            self.middlePanel.DestroyChildren()
            self.rightPanel.DestroyChildren()
            _, dataList = GetAllConstructionList(self.log, 1, self.type, state=self.state)
            self.dataArray = np.array(dataList)
            self.constructionGrid.ReCreate()

    def CombineData(self,constructionNo):
        """`图纸号`,`宽度`,`厚度`,`重量`,`图纸状态`,`图纸文件名`,`图纸大类`"""
        temp = constructionNo.split('.')
        self.data[0] = temp[0]+'.'+temp[1]+'.'+'%04d'%int(temp[2])
        self.data[1] = self.constructionWidthTXT.GetValue()
        self.data[2] = self.constructionThicknessTXT.GetValue()
        self.data[3] = self.constructionWeightTXT.GetValue()
        self.data[4] = '在用'
        self.data[5] = "Stena 生产图纸 构件_页面_179.pdf"
        self.data[6] = "构件"

    def OnCancel(self,event):
        self.busy = False
        self.middlePanel.DestroyChildren()
        self.rightPanel.DestroyChildren()

    def OnBluePrintTypeChanged(self,event):
        self.bluePrintType = self.bluePrintTypeCombo.GetValue()
        key=self.typeBluePrintDict[self.bluePrintType]
        self.bluePrintIndexCtrl.SetValue(key)

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
                    self.data = ['']*7
                else:
                    self.data = self.dataArray[0]
            self.editState = '新建'
            self.ReCreateMiddlePanel(self.type,state=self.editState)
            self.ReCreateRightPanel()
        else:
            wx.MessageBox("请先结束当前编辑工作后，再进行新的编辑操作！", "信息提示")

    def OnBluePrintIDSearch(self, event):
        self.bluePrintIDSearch = self.bluePrintIDSearchCtrl.GetValue()
        self.ReSearch()

    def OnFrontDeltaSearch(self, event):
        self.frontDeltaSearch = self.frontDeltaSearchCtrl.GetValue()
        self.ReSearch()

    def OnMiddleDeltaSearch(self, event):
        self.middleDeltaSearch = self.middleDeltaSearchCtrl.GetValue()
        self.ReSearch()

    def OnRearDeltaSearch(self, event):
        self.rearDeltaSearch = self.rearDeltaSearchCtrl.GetValue()
        self.ReSearch()

    def OnProcedureSearch(self, event):
        self.procedureSearch = self.procedureSearchCtrl.GetValue()
        self.ReSearch()

    def ReSearch(self):
        _, dataList = GetAllBluPrintList(self.log, 1, self.type,state=self.state)
        self.dataArray = np.array(dataList)
        if self.bluePrintIDSearch != '':
            bluePrintList = []
            for item in self.dataArray:
                if self.bluePrintIDSearch in str(item[0]):
                    bluePrintList.append(item)
            self.dataArray = np.array(bluePrintList)
        if self.frontDeltaSearch != '':
            bluePrintList = []
            for item in self.dataArray:
                if self.frontDeltaSearch in str(item[1]):
                    bluePrintList.append(item)
            self.dataArray = np.array(bluePrintList)
        if self.middleDeltaSearch != '':
            bluePrintList = []
            for item in self.dataArray:
                if self.middleDeltaSearch in str(item[2]):
                    bluePrintList.append(item)
            self.dataArray = np.array(bluePrintList)
        if self.rearDeltaSearch != '':
            bluePrintList = []
            for item in self.dataArray:
                if self.rearDeltaSearch in str(item[3]):
                    bluePrintList.append(item)
            self.dataArray = np.array(bluePrintList)
        if self.procedureSearch != '':
            bluePrintList = []
            for item in self.dataArray:
                if self.procedureSearch in str(item[4]):
                    bluePrintList.append(item)
            self.dataArray = np.array(bluePrintList)
        self.bluePrintGrid.ReCreate()
        # self.bluePrintGrid.Render()

    def OnResetSearchItem(self, event):
        self.bluePrintIDSearch = ''
        self.bluePrintIDSearchCtrl.SetValue('')
        self.frontDeltaSearch = ''
        self.frontDeltaSearchCtrl.SetValue('')
        self.middleDeltaSearch = ''
        self.middleDeltaSearchCtrl.SetValue('')
        self.rearDeltaSearch = ''
        self.rearDeltaSearchCtrl.SetValue('')
        self.procedureSearch = ''
        self.procedureSearchCtrl.SetValue('')
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
        self.colorCoatManagementPanel = ConstructionManagementPanel(self.notebook,self,self.log,'构件')
        self.notebook.AddPage(self.colorCoatManagementPanel, "构件图纸管理")
        self.stainlessSheetManagmentPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.stainlessSheetManagmentPanel, "检修门图纸管理")
        self.sparyBoardManagementPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.sparyBoardManagementPanel, "检修口图纸管理")
        self.notebook.SetSelection(0)
