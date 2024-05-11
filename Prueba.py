import sqlite3
import tkinter as tk
from tkinter import ttk, simpledialog

# Conectar a la base de datos
conn = sqlite3.connect('BD.db')
cursor = conn.cursor()

def load_data():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute('SELECT * FROM tblPozos_PP')
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

def edit_record(event):
    item = tree.selection()[0]
    values = tree.item(item, 'values')
    new_name = simpledialog.askstring("Input", "Nuevo nombre:", initialvalue=values[1])
    new_age = simpledialog.askinteger("Input", "Nueva edad:", initialvalue=values[2])
    if new_name and new_age:
        cursor.execute('UPDATE users SET name = ?, age = ? WHERE id = ?', (new_name, new_age, values[0]))
        conn.commit()
        load_data()

root = tk.Tk()
root.title("Visualizar y Editar Tabla")

tree = ttk.Treeview(root, columns=('ID', 'Name', 'Age'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Name', text='Name')
tree.heading('Age', text='Age')
tree.pack(fill='both', expand=True)
tree.bind('<Double-1>', edit_record)

load_data()

root.mainloop()
conn.close()
