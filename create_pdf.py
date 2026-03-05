from reportlab.pdfgen import canvas

c = canvas.Canvas("sample.pdf")
c.drawString(100, 750, "OmniRAG is a multi-model RAG system designed for enterprise use.")
c.drawString(100, 730, "It supports PDF and image parsing.")
c.drawString(100, 710, "The answer to life is 42.")
c.save()
print("Sample PDF generated.")
