import asyncio
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


async def create_pdf(examples: list):
    file = canvas.Canvas("examples.pdf", pagesize=A4)

    pos_x = 50
    pos_y = 750
    for i in examples:
        file.drawString(pos_x, pos_y, i)
        pos_y -= 20

    file.save()


if __name__ == "__main__":
    asyncio.run(create_pdf())
