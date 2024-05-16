from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/anu/Documents/IPN/Tesis/GUI/small/smallMPuntual/build/assets/frame0")
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/pi/Tesis/Thesis/Code/GUI/small/smallMPuntual/build/assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("976x549")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 549,
    width = 976,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    488.8125,
    136.41250610351562,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    488.8125,
    221.8125,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    485.76251220703125,
    307.2125244140625,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    485.76251220703125,
    392.61248779296875,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    485.76251220703125,
    478.01251220703125,
    image=image_image_5
)

canvas.create_text(
    253.14999389648438,
    122.76251220703125,
    anchor="nw",
    text="pH: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 24 * -1)
)

canvas.create_text(
    253.14999389648438,
    208.16250610351562,
    anchor="nw",
    text="Conductividad: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 24 * -1)
)

canvas.create_text(
    250.10000610351562,
    293.5625,
    anchor="nw",
    text="Temperatura: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 24 * -1)
)

canvas.create_text(
    250.10000610351562,
    378.9625244140625,
    anchor="nw",
    text="Índice de Calidad de Agua: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 24 * -1)
)

canvas.create_text(
    250.10000610351562,
    464.36248779296875,
    anchor="nw",
    text="Calidad: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 24 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=88.44999694824219,
    y=226.46249389648438,
    width=109.0374984741211,
    height=70.1500015258789
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    44.0,
    66.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    918.625,
    51.0,
    image=image_image_7
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=899.75,
    y=472.75,
    width=76.25,
    height=76.25
)

canvas.create_text(
    369.8125,
    21.350006103515625,
    anchor="nw",
    text="Medición Puntual",
    fill="#000000",
    font=("NunitoSans Regular", 30 * -1)
)
window.resizable(False, False)
window.mainloop()
