#import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tk


class MainWindows(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.InitComponents()

    def InitComponents(self):
        self.tkNotebook = ttk.Notebook(self.master, style='primary.TNotebook')

        # SE CREA PESTAÑA 1
        tkTab1_Frame = ttk.Frame(self.tkNotebook)
        self.tkNotebook.add(tkTab1_Frame, text='Seteo PSNC')
        tkTab1_Frame.grid_columnconfigure(0, weight=1)  # Cambiar el peso a 1
        tkTab1_Frame.grid_columnconfigure(1, weight=1)  # Cambiar el peso a 1

        tkTab1_FrameKLeft = tk.Frame(tkTab1_Frame)
        tkTab1_FrameKLeft.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        tkLabel = tk.Label(tkTab1_FrameKLeft, text="Detalle provisiones ingresadas y control de monto",
                           font=("Arial", 10))
        tkLabel.pack()

        tkTab1_FrameKRight = tk.Frame(tkTab1_Frame)
        tkTab1_FrameKRight.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        tkLabel = tk.Label(tkTab1_FrameKRight, text="Configuración PSNC Actual y Anterior", font=("Arial", 10))
        tkLabel.pack()

        # Generar un TreeView editable y para ingresar nuevos datos con 4 columnas
        tkTree = ttk.Treeview(tkTab1_FrameKRight, columns=('C1', 'C2', 'C3', 'C4'), show='headings')
        tkTree.heading('#1', text='C1')
        tkTree.heading('#2', text='C2')
        tkTree.heading('#3', text='C3')
        tkTree.heading('#4', text='C4')

        #tkTree.configure(height=200)
        for col in ('C1', 'C2', 'C3', 'C4'):
            tkTree.column(col, width=50)
        tkTree.pack()

        labelFrame = tk.LabelFrame(tkTab1_FrameKRight, text="Ingresar mes contable", style='primary.TLabelframe')
        labelFrame.pack()

        # ingresar fecha contable
        tkEntryMesContable = tk.DateEntry(labelFrame, bootstyle='flat')
        tkEntryMesContable.pack(pady=5, padx=5)

        self.tkEject_SAP = tk.Button(tkTab1_FrameKRight, text="Ejecutar SAP")
        self.tkEject_SAP.pack(pady=5, padx=5)

        self.tkSubir_Excel = tk.Button(tkTab1_FrameKRight, text="Subir Excel")
        self.tkSubir_Excel.pack(pady=5, padx=5)

        # SE CREA PESTAÑA 2
        tkTab2_Frame = ttk.Frame(self.tkNotebook)
        self.tkNotebook.add(tkTab2_Frame, text='PP Pozos')



        # Agregar el notebook a la ventana
        self.tkNotebook.pack(expand=False, fill='both', padx=5, pady=5)