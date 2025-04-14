from io import BytesIO

import matplotlib.pyplot as plt


def line_plot(
        data: list[int | float] = None,
        x: list[int | float] = None,
        y: list[int | float] = None,
        show: bool = True,
        save: dict | None = None
):
    """
    save_opt = {"save":True, "filename": "plot", "format":"svg", "bytes": True}
    """
    if save is None:
        save = {"save": False}

    figure, ax = plt.subplots()

    if data:
        ax.plot(data)
    elif x and y:
        ax.plot(x, y)

    if show:
        plt.show()

    if save["save"]:
        if "bytes" in save.keys() and save["bytes"]:
            buffer = BytesIO()
            figure.savefig(buffer, format=save["format"])
            buffer.seek(0)
            return buffer.getvalue()
        else:
            figure.savefig(f"{save["filename"]}.{save["format"]}")
