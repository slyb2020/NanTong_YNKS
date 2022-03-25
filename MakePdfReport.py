from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import time
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
    simple_table_with_style(filename)
    myCanvas.save()



def form_letter():
    doc = SimpleDocTemplate("form_letter.pdf",
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=18)
    flowables = []
    logo = "bitmaps/python_logo.png"
    magName = "Pythonista"
    issueNum = 12
    subPrice = "99.00"
    limitedDate = "03/05/2010"
    freeGift = "tin foil hat"

    formatted_time = time.ctime()
    full_name = "Mike Driscoll"
    address_parts = ["411 State St.", "Waterloo, IA 50158"]

    im = Image(logo, 0.5 * inch, 0.5 * inch)
    flowables.append(im)

    styles = getSampleStyleSheet()
    # Modify the Normal Style
    styles["Normal"].fontSize = 12
    styles["Normal"].leading = 14

    # Create a Justify style
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    flowables.append(Paragraph(formatted_time, styles["Normal"]))
    flowables.append(Spacer(1, 12))

    # Create return address
    flowables.append(Paragraph(full_name, styles["Normal"]))
    for part in address_parts:
        flowables.append(Paragraph(part.strip(), styles["Normal"]))

    flowables.append(Spacer(1, 12))
    ptext = 'Dear {}:'.format(full_name.split()[0].strip())
    flowables.append(Paragraph(ptext, styles["Normal"]))
    flowables.append(Spacer(1, 12))

    ptext = '''
    We would like to welcome you to our subscriber
    base for {magName} Magazine! You will receive {issueNum} issues at
    the excellent introductory price of ${subPrice}. Please respond by
    {limitedDate} to start receiving your subscription and get the
    following free gift: {freeGift}.
    '''.format(magName=magName,
               issueNum=issueNum,
               subPrice=subPrice,
               limitedDate=limitedDate,
               freeGift=freeGift)
    flowables.append(Paragraph(ptext, styles["Justify"]))
    flowables.append(Spacer(1, 12))

    ptext = '''Thank you very much and we look
    forward to serving you.'''

    flowables.append(Paragraph(ptext, styles["Justify"]))
    flowables.append(Spacer(1, 12))
    ptext = 'Sincerely,'
    flowables.append(Paragraph(ptext, styles["Normal"]))
    flowables.append(Spacer(1, 48))
    ptext = 'Ima Sucker'
    flowables.append(Paragraph(ptext, styles["Normal"]))
    flowables.append(Spacer(1, 12))
    doc.build(flowables)


if __name__ == '__main__':
    # form_letter()
    MakeMaterialScheduleTemplate("test.pdf")


