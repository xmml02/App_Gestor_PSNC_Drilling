import tkinter as tk
from tkinter import messagebox

def main():
    root = tk.Tk()
    root.title("Prueba PSNC")
    root.geometry("400x400")
    root.config(bg="lightblue")

    #creamos una etiqueta
    label = tk.Label(root, text="Bienvenido a mi programa", font=("Arial", 20), bg="lightblue")
    label.pack(pady=20)

    #creamos un boton
    button = tk.Button(root, text="Mostrar mensaje", command=lambda: messagebox.showinfo("Mensaje", "Hola Mundo"))
    button.pack(pady=20)

    root.mainloop()

import subprocess

def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()

def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()




if __name__ == "__main__":
    print(get_git_revision_hash())
    print(get_git_revision_short_hash())
    main()



