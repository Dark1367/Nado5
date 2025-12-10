import asyncio
import matplotlib.pyplot as plt
from .generate_lim import generate_easy_predel


async def create_pdf(problems):
    plt.figure(figsize=(8.27, 11.69))
    plt.axis("off")
    formulas = problems

    y_position = 0.95  # Координаты верха, откуда начинать

    for i, formula in enumerate(formulas, 1):
        plt.text(0.1, y_position, f"{i}) ${formula}$", fontsize=14, ha="left", va="top", transform=plt.gca().transAxes)

        y_position -= 0.08  # Отступ между формулами

        # У нас такое врядли будет, но если длина больше 100 символов, то будет перенос на некст строку
        if len(formula) > 100:
            y_position -= 0.02

    plt.tight_layout()
    plt.savefig("primer_list.pdf", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    asyncio.run(create_pdf())
