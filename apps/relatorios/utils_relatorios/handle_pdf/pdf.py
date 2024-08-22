from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Flowable, Spacer
from io import BytesIO


HEADER_COLOR = colors.HexColor("#010166")
HEADER_FONT_SIZE = 24
TABLE_HEADER_BACKGROUND = colors.gray
TABLE_HEADER_TEXT_COLOR = colors.whitesmoke
HEADER_HEIGHT = 30 

TABLE_STYLE = [
    ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BACKGROUND),
    ('TEXTCOLOR', (0, 0), (-1, 0), TABLE_HEADER_TEXT_COLOR),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, 0), 12)
]

class Header(Flowable):
    def __init__(self, text, width, height):
        super().__init__()
        self.text = text
        self.width = width
        self.height = height

    def draw(self):
        self.canv.setFillColor(HEADER_COLOR)
        self.canv.rect(0, 0, self.width, 50, fill=True)
        self.canv.setFillColor(colors.white)
        self.canv.setFont("Helvetica-Bold", HEADER_FONT_SIZE)
        self.canv.drawCentredString(self.width / 2.0, 15, self.text)

def create_pdf(data, file_like_object):
    doc = SimpleDocTemplate(file_like_object, pagesize=letter, topMargin=70, bottomMargin=50, leftMargin=5, rightMargin=5)

    def add_header(canvas, doc):
        header = Header("RELATÓRIO MENSAL", doc.width, HEADER_HEIGHT)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - 30)

    elements = []

    table = Table(data, colWidths=[doc.width / len(data[0])] * len(data[0]), repeatRows=1)
    style = TableStyle(TABLE_STYLE)
    for i, row in enumerate(data[1:], 1): 
        bg_color = colors.lightgrey if i % 2 == 1 else colors.whitesmoke
        style.add('BACKGROUND', (0, i), (-1, i), bg_color)
    table.setStyle(style)
    elements.append(table)

    doc.build(elements, onFirstPage=add_header, onLaterPages=add_header)
