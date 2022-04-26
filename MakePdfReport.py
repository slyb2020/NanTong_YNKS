from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import time,datetime
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from ID_DEFINE import *
from BarCodeGenerator import BarCodeGenerator

pdfmetrics.registerFont(TTFont('SimSun', 'Font/SimSun.ttf'))  #注册字体


def DrawLine(my_canvas,lineWidth,startX,startY,endX,endY):
    my_canvas.setLineWidth(lineWidth)
    my_canvas.line(startX, startY, endX, endY)


def coord(x, y, height, unit=1):
    x, y = x * unit, height -  y * unit
    return x, y

# def simple_table_with_style(filename):
#     doc = SimpleDocTemplate(filename, pagesize=letter)
#     story = []
#
#     data = [['col_{}'.format(x) for x in range(1, 6)],
#             [str(x) for x in range(1, 6)],
#             ['a', 'b', 'c', 'd', 'e']
#             ]
#
#     tblstyle = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.red),
#                            ('TEXTCOLOR', (0, 1), (-1, 1), colors.blue)
#                            ])
#
#     tbl = Table(data)
#     tbl.setStyle(tblstyle)
#     story.append(tbl)
#
#     doc.build(story)

def DrawMaterialSchedule(c,page,pageDivision):
    I = Image(bitmapDir+"/PVC.jpg")
    styleSheet = getSampleStyleSheet()
    I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
    I.drawWidth = 1.25 * inch
    P0 = Paragraph('''
         <b>A pa<font color=red>r</font>a<i>graph</i></b>
         <super><font color=yellow>1</font></super>''',
                   styleSheet["BodyText"])
    P = Paragraph('''
         <para align=center spaceb=3>The <b>ReportLab Left
         <font color=red>Logo</font></b>
         Image</para>''',
                  styleSheet["BodyText"])
    Title1 = Paragraph('<font name="SimSun">序号</font>')
    Title2 = Paragraph('<font name="SimSun">颜色</font>')
    Title3 = Paragraph('<font name="SimSun">板材厚度(mm)</font>')
    Title4 = Paragraph('<font name="SimSun">板材宽度(mm)</font>')
    Title5 = Paragraph('<font name="SimSun">出库量(米)</font>')
    Title6 = Paragraph('<font name="SimSun">当前库存量(米)</font>')
    Title7 = Paragraph('<font name="SimSun">签名</font>')
    data = [
            [Title1, Title2, Title3, Title4, Title5, Title6, Title7],
        ]
    for record in page:
        data.append(record)

    tableColWidths = [15.0 * mm, 27.5 * mm, 27.5 * mm, 35 * mm, 25.0 * mm, (186.5 - 155.0) * mm, 25.0 * mm]
    tableStyle=[
                    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # 类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
                    ('BOX', (0, 0), (-1, -1), 2, colors.black),
                    # ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.khaki),
                ]
    exSeper = pageDivision[0]
    for seperation in pageDivision[1:]:
        if seperation>1:
            sepeTemp=('SPAN',(1,exSeper),(1,seperation-1))
            tableStyle.append(sepeTemp)
            sepeTemp=('SPAN',(2,exSeper),(2,seperation-1))
            tableStyle.append(sepeTemp)
            exSeper = seperation
    tableStyle.append(('SPAN',(1,exSeper),(1,-1)))
    tableStyle.append(('SPAN',(2,exSeper),(2,-1)))
    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    startY=8+(36-len(data))*6.3
    t.drawOn(c, 12.5 * mm, startY * mm)

def MakeMaterialScheduleTemplate(orderID,subOrderID,filename,horizontalData,cuttingData,PAGEROWNUMBER=35):
    num=1
    index = 1
    pages = []
    pageDivision = []
    data = []
    seperation = []
    for type in horizontalData:
        for record in type:
            length=0
            seperation.append(num)
            for board in record[3]:
                length+=int(board[0])*int(board[1])
            temp=[index,record[0],record[1],record[2],float(length)/1000.,'','']
            data.append(temp)
            num+=1
            index+=1
            if num>PAGEROWNUMBER:
                num = 1
                pages.append(data)
                pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
                seperation=[1]
                data=[]
    # if len(data)>0:
        # pages.append(data)
        # pageDivision.append(seperation)
    for type in cuttingData:
        length=0
        seperation.append(num)
        for board in type:
            length+=int(board[0][3])*int(board[0][4])
        temp=[index,type[0][0][0],type[0][0][1],type[0][0][2],float(length)/1000.]
        data.append(temp)
        num+=1
        index+=1
        if num>PAGEROWNUMBER:
            num = 1
            pages.append(data)
            pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
            seperation=[1]
            data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
    # print("pages=",pages)
    # print("pageDivision",pageDivision)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司原材料出库单")
        myCanvas.drawImage(bitmapDir+"/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='M'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode)
        myCanvas.drawImage(dirName+"/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("SimSun", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd Plate Outbound Delivery Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawMaterialSchedule(myCanvas,page,pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def DrawVerticalCutSchedule(c,record,pageDivision):
    # if pageDivision[0] == pageDivision[1]:
    I = Image("D:\\WorkSpace\\Python\\NanTong_YNKS\\bitmaps\\PVC.jpg")
    styleSheet = getSampleStyleSheet()
    I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
    I.drawWidth = 1.25 * inch
    P0 = Paragraph('''
         <b>A pa<font color=red>r</font>a<i>graph</i></b>
         <super><font color=yellow>1</font></super>''',
                   styleSheet["BodyText"])
    P = Paragraph('''
         <para align=center spaceb=3>The <b>ReportLab Left
         <font color=red>Logo</font></b>
         Image</para>''',
                  styleSheet["BodyText"])
    Title1 = Paragraph('<font name="SimSun">序号</font>')
    Title2 = Paragraph('<font name="SimSun">原料板材颜色</font>')
    Title3 = Paragraph('<font name="SimSun">原料板材厚度mm</font>')
    Title4 = Paragraph('<font name="SimSun">原料板材宽度mm</font>')
    Title5 = Paragraph('<font name="SimSun">横剪长度mm</font>')
    Title6 = Paragraph('<font name="SimSun">数量</font>')
    title = [Title1, Title2, Title3, Title4, Title5, Title6]
    tableColWidths = [20.0 * mm, 40.0 * mm, 40.0 * mm, 40.0 * mm,30.0 * mm, 20 * mm]
# data = [
#         [Title1, Title2, Title3, Title4, Title5, Title6, Title7, Title8, Title9, Title10, Title11, Title12, Title13, Title14],
#         ['0', '9GLAV', '0.56', '1234', '2400', '37', '110', '110', '110', '110', '110', '110', '30','100'],
#         ['1', '9GLAV', '0.56', '1234', '2400', '37', '111', '111', '111', '110', '110', '110', '20','100'],
#         ['2', '9GLAV', '0.56', '1234', '2400', '37', '112', '112', '112', '110', '110', '110', '50','100'],
#     ]
#     data = pages[0]
    data= [title]
    for row in record:
        data.append(row)
    tableStyle=[
               ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
               ('GRID', (0, 0), (-1, -1), 0.5, colors.black),       #   类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
               ('BOX', (0, 0), (-1, -1), 2, colors.black),
               ('BACKGROUND', (0, 0), (-1, 0), colors.khaki),
               ('BACKGROUND', (4, 1), (5, -1), colors.beige),
               ('BACKGROUND', (6, 1), (6, -1), colors.lavender),
               ('LINEABOVE', (0, 1), (-1, 1), 2, colors.black),
               ('LINEBEFORE', (4, 0), (4, -1), 2, colors.black),
               ('LINEBEFORE', (6, 0), (6, -1), 2, colors.black),
               ('LINEBEFORE', (-1, 0), (-1, -1), 2, colors.black),
               ('VALIGN', (1, 1), (5, 6), 'MIDDLE'),
               ('VALIGN', (1, 7), (5, -1), 'MIDDLE'),
               ]
    exSeper = pageDivision[0]
    for seperation in pageDivision[1:]:
        if seperation>1:
            sepeTemp=('SPAN',(1,exSeper),(1,seperation-1))
            tableStyle.append(sepeTemp)
            sepeTemp=('SPAN',(2,exSeper),(2,seperation-1))
            tableStyle.append(sepeTemp)
            sepeTemp=('SPAN',(3,exSeper),(3,seperation-1))
            tableStyle.append(sepeTemp)
            exSeper = seperation
    tableStyle.append(('SPAN',(1,exSeper),(1,-1)))
    tableStyle.append(('SPAN',(2,exSeper),(2,-1)))
    tableStyle.append(('SPAN',(3,exSeper),(3,-1)))
    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    startY=8+(36-len(data))*6.3
    t.drawOn(c, 12.5 * mm, startY * mm)

def MakeHorizontalCutScheduleTemplate(orderID, subOrderID, filename, record=[],PAGEROWNUMBER=35):
    num=1
    index = 1
    pages = []
    pageDivision = []
    data = []
    seperation = []
    for type in record:
        for board in type:
            seperation.append(num)
            for item in board[-1]:
                temp=[index,board[0],board[1],board[2],item[0],item[1]]
                data.append(temp)
                num+=1
                index+=1
                if num>PAGEROWNUMBER:
                    num = 1
                    pages.append(data)
                    pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
                    seperation=[1]
                    data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司横剪任务单")
        myCanvas.drawImage(bitmapDir+"/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='H'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode)
        myCanvas.drawImage(dirName+"/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("SimSun", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd Plate Horizontal Shear Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawVerticalCutSchedule(myCanvas,page,pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def DrawCutSchedule(c,record,colNum,pageDivision):
    # if pageDivision[0] == pageDivision[1]:
    I = Image("D:\\WorkSpace\\Python\\NanTong_YNKS\\bitmaps\\PVC.jpg")
    styleSheet = getSampleStyleSheet()
    I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
    I.drawWidth = 1.25 * inch
    P0 = Paragraph('''
         <b>A pa<font color=red>r</font>a<i>graph</i></b>
         <super><font color=yellow>1</font></super>''',
                   styleSheet["BodyText"])
    P = Paragraph('''
         <para align=center spaceb=3>The <b>ReportLab Left
         <font color=red>Logo</font></b>
         Image</para>''',
                  styleSheet["BodyText"])
    Title1 = Paragraph('<font name="SimSun">序号</font>')
    Title2 = Paragraph('<font name="SimSun">板材颜色</font>')
    Title3 = Paragraph('<font name="SimSun">板厚</font>')
    Title4 = Paragraph('<font name="SimSun">板宽</font>')
    Title5 = Paragraph('<font name="SimSun">横切长</font>')
    Title6 = Paragraph('<font name="SimSun">数量</font>')
    Title7 = Paragraph('<font name="SimSun">纵切1</font>')
    Title8 = Paragraph('<font name="SimSun">纵切2</font>')
    Title9 = Paragraph('<font name="SimSun">纵切3</font>')
    Title10 = Paragraph('<font name="SimSun">纵切4</font>')
    Title11 = Paragraph('<font name="SimSun">纵切5</font>')
    Title12 = Paragraph('<font name="SimSun">纵切6</font>')
    Title13 = Paragraph('<font name="SimSun">纵切7</font>')
    Title14 = Paragraph('<font name="SimSun">纵切8</font>')
    Title15 = Paragraph('<font name="SimSun">纵切9</font>')
    Title16 = Paragraph('<font name="SimSun">纵切10</font>')
    Title17 = Paragraph('<font name="SimSun">纵切11</font>')
    Title18 = Paragraph('<font name="SimSun">纵切12</font>')
    Title19 = Paragraph('<font name="SimSun">纵切13</font>')
    Title20 = Paragraph('<font name="SimSun">纵切14</font>')
    Title21 = Paragraph('<font name="SimSun">数量</font>')
    TitleList = [Title1, Title2, Title3, Title4, Title5, Title6, Title7, Title8, Title9, Title10,
                 Title11, Title12, Title13, Title14, Title15, Title16, Title17, Title18, Title19, Title20, Title21]
    # if colNum>7:
    #     print("xxxxxxx   colNum>7",colNum)
    #     colNum=7
    #     for x in record:
    #         print(x)
    colWidth = 13.5*7/colNum
    tableColWidthsList = [12.0 * mm, 19.0 * mm, 12.0 * mm, 12.0 * mm, 16.0 * mm, 12.0 * mm, colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm,
                          colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm, 12.0 * mm]
    title = TitleList[:colNum+6]
    title.append(Title21)
    tableColWidths = tableColWidthsList[:colNum+6]
    tableColWidths.append(tableColWidthsList[-1])
# data = [
#         [Title1, Title2, Title3, Title4, Title5, Title6, Title7, Title8, Title9, Title10, Title11, Title12, Title13, Title14],
#         ['0', '9GLAV', '0.56', '1234', '2400', '37', '110', '110', '110', '110', '110', '110', '30','100'],
#         ['1', '9GLAV', '0.56', '1234', '2400', '37', '111', '111', '111', '110', '110', '110', '20','100'],
#         ['2', '9GLAV', '0.56', '1234', '2400', '37', '112', '112', '112', '110', '110', '110', '50','100'],
#     ]
#     data = pages[0]
    data= [title]
    for row in record:
        temp = ['']*(colNum+7)
        for k in range(len(row)-1):
            temp[k]=row[k]
        temp[-1]=row[-1]
        data.append(temp)
    tableStyle=[
               ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
               ('GRID', (0, 0), (-1, -1), 0.5, colors.black),       #   类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
               ('BOX', (0, 0), (-1, -1), 2, colors.black),
               ('BACKGROUND', (0, 0), (-1, 0), colors.khaki),
               ('BACKGROUND', (4, 1), (5, -1), colors.beige),
               ('BACKGROUND', (6, 1), (-1, -1), colors.lavender),
               ('LINEABOVE', (0, 1), (-1, 1), 2, colors.black),
               ('LINEBEFORE', (4, 0), (4, -1), 2, colors.black),
               ('LINEBEFORE', (6, 0), (6, -1), 2, colors.black),
               ('LINEBEFORE', (-1, 0), (-1, -1), 2, colors.black),
               ('VALIGN', (1, 1), (5, 6), 'MIDDLE'),
               ('VALIGN', (1, 7), (5, -1), 'MIDDLE'),
               ]
    exSeper = pageDivision[0]
    for seperation in pageDivision[1:]:
        if seperation>1:
            sepeTemp=('SPAN',(1,exSeper),(1,seperation-1))
            tableStyle.append(sepeTemp)
            sepeTemp=('SPAN',(2,exSeper),(2,seperation-1))
            tableStyle.append(sepeTemp)
            sepeTemp=('SPAN',(3,exSeper),(3,seperation-1))
            tableStyle.append(sepeTemp)
            sepeTemp=('SPAN',(4,exSeper),(4,seperation-1))
            tableStyle.append(sepeTemp)
            sepeTemp=('SPAN',(5,exSeper),(5,seperation-1))
            tableStyle.append(sepeTemp)
            exSeper = seperation
    tableStyle.append(('SPAN',(1,exSeper),(1,-1)))
    tableStyle.append(('SPAN',(2,exSeper),(2,-1)))
    tableStyle.append(('SPAN',(3,exSeper),(3,-1)))
    tableStyle.append(('SPAN',(4,exSeper),(4,-1)))
    tableStyle.append(('SPAN',(5,exSeper),(5,-1)))
    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    startY=8+(36-len(data))*6.3
    t.drawOn(c, 12.5 * mm, startY * mm)

def MakeCutScheduleTemplate(orderID,subOrderID,filename,record=[],PAGEROWNUMBER=35):
    num=1
    index = 1
    pages = []
    pageDivision = []
    pageMaxList = []
    data = []
    seperation = []
    pageMaxvCuttingCol=0
    for type in record:
        for board in type:
            seperation.append(num)
            for item in board[1]:
                temp=[index,board[0][0],board[0][1],board[0][2],board[0][3],board[0][4]]
                for vCutting in item[0]:
                    temp.append(vCutting)
                temp.append(item[1])
                data.append(temp)
                if len(item[0])>pageMaxvCuttingCol:
                    pageMaxvCuttingCol=len(item[0])
                num+=1
                index+=1
                if num>PAGEROWNUMBER:
                    num = 1
                    pages.append(data)

                    pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
                    pageMaxList.append(pageMaxvCuttingCol)
                    pageMaxvCuttingCol = 1
                    seperation=[1]
                    data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
        pageMaxList.append(pageMaxvCuttingCol)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司剪板机任务单")
        myCanvas.drawImage(bitmapDir+"/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='C'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode)
        myCanvas.drawImage(dirName+"/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("SimSun", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd Plate Shear Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawCutSchedule(myCanvas,page,pageMaxList[i],pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def DrawBendingSchedule(c,record,pageDivision):
    # if pageDivision[0] == pageDivision[1]:
    I = Image("D:\\WorkSpace\\Python\\NanTong_YNKS\\bitmaps\\PVC.jpg")
    styleSheet = getSampleStyleSheet()
    I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
    I.drawWidth = 1.25 * inch
    P0 = Paragraph('''
             <b>A pa<font color=red>r</font>a<i>graph</i></b>
             <super><font color=yellow>1</font></super>''',
                   styleSheet["BodyText"])
    P = Paragraph('''
             <para align=center spaceb=3>The <b>ReportLab Left
             <font color=red>Logo</font></b>
             Image</para>''',
                  styleSheet["BodyText"])
    Title1 = Paragraph('<font name="SimSun">序号</font>')
    Title2 = Paragraph('<font name="SimSun">面板代码</font>')
    Title3 = Paragraph('<font name="SimSun">图纸号</font>')
    Title4 = Paragraph('<font name="SimSun">长度</font>')
    Title5 = Paragraph('<font name="SimSun">宽度</font>')
    Title6 = Paragraph('<font name="SimSun">厚度</font>')
    Title7 = Paragraph('<font name="SimSun">X面颜色</font>')
    Title8 = Paragraph('<font name="SimSun">Y面颜色</font>')
    Title9 = Paragraph('<font name="SimSun">Z面颜色</font>')
    Title10 = Paragraph('<font name="SimSun">V面颜色</font>')
    Title11 = Paragraph('<font name="SimSun">数量</font>')
    Title12 = Paragraph('<font name="SimSun">胶水单号</font>')
    title = [Title1, Title2, Title3, Title4, Title5, Title6, Title7, Title8, Title9, Title10,Title11,Title12]
    tableColWidths = [11.5*mm,25.0*mm,25.0*mm,11.5*mm,11.5*mm,11.5*mm,17*mm,17*mm,17*mm,17*mm,11.5*mm,25*mm]
    data = [title]
    for row in record:
        data.append(row)
    tableStyle = [
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # 类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.khaki),
        # ('BACKGROUND', (2, 1), (2, -1), colors.pink),
        # ('BACKGROUND', (3, 1), (5, -1), colors.beige),
        # ('BACKGROUND', (6, 1), (10, -1), colors.lavender),

        ('LINEABOVE', (0, 1), (-1, 1), 2, colors.black),
        ('LINEBEFORE', (2, 0), (2, -1), 2, colors.black),
        ('LINEBEFORE', (3, 0), (3, -1), 2, colors.black),
        ('LINEBEFORE', (6, 0), (6, -1), 2, colors.black),
        ('LINEBEFORE', (10, 0), (10, -1), 2, colors.black),
        ('LINEBEFORE', (-1, 0), (-1, -1), 2, colors.black),
        ('VALIGN', (1, 1), (5, 6), 'MIDDLE'),
        ('VALIGN', (1, 7), (5, -1), 'MIDDLE'),
    ]
    for i in range(len(record)):
        if i%2 == 1:
           tableStyle.append(('BACKGROUND', (0, i+1), (-1, i+1), colors.lavender))

    t = Table(data, style=tableStyle, colWidths=tableColWidths)
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    startY = 8 + (36 - len(data)) * 6.3
    t.drawOn(c, 8 * mm, startY * mm)

def MakeBendingScheduleTemplate(orderID,subOrderID,filename,record=[],PAGEROWNUMBER=35):
    #1, 64730, '1', '3', '9', 'Corridor', 'A.2SA.0900', '0', 'YC74H', 'YQ73D', '2160', '550', '50', 2, 'None', 'None'
    num=1
    index = 1
    pages = []
    pageDivision = []
    data = []
    seperation = []
    for board in record:
        seperation.append(num)
        board=list(board)
        if board[14]=='None':
            board[14]=''
        if board[15]=='None':
            board[15]=''
        temp=[index,board[7],board[6],board[10],board[11],board[12],board[8],board[9],board[14],board[15],board[13]]
        data.append(temp)
        num+=1
        index+=1
        if num>PAGEROWNUMBER:
            num = 1
            pages.append(data)
            pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
            seperation=[1]
            data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司折弯任务单")
        myCanvas.drawImage(bitmapDir+"/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='B'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode)
        myCanvas.drawImage(dirName+"/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("SimSun", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd Bending Machine Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawBendingSchedule(myCanvas,page,pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def MakeS2FormingScheduleTemplate(orderID,subOrderID,filename,record=[],PAGEROWNUMBER=35):
    #1, 64730, '1', '3', '9', 'Corridor', 'A.2SA.0900', '0', 'YC74H', 'YQ73D', '2160', '550', '50', 2, 'None', 'None'
    num=1
    index = 1
    pages = []
    pageDivision = []
    data = []
    seperation = []
    for board in record:
        seperation.append(num)
        board=list(board)
        if board[14]=='None':
            board[14]=''
        if board[15]=='None':
            board[15]=''
        temp=[index,board[7],board[6],board[10],board[11],board[12],board[8],board[9],board[14],board[15],board[13]]
        data.append(temp)
        num+=1
        index+=1
        if num>PAGEROWNUMBER:
            num = 1
            pages.append(data)
            pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
            seperation=[1]
            data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司2S成型任务单")
        myCanvas.drawImage(bitmapDir+"/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='S'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode)
        myCanvas.drawImage(dirName+"/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("SimSun", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd S2 Forming Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawBendingSchedule(myCanvas,page,pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def MakeCeilingFormingScheduleTemplate(orderID,subOrderID,filename,record=[],PAGEROWNUMBER=35):
    #1, 64730, '1', '3', '9', 'Corridor', 'A.2SA.0900', '0', 'YC74H', 'YQ73D', '2160', '550', '50', 2, 'None', 'None'
    num=1
    index = 1
    pages = []
    pageDivision = []
    data = []
    seperation = []
    for board in record:
        seperation.append(num)
        board=list(board)
        if board[14]=='None':
            board[14]=''
        if board[15]=='None':
            board[15]=''
        temp=[index,board[7],board[6],board[10],board[11],board[12],board[8],board[9],board[14],board[15],board[13]]
        data.append(temp)
        num+=1
        index+=1
        if num>PAGEROWNUMBER:
            num = 1
            pages.append(data)
            pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
            seperation=[1]
            data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司天花板成型任务单")
        myCanvas.drawImage(bitmapDir+"/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='E'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode)
        myCanvas.drawImage(dirName+"/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("SimSun", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd Ceiling Forming Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawBendingSchedule(myCanvas,page,pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def MakePRPressScheduleTemplate(orderID,subOrderID,filename,record=[],PAGEROWNUMBER=35):
    #1, 64730, '1', '3', '9', 'Corridor', 'A.2SA.0900', '0', 'YC74H', 'YQ73D', '2160', '550', '50', 2, 'None', 'None'
    num=1
    index = 1
    pages = []
    pageDivision = []
    data = []
    seperation = []
    for board in record:
        seperation.append(num)
        board=list(board)
        if board[14]=='None':
            board[14]=''
        if board[15]=='None':
            board[15]=''
        temp=[index,board[7],board[6],board[10],board[11],board[12],board[8],board[9],board[14],board[15],board[13]]
        data.append(temp)
        num+=1
        index+=1
        if num>PAGEROWNUMBER:
            num = 1
            pages.append(data)
            pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
            seperation=[1]
            data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司PR热压任务单")
        myCanvas.drawImage(bitmapDir+"/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='P'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode)
        myCanvas.drawImage(dirName+"/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("SimSun", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd PR Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawBendingSchedule(myCanvas,page,pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def MakeVacuumScheduleTemplate(orderID,subOrderID,filename,record=[],PAGEROWNUMBER=35):
    #1, 64730, '1', '3', '9', 'Corridor', 'A.2SA.0900', '0', 'YC74H', 'YQ73D', '2160', '550', '50', 2, 'None', 'None'
    num=1
    index = 1
    pages = []
    pageDivision = []
    data = []
    seperation = []
    for board in record:
        seperation.append(num)
        board=list(board)
        if board[14]=='None':
            board[14]=''
        if board[15]=='None':
            board[15]=''
        temp=[index,board[7],board[6],board[10],board[11],board[12],board[8],board[9],board[14],board[15],board[13]]
        data.append(temp)
        num+=1
        index+=1
        if num>PAGEROWNUMBER:
            num = 1
            pages.append(data)
            pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
            seperation=[1]
            data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司特制品任务单")
        myCanvas.drawImage(bitmapDir+"/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='V'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode)
        myCanvas.drawImage(dirName+"/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("SimSun", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd Vacuum Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawBendingSchedule(myCanvas,page,pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

# def DrawGlueSheet(c,data):
#     # if pageDivision[0] == pageDivision[1]:
#     tableColWidths = [20*mm,20*mm,20*mm,20*mm,20*mm]
#     sheet = [0]*16
#     sheet[0] = ["合同编号：  %s-%03d"%(data[1],int(data[2]))]
#     print("sheet=",sheet)
#     tableStyle = [
#         ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
#         ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # 类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
#         ('BOX', (0, 0), (-1, -1), 2, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.khaki),
#         # ('BACKGROUND', (2, 1), (2, -1), colors.pink),
#         # ('BACKGROUND', (3, 1), (5, -1), colors.beige),
#         # ('BACKGROUND', (6, 1), (10, -1), colors.lavender),
#
#         ('LINEABOVE', (0, 1), (-1, 1), 2, colors.black),
#         ('LINEBEFORE', (2, 0), (2, -1), 2, colors.black),
#         ('LINEBEFORE', (3, 0), (3, -1), 2, colors.black),
#         # ('LINEBEFORE', (6, 0), (6, -1), 2, colors.black),
#         # ('LINEBEFORE', (10, 0), (10, -1), 2, colors.black),
#         # ('LINEBEFORE', (-1, 0), (-1, -1), 2, colors.black),
#         # ('VALIGN', (1, 1), (5, 6), 'MIDDLE'),
#         # ('VALIGN', (1, 7), (5, -1), 'MIDDLE'),
#     ]
#     t = Table(sheet, style=tableStyle, colWidths=tableColWidths)
#     t.wrapOn(c, 186.5 * mm, 800 * mm)
#     startY = 8 + (36 - len(sheet)) * 6.3
#     t.drawOn(c, 8 * mm, startY * mm)
def DrawGlueSheet(canvas,data,offset=0):
    width, height = letter
    DrawLine(canvas, 1, *coord(20, 40+offset, height, mm), *coord(190, 40+offset, height, mm))


def MakeGlueNoSheetTemplate(orderID,subOrderID,filename,record=[]):
    #1, 64730, '1', '3', '9', 'Corridor', 'A.2SA.0900', '0', 'YC74H', 'YQ73D', '2160', '550', '50', 2, 'None', 'None','胶水单号'
    num=1
    index = 1
    pages = []
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for board in record[:10]:
        data=list(board)
        if data[14]=='None':
            data[14]=''
        if data[15]=='None':
            data[15]=''
        for i in range(data[13]):
            myCanvas.setFont("SimSun", 18)
            myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司胶水单")
            myCanvas.drawImage(bitmapDir+"/logo.jpg", 30, 715,
                                width=40, height=40)
            tempCode='G'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
            BarCodeGenerator(tempCode)
            myCanvas.drawImage(dirName+"/tempBarcode.png", width-100, height-40,
                                width=100, height=40)
            myCanvas.setFont("SimSun", 12)
            myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd Glue Sheet")
            DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
            myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
            myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
            # simple_table_with_style(filename)
            DrawGlueSheet(myCanvas,data)

            print("height,width=",height,width)
            DrawLine(myCanvas,1,*coord(00, 140, height, mm),*coord(220, 140, height, mm))

            offset = 380
            myCanvas.setFont("SimSun", 18)
            myCanvas.drawCentredString(width/2,735-offset, text="伊纳克赛(南通)精致内饰材料有限公司胶水单")
            myCanvas.drawImage(bitmapDir+"/logo.jpg", 30, 715-offset,
                                width=40, height=40)
            tempCode='G'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
            BarCodeGenerator(tempCode)
            myCanvas.drawImage(dirName+"/tempBarcode.png", width-100, height-40-offset-35,
                                width=100, height=40)
            myCanvas.setFont("SimSun", 12)
            offset2=135
            myCanvas.drawCentredString(width/2,715-offset, text="Inexa (NanTong) Interiors Co.Ltd Glue Sheet")
            DrawLine(myCanvas,1,*coord(10, 31+offset2, height, mm),*coord(200, 31+offset2, height, mm))
            myCanvas.drawString(40,685-offset, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
            myCanvas.drawRightString(width-50, 685-offset, '出单日期：%s'%(datetime.date.today()))
            # simple_table_with_style(filename)
            DrawGlueSheet(myCanvas,data,offset=offset2)
            myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
            myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def DrawFormingSchedule(c):
    Title1 = Paragraph('<font name="SimSun">序号</font>')
    Title2 = Paragraph('<font name="SimSun">胶水单</font>')
    Title3 = Paragraph('<font name="SimSun">图纸</font>')
    Title4 = Paragraph('<font name="SimSun">长度</font>')
    Title5 = Paragraph('<font name="SimSun">宽度</font>')
    Title6 = Paragraph('<font name="SimSun">厚度</font>')
    Title7 = Paragraph('<font name="SimSun">X</font>')
    Title8 = Paragraph('<font name="SimSun">Y</font>')
    Title9 = Paragraph('<font name="SimSun">Z</font>')
    Title10 = Paragraph('<font name="SimSun">V</font>')
    Title11 = Paragraph('<font name="SimSun">数量</font>')
    data = [
            [Title1, Title2, Title3, Title4, Title5, Title6, Title7, Title8, Title9, Title10, Title11],
            ['1', '1122', 'N.2SA.0001', '1495','548', '50','79070','Y1058','','','1'],
            ['2', '1122', 'CC64001',    '1495','548', '25','RAL1101','G','','','2'],
            ['3', '1122', 'N.2SA.0001', '1495','548', '100','79070','G','','','3'],
            ['4', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','4'],
            ['5', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','5'],
            ['6', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','23'],
            ['7', '1122', 'CC64001',    '1495','548', '25','79070','G','','','2'],
            ['8', '1122', 'N.2SA.0001', '1495','548', '100','79070','G','','','3'],
            ['9', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','34'],
            ['10', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','2'],
            ['11', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','23'],
            ['12', '1122', 'CC64001',    '1495','548', '25','79070','G','','','56'],
            ['13', '1122', 'N.2SA.0001', '1495','548', '100','79070','G','','','3'],
            ['14', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','34'],
            ['15', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','100'],
    ]
    t = Table(data, style=[
                           ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black),       #   类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
                           ('BOX', (0, 0), (-1, -1), 2, colors.black),
                           ('BACKGROUND', (0, 0), (-1, 0), colors.khaki),
                           ('BACKGROUND', (3, 1), (5, -1), colors.beige),
                           ('BACKGROUND', (6, 1), (9, -1), colors.pink),
                           # ('SPAN',(0,0),(1,0)),
                           # ('LINEABOVE', (1, 2), (-2, 2), 1, colors.blue),
                           # ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
                           # ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
                           # ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                           # ('BOX', (0, 0), (-1, -1), 2, colors.black),
                           # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                           # ('VALIGN', (3, 0), (3, 0), 'BOTTOM'),
                           # # ('ALIGN', (0, 3), (0, 3), 'CENTER'),
                           # ('BACKGROUND', (3, 0), (3, 0), colors.limegreen),
                           # ('BACKGROUND', (3, 1), (3, 1), colors.khaki),
                           # # ('ALIGN', (3, 1), (3, 1), 'CENTER'),
                           # ('BACKGROUND', (3, 2), (3, 2), colors.beige),
                           # # ('ALIGN', (3, 2), (3, 2), 'LEFT'),
                           ],colWidths=[12*mm,15.0*mm,25.0*mm,15.0*mm,15.0*mm,12.0*mm,20.0*mm,20.0*mm,20.0*mm,20*mm,22.0*mm])
    # Table(data, colWidths=[1.9 * inch] * 5)
    # t._argW[3] = 1.5 * inch
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    t.drawOn(c, 12.5 * mm, 130 * mm)
def MakeFormingScheduleTemplate(filename,data=[]):
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    myCanvas.setFont("SimSun", 18)
    myCanvas.drawCentredString(width/2,730, text="伊纳克赛(南通)精致内饰材料有限公司成型任务单")
    myCanvas.drawImage(bitmapDir+"/python_logo.png", 30, 710,
                        width=40, height=40)
    myCanvas.setFont("SimSun", 12)
    myCanvas.drawCentredString(width/2,710, text="Inexa (NanTong) Interiors Co.Ltd Forming Schedule")
    DrawLine(myCanvas,1,*coord(10, 33, height, mm),*coord(200, 33, height, mm))
    myCanvas.drawString(40,670, text="订单号；%s"%'64757-001')
    myCanvas.drawRightString(width-50, 670, '出单日期：%s'%(datetime.date.today()))
    # simple_table_with_style(filename)
    DrawFormingSchedule(myCanvas)
    myCanvas.save()


# def form_letter():
#     doc = SimpleDocTemplate("form_letter.pdf",
#                             pagesize=letter,
#                             rightMargin=72,
#                             leftMargin=72,
#                             topMargin=72,
#                             bottomMargin=18)
#     flowables = []
#     logo = bitmapDir+"/python_logo.png"
#     magName = "Pythonista"
#     issueNum = 12
#     subPrice = "99.00"
#     limitedDate = "03/05/2010"
#     freeGift = "tin foil hat"
#
#     formatted_time = time.ctime()
#     full_name = "Mike Driscoll"
#     address_parts = ["411 State St.", "Waterloo, IA 50158"]
#
#     im = Image(logo, 0.5 * inch, 0.5 * inch)
#     flowables.append(im)
#
#     styles = getSampleStyleSheet()
#     # Modify the Normal Style
#     styles["Normal"].fontSize = 12
#     styles["Normal"].leading = 14
#
#     # Create a Justify style
#     styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
#
#     flowables.append(Paragraph(formatted_time, styles["Normal"]))
#     flowables.append(Spacer(1, 12))
#
#     # Create return address
#     flowables.append(Paragraph(full_name, styles["Normal"]))
#     for part in address_parts:
#         flowables.append(Paragraph(part.strip(), styles["Normal"]))
#
#     flowables.append(Spacer(1, 12))
#     ptext = 'Dear {}:'.format(full_name.split()[0].strip())
#     flowables.append(Paragraph(ptext, styles["Normal"]))
#     flowables.append(Spacer(1, 12))
#
#     ptext = '''
#     We would like to welcome you to our subscriber
#     base for {magName} Magazine! You will receive {issueNum} issues at
#     the excellent introductory price of ${subPrice}. Please respond by
#     {limitedDate} to start receiving your subscription and get the
#     following free gift: {freeGift}.
#     '''.format(magName=magName,
#                issueNum=issueNum,
#                subPrice=subPrice,
#                limitedDate=limitedDate,
#                freeGift=freeGift)
#     flowables.append(Paragraph(ptext, styles["Justify"]))
#     flowables.append(Spacer(1, 12))
#
#     ptext = '''Thank you very much and we look
#     forward to serving you.'''
#
#     flowables.append(Paragraph(ptext, styles["Justify"]))
#     flowables.append(Spacer(1, 12))
#     ptext = 'Sincerely,'
#     flowables.append(Paragraph(ptext, styles["Normal"]))
#     flowables.append(Spacer(1, 48))
#     ptext = 'Ima Sucker'
#     flowables.append(Paragraph(ptext, styles["Normal"]))
#     flowables.append(Spacer(1, 12))
#     doc.build(flowables)


if __name__ == '__main__':
    # form_letter()
    MakeFormingScheduleTemplate("成型任务单.pdf")


