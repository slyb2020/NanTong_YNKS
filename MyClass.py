#!/usr/bin/env python
# encoding: utf-8
"""
@author: slyb
@license: (C) Copyright 2017-2020, 天津定智科技有限公司.
@contact: slyb@tju.edu.cn
@file: MyClass.py.py
@time: 2019/6/16 14:05
@desc:
"""
from MyLog import MyLogCtrl
import wx.lib.agw.pybusyinfo as PBI
import time
import wx.lib.agw.aquabutton as AB
import wx.lib.agw.gradientbutton as GB
# from OrderInfoEditDialog import *
# from ScheduleDemoDialog import *
import wx
import wx.adv
import wx.lib.agw.foldpanelbar as fpb
import wx.lib.gizmos as gizmos  # Formerly wx.gizmos in Classic
from six import BytesIO
import images
from ID_DEFINE import *
import math
import random
import os
import sys
import images
import wx.lib.agw.hypertreelist as HTL
import random
import numpy as np

import wx.lib.agw.flatmenu as FM
from wx.lib.agw.artmanager import ArtManager, RendererBase, DCSaver
from wx.lib.agw.fmresources import ControlFocus, ControlPressed
from wx.lib.agw.fmresources import FM_OPT_SHOW_CUSTOMIZE, FM_OPT_SHOW_TOOLBAR, FM_OPT_MINIBAR
import datetime
from SystemIntroductionPanel import SystemIntroductionPanel
from OrderManagementPanel import OrderManagementPanel
from BoardManagementPanel import BoardManagementPanel
from BluePrintManagementPanel import BluePrintManagementPanel
from ExcelImport import XLSGridFrame
from DBOperation import CreateNewOrderSheet,InsertNewOrderRecord,GetAllOrderList
from ImportOrderDialog import ImportOrderFromExcelDialog
from ProductionScheduleDialog import ProductionScheduleDialog

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')
sys.path.append(os.path.split(dirName)[0])


def switchRGBtoBGR(colour):
    return wx.Colour(colour.Blue(), colour.Green(), colour.Red())


def CreateBackgroundBitmap():
    mem_dc = wx.MemoryDC()
    bmp = wx.Bitmap(200, 300)
    mem_dc.SelectObject(bmp)
    mem_dc.Clear()
    # colour the menu face with background colour
    top = wx.Colour("blue")
    bottom = wx.Colour("light blue")
    filRect = wx.Rect(0, 0, 200, 300)
    mem_dc.GradientFillConcentric(filRect, top, bottom, wx.Point(100, 150))
    mem_dc.SelectObject(wx.NullBitmap)
    return bmp


class FM_MyRenderer(FM.FMRenderer):
    def __init__(self):
        FM.FMRenderer.__init__(self)

    def DrawMenuButton(self, dc, rect, state):
        self.DrawButton(dc, rect, state)

    def DrawMenuBarButton(self, dc, rect, state):
        self.DrawButton(dc, rect, state)

    def DrawButton(self, dc, rect, state, colour=None):
        if state == ControlFocus:
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().BackgroundColour())
        elif state == ControlPressed:
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().HighlightBackgroundColour())
        else:  # ControlNormal, ControlDisabled, default
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().BackgroundColour())
        dc.SetPen(wx.Pen(penColour))
        dc.SetBrush(wx.Brush(brushColour))
        dc.DrawRoundedRectangle(rect.x, rect.y, rect.width, rect.height, 4)

    def DrawMenuBarBackground(self, dc, rect):
        vertical = ArtManager.Get().GetMBVerticalGradient()
        dcsaver = DCSaver(dc)
        # fill with gradient
        startColour = self.menuBarFaceColour
        endColour = ArtManager.Get().LightColour(startColour, 90)
        dc.SetPen(wx.Pen(endColour))
        dc.SetBrush(wx.Brush(endColour))
        dc.DrawRectangle(rect)

    def DrawToolBarBg(self, dc, rect):
        if not ArtManager.Get().GetRaiseToolbar():
            return
        # fill with gradient
        startColour = self.menuBarFaceColour()
        dc.SetPen(wx.Pen(startColour))
        dc.SetBrush(wx.Brush(startColour))
        dc.DrawRectangle(0, 0, rect.GetWidth(), rect.GetHeight())


ArtIDs = ["None",
          "wx.ART_ADD_BOOKMARK",
          "wx.ART_DEL_BOOKMARK",
          "wx.ART_HELP_SIDE_PANEL",
          "wx.ART_HELP_SETTINGS",
          "wx.ART_HELP_BOOK",
          "wx.ART_HELP_FOLDER",
          "wx.ART_HELP_PAGE",
          "wx.ART_GO_BACK",
          "wx.ART_GO_FORWARD",
          "wx.ART_GO_UP",
          "wx.ART_GO_DOWN",
          "wx.ART_GO_TO_PARENT",
          "wx.ART_GO_HOME",
          "wx.ART_FILE_OPEN",
          "wx.ART_PRINT",
          "wx.ART_HELP",
          "wx.ART_TIP",
          "wx.ART_REPORT_VIEW",
          "wx.ART_LIST_VIEW",
          "wx.ART_NEW_DIR",
          "wx.ART_HARDDISK",
          "wx.ART_FLOPPY",
          "wx.ART_CDROM",
          "wx.ART_REMOVABLE",
          "wx.ART_FOLDER",
          "wx.ART_FOLDER_OPEN",
          "wx.ART_GO_DIR_UP",
          "wx.ART_EXECUTABLE_FILE",
          "wx.ART_NORMAL_FILE",
          "wx.ART_TICK_MARK",
          "wx.ART_CROSS_MARK",
          "wx.ART_ERROR",
          "wx.ART_QUESTION",
          "wx.ART_WARNING",
          "wx.ART_INFORMATION",
          "wx.ART_MISSING_IMAGE",
          "SmileBitmap"
          ]


##########################################################################
def GetCollapsedIconData():
    return \
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x8eIDAT8\x8d\xa5\x93-n\xe4@\x10\x85?g\x03\n6lh)\xc4\xd2\x12\xc3\x81\
\xd6\xa2I\x90\x154\xb9\x81\x8f1G\xc8\x11\x16\x86\xcd\xa0\x99F\xb3A\x91\xa1\
\xc9J&\x96L"5lX\xcc\x0bl\xf7v\xb2\x7fZ\xa5\x98\xebU\xbdz\xf5\\\x9deW\x9f\xf8\
H\\\xbfO|{y\x9dT\x15P\x04\x01\x01UPUD\x84\xdb/7YZ\x9f\xa5\n\xce\x97aRU\x8a\
\xdc`\xacA\x00\x04P\xf0!0\xf6\x81\xa0\xf0p\xff9\xfb\x85\xe0|\x19&T)K\x8b\x18\
\xf9\xa3\xe4\xbe\xf3\x8c^#\xc9\xd5\n\xa8*\xc5?\x9a\x01\x8a\xd2b\r\x1cN\xc3\
\x14\t\xce\x97a\xb2F0Ks\xd58\xaa\xc6\xc5\xa6\xf7\xdfya\xe7\xbdR\x13M2\xf9\
\xf9qKQ\x1fi\xf6-\x00~T\xfac\x1dq#\x82,\xe5q\x05\x91D\xba@\xefj\xba1\xf0\xdc\
zzW\xcff&\xb8,\x89\xa8@Q\xd6\xaaf\xdfRm,\xee\xb1BDxr#\xae\xf5|\xddo\xd6\xe2H\
\x18\x15\x84\xa0q@]\xe54\x8d\xa3\xedf\x05M\xe3\xd8Uy\xc4\x15\x8d\xf5\xd7\x8b\
~\x82\x0fh\x0e"\xb0\xad,\xee\xb8c\xbb\x18\xe7\x8e;6\xa5\x89\x04\xde\xff\x1c\
\x16\xef\xe0p\xfa>\x19\x11\xca\x8d\x8d\xe0\x93\x1b\x01\xd8m\xf3(;x\xa5\xef=\
\xb7w\xf3\x1d$\x7f\xc1\xe0\xbd\xa7\xeb\xa0(,"Kc\x12\xc1+\xfd\xe8\tI\xee\xed)\
\xbf\xbcN\xc1{D\x04k\x05#\x12\xfd\xf2a\xde[\x81\x87\xbb\xdf\x9cr\x1a\x87\xd3\
0)\xba>\x83\xd5\xb97o\xe0\xaf\x04\xff\x13?\x00\xd2\xfb\xa9`z\xac\x80w\x00\
\x00\x00\x00IEND\xaeB`\x82'


def GetCollapsedIconBitmap():
    return wx.Bitmap(GetCollapsedIconImage())


def GetCollapsedIconImage():
    stream = BytesIO(GetCollapsedIconData())
    return wx.Image(stream)


# ----------------------------------------------------------------------
def GetExpandedIconData():
    return \
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x9fIDAT8\x8d\x95\x93\xa1\x8e\xdc0\x14EO\xb2\xc4\xd0\xd2\x12\xb7(mI\
\xa4%V\xd1lQT4[4-\x9a\xfe\xc1\xc2|\xc6\xc2~BY\x83:A3E\xd3\xa0*\xa4\xd2\x90H!\
\x95\x0c\r\r\x1fK\x81g\xb2\x99\x84\xb4\x0fY\xd6\xbb\xc7\xf7>=\'Iz\xc3\xbcv\
\xfbn\xb8\x9c\x15 \xe7\xf3\xc7\x0fw\xc9\xbc7\x99\x03\x0e\xfbn0\x99F+\x85R\
\x80RH\x10\x82\x08\xde\x05\x1ef\x90+\xc0\xe1\xd8\ryn\xd0Z-\\A\xb4\xd2\xf7\
\x9e\xfbwoF\xc8\x088\x1c\xbbae\xb3\xe8y&\x9a\xdf\xf5\xbd\xe7\xfem\x84\xa4\
\x97\xccYf\x16\x8d\xdb\xb2a]\xfeX\x18\xc9s\xc3\xe1\x18\xe7\x94\x12cb\xcc\xb5\
\xfa\xb1l8\xf5\x01\xe7\x84\xc7\xb2Y@\xb2\xcc0\x02\xb4\x9a\x88%\xbe\xdc\xb4\
\x9e\xb6Zs\xaa74\xadg[6\x88<\xb7]\xc6\x14\x1dL\x86\xe6\x83\xa0\x81\xba\xda\
\x10\x02x/\xd4\xd5\x06\r\x840!\x9c\x1fM\x92\xf4\x86\x9f\xbf\xfe\x0c\xd6\x9ae\
\xd6u\x8d \xf4\xf5\x165\x9b\x8f\x04\xe1\xc5\xcb\xdb$\x05\x90\xa97@\x04lQas\
\xcd*7\x14\xdb\x9aY\xcb\xb8\\\xe9E\x10|\xbc\xf2^\xb0E\x85\xc95_\x9f\n\xaa/\
\x05\x10\x81\xce\xc9\xa8\xf6><G\xd8\xed\xbbA)X\xd9\x0c\x01\x9a\xc6Q\x14\xd9h\
[\x04\xda\xd6c\xadFkE\xf0\xc2\xab\xd7\xb7\xc9\x08\x00\xf8\xf6\xbd\x1b\x8cQ\
\xd8|\xb9\x0f\xd3\x9a\x8a\xc7\x08\x00\x9f?\xdd%\xde\x07\xda\x93\xc3{\x19C\
\x8a\x9c\x03\x0b8\x17\xe8\x9d\xbf\x02.>\x13\xc0n\xff{PJ\xc5\xfdP\x11""<\xbc\
\xff\x87\xdf\xf8\xbf\xf5\x17FF\xaf\x8f\x8b\xd3\xe6K\x00\x00\x00\x00IEND\xaeB\
`\x82'


def GetExpandedIconBitmap():
    return wx.Bitmap(GetExpandedIconImage())


def GetExpandedIconImage():
    stream = BytesIO(GetExpandedIconData())
    return wx.Image(stream)


# ----------------------------------------------------------------------
def GetMondrianData():
    return \
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qID\
ATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16\
o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\
\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\
\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\
\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82'


def GetMondrianBitmap():
    return wx.Bitmap(GetMondrianImage())


def GetMondrianImage():
    stream = BytesIO(GetMondrianData())
    return wx.Image(stream)


def GetMondrianIcon():
    icon = wx.Icon()
    icon.CopyFromBitmap(GetMondrianBitmap())
    return icon


class MainPanel(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(1024, 768), style=wx.TAB_TRAVERSAL):
        wx.Panel.__init__(self, parent, id, pos, size, style)
        self.parent = parent
        il = wx.ImageList(16, 16)
        self.idx1 = il.Add(images._rt_smiley.GetBitmap())
        self.idx2 = il.Add(images.GridBG.GetBitmap())
        self.idx3 = il.Add(images.Smiles.GetBitmap())
        self.idx4 = il.Add(images._rt_undo.GetBitmap())
        self.idx5 = il.Add(images._rt_save.GetBitmap())
        self.idx6 = il.Add(images._rt_redo.GetBitmap())

        self._leftWindow1 = wx.adv.SashLayoutWindow(self, ID_WINDOW_LEFT, wx.DefaultPosition,
                                                    wx.Size(200, 1000), wx.NO_BORDER |
                                                    wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(220, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0
        # will occupy the space not used by the Layout Algorithm
        self.CreateBottomWindow()
        self.log = MyLogCtrl(self.bottomWindow, -1, "")
        self.work_zone_Panel = WorkZonePanel(self, self.parent, self.log)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.ReCreateFoldPanel(0)
        self.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnSashDrag, id=ID_WINDOW_LEFT,
                  id2=ID_WINDOW_BOTTOM)  # BOTTOM和LEFT顺序不能换，要想更改哪个先分，只需更改上面窗口定义的顺序
        self._pnl.Bind(fpb.EVT_CAPTIONBAR, self.OnPressCaption)

    def CreateBottomWindow(self):
        self.bottomWindow = wx.adv.SashLayoutWindow(self, ID_WINDOW_BOTTOM, style=wx.NO_BORDER | wx.adv.SW_3D)
        self.bottomWindow.SetDefaultSize((1000, 200))
        self.bottomWindow.SetOrientation(wx.adv.LAYOUT_HORIZONTAL)
        self.bottomWindow.SetAlignment(wx.adv.LAYOUT_BOTTOM)
        # win.SetBackgroundColour(wx.Colour(0, 0, 255))
        self.bottomWindow.SetSashVisible(wx.adv.SASH_TOP, True)
        self.bottomWindow.SetExtraBorderSize(5)

    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.work_zone_Panel)
        event.Skip()

    def OnSashDrag(self, event):
        if event.GetDragStatus() == wx.adv.SASH_STATUS_OUT_OF_RANGE:
            return
        eID = event.GetId()
        if eID == ID_WINDOW_LEFT:
            self._leftWindow1.SetDefaultSize((event.GetDragRect().width, 1000))
        elif eID == ID_WINDOW_BOTTOM:
            self.bottomWindow.SetDefaultSize((1000, event.GetDragRect().height))
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.work_zone_Panel)
        self.work_zone_Panel.Refresh()

    def ReCreateFoldPanel(self, fpb_flags, state=0):
        # delete earlier panel
        self._leftWindow1.DestroyChildren()
        self._pnl = fpb.FoldPanelBar(self._leftWindow1, -1, wx.DefaultPosition,
                                     wx.Size(-1, -1), agwStyle=fpb_flags|fpb.FPB_COLLAPSE_TO_BOTTOM)
        Images = wx.ImageList(16, 16)
        Images.Add(GetExpandedIconBitmap())
        Images.Add(GetCollapsedIconBitmap())

        if self.parent.operatorCharacter in ["技术员","管理员"]:
            item = self._pnl.AddFoldPanel("基材操作面板", collapsed=False,
                                          foldIcons=Images)
            panel = wx.Panel(item, -1, size=(300, 300))
            bitmap = wx.Bitmap("bitmaps/aquabutton.png",
                               wx.BITMAP_TYPE_PNG)
            self.newBoardBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, "  新建基材", size=(100, 50))
            self.newBoardBTN.SetForegroundColour(wx.BLACK)
            self.editBoardBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, "  基材管理", size=(100, 50))
            self.editBoardBTN.SetForegroundColour(wx.BLACK)
            static = wx.StaticLine(panel, -1)
            vbox = wx.BoxSizer(wx.VERTICAL)
            vbox.Add(self.newBoardBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            vbox.Add(self.editBoardBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            vbox.Add(static, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            panel.SetSizer(vbox)
            self._pnl.AddFoldPanelWindow(item, panel, fpb.FPB_ALIGN_WIDTH, 0, 0)
            if self.parent.operatorCharacter == "技术员":
                item.Expand()
            else:
                item.Collapse()

        if self.parent.operatorCharacter in ["技术员","管理员"]:
            item = self._pnl.AddFoldPanel("图纸操作面板", collapsed=False,
                                          foldIcons=Images)
            panel = wx.Panel(item, -1, size=(300, 300))
            bitmap = wx.Bitmap("bitmaps/aquabutton.png",
                               wx.BITMAP_TYPE_PNG)
            self.newSchematicBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, "  新建图纸", size=(100, 50))
            self.newSchematicBTN.SetForegroundColour(wx.BLACK)
            self.editSchematicBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, "  图纸管理", size=(100, 50))
            self.editSchematicBTN.SetForegroundColour(wx.BLACK)
            static = wx.StaticLine(panel, -1)
            vbox = wx.BoxSizer(wx.VERTICAL)
            vbox.Add(self.newSchematicBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            vbox.Add(self.editSchematicBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            vbox.Add(static, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            panel.SetSizer(vbox)
            self._pnl.AddFoldPanelWindow(item, panel, fpb.FPB_ALIGN_WIDTH, 5, 0)
            item.Collapse()

        if self.parent.operatorCharacter in ["技术员","下单员","管理员"]:
            item = self._pnl.AddFoldPanel("订单操作面板", collapsed=False,
                                          foldIcons=Images)
            panel = wx.Panel(item, -1, size=(300, 600))
            bitmap = wx.Bitmap("bitmaps/aquabutton.png",
                               wx.BITMAP_TYPE_PNG)
            self.newOrderBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, "  新建订单", size=(100, 50))
            self.newOrderBTN.Bind(wx.EVT_BUTTON,self.OnNewOrderBTN)
            self.newOrderBTN.SetForegroundColour(wx.BLACK)
            self.editOrderBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, "  批量排产", size=(100, 50))
            self.editOrderBTN.SetForegroundColour(wx.BLACK)
            static = wx.StaticLine(panel, -1)
            vbox = wx.BoxSizer(wx.VERTICAL)
            vbox.Add(self.newOrderBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            vbox.Add(self.editOrderBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            vbox.Add(static, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            self.orderInfoPanel=wx.Panel(panel,size=(-1,500))
            vbox.Add(self.orderInfoPanel,0,wx.EXPAND)
            panel.SetSizer(vbox)
            # self.ReCreateOrderInfoPanel()
            self._pnl.AddFoldPanelWindow(item, panel, fpb.FPB_ALIGN_WIDTH, 5, 0)
            if self.parent.operatorCharacter == "下单员":
                item.Expand()
            else:
                item.Collapse()

        if self.parent.operatorCharacter in ["技术员","管理员"]:
            cs = fpb.CaptionBarStyle()
            cs.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_H)
            cs.SetFirstColour(wx.Colour(223,223,223))
            cs.SetSecondColour(wx.Colour(123,0,0))
            item = self._pnl.AddFoldPanel("标签/胶水单操作面板", collapsed=False,
                                          foldIcons=Images, cbstyle=cs)
            panel = wx.Panel(item, -1, size=(300, 300))
            bitmap = wx.Bitmap("bitmaps/aquabutton.png",
                               wx.BITMAP_TYPE_PNG)
            self.newGlueBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, " 新建标签/胶水单", size=(100, 50))
            self.newGlueBTN.SetForegroundColour(wx.BLACK)
            self.editGlueBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, " 查询标签/胶水单", size=(100, 50))
            self.editGlueBTN.SetForegroundColour(wx.BLACK)
            static = wx.StaticLine(panel, -1)
            vbox = wx.BoxSizer(wx.VERTICAL)
            vbox.Add(self.newGlueBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            vbox.Add(self.editGlueBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            vbox.Add(static, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            panel.SetSizer(vbox)
            self._pnl.AddFoldPanelWindow(item, panel, fpb.FPB_ALIGN_WIDTH, 5, 0)
            item.Collapse()

        if self.parent.operatorCharacter in ["技术员","发货员","管理员"]:
            cs = fpb.CaptionBarStyle()
            cs.SetCaptionStyle(fpb.CAPTIONBAR_GRADIENT_H)
            cs.SetFirstColour(wx.Colour(123,123,123))
            cs.SetSecondColour(wx.Colour(123,12,123))
            # cs.SetCaptionColour(wx.Colour(123,124,235))
            cs.SetCaptionStyle(fpb.CAPTIONBAR_RECTANGLE)
            item = self._pnl.AddFoldPanel("货盘单操作面板", collapsed=False,
                                          foldIcons=Images, cbstyle=cs)
            panel = wx.Panel(item, -1, size=(300, 300))
            bitmap = wx.Bitmap("bitmaps/aquabutton.png",
                               wx.BITMAP_TYPE_PNG)
            self.newDockerBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, " 新建货盘", size=(100, 50))
            self.newDockerBTN.SetForegroundColour(wx.BLACK)
            self.editDockerBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, " 编辑货盘", size=(100, 50))
            self.editDockerBTN.SetForegroundColour(wx.BLACK)
            static = wx.StaticLine(panel, -1)
            vbox = wx.BoxSizer(wx.VERTICAL)
            vbox.Add(self.newDockerBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            vbox.Add(self.editDockerBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            vbox.Add(static, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            panel.SetSizer(vbox)
            self._pnl.AddFoldPanelWindow(item, panel, fpb.FPB_ALIGN_WIDTH, 5, 0)
            if self.parent.operatorCharacter == "发货员":
                item.Expand()
            else:
                item.Collapse()

    def ReCreateOrderInfoPanel(self):
        self.orderInfoPanel.DestroyChildren()
        vbox=wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticBox(self.orderInfoPanel,label=("订单详细信息"),size=(-1,500))
        vbox.Add(title,1,wx.EXPAND)
        self.orderInfoPanel.SetSizer(vbox)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1,20))
        hhbox = wx.BoxSizer()
        hhbox.Add((5,-1))
        hhbox.Add(wx.StaticText(title,label="总面积:",size=(70,-1)),0,wx.TOP,5)
        self.orderTotalSquireTXT=wx.TextCtrl(title,size=(40,-1))
        hhbox.Add(self.orderTotalSquireTXT,1,wx.RIGHT,5)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((5,-1))
        hhbox.Add(wx.StaticText(title,label="子订单数:",size=(70,-1)),0,wx.TOP,5)
        self.subOrderAmountTXT=wx.TextCtrl(title,size=(40,-1))
        hhbox.Add(self.subOrderAmountTXT,1,wx.RIGHT,5)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((5,-1))
        hhbox.Add(wx.StaticText(title,label="总墙板数:",size=(70,-1)),0,wx.TOP,5)
        self.orderTotalPanelAmountTXT=wx.TextCtrl(title,size=(40,-1))
        hhbox.Add(self.orderTotalPanelAmountTXT,1,wx.RIGHT,5)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((5,-1))
        hhbox.Add(wx.StaticText(title,label="总天花板数:",size=(70,-1)),0,wx.TOP,5)
        self.orderTotalCeilingAmountTXT=wx.TextCtrl(title,size=(40,-1))
        hhbox.Add(self.orderTotalCeilingAmountTXT,1,wx.RIGHT,5)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((5,-1))
        hhbox.Add(wx.StaticText(title,label="总构件数:",size=(70,-1)),0,wx.TOP,5)
        self.orderTotalConstructionAmountTXT=wx.TextCtrl(title,size=(40,-1))
        hhbox.Add(self.orderTotalConstructionAmountTXT,1,wx.RIGHT,5)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((5,-1))
        hhbox.Add(wx.StaticText(title,label="总部件数:",size=(70,-1)),0,wx.TOP,5)
        self.orderTotalComponentAmountTXT=wx.TextCtrl(title,size=(40,-1))
        hhbox.Add(self.orderTotalComponentAmountTXT,1,wx.RIGHT,5)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((5,-1))
        hhbox.Add(wx.StaticText(title,label="订单状态:",size=(70,-1)),0,wx.TOP,5)
        self.orderStateTXT=wx.TextCtrl(title,size=(40,-1),style=wx.TE_READONLY)
        self.orderStateTXT.SetValue(self.work_zone_Panel.orderManagmentPanel.data[7])
        hhbox.Add(self.orderStateTXT,1,wx.RIGHT,5)
        vbox.Add(hhbox,0,wx.EXPAND)
        print(self.work_zone_Panel.orderManagmentPanel.data)
        if self.work_zone_Panel.orderManagmentPanel.data[7] == "接单":
            vbox.Add((-1,5))
            self.specificOrderProductionBTN = wx.Button(title,label="排  产",size=(-1,40))
            self.specificOrderProductionBTN.Bind(wx.EVT_BUTTON,self.OnSpecificOrderProductionBTN)
            vbox.Add(self.specificOrderProductionBTN,0,wx.EXPAND|wx.ALL,5)
        elif self.work_zone_Panel.orderManagmentPanel.data[7] == "已排产":
            vbox.Add((-1,5))
            self.specificOrderPrintScheduleBTN = wx.Button(title,label="打印任务单",size=(-1,40))
            vbox.Add(self.specificOrderPrintScheduleBTN,0,wx.EXPAND|wx.ALL,5)

        title.SetSizer(vbox)
        self.orderInfoPanel.Layout()

    def OnSpecificOrderProductionBTN(self,event):
        dlg = wx.MessageDialog(self, '将进行排产操作，此操作不可逆，是否继续?',
                               '信息提示',
                               wx.OK | wx.CANCEL | wx.ICON_INFORMATION
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        if dlg.ShowModal()==wx.ID_OK:
            dlg.Destroy()
            dlg = ProductionScheduleDialog(self,self.work_zone_Panel.orderManagmentPanel.data[0])
            dlg.CenterOnScreen()
            if dlg.ShowModal()==wx.ID_OK:
                self.work_zone_Panel.orderManagmentPanel.data[7] = "已排产"#这个之前应该增加一个数据库更新操作
                self.work_zone_Panel.orderManagmentPanel.orderGrid.ReCreate()
        else:
            dlg.Destroy()
        self.ReCreateOrderInfoPanel()

    def OnNewOrderBTN(self,event):
        from DBOperation import GetTableListFromDB
        _,dbNameList = GetTableListFromDB(None,1)
        if len(dbNameList)>0:
            nameList=[]
            for name in dbNameList:
                nameList.append(int(name))
            self.newOrderID = max(nameList) + 1
        else:
            self.newOrderID = 1
        from NewOrderInquireDialog import NewOrderInquiredDialog
        dlg = NewOrderInquiredDialog(self, self.newOrderID)
        dlg.CenterOnScreen()
        value = dlg.ShowModal()
        dlg.Destroy()
        if value == wx.ID_OK:
            wildcard = "Excel文件 (*.xls)|*.xlsx|" \
                       "Compiled Python (*.pyc)|*.pyc|" \
                       "All files (*.*)|*.*"
            dlg = wx.FileDialog(
                self, message="请选择Excel文件",
                defaultDir=os.getcwd(),
                defaultFile="",
                wildcard=wildcard,
                style=wx.FD_OPEN | wx.FD_MULTIPLE |
                      wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
                      wx.FD_PREVIEW
            )
            if dlg.ShowModal() == wx.ID_OK:
                self.excelFileName = dlg.GetPaths()[0]
                dlg.Destroy()
                dlg = ImportOrderFromExcelDialog(self, self.newOrderID)
                dlg.CenterOnScreen()
                if dlg.ShowModal() == wx.ID_OK:
                    pass
                    # InsertNewOrderRecord(self.log, 1, self.newOrderID)
                    # CreateNewOrderSheet(self.log, 1, self.newOrderID)
                    # _, boardList = GetAllOrderList(self.log, 1)
                    # self.work_zone_Panel.orderManagmentPanel.dataArray = np.array(boardList)
                    # self.work_zone_Panel.orderManagmentPanel.orderGrid.ReCreate()
                dlg.Destroy()

                # _, boardList = GetAllOrderList(self.log, 1)
                # self.work_zone_Panel.orderManagmentPanel.dataArray = np.array(boardList)
                # self.work_zone_Panel.orderManagmentPanel.orderGrid.ReCreate()
                # # XLSGridFrame(None,paths[0])
        else:
            from NewOrderInquireDialog import NewOrderMainDialog
            dlg = NewOrderMainDialog(self, self.newOrderID)
            dlg.CenterOnScreen()
            if dlg.ShowModal() == wx.ID_OK:
                InsertNewOrderRecord(self.log,1,self.newOrderID)
                CreateNewOrderSheet(self.log,1,self.newOrderID)
                _, boardList = GetAllOrderList(self.log, 1)
                self.work_zone_Panel.orderManagmentPanel.dataArray = np.array(boardList)
                self.work_zone_Panel.orderManagmentPanel.orderGrid.ReCreate()
            dlg.Destroy()

    def OnPressCaption(self,event):
        for i in range(0, self._pnl.GetCount()):
            item = self._pnl.GetFoldPanel(i)
            self._pnl.Collapse(item)
        event.Skip()


class WorkZonePanel(wx.Panel):
    def __init__(self, parent, master, log):
        wx.Panel.__init__(self, parent, -1)
        self.master = master
        self.log = log
        self.notebook = wx.Notebook(self, -1, size=(21, 21), style=
                                    wx.BK_DEFAULT
                                    # wx.BK_TOP
                                    # wx.BK_BOTTOM
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
        self.systemIntroductionPanel = SystemIntroductionPanel(self.notebook)
        self.notebook.AddPage(self.systemIntroductionPanel,"系统介绍")
        if self.master.operatorCharacter in ["技术员","管理员"]:
            self.boardManagmentPanel = BoardManagementPanel(self.notebook,self,self.log)
            self.notebook.AddPage(self.boardManagmentPanel, "基材管理")
        if self.master.operatorCharacter in ["技术员","管理员"]:
            self.bluePrintManagmentPanel = BluePrintManagementPanel(self.notebook,self,self.log)
            self.notebook.AddPage(self.bluePrintManagmentPanel, "图纸管理")
        if self.master.operatorCharacter in ["技术员","管理员","下单员"]:
            self.orderManagmentPanel = OrderManagementPanel(self.notebook,self.master, self.log)
            self.notebook.AddPage(self.orderManagmentPanel, "订单管理")
        if self.master.operatorCharacter == '下单员':
            self.notebook.SetSelection(1)
        elif self.master.operatorCharacter in ["技术员","管理员"]:
            self.notebook.SetSelection(3)

