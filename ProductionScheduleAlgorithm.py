import wx
from DBOperation import GetOrderDetailRecord,GetDeltaWithBluePrintNo,GetConstructionDetailWithDrawingNo
import numpy as np
from operator import itemgetter

class ProductionScheduleAlgorithm(object):
    def __init__(self,log,orderID):
        super(ProductionScheduleAlgorithm, self).__init__()
        self.log = log
        self.orderID = orderID
        _, self.orderDetailData = GetOrderDetailRecord(self.log, 1, orderID)
        self.wrongNumber = 0
        self.materialBoard=[]#0:订单号，1：
        self.missList=[]
        self.wallOrderData=[]
        self.ceilingOrderData=[]
        self.constructionOrderData=[]
        self.DisassembleOrderData()#将全部订单数据拆分成墙板，天花板，构件等3个数据列表
        self.CreateGlueNoForOrder()#未全部订单生成胶水单号码
        for record in self.wallOrderData:
            #record->0:ID,1:订单号,2:子订单号,3:甲板号,4:区域,5:房间,6:图纸号,7:胶水单号,8:X面颜色,9:Y面颜色,10:长,11:宽,12:厚,13:数量,14:Z面颜色,15:V面颜色
            errorCode,delta = self.GetWalllBoardDelta(record)
            if errorCode:
                self.missList.append(record[6])
                self.wrongNumber += 1
            else:
                temp = [record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],'X',record[8],
                        int(record[10])+delta[0],int(record[11])+delta[1],int(record[12]),int(record[13]),'墙板']#现在的record[12]还是墙板厚，而不是基材厚
                self.materialBoard.append(temp)
                temp = [record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],'Y',record[9],
                        int(record[10])+delta[6],int(record[11])+delta[7],int(record[12]),int(record[13]),'墙板']
                self.materialBoard.append(temp)
                if record[14] != 'None' and record[14] != '0':
                    temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6],record[7], 'Z',
                            record[14], int(record[10]) + delta[2], int(record[11]) + delta[3], int(record[12]),int(record[13]),'墙板']
                    self.materialBoard.append(temp)
                if record[15] != 'None'and record[15] != '0':
                    temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6],record[7], 'V',
                            record[15], int(record[10]) + delta[4], int(record[11]) + delta[5], int(record[12]),int(record[13]),'墙板']
                    self.materialBoard.append(temp)
        for record in self.constructionOrderData:
            drawingNo = record[6]
            errorCode,data = self.CalculateConstructionBoardNeeded(drawingNo)
            if errorCode:
                self.wrongNumber += 1
                self.missList.append(drawingNo)
            else:
                if data[2]=='L':
                    temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], 'Co',
                            record[8], int(record[10]), int(data[1]), float(data[3]), int(record[13]), '构件']
                else:
                    temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], 'Co',
                            record[8], int(record[10]), int(data[1]), float(data[3]), int(record[13]), '构件']
                self.materialBoard.append(temp)
        for record in self.ceilingOrderData:
            #record->0:ID,1:订单号,2:子订单号,3:甲板号,4:区域,5:房间,6:图纸号,7:胶水单号,8:X面颜色,9:Y面颜色,10:长,11:宽,12:厚,13:数量,14:Z面颜色,15:V面颜色
            errorCode,delta = self.GetCeilingDelta(record)
            if errorCode:
                self.missList.append(record[6])
                self.wrongNumber += 1
            else:
                temp = [record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],'X',record[8],
                        int(record[10])+delta[0],int(record[11])+delta[1],int(record[12]),int(record[13]),'天花板']#现在的record[12]还是墙板厚，而不是基材厚
                self.materialBoard.append(temp)
                temp = [record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],'Y',record[9],
                        int(record[10])+delta[6],int(record[11])+delta[7],int(record[12]),int(record[13]),'天花板']
                self.materialBoard.append(temp)
                if record[14] != 'None' and record[14] != '0':
                    temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6],record[7], 'Z',
                            record[14], int(record[10]) + delta[2], int(record[11]) + delta[3], int(record[12]),int(record[13]),'天花板']
                    self.materialBoard.append(temp)
                if record[15] != 'None' and record[15] != '0':
                    temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6],record[7], 'V',
                            record[15], int(record[10]) + delta[4], int(record[11]) + delta[5], int(record[12]),int(record[13]),'天花板']
                    self.materialBoard.append(temp)
        self.materialBoard.sort(key=itemgetter(9), reverse=True)

        self.materialBoardList=[]
        kind = []
        temp = []
        thisKind=self.materialBoard[0][9]
        temp.append(self.materialBoard[0])
        for record in self.materialBoard[1:]:
            if thisKind != record[9]:
                kind.append(thisKind)
                self.materialBoardList.append(temp)
                temp = []
            temp.append(record)
            thisKind = record[9]
        kind.append(thisKind)
        self.materialBoardList.append(temp)

        self.cuttingScheduleList=[]
        for i in range(len(self.materialBoardList)):
            self.materialBoardList[i].sort(key=itemgetter(10,11),reverse=True)
            cuttingSchedule = self.CalculateCuttingSchedule(self.materialBoardList[i])
            self.cuttingScheduleList.append(cuttingSchedule)

        print("wrong Number", self.wrongNumber)

    def CalculateCuttingSchedule(self,data):
        dataList = []
        for record in data:
            for i in range(int(record[13])):
                temp = record[:13]
                temp.append(1)
                dataList.append(temp)
        for record in dataList:
            print(record)
        return data

    def CreateGlueNoForOrder(self):
        pass

    def DisassembleOrderData(self):
        for data in self.orderDetailData:
            temp = str(data[6])
            if '.' not in temp:
                index = temp[0]+'.'+temp[1:4]+'.'+temp[4:]
            else:
                index = temp
            temp = index.split('.')
            if str(temp[1]).isdigit():
                self.constructionOrderData.append(data)
            elif temp[1][0]=='C':
                self.ceilingOrderData.append(data)
            else:
                self.wallOrderData.append(data)

    def GetWalllBoardDelta(self, orderRecord):
        delta = self.GetDeltaWithBluePrintNo(orderRecord[6])
        if delta!=None:#说明返回了有效的增减量
            frontLengthDelta = int(delta[0].split(',')[0])
            frontWidthDelta = int(delta[0].split(',')[1])
            m1LengthDelta = int(delta[1].split(',')[0])
            m1WidthDelta = int(delta[1].split(',')[1])
            m2LengthDelta = int(delta[1].split(',')[2])
            m2WidthDelta = int(delta[1].split(',')[3])
            rearLengthDelta = int(delta[2].split(',')[0])
            rearWidthDelta = int(delta[2].split(',')[1])
            return 0,[frontLengthDelta,frontWidthDelta,m1LengthDelta,m1WidthDelta,m2LengthDelta,m2WidthDelta,rearLengthDelta,rearWidthDelta]
        else:
            return 1,[]

    def GetCeilingDelta(self, orderRecord):
        delta = self.GetDeltaWithBluePrintNo(orderRecord[6])
        if delta!=None:#说明返回了有效的增减量
            frontLengthDelta = int(delta[0].split(',')[0])
            frontWidthDelta = int(delta[0].split(',')[1])
            m1LengthDelta = int(delta[1].split(',')[0])
            m1WidthDelta = int(delta[1].split(',')[1])
            m2LengthDelta = int(delta[1].split(',')[2])
            m2WidthDelta = int(delta[1].split(',')[3])
            rearLengthDelta = int(delta[2].split(',')[0])
            rearWidthDelta = int(delta[2].split(',')[1])
            return 0,[frontLengthDelta,frontWidthDelta,m1LengthDelta,m1WidthDelta,m2LengthDelta,m2WidthDelta,rearLengthDelta,rearWidthDelta]
        else:
            return 1,[]

    def CalculateConstructionBoardNeeded(self, drawingNo):
        """record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], 'V',
        record[15], int(record[10]) + delta[4], int(record[11]) + delta[5], int(record[12])]"""
        error,data = GetConstructionDetailWithDrawingNo(self.log,1,drawingNo)
        if data!=None:#说明返回了有效的构件数据
            return False,data
        return True,data

    def GetDeltaWithBluePrintNo(self,bluePrintNo):
        if '.' not in bluePrintNo:
            if len(bluePrintNo)<10:
                try:
                    index = int(bluePrintNo[4:])
                except:
                    index = int(bluePrintNo[5:])
                bluePrintNo = bluePrintNo[0]+'.'+bluePrintNo[1:4]+'.%04d'%index
        _,delta = GetDeltaWithBluePrintNo(self.log,1,bluePrintNo)
        return delta
