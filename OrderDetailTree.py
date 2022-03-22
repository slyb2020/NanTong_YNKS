import wx
from math import *
from ID_DEFINE import *
import string
import images
import xml.etree.ElementTree as ET
import os
import cv2



class MyTreeCtrl(wx.TreeCtrl):
    def __init__(self, parent, id, pos, size, style, log):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
        self.log = log
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        # self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit)
        # self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndEdit)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate)

        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

    def OnCompareItems(self, item1, item2):
        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)
        self.log.WriteText('compare: ' + t1 + ' <> ' + t2 + '\n')
        if t1 < t2: return -1
        if t1 == t2: return 0
        return 1

    def OnRightDown(self, event):
        pt = event.GetPosition();
        item, flags = self.HitTest(pt)
        if item:
            self.log.WriteText("OnRightClick: %s, %s, %s\n" %
                               (self.GetItemText(item), type(item), item.__class__))
            self.SelectItem(item)
            if not hasattr(self, "popupID1"):
                self.popupID1 = wx.NewIdRef()
                self.popupID2 = wx.NewIdRef()
                self.popupID3 = wx.NewIdRef()
                self.popupID4 = wx.NewIdRef()
                self.popupID5 = wx.NewIdRef()
                self.popupID6 = wx.NewIdRef()
                self.popupID7 = wx.NewIdRef()
                self.popupID8 = wx.NewIdRef()
                self.popupID9 = wx.NewIdRef()

                self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
                self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
                self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
                self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
                self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
                self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)
                self.Bind(wx.EVT_MENU, self.OnPopupSeven, id=self.popupID7)
                self.Bind(wx.EVT_MENU, self.OnPopupEight, id=self.popupID8)
                self.Bind(wx.EVT_MENU, self.OnPopupNine, id=self.popupID9)

            # make a menu
            menu = wx.Menu()
            # Show how to put an icon in the menu
            item = wx.MenuItem(menu, self.popupID1,"One")
            bmp = images.Smiles.GetBitmap()
            item.SetBitmap(bmp)
            menu.Append(item)
            # add some other items
            menu.Append(self.popupID2, "Two")
            menu.Append(self.popupID3, "Three")
            menu.Append(self.popupID4, "Four")
            menu.Append(self.popupID5, "Five")
            menu.Append(self.popupID6, "Six")
            # make a submenu
            sm = wx.Menu()
            sm.Append(self.popupID8, "sub item 1")
            sm.Append(self.popupID9, "sub item 1")
            menu.Append(self.popupID7, "Test Submenu", sm)


            # Popup the menu.  If an item is selected then its handler
            # will be called before PopupMenu returns.
            self.PopupMenu(menu)
            menu.Destroy()


    def OnPopupOne(self, event):
        self.log.WriteText("Popup one\n")

    def OnPopupTwo(self, event):
        self.log.WriteText("Popup two\n")

    def OnPopupThree(self, event):
        self.log.WriteText("Popup three\n")

    def OnPopupFour(self, event):
        self.log.WriteText("Popup four\n")

    def OnPopupFive(self, event):
        self.log.WriteText("Popup five\n")

    def OnPopupSix(self, event):
        self.log.WriteText("Popup six\n")

    def OnPopupSeven(self, event):
        self.log.WriteText("Popup seven\n")

    def OnPopupEight(self, event):
        self.log.WriteText("Popup eight\n")

    def OnPopupNine(self, event):
        self.log.WriteText("Popup nine\n")


    def OnRightUp(self, event):
        pt = event.GetPosition();
        item, flags = self.HitTest(pt)
        if item:
            self.log.WriteText("OnRightUp: %s (manually starting label edit)\n"
                               % self.GetItemText(item))
            self.EditLabel(item)

    def OnBeginEdit(self, event):
        self.log.WriteText("OnBeginEdit\n")
        # show how to prevent edit...
        item = event.GetItem()
        if item and self.GetItemText(item) == "The Root Item":
            wx.Bell()
            self.log.WriteText("You can't edit this one...\n")

            # Lets just see what's visible of its children
            cookie = 0
            root = event.GetItem()
            (child, cookie) = self.GetFirstChild(root)

            while child.IsOk():
                self.log.WriteText("Child [%s] visible = %d" %
                                   (self.GetItemText(child),
                                    self.IsVisible(child)))
                (child, cookie) = self.GetNextChild(root, cookie)

            event.Veto()

    def OnEndEdit(self, event):
        self.log.WriteText("OnEndEdit: %s %s\n" %
                           (event.IsEditCancelled(), event.GetLabel()) )
        # show how to reject edit, we'll not allow any digits
        for x in event.GetLabel():
            if x in string.digits:
                self.log.WriteText("You can't enter digits...\n")
                event.Veto()
                return

    def OnLeftDClick(self, event):
        pt = event.GetPosition();
        item, flags = self.HitTest(pt)
        if item:
            self.log.WriteText("OnLeftDClick: %s\n" % self.GetItemText(item))
            parent = self.GetItemParent(item)
            if parent.IsOk():
                self.SortChildren(parent)
        event.Skip()

    def OnSize(self, event):
        w,h = self.GetClientSize()
        self.SetSize(0, 0, w, h)

    def OnItemExpanded(self, event):
        item = event.GetItem()
        if item:
            self.log.WriteText("OnItemExpanded: %s\n" % self.GetItemText(item))

    def OnItemCollapsed(self, event):
        item = event.GetItem()
        if item:
            self.log.WriteText("OnItemCollapsed: %s\n" % self.GetItemText(item))

    def OnSelChanged(self, event):
        self.item = event.GetItem()
        if self.item:
            self.log.WriteText("OnSelChanged: %s\n" % self.GetItemText(self.item))
            if wx.Platform == '__WXMSW__':
                self.log.WriteText("BoundingRect: %s\n" %
                                   self.GetBoundingRect(self.item, True))
            #items = self.GetSelections()
            #print(map(self.GetItemText, items))
        event.Skip()

    def OnActivate(self, event):
        if self.item:
            self.log.WriteText("OnActivate: %s\n" % self.GetItemText(self.item))




class OrderDetailTree(wx.Panel):
    def __init__(self, parent, log, structureList,size=wx.DefaultSize, ):
        # Use the WANTS_CHARS style so the panel doesn't eat the Return key.
        wx.Panel.__init__(self, parent, -1, size=size, style=wx.BORDER_THEME)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.log = log
        tID = wx.NewIdRef()
        dataList = structureList[1]
        # datasetList = [
        #     ["ImageNet", [["2017", []], ["2018", []]]],
        #     ["FasionMNIST", [["2007", []], ["2012", []]]],
        #     ["MNIST", [["2007", []], ["2012", []]]],
        #     ["猫狗大战", []],
        # ]

        self.tree = MyTreeCtrl(self, tID, wx.DefaultPosition, size,
                               wx.TR_HAS_BUTTONS
                               | wx.TR_EDIT_LABELS
                               # | wx.TR_MULTIPLE
                               # | wx.TR_HIDE_ROOT
                               , self.log)
        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        fileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_OTHER, isz))
        smileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_OTHER, isz))
        # smileidx    = il.Add(images.Smiles.GetBitmap())
        self.tree.SetImageList(il)
        self.il = il
        self.root = self.tree.AddRoot('订单%s'%structureList[0])
        self.tree.SetItemData(self.root, "根")
        self.tree.SetItemImage(self.root, fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.root, fldropenidx, wx.TreeItemIcon_Expanded)
        subOrderTreePass = True if len(dataList)==1 else False
        for subOrderList in dataList:
            if not subOrderTreePass:
                sub = self.tree.AppendItem(self.root, subOrderList[0])
                self.tree.SetItemData(sub, "子订单")
                self.tree.SetItemImage(sub, fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(sub, fldropenidx, wx.TreeItemIcon_Expanded)
            else:
                sub = self.root
            deckOrderTreePass = True if len(subOrderList[1])==1 else False
            for deckOrderList in subOrderList[1]:
                if not deckOrderTreePass:
                    deck = self.tree.AppendItem(sub, deckOrderList[0])
                    self.tree.SetItemData(deck, "甲板订单")
                    self.tree.SetItemImage(deck, fldridx, wx.TreeItemIcon_Normal)
                    self.tree.SetItemImage(deck, fldropenidx, wx.TreeItemIcon_Expanded)
                else:
                    deck = sub
                zoneOrderTreePass = True if len(deckOrderList[1])==1 else False
                for zoneOrderList in deckOrderList[1]:
                    if not zoneOrderTreePass:
                        zone = self.tree.AppendItem(deck, zoneOrderList[0])
                        self.tree.SetItemData(zone, "区域订单")
                        self.tree.SetItemImage(zone, fileidx, wx.TreeItemIcon_Normal)
                        self.tree.SetItemImage(zone, smileidx, wx.TreeItemIcon_Selected)
                    else:
                        zone = deck
                    roomOrderTreePass = True if len(zoneOrderList[1])==1 else False
                    for roomOrderList in zoneOrderList[1]:
                        if not roomOrderTreePass:
                            room = self.tree.AppendItem(zone, roomOrderList[0])
                            self.tree.SetItemData(room, "房间订单")
                            self.tree.SetItemImage(room, fileidx, wx.TreeItemIcon_Normal)
                            self.tree.SetItemImage(room, smileidx, wx.TreeItemIcon_Selected)
                        else:
                            room = zone
                        for componentList in roomOrderList[1]:
                            item = self.tree.AppendItem(zone, componentList[6])
                            self.tree.SetItemData(item, "零件订单")
                            self.tree.SetItemImage(item, fileidx, wx.TreeItemIcon_Normal)
                            self.tree.SetItemImage(item, smileidx, wx.TreeItemIcon_Selected)

        self.tree.ExpandAll()
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.tree)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndEdit, self.tree)

    def OnSize(self, event):
        w, h = self.GetClientSize()
        self.tree.SetSize(0, 0, w, h)

    def OnBeginEdit(self, event):
        event.Veto()

    def OnEndEdit(self, event):
        event.Veto()

    def ReCreateTree(self):
        self.tree.Destroy()
        tID = wx.NewIdRef()
        self.tree = MyTreeCtrl(self, tID, wx.DefaultPosition, (200, 900),
                               wx.TR_HAS_BUTTONS
                               | wx.TR_EDIT_LABELS
                               # | wx.TR_MULTIPLE
                               # | wx.TR_HIDE_ROOT
                               , self.log)
        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        fileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_OTHER, isz))
        smileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_OTHER, isz))
        # smileidx    = il.Add(images.Smiles.GetBitmap())
        self.tree.SetImageList(il)
        self.il = il
        self.root = self.tree.AddRoot("数据集")
        self.tree.SetItemData(self.root, "根")
        self.tree.SetItemImage(self.root, fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.root, fldropenidx, wx.TreeItemIcon_Expanded)
        for i in self.master.department_list:
            child = self.tree.AppendItem(self.root, i[0])
            self.tree.SetItemData(child, "集")
            self.tree.SetItemImage(child, fldridx, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(child, fldropenidx, wx.TreeItemIcon_Expanded)
            for j in i[1]:
                last = self.tree.AppendItem(child, j[0])
                self.tree.SetItemData(last, "子集")
                self.tree.SetItemImage(last, fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(last, fldropenidx, wx.TreeItemIcon_Expanded)
                for k in j[1]:
                    item = self.tree.AppendItem(last, k[0])
                    self.tree.SetItemData(item, "孙集")
                    self.tree.SetItemImage(item, fileidx, wx.TreeItemIcon_Normal)
                    self.tree.SetItemImage(item, smileidx, wx.TreeItemIcon_Selected)
        self.tree.ExpandAll()
        # self.tree.Refresh()
