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
    sql = """SELECT `订单编号`,`客户名称`,`产品名称`,`产品数量`,`订单交货日期`,`下单时间`,`下单员ID`,`状态` from `订单信息` """
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    return 0, temp

