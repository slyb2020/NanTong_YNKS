import copy
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
                wallType = record[6].split('.')[1]
                if record[8]=='S.S':
                    boardThickness = 0.7
                elif wallType=='2SP':
                    boardThickness=0.7
                else:
                    boardThickness=0.56
                temp = [record[0],record[1],record[2],record[3],record[4],record[5],record[6],"%04d-%04d"%(int(record[1]),int(record[0])),'X',record[8],
                        int(record[10])+delta[0],int(record[11])+delta[1],boardThickness,int(record[13]),'墙板',record[10],record[11]]#现在的record[12]还是墙板厚，而不是基材厚
                self.materialBoard.append(temp)
                temp = [record[0],record[1],record[2],record[3],record[4],record[5],record[6],"%04d-%04d"%(int(record[1]),int(record[0])),'Y',record[9],
                        int(record[10])+delta[6],int(record[11])+delta[7],boardThickness,int(record[13]),'墙板',record[10],record[11]]
                self.materialBoard.append(temp)
                if record[14] != 'None' and record[14] != '0':
                    temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6],"%04d-%04d"%(int(record[1]),int(record[0])), 'Z',
                            record[14], int(record[10]) + delta[2], int(record[11]) + delta[3], boardThickness,int(record[13]),'墙板',record[10],record[11]]
                    self.materialBoard.append(temp)
                if record[15] != 'None'and record[15] != '0':
                    temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6],"%04d-%04d"%(int(record[1]),int(record[0])), 'V',
                            record[15], int(record[10]) + delta[4], int(record[11]) + delta[5], boardThickness,int(record[13]),'墙板',record[10],record[11]]
                    self.materialBoard.append(temp)
        # for record in self.constructionOrderData:
        #     drawingNo = record[6]
        #     errorCode,data = self.CalculateConstructionBoardNeeded(drawingNo)
        #     if errorCode:
        #         self.wrongNumber += 1
        #         self.missList.append(drawingNo)
        #     else:
        #         if data[2]=='L':
        #             temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], 'Co',
        #                     record[8], int(record[10]), int(data[1]), float(data[3]), int(record[13]), '构件']
        #         else:
        #             temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], 'Co',
        #                     record[8], int(record[10]), int(data[1]), float(data[3]), int(record[13]), '构件']
        #         self.materialBoard.append(temp)
        for record in self.ceilingOrderData:
            #record->0:ID,1:订单号,2:子订单号,3:甲板号,4:区域,5:房间,6:图纸号,7:胶水单号,8:X面颜色,9:Y面颜色,10:长,11:宽,12:厚,13:数量,14:Z面颜色,15:V面颜色
            errorCode,delta = self.GetCeilingDelta(record)
            if errorCode:
                self.missList.append(record[6])
                self.wrongNumber += 1
            else:
                boardThickness=0.56
                temp = [record[0],record[1],record[2],record[3],record[4],record[5],record[6],"%04d-%04d"%(int(record[1]),int(record[0])),'X',record[8],
                        int(record[10])+delta[0],int(record[11])+delta[1],boardThickness,int(record[13]),'天花板',record[10],record[11]]#现在的record[12]还是墙板厚，而不是基材厚
                self.materialBoard.append(temp)
                temp = [record[0],record[1],record[2],record[3],record[4],record[5],record[6],"%04d-%04d"%(int(record[1]),int(record[0])),'Y',record[9],
                        int(record[10])+delta[6],int(record[11])+delta[7],boardThickness,int(record[13]),'天花板',record[10],record[11]]
                self.materialBoard.append(temp)
                if record[14] != 'None' and record[14] != '0':
                    temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6],"%04d-%04d"%(int(record[1]),int(record[0])), 'Z',
                            record[14], int(record[10]) + delta[2], int(record[11]) + delta[3], boardThickness,int(record[13]),'天花板',record[10],record[11]]
                    self.materialBoard.append(temp)
                if record[15] != 'None' and record[15] != '0':
                    temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6],"%04d-%04d"%(int(record[1]),int(record[0])), 'V',
                            record[15], int(record[10]) + delta[4], int(record[11]) + delta[5], boardThickness,int(record[13]),'天花板',record[10],record[11]]
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
        self.materialBoardList.append(temp)#把待裁切的板材按原材料的不同分开到不同的列表

        self.cuttingScheduleList=[]
        for i in range(len(self.materialBoardList)):
            self.materialBoardList[i].sort(key=itemgetter(12,10,11),reverse=True)#对同一种材料的待裁切板材按长度（第一序）、宽度（第二序）及厚度（第三序）排序，这一步已验证正确性
            cuttingSchedule = self.CalculateCuttingSchedule(self.materialBoardList[i])#用排列好的板材计算裁切计划，这一步已验证正确性
            cuttingSchedule = self.MergeSameSchedule(cuttingSchedule)#cuttingSchedule是合并之前的裁切计划，如果以此直接打印生成裁切任务单的话，会是很多行。所以还要进行合并同类项处理
            self.cuttingScheduleList.append(cuttingSchedule)

        self.bendingScheduleList=[]
        for i in self.materialBoard:
            print('i=',i)

        print("wrong Number", self.wrongNumber)

    def MergeSameSchedule(self,data):
        # [['YQ73D', 2160, 1234], [553, 553]]
        result = []
        exBoard = data[0][0]
        horizentalCuttingBoard = exBoard
        horizentalCuttingBoard.append(1)
        verticalCuttingBoard = [data[0][1]]
        for horizentalCutting,verticalCutting in data[1:]:#第一步合并相同的横切
            if horizentalCutting[1]==exBoard[1] and horizentalCutting[2]==exBoard[2] and horizentalCutting[3]==exBoard[3]:
                horizentalCuttingBoard[-1] = horizentalCuttingBoard[-1]+1
                verticalCuttingBoard.append(verticalCutting)
            else:
                result.append([horizentalCuttingBoard,verticalCuttingBoard])
                exBoard=horizentalCutting
                horizentalCuttingBoard = horizentalCutting
                horizentalCuttingBoard.append(1)
                verticalCuttingBoard=[verticalCutting]
        result.append([horizentalCuttingBoard,verticalCuttingBoard])
        # for record in result:
        #     print("after Merge step1:",record)
        for i, schedule in enumerate(result):#第二部再合并相同的纵切
            verticalCuttingList=[]
            exVerticalCutting=schedule[1][0]
            amount=1
            for verticalCutting in schedule[1][1:]:
                # print("verticalCutting",verticalCutting,exVerticalCutting)
                if verticalCutting == exVerticalCutting:
                    amount+=1
                else:
                    verticalCuttingList.append([exVerticalCutting,amount])
                    exVerticalCutting=verticalCutting
                    amount=1
            verticalCuttingList.append([exVerticalCutting,amount])
            result[i] = [schedule[0],verticalCuttingList]

        return result

    def CalculateCuttingSchedule(self,data):
        # boardName = data[0][9]  #获得板材名称
        # boardThickness = data[0][12]#获得板材厚度
        dataList = []
        for record in data:#将待裁切板材按单块列表
            for i in range(int(record[13])):
                temp = record[:13]
                temp.append(1)
                dataList.append(temp)
        sameLenthBoardListSet=[]
        temp=[]
        thisLength = dataList[0][10]
        temp.append(dataList[0])
        for record in dataList[1:]:#把同一种板材，按相同长度分堆
            if thisLength != record[10]:
                sameLenthBoardListSet.append(temp)
                temp=[]
            temp.append(record)
            thisLength=record[10]
        sameLenthBoardListSet.append(temp)
        result=[]
        for sameLenthBoardList in sameLenthBoardListSet:
            CuttingFinish = False
            while not CuttingFinish:   #循环调用直到将所有待裁切板材全部裁切完毕
                result,sameLenthBoardList = self.MakeHorizontalCutting(result,sameLenthBoardList)   #每次待用都开始一次新的横切
                temp = []
                for record in sameLenthBoardList:
                    if record[-1]>0:
                        temp.append(record)
                sameLenthBoardList = temp
                CuttingFinish = False if len(sameLenthBoardList)>0 else True
        return result

    def MakeHorizontalCutting(self,result,data):
        verticalCutting = [] #用于存储本次的纵切计划
        verticalCutting.append(data[0][11])
        restWidth=1234-data[0][11]   #剩余板材宽度，长度由第一块板确定
        data[0][13]=0
        for i,board in enumerate(data[1:]):
            if board[11] <= restWidth:
                restWidth -= board[11]
                verticalCutting.append(board[11])
                data[i+1][-1]=0#因为是从data[1]开始循环的，所以这里i要加一*******
                if restWidth<data[-1][11]:
                    break
        result.append([[data[0][9],data[0][12],1234,data[0][10]],verticalCutting])#第一部分位横切板材，第二部分位纵切计划
        return result,data

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
