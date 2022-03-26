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



pdfmetrics.registerFont(TTFont('SimSun', 'Font/SimSun.ttf'))  #注册字体


def DrawLine(my_canvas,lineWidth,startX,startY,endX,endY):
    my_canvas.setLineWidth(lineWidth)
    my_canvas.line(startX, startY, endX, endY)


def coord(x, y, height, unit=1):
    x, y = x * unit, height -  y * unit
    return x, y

def simple_table_with_style(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []

    data = [['col_{}'.format(x) for x in range(1, 6)],
            [str(x) for x in range(1, 6)],
            ['a', 'b', 'c', 'd', 'e']
            ]

    tblstyle = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.red),
                           ('TEXTCOLOR', (0, 1), (-1, 1), colors.blue)
                           ])

    tbl = Table(data)
    tbl.setStyle(tblstyle)
    story.append(tbl)

    doc.build(story)
    print("here")

def drawBitmap(c):
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
    Title2 = Paragraph('<font name="SimSun">颜色</font>')
    Title3 = Paragraph('<font name="SimSun">板材厚度(mm)</font>')
    Title4 = Paragraph('<font name="SimSun">板材宽度(mm)</font>')
    Title5 = Paragraph('<font name="SimSun">出库量(米)</font>')
    Title6 = Paragraph('<font name="SimSun">当前库存量(米)</font>')
    Title7 = Paragraph('<font name="SimSun">签名</font>')
    data = [
            [Title1, Title2, Title3, Title4, Title5, Title6, Title7],
            ['0', '9GLAV', '0.56', 'Hoved 1234.00mm', '516.95','',''],
            ['1', 'G', '0.56', 'Hoved 1234.00mm', '516.95','',''],
            ['1', '9GLAV', '0.56', 'Hoved 1234.00mm', '516.95','',''],
            ['3', 'G', '0.56', 'Hoved 610.00mm', '516.95','',''],
            ['4', '9GLAV', '0.56', 'Hoved 694.00mm', '516.95','',''],
            ['5', 'G', '0.56', 'Hoved 164.50mm', '516.95','',''],
            ['6', '9GLAV', '0.56', 'Hoved 612.00mm', '516.95','',''],
            ['7', 'G', '0.56', 'Hoved 622.00mm', '516.95','',''],
            ['8', 'G', '0.7', 'Hoved 622.00mm', '516.95','',''],
            ['9', 'G', '1.0', 'Hoved 622.00mm', '516.95','',''],
            ['10', 'G', '1.25', 'Hoved 622.00mm', '516.95','',''],
            ['11', 'G', '0.56', 'Hoved 622.00mm', '516.95','',''],
            ['12', 'G', '0.56', 'Hoved 622.00mm', '516.95','',''],
            ['13', 'G', '0.56', 'Hoved 622.00mm', '516.95','',''],
            ['14', 'G', '0.56', 'Hoved 622.00mm', '516.95','',''],
        ]
    t = Table(data, style=[
                           ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black),       #   类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
                           ('BOX', (0, 0), (-1, -1), 2, colors.black),
                           # ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
                           ('BACKGROUND', (0, 0), (-1, 0), colors.khaki),
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
                           ],colWidths=[15.0*mm,27.5*mm,27.5*mm,35*mm,25.0*mm,(186.5-155.0)*mm,25.0*mm])
    # Table(data, colWidths=[1.9 * inch] * 5)
    # t._argW[3] = 1.5 * inch
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    t.drawOn(c, 12.5 * mm, 130 * mm)

def MakeMaterialScheduleTemplate(filename,data=[]):
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    myCanvas.setFont("SimSun", 18)
    myCanvas.drawCentredString(width/2,730, text="伊纳克赛(南通)精致内饰材料有限公司出料单")
    myCanvas.drawImage("bitmaps/python_logo.png", 30, 710,
                        width=40, height=40)
    myCanvas.setFont("SimSun", 12)
    myCanvas.drawCentredString(width/2,710, text="Inexa (NanTong) Interiors Co.Ltd Meterial Requisition")
    DrawLine(myCanvas,1,*coord(10, 33, height, mm),*coord(200, 33, height, mm))
    myCanvas.drawString(40,670, text="订单号；%s"%'15457-001')
    myCanvas.drawRightString(width-50, 670, '出单日期：%s'%(datetime.date.today()))
    # simple_table_with_style(filename)
    drawBitmap(myCanvas)
    myCanvas.save()



# def form_letter():
#     doc = SimpleDocTemplate("form_letter.pdf",
#                             pagesize=letter,
#                             rightMargin=72,
#                             leftMargin=72,
#                             topMargin=72,
#                             bottomMargin=18)
#     flowables = []
#     logo = "bitmaps/python_logo.png"
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
    MakeMaterialScheduleTemplate("出料单.pdf")


