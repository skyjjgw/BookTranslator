from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

if not os.path.exists("test"):
    os.makedirs("test")

doc = SimpleDocTemplate("test/test_table.pdf", pagesize=letter)
elements = []
styles = getSampleStyleSheet()

elements.append(Paragraph("This is a test document with a table.", styles['Normal']))
elements.append(Paragraph("Below is the table containing user data:", styles['Normal']))

data = [
    ['Name', 'Age', 'City', 'Occupation'],
    ['Alice', '24', 'New York', 'Engineer'],
    ['Bob', '30', 'Los Angeles', 'Designer'],
    ['Charlie', '28', 'Chicago', 'Teacher']
]

t = Table(data)
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 12),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
    ('GRID', (0,0), (-1,-1), 1, colors.black)
]))

elements.append(t)
elements.append(Paragraph("End of the table document.", styles['Normal']))

doc.build(elements)
print("PDF created successfully at test/test_table.pdf")
