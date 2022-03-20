from reportlab.platypus import SimpleDocTemplate, Image

from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("Hello.pdf")
styles = getSampleStyleSheet()
style = styles['Normal']
story =[]

t = Image("bitmaps/镀锌板.jpg")
story.append(t)

doc.build(story)