# create document
from reportlab.pdfgen import canvas

file_name = 'MyPdf.pdf'
document_title = 'Document title!'
title = 'Tasmanian devil'
subtitle = 'subtitle subtitle subtitle'

textlines = ['first line', 'second line', 'third line']

image = ''




pdf = canvas.Canvas()