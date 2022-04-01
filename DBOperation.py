from ID_DEFINE import *
import pymysql as MySQLdb
import time
import datetime


def GetEnterpriseInfo(log, whichDB):
    try:
        # db = MySQLdb.connect(host="127.0.0.1", user="root", passwd='', db="智能生产管理系统_调试",charset='utf8')
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `企业名称` from `企业基本信息表` """
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp[0]

def GetAllPasswords(log, whichDB):
    try:
        # db = MySQLdb.connect(host="127.0.0.1", user="root", passwd='', db="智能生产管理系统_调试",charset='utf8')
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `密码` from `info_staff` """
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    data = []
    for psw in temp:
        data.append(psw[0])
    db.close()
    return 0, data


def GetStaffInfoWithPassword(log, whichDB, psw):
    try:
        # db = MySQLdb.connect(host="127.0.0.1", user="root", passwd='', db="智能生产管理系统_调试",charset='utf8')
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `处`,`科`,`工位名`,`姓名`,`员工编号`,`工作状态` from `info_staff` WHERE `密码`='%s'"""%(psw)
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp

def GetAllOrderList(log, whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `订单编号`,`订单名称`,`总价`,`产品数量`,`订单交货日期`,`下单时间`,`下单员ID`,`状态` from `订单信息` """
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp

def UpdateOrderInfo(log, whichDB,data):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE 订单信息 SET `订单名称`='%s',`总价`='%s',`产品数量`='%s',`状态`='%s' WHERE `订单编号` = '%s'" \
          % (str(data[1]),str(data[2]),str(data[3]),str(data[4]),str(data[0]))
    # sql = "INSERT INTO 图纸信息(`图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`," \
    #       "`热压100`,`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,`打包9000`,`图纸大类`,`创建时间`,`备注`)" \
    #       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
    #       % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],datetime.date.today(),data[17])
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
    db.close()

def GetAllBoardList(log, whichDB,whichBoard,state='在用'):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    if state=='全部':
        sql = """SELECT `板材`,`厚度`,`材质`,`密度`,`支持部件`,`支持宽度`,`颜色`,`状态` from `基材表单` 
                    where `板材`='%s'""" % (whichBoard)
    else:
        sql = """SELECT `板材`,`厚度`,`材质`,`密度`,`支持部件`,`支持宽度`,`颜色`,`状态` from `基材表单` 
                    where `板材`='%s' and `状态`='%s'"""%(whichBoard,state)
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp

def GetRGBWithRalID(log,whichDB,RalID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `R`,`G`,`B`,`颜色名`,`颜色别名` from `ral标准色卡` where `RAL代码`='%s'"""%RalID
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp

def GetAllColor(log,whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `RAL代码`,`R`,`G`,`B`,`颜色名`,`颜色别名` from `ral标准色卡` """
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp

def GetDeltaWithBluePrintNo(log,whichDB,bluePrintNo):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `面板增量`,`中板增量`,`背板增量` from `图纸信息` where `图纸号`='%s'"""%bluePrintNo
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp

def GetAllBluPrintList(log,whichDB, type,state='在用'):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    if state == '全部':
        sql = """SELECT `图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`,`热压100`,
                    `热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,'打包9000',`创建时间`,`备注` 
                    ,`a使能`,`a`,`b使能`,`b`,`c使能`,`c`,`d使能`,`d`,`e使能`,`e`,`f使能`,`f`,`CY使能`,`CY`,`图纸名` 
                    from `图纸信息` """
    else:
        sql = """SELECT `图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`,`热压100`,
                    `热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,'打包9000',`创建时间`,`备注` 
                    ,`a使能`,`a`,`b使能`,`b`,`c使能`,`c`,`d使能`,`d`,`e使能`,`e`,`f使能`,`f`,`CY使能`,`CY`,`图纸名`
                    from `图纸信息` where `图纸状态`='%s'"""%state
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp
def GetAllConstructionList(log,whichDB, type,state='在用'):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    if state == '全部':
        sql = """SELECT `图纸号`,`宽度`,`厚度`,`重量`,`图纸状态`,`图纸文件名`,`图纸大类` from `构件图纸信息表` """
    else:
        sql = """SELECT `图纸号`,`宽度`,`厚度`,`重量`,`图纸状态`,`图纸文件名`,`图纸大类` from `构件图纸信息表` where `图纸状态`='%s'"""%state
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp

def SaveBluePrintInDB(log,whichDB,data):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "INSERT INTO 图纸信息(`图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`,`热压100`," \
          "`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,'打包9000',`创建时间`,`备注`,`a使能`,`a`," \
          "`b使能`,`b`,`c使能`,`c`,`d使能`,`d`,`e使能`,`e`,`f使能`,`f`," \
          "`CY使能`,`CY`,`图纸名`)" \
          "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
          "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
          % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],
             data[10],data[11],data[12],data[13],data[14],data[15],data[16],data[17],data[18],data[19],
             data[20],data[21],data[22],data[23],data[24],data[25],data[26],data[27],data[28],data[29],data[30],data[31],data[32])
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
    db.close()

def UpdateBluePrintInDB(log,whichDB,data):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "UPDATE 图纸信息 SET `面板增量`='%s',`中板增量`='%s',`背板增量`='%s',`剪板505`='%s',`成型405`='%s'," \
          "`成型409`='%s',`成型406`='%s',`折弯652`='%s',`热压100`='%s',`热压306`='%s',`冲铣`='%s',`图纸状态`='%s',`创建人`='%s'," \
          "`中板`='%s',`打包9000`='%s',`图纸大类`='%s',`创建时间`='%s',`备注`='%s' WHERE `图纸号` = '%s'" \
          % (data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],
             data[13],data[14],data[15],data[16],datetime.date.today(),data[17],data[0])
    # sql = "INSERT INTO 图纸信息(`图纸号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`," \
    #       "`热压100`,`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,`打包9000`,`图纸大类`,`创建时间`,`备注`)" \
    #       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
    #       % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],datetime.date.today(),data[17])
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
    db.close()

def GetTableListFromDB(log,whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = "select table_name from information_schema.tables where table_schema='%s'"%orderDBName[whichDB]
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    result=[]
    for i in temp:
        result.append(i[0])
    return 0, result

def InsertNewOrderRecord(log,whichDB):
    return

def CreateNewOrderSheet(log,whichDB,newOrderID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """CREATE TABLE `%d` (
            `Index` INT(11) NOT NULL AUTO_INCREMENT,
            `订单号` INT(11) NOT NULL,
            `子订单号` INT(11) NOT NULL,
            `甲板` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `区域` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `房间` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `图纸` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `产品类型` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `面板代码` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `数量` INT(11) NOT NULL,
            `宽度` INT(11) NOT NULL,
            `高度` INT(11) NOT NULL,
            `厚度` INT(11) NOT NULL,
            `X面材质` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `X面颜色` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `Y面材质` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `Y面颜色` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `Z面材质` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `Z面颜色` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `V面材质` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `V面颜色` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `备注` TEXT NOT NULL COLLATE 'utf8_general_ci',
            `重量` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `胶水单编号` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `胶水单注释` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `所处工位` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            `状态` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
            PRIMARY KEY (`Index`) USING BTREE
        )
        COLLATE='utf8_general_ci'
        ENGINE=InnoDB
        AUTO_INCREMENT=0
        ;
        """%newOrderID
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error")
        db.rollback()
    db.close()

def InsertNewOrderRecord(log,whichDB,newOrderID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    # sql = "INSERT INTO 订单信息(`订单编号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`," \
    #       "`热压100`,`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,`打包9000`,`图纸大类`,`创建时间`,`备注`)" \
    #       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
    #       % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],datetime.date.today(),data[17])
    sql = "INSERT INTO 订单信息(`订单编号`) VALUES (%s)" % (newOrderID)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
    db.close()

def GetOrderDetailRecord(log, whichDB, orderDetailID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `Index`,`订单号`,`子订单号`,`甲板`,`区域`,`房间`,`图纸`,`面板代码`,`X面颜色`,`Y面颜色`,`高度`,`宽度`,`厚度`,`数量`,`Z面颜色`,`V面颜色` from `%s` """%(str(orderDetailID))
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp

def InsertOrderDetailRecord(log,whichDB,OrderID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    # sql = "INSERT INTO 订单信息(`订单编号`,`面板增量`,`中板增量`,`背板增量`,`剪板505`,`成型405`,`成型409`,`成型406`,`折弯652`," \
    #       "`热压100`,`热压306`,`冲铣`,`图纸状态`,`创建人`,`中板`,`打包9000`,`图纸大类`,`创建时间`,`备注`)" \
    #       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
    #       % (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],datetime.date.today(),data[17])
    sql = "INSERT INTO '%s'(`订单号`) VALUES (%s)" % (OrderID,1)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
    db.close()

def InsertBatchOrderDataIntoDB(log, whichDB, orderTabelName, orderDataList):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % orderDBName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    for data in orderDataList:
        if data[10]==None:
            data[10]=0
        if data[11]==None:
            data[11]=0
        sql="""INSERT INTO `%d`(`订单号`,`子订单号`,`产品类型`,`图纸`,`面板代码`,`X面颜色`,`Y面颜色`,`Z面颜色`,`V面颜色`,`高度`,`宽度`,`厚度`,`甲板`,`区域`,`房间`,`数量`)
        VALUES (%d,%d,'%s','%s','%s','%s','%s','%s','%s',%d,%d,%d,'%s','%s','%s',%d)"""\
            %(int(orderTabelName),int(orderTabelName),int(data[0]),data[1],data[3],data[4],data[5],data[6],data[7],data[8],int(data[9]),int(data[10]),int(data[11]),data[12],data[13],data[14],int(data[15]))
        cursor.execute(sql)
        try:
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            db.rollback()
    db.close()
