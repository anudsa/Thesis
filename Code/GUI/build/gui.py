from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/pi/Tesis/Thesis/Code/GUI/build/assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.title("Sistema de Adquisición de Datos")
window.geometry("1280x720")
window.configure(bg = "#FFFFFF")

#Se crea el fondo
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

#Se añaden  las imágenes de las lecturas
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    627.0,
    122.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    627.0,
    264.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    627.0,
    406.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    627.0,
    548.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    627.0,
    673.0,
    image=image_image_5
)

#Se añaden los textos de las lecturas
pHText=canvas.create_text(
    318.0,
    104.0,
    anchor="nw",
    text="pH: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

conductividadText=canvas.create_text(
    318.0,
    246.0,
    anchor="nw",
    text="Conductividad: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

temperaturaText=canvas.create_text(
    318.0,
    388.0,
    anchor="nw",
    text="Temperatura: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

indiceText=canvas.create_text(
    318.0,
    530.0,
    anchor="nw",
    text="Índice de Calidad de Agua: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

calidadText=canvas.create_text(
    318.0,
    655.0,
    anchor="nw",
    text="Calidad: N/A",
    fill="#FFFFFF",
    font=("NunitoSans Regular", 32 * -1)
)

#Se definen las funciones
def actualizarDatos():
    pHValor = 7
    canvas.itemconfig(tagOrId=pHText,text=f"ph: {pHValor}")

    conductividadValor = 400
    canvas.itemconfig(tagOrId=conductividadText,text=f"Conductividad: {conductividadValor}")

    temperaturaValor=25
    canvas.itemconfig(tagOrId=temperaturaText,text=f"Temperatura: {temperaturaValor}")
    
    indice=2.5
    canvas.itemconfig(tagOrId=indiceText,text=f"Índice de Calidad de Agua: {indice}")

    calidad=["Baja","Aceptable","Excelente"]
    canvas.itemconfig(tagOrId=calidadText,text=f"Calidad: {calidad[1]}")


#Se crean los botones
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=actualizarDatos,
    relief="flat"
)
button_1.place(
    x=31.0,
    y=482.0,
    width=143.0,
    height=92.0
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
    x=31.0,
    y=596.0,
    width=143.0,
    height=92.0
)

#Se insertan los logos
image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    68.0,
    90.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    1195.0,
    76.0,
    image=image_image_7
)

#Se crea el header
canvas.create_text(
    385.0,
    10.0,
    anchor="nw",
    text="Sistema de Adquisición de Datos",
    fill="#000000",
    font=("NunitoSans Regular", 32 * -1)
)
window.resizable(False, False)
window.mainloop()
