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
        print("data=",self.master.dataArray)
        for i, order in enumerate(self.master.dataArray):
            self.SetRowSize(i, 25)
            for j, item in enumerate(order):
                # self.SetCellBackgroundColour(i,j,wx.Colour(250, 250, 250))
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)
                self.SetCellValue(i, j, str(item))

        # self.SetCellValue(2, 2, "Yet another cell")
        # self.SetCellValue(3, 3, "This cell is read-only")
        # self.SetCellFont(0, 0, wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        # self.SetCellTextColour(1, 1, wx.RED)
        # self.SetCellBackgroundColour(2, 2, wx.CYAN)
        # self.SetReadOnly(3, 3, True)

        # self.SetCellEditor(5, 0, gridlib.GridCellNumberEditor(1,1000))
        # self.SetCellValue(5, 0, "123")
        # self.SetCellEditor(6, 0, gridlib.GridCellFloatEditor())
        # self.SetCellValue(6, 0, "123.34")
        # self.SetCellEditor(7, 0, gridlib.GridCellNumberEditor())
        #
        # self.SetCellValue(6, 3, "You can veto editing this cell")

        # attribute objects let you keep a set of formatting values
        # in one spot, and reuse them if needed
        # attr = gridlib.GridCellAttr()
        # attr.SetTextColour(wx.BLACK)
        # attr.SetBackgroundColour(wx.RED)
        # attr.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        #
        # # you can set cell attributes for the whole row (or column)
        # self.SetRowAttr(5, attr)

        # self.SetDefaultCellOverflow(False)
        # r = gridlib.GridCellAutoWrapStringRenderer()
        # self.SetCellRenderer(9, 1, r)

        # overflow cells
        # self.SetCellValue( 9, 1, "This default cell will overflow into neighboring cells, but not if you turn overflow off.");
        # self.SetCellSize(11, 1, 3, 3);
        # self.SetCellAlignment(11, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE);
        # self.SetCellValue(11, 1, "This cell is set to span 3 rows and 3 columns");

        # editor = gridlib.GridCellTextEditor()
        # editor.SetParameters('10')
        # self.SetCellEditor(0, 4, editor)
        # self.SetCellValue(0, 4, "Limited text")
        #
        # renderer = gridlib.GridCellAutoWrapStringRenderer()
        # self.SetCellRenderer(15,0, renderer)
        # self.SetCellValue(15,0, "The text in this cell will be rendered with word-wrapping")

        # test all the events
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
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

        for i, order in enumerate(self.master.boardArray):
            self.SetRowSize(i, 25)
            for j, item in enumerate(order):
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)
                self.SetCellValue(i, j, str(item))

    def OnCellLeftClick(self, evt):
        self.log.write("OnCellLeftClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

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

class ColorPalettePanel(scrolled.ScrolledPanel):
    def __init__(self, parent, log):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        self.log = log
        # self.ReCreate()

    def ReCreate(self):
        self.Freeze()
        self.DestroyChildren()
        _, colorList = GetAllColor(self.log, 1)
        wsizer = wx.WrapSizer(orient=wx.VERTICAL)
        for color in colorList:
            btn = wx.Button(self, label=color[0], size=(70,30),name=str(color[1:4]))
            btn.SetBackgroundColour(wx.Colour(color[1],color[2],color[3]))
            btn.SetForegroundColour(wx.Colour(255-color[1],255-color[2],255-color[3]))
            btn.SetToolTip(color[4]+'('+color[5]+')')
            wsizer.Add(btn, 0)
        self.SetSizer(wsizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        self.Thaw()

class PicShowPanel(wx.Panel):
    def __init__(self, parent,boardType,size):
        wx.Panel.__init__(self, parent, size=size, style=wx.BORDER_THEME)
        self.boardType = boardType
        self.SetAutoLayout(True)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def OnResize(self, evt):
        self.Refresh()

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush("WHITE"))
        dc.Clear()
        x,y = self.GetClientSize()
        bmp = wx.Image('bitmaps/%s.jpg'%self.boardType).Scale(width=x, height=y,
                                                  quality=wx.IMAGE_QUALITY_BOX_AVERAGE).ConvertToBitmap()
        dc.DrawBitmap(bmp, 0, 0, True)

# class BoardGrid(OrderGrid):
#     def __init__(self, parent, master, log):
#         super(BoardGrid, self).__init__(parent, master, log)
#         self.Render()
#
#     def Render(self):
#         for i in range(self.GetNumberRows()):
#             self.SetCellBackgroundColour(i, 6, wx.Colour(255, 255, 255))#清第6列（RAL色卡列）
#             self.SetCellBackgroundColour(i, 8, wx.Colour(255, 255, 255))#清第8列（编辑按钮列）
#             self.SetCellBackgroundColour(i, 9, wx.Colour(255, 255, 255))#清第9列（编辑按钮列）
#
#         for i, item in enumerate(self.master.boardArray):
#             RalID = item[6]
#             _, color = GetRGBWithRalID(self.log, 1, RalID)
#             self.SetCellBackgroundColour(i, 6, wx.Colour(color[0], color[1], color[2]))
#             self.SetCellTextColour(i, 6,wx.Colour( 255-color[0], 255-color[1], 255-color[2]))
#             self.SetCellAlignment(i, 7, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)
#             self.SetCellValue(i, 7, color[3])
#             if item[7]=='在用':
#                 self.SetCellBackgroundColour(i, 8, wx.Colour(240,240,240))
#             else:
#                 self.SetCellBackgroundColour(i, 8, wx.RED)
#             self.SetCellAlignment(i, 8, wx.ALIGN_CENTER, wx.ALIGN_CENTRE_VERTICAL)
#             self.SetCellValue(i, 8, item[7])
#             self.SetCellBackgroundColour(i, 9, wx.Colour(210,210,210))
#             self.SetCellAlignment(i, 9, wx.ALIGN_CENTER, wx.ALIGN_CENTRE_VERTICAL)
#             self.SetCellValue(i, 9, '编辑')

class SpecificBluePrintManagementPanel(wx.Panel):
    def __init__(self, parent, master, log, type,state='在用'):
        wx.Panel.__init__(self, parent)
        self.master = master
        self.log = log
        self.type = type
        self.state = state
        self.colWidthList = [50, 102, 101, 100, 100, 170]
        self.colLabelValueList = ['图纸号', '中板长增量', '中板宽增量', '背板长增量', '背板宽增量', '所需工序']
        _, dataList = GetAllBluPrintList(self.log, 1, self.type,state=self.state)
        self.dataArray = np.array(dataList)
        self.orderIDSearch = ''
        self.boardFormatSearch = ''
        self.boardMaterialSearch = ''
        self.boardDensitySearch = ''
        self.boardSupportComponentSearch=''
        self.boardSupportWidthSearch=''
        self.boardRALIDSearch = ''
        self.editBoardPanelOccupied = False
        hbox = wx.BoxSizer()
        self.leftPanel = wx.Panel(self, size=(650, -1))
        hbox.Add(self.leftPanel, 0, wx.EXPAND)
        self.middlePanel = wx.Panel(self, size=(260,-1), style=wx.BORDER_THEME)
        hbox.Add(self.middlePanel, 0, wx.EXPAND)
        self.colorPalettePanel = ColorPalettePanel(self, self.log)
        hbox.Add(self.colorPalettePanel, 1, wx.EXPAND)
        self.SetSizer(hbox)
        vvbox = wx.BoxSizer(wx.VERTICAL)
        self.bluePrintGrid = BluePrintGrid(self.leftPanel, self, self.log)
        vvbox.Add(self.boardGrid, 1, wx.EXPAND)
        hhbox = wx.BoxSizer()
        searchPanel = wx.Panel(self.leftPanel, size=(-1, 30), style=wx.BORDER_DOUBLE)
        vvbox.Add(searchPanel, 0, wx.EXPAND)
        hhbox = wx.BoxSizer()
        self.searchResetBTN = wx.Button(searchPanel, label='Rest', size=(48, -1))
        self.searchResetBTN.Bind(wx.EVT_BUTTON, self.OnResetSearchItem)
        hhbox.Add(self.searchResetBTN, 0, wx.EXPAND)

        self.boardSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[0], -1), style=wx.TE_PROCESS_ENTER)
        self.boardSearchCtrl.Enable(False)
        hhbox.Add(self.boardSearchCtrl, 0, wx.EXPAND)

        self.boardFormatSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[1], -1),
                                                 style=wx.TE_PROCESS_ENTER)
        self.boardFormatSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnBoardFormatSearch)
        hhbox.Add(self.boardFormatSearchCtrl, 0, wx.EXPAND)

        self.boardMaterialSearchCtrl = wx.ComboBox(searchPanel, choices=['A1', 'B0', 'B1', 'B5', 'B7'],
                                                   size=(self.colWidthList[2], -1))
        self.boardMaterialSearchCtrl.Bind(wx.EVT_COMBOBOX, self.OnBoardMaterailSearch)
        hhbox.Add(self.boardMaterialSearchCtrl, 0, wx.EXPAND)

        self.boardDensitySearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[3], -1),
                                                 style=wx.TE_PROCESS_ENTER)
        self.boardDensitySearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnBoardDensitySearch)
        hhbox.Add(self.boardDensitySearchCtrl, 0, wx.EXPAND)

        self.boardSupportComponentSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[4], -1),
                                                 style=wx.TE_PROCESS_ENTER)
        self.boardSupportComponentSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnBoardSupportComponentSearch)
        hhbox.Add(self.boardSupportComponentSearchCtrl, 0, wx.EXPAND)

        self.boardSupportWidthSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[5], -1),
                                                 style=wx.TE_PROCESS_ENTER)
        self.boardSupportWidthSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnBoardSupportWidthSearch)
        hhbox.Add(self.boardSupportWidthSearchCtrl, 0, wx.EXPAND)

        self.boardRALIDSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[6], -1), style=wx.TE_PROCESS_ENTER)
        self.boardRALIDSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnBoardRALIDSearch)
        hhbox.Add(self.boardRALIDSearchCtrl, 0, wx.EXPAND)

        self.newBoardBTN = wx.Button(searchPanel, label='新建%s基材' % self.boardType)
        self.newBoardBTN.SetBackgroundColour(wx.Colour(22, 211, 111))
        self.newBoardBTN.Bind(wx.EVT_BUTTON, self.OnCreateNewBoard)
        hhbox.Add(self.newBoardBTN, 1, wx.EXPAND | wx.RIGHT | wx.LEFT, 1)

        self.changeStateBTN = wx.Button(searchPanel, size=(15,-1))
        self.changeStateBTN.Bind(wx.EVT_BUTTON, self.OnChangeState)
        if self.state == '在用':
            self.changeStateBTN.SetBackgroundColour(wx.GREEN)
        else:
            self.changeStateBTN.SetBackgroundColour(wx.RED)
        hhbox.Add(self.changeStateBTN,0,wx.EXPAND)
        # self.newBoardBTN.SetBackgroundColour(wx.Colour(22, 211, 111))
        # self.newBoardBTN.Bind(wx.EVT_BUTTON, self.OnCreateNewBoard)
        # hhbox.Add(self.newBoardBTN, 1, wx.EXPAND | wx.RIGHT | wx.LEFT, 1)
        searchPanel.SetSizer(hhbox)
        self.leftPanel.SetSizer(vvbox)

        vvbox = wx.BoxSizer(wx.VERTICAL)
        self.picPanel = PicShowPanel(self.middlePanel, self.boardType,size=(300,200))
        vvbox.Add(self.picPanel,1,wx.EXPAND)
        self.editBoardPanel=wx.Panel(self.middlePanel,size=(300,290))
        vvbox.Add(self.editBoardPanel, 0, wx.EXPAND)
        self.middlePanel.SetSizer(vvbox)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)

    def OnCellLeftDClick(self, evt):
        row = evt.GetRow()
        col = evt.GetCol()
        if col == 9:
            if self.editBoardPanelOccupied == False:
                self.editBoardPanelOccupied=True
                self.ReCreateEditBoardPanel(self.boardType,state='编辑')
            else:
                wx.MessageBox("请先结束当前编辑工作后，再进行新的编辑操作！","信息提示")
        # evt.Skip()

    def ReCreateEditBoardPanel(self,type, state='新建'):
        self.editBoardPanel.Freeze()
        self.editBoardPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        frame = wx.StaticBox(self.editBoardPanel, label="%s基材"%state,size=(200,200))
        vbox.Add(frame,1,wx.EXPAND|wx.ALL,5)
        self.editBoardPanel.SetSizer(vbox)
        vvbox = wx.BoxSizer(wx.VERTICAL)
        vvbox.Add((-1,20))
        hhbox = wx.BoxSizer()
        label = wx.StaticText(frame, label="基材类型：", size=(70,-1))
        self.editBoardTypeCombo = wx.ComboBox(frame,choices=["PVC",'不锈钢'],size=(130,-1))
        self.editBoardTypeCombo.SetValue(self.boardType)
        self.editBoardTypeCombo.Enable(False)
        hhbox.Add((20,-1))
        hhbox.Add(label,0,wx.TOP,5)
        hhbox.Add(self.editBoardTypeCombo,1,wx.RIGHT,5)
        vvbox.Add(hhbox)

        vvbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        label = wx.StaticText(frame, label="基材厚度：", size=(70,-1))
        self.editBoardFormatTXT = wx.TextCtrl(frame,size=(130,-1))
        hhbox.Add((20,-1))
        hhbox.Add(label,0,wx.TOP,5)
        hhbox.Add(self.editBoardFormatTXT,1,wx.RIGHT,5)
        vvbox.Add(hhbox)

        vvbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        label = wx.StaticText(frame, label="基材规格：", size=(70,-1))
        self.editBoardMaterialTXT = wx.TextCtrl(frame,size=(130,-1))
        hhbox.Add((20,-1))
        hhbox.Add(label,0,wx.TOP,5)
        hhbox.Add(self.editBoardMaterialTXT,1,wx.RIGHT,5)
        vvbox.Add(hhbox)

        vvbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        label = wx.StaticText(frame, label="单位重量：", size=(70,-1))
        self.editBoardDensityTXT = wx.TextCtrl(frame,size=(130,-1))
        hhbox.Add((20,-1))
        hhbox.Add(label,0,wx.TOP,5)
        hhbox.Add(self.editBoardDensityTXT,1,wx.RIGHT,5)
        vvbox.Add(hhbox)

        vvbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        label = wx.StaticText(frame, label="支持组件：", size=(60,-1))
        self.editBoardSupportWallCHeck = wx.CheckBox(frame,label="墙板")
        self.editBoardSupportCeilingCHeck = wx.CheckBox(frame,label="天花板")
        self.editBoardSupportConnecterCHeck = wx.CheckBox(frame,label="构件")
        hhbox.Add((20,-1))
        hhbox.Add(label,0,wx.TOP,5)
        hhbox.Add(self.editBoardSupportWallCHeck, 1, wx.TOP,5)
        hhbox.Add(self.editBoardSupportCeilingCHeck, 1, wx.TOP,5)
        hhbox.Add(self.editBoardSupportConnecterCHeck, 1, wx.TOP,5)
        vvbox.Add(hhbox)

        vvbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        label = wx.StaticText(frame, label="支持宽度：", size=(70,-1))
        self.editBoardSupportWidthTXT = wx.TextCtrl(frame, size=(130,-1))
        hhbox.Add((20,-1))
        hhbox.Add(label,0,wx.TOP,5)
        hhbox.Add(self.editBoardSupportWidthTXT,1,wx.RIGHT,5)
        vvbox.Add(hhbox)

        vvbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        label = wx.StaticText(frame, label="颜色：", size=(40,-1))
        self.editBoardSelectColorBTN = wx.Button(frame, size=(80,26))
        self.editBoardSelectColorBTN.Bind(wx.EVT_BUTTON, self.OnSelectColorBTN)
        hhbox.Add((20,-1))
        hhbox.Add(label,0,wx.TOP,5)
        hhbox.Add(self.editBoardSelectColorBTN,0,wx.RIGHT,5)
        self.editBoardStateCombo = wx.ComboBox(frame,choices=["在用","停用"],size=(75,25))
        self.editBoardStateCombo.SetValue("在用")
        if state=='新建':
            self.editBoardStateCombo.Enable(False)
        hhbox.Add(self.editBoardStateCombo,0,wx.RIGHT,5)
        vvbox.Add(hhbox)
        vvbox.Add(wx.StaticLine(frame,size=(100,-1), style=wx.HORIZONTAL), 0,wx.EXPAND|wx.TOP|wx.BOTTOM,5)

        self.editBoardOkButton = wx.Button(frame, label="确定", size=(100,30))
        self.editBoardOkButton.Bind(wx.EVT_BUTTON, self.OnEditBoardOkButton)
        self.editBoardCancelButton = wx.Button(frame, label="取消", size=(100,30))
        self.editBoardCancelButton.Bind(wx.EVT_BUTTON, self.OnEditBoardCancelButton)
        hhbox = wx.BoxSizer()
        hhbox.Add((10,-1))
        hhbox.Add(self.editBoardOkButton)
        hhbox.Add((20,-1))
        hhbox.Add(self.editBoardCancelButton)
        vvbox.Add((-1,3))
        vvbox.Add(hhbox,0,wx.EXPAND)

        frame.SetSizer(vvbox)
        self.editBoardPanel.Layout()
        # self.colorPalettePanel.ReCreate()
        self.editBoardPanel.Thaw()

    def OnSelectColorBTN(self, event):
        self.colorPalettePanel.ReCreate()
        self.colorPalettePanel.Bind(wx.EVT_BUTTON, self.OnColorBTN)

    def OnColorBTN(self, event):
        obj = event.GetEventObject()
        ralCode = obj.GetLabel()
        color = eval(obj.GetName())
        self.editBoardSelectColorBTN.SetBackgroundColour(wx.Colour(color))
        self.editBoardSelectColorBTN.SetForegroundColour(wx.Colour(255-color[0],255-color[1],255-color[2]))
        self.editBoardSelectColorBTN.SetLabel(ralCode)


    def OnEditBoardCancelButton(self,event):
        dlg = wx.MessageDialog(self,"取消操作将导致之前的输入工作全部作废，您是否确认？",'信息提示',style=wx.YES_NO)
        if dlg.ShowModal() == wx.ID_YES:
            self.editBoardPanel.DestroyChildren()
            self.colorPalettePanel.DestroyChildren()
            self.editBoardPanelOccupied = False
        dlg.Destroy()

    def OnEditBoardOkButton(self,event):
        self.editBoardPanel.DestroyChildren()
        self.colorPalettePanel.DestroyChildren()
        self.editBoardPanelOccupied = False

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
        _, data = GetAllBoardList(self.log, 1, self.boardType,state=self.state)
        self.boardArray = np.array(data)
        self.boardGrid.ReCreate()
        self.boardGrid.Render()

    def OnCreateNewBoard(self,event):
        if self.editBoardPanelOccupied == False:
            self.editBoardPanelOccupied = True
            self.ReCreateEditBoardPanel(self.boardType)
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

    def OnBoardDensitySearch(self, event):
        self.boardDensitySearch = self.boardDensitySearchCtrl.GetValue()
        self.ReSearch()

    def OnBoardFormatSearch(self, event):
        self.boardFormatSearch = self.boardFormatSearchCtrl.GetValue()
        self.ReSearch()

    def OnBoardMaterailSearch(self, event):
        self.boardMaterialSearch = self.boardMaterialSearchCtrl.GetValue()
        self.ReSearch()

    def OnBoardRALIDSearch(self, event):
        self.boardRALIDSearch = self.boardRALIDSearchCtrl.GetValue()
        self.ReSearch()

    def OnBoardSupportComponentSearch(self,event):
        self.boardSupportComponentSearch = self.boardSupportComponentSearchCtrl.GetValue()
        self.ReSearch()

    def OnBoardSupportWidthSearch(self,event):
        self.boardSupportWidthSearch = self.boardSupportWidthSearchCtrl.GetValue()
        self.ReSearch()

    def ReSearch(self):
        _, boardList = GetAllBoardList(self.log, 1, self.boardType, state=self.state)
        self.boardArray = np.array(boardList)
        if self.boardFormatSearch != '':
            boardList = []
            for board in self.boardArray:
                if self.boardFormatSearch in str(board[1]):
                    boardList.append(board)
            self.boardArray = np.array(boardList)
        if self.boardMaterialSearch != '':
            boardList = []
            for board in self.boardArray:
                if self.boardMaterialSearch in board[2]:
                    boardList.append(board)
            self.boardArray = np.array(boardList)
        if self.boardDensitySearch != '':
            boardList = []
            for board in self.boardArray:
                if self.boardDensitySearch in str(board[3]):
                    boardList.append(board)
            self.boardArray = np.array(boardList)
        if self.boardSupportComponentSearch != '':
            boardList = []
            for board in self.boardArray:
                if self.boardSupportComponentSearch in str(board[4]):
                    boardList.append(board)
            self.boardArray = np.array(boardList)
        if self.boardSupportWidthSearch != '':
            boardList = []
            for board in self.boardArray:
                if self.boardSupportWidthSearch == str(board[5]):
                    boardList.append(board)
            self.boardArray = np.array(boardList)
        if self.boardRALIDSearch != '':
            boardList = []
            for board in self.boardArray:
                if self.boardRALIDSearch in str(board[6]):
                    boardList.append(board)
            self.boardArray = np.array(boardList)
        self.boardGrid.ReCreate()
        self.boardGrid.Render()

    def OnResetSearchItem(self, event):
        self.boardFormatSearch = ''
        self.boardFormatSearchCtrl.SetValue('')
        self.boardMaterialSearch = ''
        self.boardMaterialSearchCtrl.SetValue('')
        self.boardDensitySearch = ''
        self.boardDensitySearchCtrl.SetValue('')
        self.boardRALIDSearch = ''
        self.boardSupportComponentSearchCtrl.SetValue('')
        self.boardSupportComponentSearch = ''
        self.boardSupportWidthSearchCtrl.SetValue('')
        self.boardSupportWidthSearch = ''
        self.boardRALIDSearchCtrl.SetValue('')
        self.ReSearch()


class BluePrintManagementPanel(wx.Panel):
    def __init__(self, parent, master, log):
        wx.Panel.__init__(self, parent, -1)
        self.master = master
        self.log = log
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
