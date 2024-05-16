from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/anu/Documents/IPN/Tesis/GUI/small/smallMContinua/build/assets/frame0")
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/pi/Tesis/Thesis/Code/GUI/small/smallMContinua/build/assets/frame0")

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
    107.4375,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    488.8125,
    192.83749389648438,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    485.76251220703125,
    278.23748779296875,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    485.76251220703125,
    363.6375732421875,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    485.76251220703125,
    449.0374755859375,
    image=image_image_5
)

canvas.create_text(
    253.14999389648438,
    93.78750610351562,
    anchor="nw",
    text="pH: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 24 * -1)
)

canvas.create_text(
    253.14999389648438,
    179.18753051757812,
    anchor="nw",
    text="Conductividad: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 24 * -1)
)

canvas.create_text(
    250.10003662109375,
    264.5875244140625,
    anchor="nw",
    text="Temperatura: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 24 * -1)
)

canvas.create_text(
    250.10003662109375,
    349.987548828125,
    anchor="nw",
    text="Índice de Calidad de Agua: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 24 * -1)
)

canvas.create_text(
    250.10003662109375,
    435.38751220703125,
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
    y=226.46246337890625,
    width=109.03750610351562,
    height=70.1500015258789
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
    x=88.44999694824219,
    y=305.762451171875,
    width=109.03750610351562,
    height=70.1500015258789
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
    x=783.0875244140625,
    y=226.46246337890625,
    width=109.03750610351562,
    height=70.1500015258789
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=783.0875244140625,
    y=305.762451171875,
    width=109.03750610351562,
    height=70.1500015258789
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=681.675048828125,
    y=496.38751220703125,
    width=45.750003814697266,
    height=44.98750305175781
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=899.75,
    y=472.75006103515625,
    width=76.25000762939453,
    height=76.25000762939453
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
    918.6250610351562,
    51.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    462.76251220703125,
    518.3875122070312,
    image=image_image_8
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    568.8249931335449,
    521.9311771392822,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=525.3624877929688,
    y=510.1124267578125,
    width=86.92501068115234,
    height=21.637500762939453
)

canvas.create_text(
    361.42498779296875,
    21.350006103515625,
    anchor="nw",
    text="Medición Continua",
    fill="#000000",
    font=("NunitoSans Regular", 30 * -1)
)
window.resizable(False, False)
window.mainloop()
