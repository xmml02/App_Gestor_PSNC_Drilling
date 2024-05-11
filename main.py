import tkinter as tk
from tkinter import messagebox
import subprocess
from datetime import datetime

def main():

    listCommits = get_git_commits()
    currentCommit = get_current_commit()
    # NOSE

    root = tk.Tk()
    root.title("Prueba PSNC")
    root.geometry("400x400")
    root.config(bg="lightblue")

    # etiqueta ultima version
    label = tk.Label(root, text="Ultima version: "+listCommits[0]['denominacion'], font=("Arial", 10), bg="lightblue")
    label.pack(pady=2, padx=2, anchor=tk.E)

    # current commit
    label = tk.Label(root, text="Current commit: "+currentCommit['denominacion'], font=("Arial", 10), bg="lightblue")
    label.pack(pady=2, padx=2, anchor=tk.E)

    #creamos una etiqueta
    label = tk.Label(root, text="VERSION DE PRUEBA", font=("Arial", 20), bg="lightblue")
    label.pack(pady=20)

    #creamos un boton
    button = tk.Button(root, text="Mostrar mensaje", command=lambda: messagebox.showinfo("Mensaje", "Hola Mundo"))
    button.pack(pady=20)

    root.mainloop()

def get_current_commit():
    try:
        current_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
        version = subprocess.check_output(['git', 'show', '-s', '--pretty=format:%s', current_commit]).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        current_commit = 's/n'
        version = 's/n'
    commit_dict = {
        'rev-parse': current_commit,
        'denominacion': version
    }
    return commit_dict


def get_git_commits():
    commit_info = subprocess.check_output(['git', 'log', '--pretty=format:%h - %ad']).decode('utf-8').strip()
    commit_list = commit_info.split('\n')
    commit_dicts = []
    for commit in commit_list:
        parts = commit.split(' - ')
        try:
            version = subprocess.check_output(['git', 'show', '-s', '--pretty=format:%s', parts[0]]).decode('utf-8').strip()
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
    return commit_dicts


if __name__ == "__main__":

    main()



