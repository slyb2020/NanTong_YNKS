import wx
from DBOperation import GetOrderDetailRecord,GetDeltaWithBluePrintNo


class ProductionScheduleAlgorithm(object):
    def __init__(self,log,orderID):
        super(ProductionScheduleAlgorithm, self).__init__()
        self.log = log
        self.orderID = orderID
        _, self.orderDetailData = GetOrderDetailRecord(self.log, 1, orderID)
        self.wrongNumber = 0
        self.materialBoardList=[]
        self.missDrawingList=[]
        for record in self.orderDetailData:
            errorCode,delta = self.CalculateMeterailBoardNeeded(record)
            if errorCode:
                self.missDrawingList.append(record[6])
                self.wrongNumber += 1
                temp = [record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[12],record[13],[record[8],int(record[10]),int(record[11])],[record[9],int(record[10]),int(record[11])],[],[]]
                if record[14] != 'None':
                    temp[11] = [record[8],int(record[10]),int(record[11])]
                if record[15] != 'None':
                    temp[12] = [record[8],int(record[10]),int(record[11])]
            else:
                temp = [record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[12],record[13],[record[8],int(record[10])+delta[0],int(record[11])+delta[0]],[record[9],int(record[10])+delta[6],int(record[11])+delta[7]],[],[]]
                if record[14] != 'None':
                    temp[11] = [record[8],int(record[10])+delta[2],int(record[11])+delta[3]]
                if record[15] != 'None':
                    temp[12] = [record[8],int(record[10])+delta[4],int(record[11])+delta[5]]
            self.materialBoardList.append(temp)
        print("wrong Number",self.wrongNumber)

    def CalculateMeterailBoardNeeded(self,orderRecord):
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

    def GetDeltaWithBluePrintNo(self,bluePrintNo):
        if len(bluePrintNo)<10:
            try:
                index = int(bluePrintNo[4:])
            except:
                index = int(bluePrintNo[5:])
            bluePrintNo = bluePrintNo[0]+'.'+bluePrintNo[1:4]+'.%04d'%index
        _,delta = GetDeltaWithBluePrintNo(self.log,1,bluePrintNo)
        return delta
