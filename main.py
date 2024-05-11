import subprocess
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

import pyperclip
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Clases.cls_GUI import MainWindows
from DB.tblPozos import clsPozos_PP

import pandas as pd
from tkinter import filedialog
from sqlalchemy.orm import Session


def main():
    def load_excel_to_db():

        # Abrir el explorador de archivos y obtener la ruta del archivo seleccionado
        file_path = filedialog.askopenfilename(filetypes=[('Excel files', '*.xlsx')])

        # Leer el archivo Excel
        df = pd.read_excel(file_path, sheet_name='perforacion')

        # Definir los campos esperados
        expected_fields = ['Baja', 'Pozo', 'Pozo_Tipo', 'Fecha_Fin', 'Equipo', 'Estado', 'Cert_Op']

        # Verificar si los campos del DataFrame coinciden con los campos esperados
        for field in expected_fields:
            if field not in df.columns:
                print(f'El campo {field} no se encuentra en la solapa perforacion del archivo Excel.')
                return False

        print('Todos los campos esperados se encuentran en la solapa perforacion del archivo Excel.')

        # Crear una sesión de SQLAlchemy
        session = Session(bind=engine)

        # Recorrer cada fila del DataFrame
        for index, row in df.iterrows():
            # Crear un nuevo objeto clsPozos_PP
            new_pozo = clsPozos_PP(
                Baja=row['Baja'],
                Pozo=row['Pozo'],
                Pozo_Tipo=row['Pozo_Tipo'],
                Fecha_Fin=row['Fecha_Fin'],
                Equipo=row['Equipo'],
                Estado=row['Estado'],
                Cert_Op=row['Cert_Op']
            )

            # Agregar el nuevo objeto a la sesión
            session.add(new_pozo)

        # Comprometer los cambios en la base de datos
        session.commit()

        print('Los datos del archivo Excel se han cargado en la base de datos.')
        return True

    currentCommit = 'v5 Prueba'
    #get_git_commits(currentCommit)

    root = tk.Tk()
    root.title("Prueba PSNC")
    # root.geometry("400x400")
    root.config(bg="lightblue")

    # etiqueta ultima version
    label = tk.Label(root, text="Ultima version: " + currentCommit, font=("Arial", 10), bg="lightblue")
    label.pack(pady=2, padx=2, anchor=tk.E)

    guiMainWindows = MainWindows(root)

    guiMainWindows.tkSubir_Excel.config(command=lambda: load_excel_to_db())


    root.mainloop()


def get_git_commits(currentCommit: str):
    def copy_to_clipboard(text: str):
        pyperclip.copy(text)

    commit_info = subprocess.check_output(['git', 'log', '--pretty=format:%h - %ad']).decode('utf-8').strip()
    commit_list = commit_info.split('\n')
    commit_dicts = []
    for commit in commit_list:
        parts = commit.split(' - ')
        try:
            version = subprocess.check_output(['git', 'show', '-s', '--pretty=format:%s', parts[0]]).decode(
                'utf-8').strip()
        except subprocess.CalledProcessError:
            version = 's/n'
        commit_dict = {
            'rev-parse': parts[0],
            'denominacion': version,
            'fecha': datetime.strptime(parts[1], '%a %b %d %H:%M:%S %Y %z')
        }
        commit_dicts.append(commit_dict)

    # sort the commits by date in descending order
    commit_dicts = sorted(commit_dicts, key=lambda x: x['fecha'], reverse=True)

    lastCommit = commit_dicts[0]['denominacion']
    if lastCommit != currentCommit:
        messagebox.showinfo("Mensaje", "Nueva version disponible: " + lastCommit)
        copy_to_clipboard(lastCommit)
        exit()






if __name__ == "__main__":
    # abrir BD
    engine = create_engine('sqlite:///BD.db')
    #Base = declarative_base()
    #Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    pozosPP = clsPozos_PP(Pozo='Pozo1', Pozo_Tipo='Tipo1', Equipo='Equipo1', Estado='Estado1', Cert_Op=1.0)
    session.add(pozosPP)
    session.commit()

    main()
