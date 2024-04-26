from pathlib import Path
from tkinter import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("/Users/anu/Documents/IPN/Tesis/GUI/Screens/Homescreen/build/assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def show_frame(frame):
    frame.tkraise()

window = Tk()
window.title("Sistema de Adquisición de Datos")
window.geometry("1280x720")


medicionContinua = Frame(window)
medicionEnIntervalos = Frame(window)
medicionPuntual = Frame(window)

# Initially hide frames other than Homescreen
medicionPuntual.grid(row=0, column=0)
medicionContinua.grid(row=0, column=0)
medicionEnIntervalos.grid(row=0, column=0)

##### Medicion En Intervalos ####
#Fondo
canvas_intervalos = Canvas(
    medicionEnIntervalos,
    bg = "#FFFFFF",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas_intervalos.pack()
#Imagenes
image_image_1_intervalos = PhotoImage(
    file=relative_to_assets("image_1_intervalos.png"))
image_1_intervalos = canvas_intervalos.create_image(
    641.0,
    141.0,
    image=image_image_1_intervalos
)

image_image_2_intervalos = PhotoImage(
    file=relative_to_assets("image_2_intervalos.png"))
image_2_intervalos = canvas_intervalos.create_image(
    641.0,
    253.0,
    image=image_image_2_intervalos
)

image_image_3_intervalos = PhotoImage(
    file=relative_to_assets("image_3_intervalos.png"))
image_3_intervalos = canvas_intervalos.create_image(
    637.0,
    365.0,
    image=image_image_3_intervalos
)

image_image_4_intervalos = PhotoImage(
    file=relative_to_assets("image_4_intervalos.png"))
image_4_intervalos = canvas_intervalos.create_image(
    637.0,
    477.0,
    image=image_image_4_intervalos
)

image_image_5_intervalos = PhotoImage(
    file=relative_to_assets("image_5_intervalos.png"))
image_5_intervalos = canvas_intervalos.create_image(
    637.0,
    589.0,
    image=image_image_5_intervalos
)

image_image_6_intervalos = PhotoImage(
    file=relative_to_assets("image_6_intervalos.png"))
image_6_intervalos = canvas_intervalos.create_image(
    57.0,
    87.0,
    image=image_image_6_intervalos
)

image_image_7_intervalos = PhotoImage(
    file=relative_to_assets("image_7_intervalos.png"))
image_7_intervalos = canvas_intervalos.create_image(
    1205.0,
    67.0,
    image=image_image_7_intervalos
)

image_image_8_intervalos = PhotoImage(
    file=relative_to_assets("image_8_intervalos.png"))
image_8_intervalos = canvas_intervalos.create_image(
    456.0,
    684.0,
    image=image_image_8_intervalos
)

image_image_9_intervalos = PhotoImage(
    file=relative_to_assets("image_9_intervalos.png"))
image_9_intervalos = canvas_intervalos.create_image(
    785.0,
    684.0,
    image=image_image_9_intervalos
)
#Texto
canvas_intervalos.create_text(
    332.0,
    123.0,
    anchor="nw",
    text="pH: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

canvas_intervalos.create_text(
    332.0,
    235.0,
    anchor="nw",
    text="Conductividad: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

canvas_intervalos.create_text(
    328.0,
    347.0,
    anchor="nw",
    text="Temperatura: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

canvas_intervalos.create_text(
    328.0,
    459.0,
    anchor="nw",
    text="Índice de Calidad de Agua: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

canvas_intervalos.create_text(
    328.0,
    571.0,
    anchor="nw",
    text="Calidad: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)
#Botones
button_image_1_intervalos = PhotoImage(
    file=relative_to_assets("button_1_intervalos.png"))
button_1_intervalos = Button(medicionEnIntervalos,
    image=button_image_1_intervalos,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1_intervalos clicked"),
    relief="flat"
)
button_1_intervalos.place(
    x=116.0,
    y=297.0,
    width=143.0,
    height=92.0
)

button_image_2_intervalos = PhotoImage(
    file=relative_to_assets("button_2_intervalos.png"))
button_2_intervalos = Button(medicionEnIntervalos,
    image=button_image_2_intervalos,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2_intervalos clicked"),
    relief="flat"
)
button_2_intervalos.place(
    x=1027.0,
    y=297.0,
    width=143.0,
    height=92.0
)

button_image_3_intervalos = PhotoImage(
    file=relative_to_assets("button_3_intervalos.png"))
button_3_intervalos = Button(medicionEnIntervalos,
    image=button_image_3_intervalos,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3_intervalos clicked"),
    relief="flat"
)
button_3_intervalos.place(
    x=1027.0,
    y=401.0,
    width=143.0,
    height=92.0
)

button_image_4_intervalos = PhotoImage(
    file=relative_to_assets("button_4_intervalos.png"))
button_4_intervalos = Button(medicionEnIntervalos,
    image=button_image_4_intervalos,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4_intervalos clicked"),
    relief="flat"
)
button_4_intervalos.place(
    x=943.0,
    y=655.0,
    width=60.0,
    height=59.0
)

button_image_5_intervalos = PhotoImage(
    file=relative_to_assets("button_5_intervalos.png"))
button_5_intervalos = Button(medicionEnIntervalos,
    image=button_image_5_intervalos,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(Homescreen),  #Home
    relief="flat"
)
button_5_intervalos.place(
    x=1180.0,
    y=620.0,
    width=100.0,
    height=100.0
)
#Input texts
entry_image_1_intervalos = PhotoImage(
    file=relative_to_assets("entry_1_intervalos.png"))

entry_bg_1_intervalos = canvas_intervalos.create_image(
    539.5,
    688.5,
    image=entry_image_1_intervalos
)
entry_1_intervalos = Entry(medicionEnIntervalos,
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1_intervalos.place(
    x=508.0,
    y=673.0,
    width=63.0,
    height=29.0
)

entry_image_2_intervalos = PhotoImage(
    file=relative_to_assets("entry_2_intervalos.png"))
entry_bg_2_intervalos = canvas_intervalos.create_image(
    841.5,
    685.5,
    image=entry_image_2_intervalos
)
entry_2_intervalos = Entry(medicionEnIntervalos,
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2_intervalos.place(
    x=810.0,
    y=670.0,
    width=63.0,
    height=29.0
)
#Header
canvas_intervalos.create_text(
    363.0,
    28.0,
    anchor="nw",
    text="Medición En Intervalos",
    fill="#000000",
    font=("NunitoSans Regular", 40 * -1)
)


##### Medicion Continua Widgets ####
#Fondo
canvasContinua = Canvas(
    medicionContinua,
    bg = "#FFFFFF",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvasContinua.pack()
#Imagenes
image_image_1_continua = PhotoImage(
    file=relative_to_assets("image_1_continua.png"))
image_1_continua = canvasContinua.create_image(
    641.0,
    141.0,
    image=image_image_1_continua
)

image_image_2_continua = PhotoImage(
    file=relative_to_assets("image_2_continua.png"))
image_2_continua = canvasContinua.create_image(
    641.0,
    253.0,
    image=image_image_2_continua 
)

image_image_3_continua = PhotoImage(
    file=relative_to_assets("image_3_continua.png"))
image_3_continua = canvasContinua.create_image(
    637.0,
    365.0,
    image=image_image_3_continua
)

image_image_4_continua = PhotoImage(
    file=relative_to_assets("image_4_continua.png"))
image_4_continua = canvasContinua.create_image(
    637.0,
    477.0,
    image=image_image_4_continua
)

image_image_5_continua = PhotoImage(
    file=relative_to_assets("image_5_continua.png"))
image_5_continua = canvasContinua.create_image(
    637.0,
    589.0,
    image=image_image_5_continua
)

image_image_6_continua = PhotoImage(
    file=relative_to_assets("image_6_continua.png"))
image_6_continua = canvasContinua.create_image(
    57.0,
    87.0,
    image=image_image_6_continua
)

image_image_7_continua = PhotoImage(
    file=relative_to_assets("image_7_continua.png"))
image_7_continua = canvasContinua.create_image(
    1205.0,
    67.0,
    image=image_image_7_continua
)

image_image_8_continua = PhotoImage(
    file=relative_to_assets("image_8_continua.png"))
image_8_continua = canvasContinua.create_image(
    607.0,
    680.0,
    image=image_image_8_continua
)
#Texto
canvasContinua.create_text(
    332.0,
    123.0,
    anchor="nw",
    text="pH: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

canvasContinua.create_text(
    332.0,
    235.0,
    anchor="nw",
    text="Conductividad: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

canvasContinua.create_text(
    328.0,
    347.0,
    anchor="nw",
    text="Temperatura: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

canvasContinua.create_text(
    328.0,
    459.0,
    anchor="nw",
    text="Índice de Calidad de Agua: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

canvasContinua.create_text(
    328.0,
    571.0,
    anchor="nw",
    text="Calidad: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)
#Botones
button_image_1_continua = PhotoImage(
    file=relative_to_assets("button_1_continua.png"))
button_1_continua = Button(
    medicionContinua,
    image=button_image_1_continua,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1_continua clicked"),
    relief="flat"
)
button_1_continua.place(
    x=116.0,
    y=297.0,
    width=143.0,
    height=92.0
)

button_image_2_continua = PhotoImage(
    file=relative_to_assets("button_2_continua.png"))
button_2_continua = Button(
    medicionContinua,
    image=button_image_2_continua,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2_continua clicked"),
    relief="flat"
)
button_2_continua.place(
    x=116.0,
    y=401.0,
    width=143.0,
    height=92.0
)

button_image_3_continua = PhotoImage(
    file=relative_to_assets("button_3_continua.png"))
button_3_continua = Button(
    medicionContinua,
    image=button_image_3_continua,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3_continua clicked"),
    relief="flat"
)
button_3_continua.place(
    x=1027.0,
    y=297.0,
    width=143.0,
    height=92.0
)

button_image_4_continua = PhotoImage(
    file=relative_to_assets("button_4_continua.png"))
button_4_continua = Button(
    medicionContinua,
    image=button_image_4_continua,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4_continua clicked"),
    relief="flat"
)
button_4_continua.place(
    x=1027.0,
    y=401.0,
    width=143.0,
    height=92.0
)

button_image_5_continua = PhotoImage(
    file=relative_to_assets("button_5_continua.png"))
button_5_continua = Button(
    medicionContinua,
    image=button_image_5_continua,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5_continua clicked"),
    relief="flat"
)
button_5_continua.place(
    x=894.0,
    y=651.0,
    width=60.0,
    height=59.0
)

button_image_6_continua = PhotoImage(
    file=relative_to_assets("button_6_continua.png"))
button_6_continua = Button(
    medicionContinua,
    image=button_image_6_continua,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(Homescreen),  #Home
    relief="flat"
)
button_6_continua.place(
    x=1180.0,
    y=620.0,
    width=100.0,
    height=100.0
)
#Input text
entry_image_1_continua = PhotoImage(
    file=relative_to_assets("entry_1_continua.png"))

entry_bg_1_continua = canvasContinua.create_image(
    746.0,
    684.5,
    image=entry_image_1_continua
)
entry_1_continua = Entry(
    medicionContinua,
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1_continua.place(
    x=689.0,
    y=669.0,
    width=114.0,
    height=29.0
)
#Header
canvasContinua.create_text(
    474.0,
    28.0,
    anchor="nw",
    text="Medición Continua",
    fill="#000000",
    font=("NunitoSans Regular", 40 * -1)
)
###

##### Medicion Puntual Widgets ####
#Fondo
canvasPuntual = Canvas(
    medicionPuntual,
    bg = "#FFFFFF",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvasPuntual.pack()

#Imagenes
image_image_1_puntual = PhotoImage(
    file=relative_to_assets("image_1_puntual.png"))
image_1_puntual = canvasPuntual.create_image(
    641.0,
    179.0,
    image=image_image_1_puntual
)
image_image_2_puntual = PhotoImage(
    file=relative_to_assets("image_2_puntual.png"))
image_2_puntual = canvasPuntual.create_image(
    641.0,
    291.0,
    image=image_image_2_puntual
)

image_image_3_puntual = PhotoImage(
    file=relative_to_assets("image_3_puntual.png"))
image_3 = canvasPuntual.create_image(
    637.0,
    403.0,
    image=image_image_3_puntual
)

image_image_4_puntual = PhotoImage(
    file=relative_to_assets("image_4_puntual.png"))
image_4 = canvasPuntual.create_image(
    637.0,
    515.0,
    image=image_image_4_puntual
)

image_image_5_puntual = PhotoImage(
    file=relative_to_assets("image_5_puntual.png"))
image_5_puntual = canvasPuntual.create_image(
    637.0,
    627.0,
    image=image_image_5_puntual
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6_puntual.png"))
image_6_puntual = canvasPuntual.create_image(
    57.0,
    87.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7_puntual.png"))
image_7_puntual = canvasPuntual.create_image(
    1205.0,
    67.0,
    image=image_image_7
)
#Texto
canvasPuntual.create_text(
    332.0,
    161.0,
    anchor="nw",
    text="pH: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

canvasPuntual.create_text(
    332.0,
    273.0,
    anchor="nw",
    text="Conductividad: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

canvasPuntual.create_text(
    328.0,
    385.0,
    anchor="nw",
    text="Temperatura: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

canvasPuntual.create_text(
    328.0,
    497.0,
    anchor="nw",
    text="Índice de Calidad de Agua: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

canvasPuntual.create_text(
    328.0,
    609.0,
    anchor="nw",
    text="Calidad: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

#Botones
button_image_1_puntual = PhotoImage(
    file=relative_to_assets("button_1_puntual.png"))
button_1_puntual = Button(
    medicionPuntual,
    image=button_image_1_puntual,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1_puntual clicked"),
    relief="flat"
)
button_1_puntual.place(
    x=116.0,
    y=297.0,
    width=143.0,
    height=92.0
)

button_image_2_puntual = PhotoImage(
    file=relative_to_assets("button_2_puntual.png"))
button_2_puntual = Button(
    medicionPuntual,
    image=button_image_2_puntual,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(Homescreen),  #Home
    relief="flat"
)
button_2_puntual.place(
    x=1180.0,
    y=620.0,
    width=100.0,
    height=100.0
)
#Header text
canvasPuntual.create_text(
    485.0,
    28.0,
    anchor="nw",
    text="Medición Puntual",
    fill="#000000",
    font=("NunitoSans Regular", 40 * -1)
)
###

# Create the Homescreen frame
Homescreen = Frame(window)
Homescreen.grid(row=0, column=0)

# Create a canvas within the Homescreen frame
canvasHomescreen = Canvas(
    Homescreen,
    bg="#FFFFFF",
    height=720,
    width=1280,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvasHomescreen.pack()

# Create buttons within the Homescreen frame
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    Homescreen,
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(medicionPuntual),  # Switch to medicionPuntual frame
    relief="flat"
)
button_1.place(
    x=63.0,
    y=331.0,
    width=369.0,
    height=92.0
)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    Homescreen,
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(medicionContinua),  # Switch 
    relief="flat"
)
button_2.place(
    x=444.0,
    y=331.0,
    width=369.0,
    height=92.0
)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    Homescreen,
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(medicionEnIntervalos),  # Switch 
    relief="flat"
)
button_3.place(
    x=825.0,
    y=328.0,
    width=391.0,
    height=98.0
)

# Create images within the canvas
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvasHomescreen.create_image(
    57.0,
    87.0,
    image=image_image_1
)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvasHomescreen.create_image(
    1205.0,
    67.0,
    image=image_image_2
)

# Create text within the canvas
canvasHomescreen.create_text(
    346.0,
    28.0,
    anchor="nw",
    text="Sistema de Adquisición de Datos",
    fill="#000000",
    font=("NunitoSans Regular", 40 * -1)
)

window.resizable(False, False)
window.mainloop()