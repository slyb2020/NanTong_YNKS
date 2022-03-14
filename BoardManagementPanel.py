import wx
import wx.grid as gridlib
from DBOperation import GetAllBoardList,GetRGBWithRalID
from OrderManagementPanel import OrderGrid
import numpy as np
import images

class BoardGrid(OrderGrid):
    def __init__(self, parent, master, log):
        super(BoardGrid, self).__init__(parent, master, log)
        self.Render()

    def Render(self):
        for i in range(self.GetNumberRows()):
            self.SetCellBackgroundColour(i, 4, wx.Colour(255,255,255))
        for i, item in enumerate(self.master.boardArray):
            RalID = item[3]
            _, color = GetRGBWithRalID(self.log, 1, RalID)
            self.SetCellBackgroundColour(i,4,wx.Colour(color[0],color[1],color[2]))
            self.SetCellAlignment(i,5,wx.ALIGN_CENTRE,wx.ALIGN_CENTRE_VERTICAL)
            self.SetCellValue(i,5,color[3])


class SpecificBoardManagementPanel(wx.Panel):
    def __init__(self, parent, master, log, boardType):
        wx.Panel.__init__(self, parent)
        self.master = master
        self.log = log
        self.boardType = boardType
        self.colWidthList = [70, 70,70, 70,80,70]
        self.colLabelValueList = ['板材', '规格', '材质', 'RAL色号','RAL色卡','颜色名']
        _, orderList = GetAllBoardList(self.log, 1, self.boardType)
        self.boardArray = np.array(orderList)
        self.orderIDSearch=''
        self.boardFormatSearch=''
        self.boardMaterialSearch= ''
        self.boardRALIDSearch=''
        hbox = wx.BoxSizer()
        self.leftPanel = wx.Panel(self, size=(500, -1))
        hbox.Add(self.leftPanel, 0, wx.EXPAND)
        self.rightPanel = wx.Panel(self, style=wx.BORDER_THEME)
        hbox.Add(self.rightPanel, 1, wx.EXPAND)
        self.SetSizer(hbox)
        vvbox = wx.BoxSizer(wx.VERTICAL)
        self.boardGrid = BoardGrid(self.leftPanel, self, self.log)
        vvbox.Add(self.boardGrid, 1, wx.EXPAND)
        hhbox = wx.BoxSizer()
        searchPanel = wx.Panel(self.leftPanel, size=(-1, 30), style=wx.BORDER_DOUBLE)
        vvbox.Add(searchPanel, 0, wx.EXPAND)
        hhbox = wx.BoxSizer()
        self.searchResetBTN = wx.Button(searchPanel, label='Rest', size=(48, -1))
        self.searchResetBTN.Bind(wx.EVT_BUTTON, self.OnResetSearchItem)
        hhbox.Add(self.searchResetBTN, 0, wx.EXPAND)

        self.boardSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[0], -1), style=wx.TE_PROCESS_ENTER )
        self.boardSearchCtrl.Enable(False)
        # self.boardSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnBoardSearch)
        hhbox.Add(self.boardSearchCtrl, 0, wx.EXPAND)

        self.boardFormatSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[1], -1), style=wx.TE_PROCESS_ENTER )
        self.boardFormatSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnBoardFormatSearch)
        hhbox.Add(self.boardFormatSearchCtrl, 0, wx.EXPAND)

        self.boardMaterialSearchCtrl = wx.ComboBox(searchPanel, choices=['A1', 'B0', 'B1', 'B5', 'B7'],
                                                   size=(self.colWidthList[2], -1))
        self.boardMaterialSearchCtrl.Bind(wx.EVT_COMBOBOX, self.OnBoardMaterailSearch)
        hhbox.Add(self.boardMaterialSearchCtrl, 0, wx.EXPAND)

        self.boardRALIDSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[3], -1), style=wx.TE_PROCESS_ENTER )
        self.boardRALIDSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnBoardRALIDSearch)
        hhbox.Add(self.boardRALIDSearchCtrl, 0, wx.EXPAND)

        self.newBoardBTN = wx.Button(searchPanel,label='新建%s板材'%self.boardType)
        self.newBoardBTN.SetBackgroundColour(wx.Colour(22,211,111))
        hhbox.Add(self.newBoardBTN,1,wx.EXPAND|wx.RIGHT|wx.LEFT,1)
        # self.deliverDateSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[4], -1))
        # hhbox.Add(self.deliverDateSearchCtrl, 0, wx.EXPAND)
        # self.orderDateSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[5], -1))
        # hhbox.Add(self.orderDateSearchCtrl, 0, wx.EXPAND)
        # self.operatorSearchCtrl = wx.ComboBox(searchPanel, choices=["1803089"], size=(self.colWidthList[6], -1))
        # self.operatorSearchCtrl.Bind(wx.EVT_COMBOBOX, self.OnOperatorSearch)
        # hhbox.Add(self.operatorSearchCtrl, 0, wx.EXPAND)
        # self.orderStateSearchCtrl = wx.ComboBox(searchPanel, choices=["接单","排产","下料","加工","打包","发货"], size=(self.colWidthList[7], -1))
        # self.orderStateSearchCtrl.Bind(wx.EVT_COMBOBOX, self.OnOrderStateSearch)
        # hhbox.Add(self.orderStateSearchCtrl, 0, wx.EXPAND)

        # for i,width in enumerate(self.colWidthList):
        #     if i==6:
        #         width+=55
        #     searchTXT = wx.TextCtrl(searchPanel, size=(width,-1))
        #     hhbox.Add(searchTXT, 0, wx.EXPAND)
        searchPanel.SetSizer(hhbox)
        # self.filter = wx.SearchCtrl(self.leftPanel, size=(200,-1), style=wx.TE_PROCESS_ENTER)
        # self.filter.ShowCancelButton(True)
        # hhbox.Add((1,-1))
        # hhbox.Add(self.filter,0)
        # vvbox.Add(hhbox,0,wx.EXPAND)
        self.leftPanel.SetSizer(vvbox)
        # self.filter.Bind(wx.EVT_TEXT, self.RecreateTree)
        # self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN,
        #                  lambda e: self.filter.SetValue(''))
        # self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)

    def OnBoardFormatSearch(self, event):
        self.boardFormatSearch = self.boardFormatSearchCtrl.GetValue()
        self.ReSearch()

    def OnBoardMaterailSearch(self, event):
        self.boardMaterialSearch=self.boardMaterialSearchCtrl.GetValue()
        self.ReSearch()

    def OnBoardRALIDSearch(self, event):
        self.boardRALIDSearch = self.boardRALIDSearchCtrl.GetValue()
        self.ReSearch()

    # def OnBoardSearch(self, event):
    #     self.orderIDSearch = self.orderIDSearchCtrl.GetValue()
    #     self.ReSearch()


    def ReSearch(self):
        _, boardList = GetAllBoardList(self.log, 1, self.boardType)
        self.boardArray = np.array(boardList)
        if self.boardMaterialSearch != '':
            boardList = []
            for board in self.boardArray:
                if self.boardMaterialSearch in board[2]:
                    boardList.append(board)
            self.boardArray = np.array(boardList)
        # if self.orderIDSearch != '':
        #     orderList = []
        #     for order in self.orderArray:
        #         if str(order[0]) == self.orderIDSearch:
        #             orderList.append(order)
        #     self.orderArray = np.array(orderList)
        if self.boardFormatSearch != '':
            boardList = []
            for board in self.boardArray:
                if self.boardFormatSearch in str(board[1]):
                    boardList.append(board)
            self.boardArray = np.array(boardList)
        if self.boardRALIDSearch != '':
            print(self.boardRALIDSearch)
            boardList = []
            for board in self.boardArray:
                if self.boardRALIDSearch in str(board[3]):
                    boardList.append(board)
            self.boardArray = np.array(boardList)
        self.boardGrid.ReCreate()
        self.boardGrid.Render()


    def OnResetSearchItem(self,event):
        self.boardFormatSearch=''
        self.boardFormatSearchCtrl.SetValue('')
        self.boardMaterialSearch= ''
        self.boardMaterialSearchCtrl.SetValue('')
        self.boardRALIDSearch=''
        self.boardRALIDSearchCtrl.SetValue('')
        self.ReSearch()



class BoardManagementPanel(wx.Panel):
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
        self.pvcManagementPanel = SpecificBoardManagementPanel(self.notebook, self, self.log, 'PVC')
        self.notebook.AddPage(self.pvcManagementPanel,"PVC板材管理")
        self.galvanizedSheetManagmentPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.galvanizedSheetManagmentPanel, "镀锌板材管理")
        self.colorCoatManagementPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.colorCoatManagementPanel, "彩涂板材管理")
        self.stainlessSheetManagmentPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.stainlessSheetManagmentPanel, "不锈钢板材管理")
        self.sparyBoardManagementPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.sparyBoardManagementPanel, "喷涂板材管理")

        self.notebook.SetSelection(0)
