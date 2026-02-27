import asyncio
import matplotlib.pyplot as plt


def create_pdf(problems):
    plt.figure(figsize=(8.27, 11.69))
    plt.axis("off")

    y_position = 0.95
    for i, formula in enumerate(problems, 1):
        plt.text(
            0.1, y_position,
            f"{i}) ${formula}$",
            fontsize=14,
            ha="left",
            va="top",
            transform=plt.gca().transAxes
        )
        y_position -= 0.08
        if len(formula) > 100:
            y_position -= 0.02

    plt.tight_layout()
    plt.savefig("primer_list.pdf", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    asyncio.run(create_pdf())
