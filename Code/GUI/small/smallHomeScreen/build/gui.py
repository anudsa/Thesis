from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/anu/Documents/IPN/Tesis/GUI/small/smallHomeScreen/build/assets/frame0")
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/pi/Tesis/Thesis/Code/GUI/small/smallHomeScreen/build/assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
#Tamaño de ventana
window.geometry("976x549")
window.configure(bg = "#FFFFFF")

#Tamaño del canvas
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 549,###
    width = 976,###
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
#Cambiar dirección de imágenes para que tome las nuevas (verficar que hayan mantenido el mismo nombre)
canvas.place(x = 0, y = 0)
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
    x=48.037506103515625,
    y=252.38763427734375,
    width=281.36248779296875,
    height=70.15000915527344
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
    x=338.54998779296875,
    y=252.38763427734375,
    width=281.36248779296875,
    height=70.15000915527344
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=629.0625,
    y=250.0999755859375,
    width=298.1375732421875,
    height=74.7249984741211
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    44.0,
    66.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    918.625,
    51.0,
    image=image_image_2
)

canvas.create_text(
    263.8250427246094,
    21.350006103515625,
    anchor="nw",
    text="Sistema de Adquisición de Datos",
    fill="#000000",
    font=("NunitoSans Regular", 30 * -1)
)
window.resizable(False, False)
window.mainloop()
