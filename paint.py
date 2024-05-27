import tkinter as tk
from tkinter import Canvas, Button, Scale, HORIZONTAL, filedialog, messagebox, Entry
import pyscreenshot as ImageGrab  

class Paint:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Aplicación de Dibujo")
        self.ventana.resizable(1,1)

        frame = tk.Frame(self.ventana, bg='Black', height=200)
        frame.grid(column=0, row=0, sticky='nsew')
        
        frame.columnconfigure(0, weight=1)
        for i in range(1, 7):
            frame.columnconfigure(i, weight=0)

        self.ventana.rowconfigure(1, weight=1)
        self.ventana.columnconfigure(0, weight=1)

        frame.columnconfigure(0, minsize=200, weight=1)

        self.canvas = Canvas(self.ventana, height=660, bg='white')
        self.canvas.grid(row=1, column=0, sticky='nsew')

        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1, minsize=100)

        self.canvas.bind('<Button-1>', self.linea_xy)
        self.canvas.bind('<B1-Motion>', self.linea)

        canvas_colores = Canvas(frame, bg='black', width=5, height=40)
        canvas_colores.grid(column=0, row=0, sticky='ew', padx=1, pady=1)

        self.colores = [
            ('red', 'Rojo'), ('green', 'Verde'), ('yellow', 'Amarillo'), ('magenta', 'Magenta'),
            ('blue', 'Azul'), ('orange', 'Naranja'), ('salmon', 'Salmon'), ('sky blue', 'Cielo'),
            ('gold', 'Dorado'), ('hot pink', 'Rosa Fuerte'), ('bisque', 'Bisque'), ('brown4', 'Café'),
            ('gray', 'Gris'), ('purple', 'Morado'), ('green2', 'Verde Oscuro'), ('dodger blue', 'Azul Oscuro'),
            ('black', 'Negro'), ('white', 'Blanco')
        ]

        for idx, (color, _) in enumerate(self.colores):
            id = canvas_colores.create_rectangle((10 + idx * 30, 10, 30 + idx * 30, 30), fill=color)
            canvas_colores.tag_bind(id, '<Button-1>', lambda e, col=color: self.mostrar_color(col))

        self.espesor_pincel = Scale(frame, orient=HORIZONTAL, from_=0, to=50, length=200, relief='groove', bg='gold',
                                    width=17, sliderlength=20, highlightbackground='white', activebackground='red')
        self.espesor_pincel.set(1)
        self.espesor_pincel.grid(column=1, row=0, sticky='ew', pady=1, padx=2)

        btnGuardar = Button(frame, text='Guardar', bg='green2', command=self.guardar_dibujo,
                            width=10, height=2, activebackground='white', font=('comic sans MS', 10, 'bold'))
        btnGuardar.grid(column=2, row=0, sticky='ew', pady=1, padx=4)

        btnBorrar = Button(frame, text='Borrar', bg='cyan2', command=self.borrar,
                           width=10, height=2, activebackground='white', font=('comic sans MS', 10, 'bold'))
        btnBorrar.grid(column=3, row=0, sticky='ew', pady=1, padx=4)

        btnLimpiar = Button(frame, text='Limpiar', bg='Violet Red', command=self.limpiar,
                            width=10, height=2, activebackground='white', font=('comic sans MS', 10, 'bold'))
        btnLimpiar.grid(column=4, row=0, sticky='ew', pady=1, padx=4)

        btnSalir = Button(frame, text='Salir', bg='firebrick1', command=self.salir,
                          width=10, height=2, activebackground='white', font=('comic sans MS', 10, 'bold'))
        btnSalir.grid(column=5, row=0, sticky='ew', pady=1, padx=4)


        self.modo_dibujo = "linea"
        btnCirculo = Button(frame, text='Círculo', bg='lightblue', command=self.modo_circulo,
                             width=15, height=2, activebackground='white', font=('comic sans MS', 10, 'bold'))
        btnCirculo.grid(column=6, row=0, sticky='ew', pady=1, padx=4)


        btnLinea = Button(frame, text='Línea', bg='lightblue', command=self.modo_linea,
                          width=10, height=2, activebackground='white', font=('comic sans MS', 10, 'bold'))
        btnLinea.grid(column=7, row=0, sticky='ew', pady=1, padx=4)


        btnCuadrado = Button(frame, text='Cuadrado', bg='lightblue', command=self.modo_cuadrado,
                             width=10, height=2, activebackground='white', font=('comic sans MS', 10, 'bold'))
        btnCuadrado.grid(column=8, row=0, sticky='ew', pady=1, padx=4)

        self.linea_x = 0
        self.linea_y = 0
        self.color = 'black'
        self.start_x = None
        self.start_y = None
        self.circle = None

        self.ventana.mainloop()

    def modo_linea(self):
        self.modo_dibujo = "linea"

    def modo_cuadrado(self):
        self.modo_dibujo = "cuadrado"

    
    def linea_xy(self, event):
        if self.modo_dibujo == "linea":
            self.linea_x = event.x
            self.linea_y = event.y
        elif self.modo_dibujo == "circulo":
            self.start_x = event.x
            self.start_y = event.y
            self.circle = self.canvas.create_oval(self.start_x, self.start_y, self.start_x, self.start_y, outline=self.color)
        
        self.start_x = event.x
        self.start_y = event.y
        if self.modo_dibujo == "linea":
            self.linea = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, fill=self.color)
        elif self.modo_dibujo == "cuadrado":
            self.cuadrado = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline=self.color)

    def linea(self, event):
        if self.modo_dibujo == "linea":
            self.canvas.create_line((self.linea_x, self.linea_y, event.x, event.y), fill=self.color, width=self.espesor_pincel.get())
            self.linea_x = event.x
            self.linea_y = event.y
        elif self.modo_dibujo == "circulo" and self.circle is not None:
            self.canvas.coords(self.circle, self.start_x, self.start_y, event.x, event.y)

        if self.modo_dibujo == "linea":
            self.canvas.coords(self.linea, self.start_x, self.start_y, event.x, event.y)
        elif self.modo_dibujo == "cuadrado":
            self.canvas.coords(self.cuadrado, self.start_x, self.start_y, event.x, event.y)


    def modo_circulo(self):
        if self.modo_dibujo == "linea":
            self.modo_dibujo = "circulo"
        else:
            self.modo_dibujo = "linea"


    def mostrar_color(self, nuevo_color):
        self.color = nuevo_color

    def borrar(self):
        self.color = 'white'

    def limpiar(self):
        self.canvas.delete("all")

    def salir(self):
        self.ventana.destroy()

    def guardar_dibujo(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension='.png')
            if filename:
                x = self.ventana.winfo_rootx() + self.canvas.winfo_x()
                y = self.ventana.winfo_rooty() + self.canvas.winfo_y()
                x1 = x + self.canvas.winfo_width()
                y1 = y + self.canvas.winfo_height()
                ImageGrab.grab().crop((x, y, x1, y1)).save(filename)
                messagebox.showinfo('Guardar Dibujo', 'Imagen Guardada en: ' + str(filename))
        except Exception as e:
            messagebox.showerror('Guardar Dibujo', 'Imagen no guardada\nError: ' + str(e))