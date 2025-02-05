import requests
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import os

def check_username_availability(username):
    """Vérifie la disponibilité du pseudonyme sur Minecraft."""
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return False  
        elif response.status_code == 204:
            return True  
        else:
            return None   
    except requests.RequestException as e:
       
        return None

def check_usernames_list():
    """Prend la liste de pseudonymes entrés par l'utilisateur et affiche leur statut."""
    user_input = entry.get()  
    usernames_to_check = user_input.split(',') 

    available = []
    taken = []
    error = []

    for username in usernames_to_check:
        username = username.strip()  
        availability = check_username_availability(username)
        
        if availability is True:
            available.append(username)
        elif availability is False:
            taken.append(username)
        else:
            available.append(username)  
            error.append(username)


    result_message = ""
    if available:
        result_message += f"Pseudos disponibles : {', '.join(available)}\n"
    if taken:
        result_message += f"Pseudos déjà pris : {', '.join(taken)}\n"
    if error:
        result_message += f"Erreurs (considérés comme disponibles) : {', '.join(error)}\n"
    
 
    result_text.config(state='normal')  
    result_text.delete(1.0, tk.END) 
    result_text.insert(tk.END, result_message)  
    result_text.config(state='disabled')

def save_notes():
    """Sauvegarde les notes dans un fichier texte."""
    notes = notes_text.get(1.0, tk.END).strip()
    with open("notes.txt", "w") as file:
        file.write(notes)
    print("Notes sauvegardées dans 'notes.txt'.")


root = tk.Tk()
root.title("Vérification de Pseudonymes Minecraft")


root.geometry("800x600") 


try:
    image = Image.open("fond.jpg")
    background_image = ImageTk.PhotoImage(image)
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)  
except Exception as e:
    print(f"Erreur lors du chargement de l'image de fond : {e}")


label = tk.Label(root, text="Entrez une liste de pseudonymes séparés par des virgules :", bg="lightblue")
label.pack(pady=10)

entry = tk.Entry(root, width=60)
entry.pack(pady=10)

check_button = tk.Button(root, text="Vérifier", command=check_usernames_list)
check_button.pack(pady=10)


result_text = scrolledtext.ScrolledText(root, width=90, height=15, wrap=tk.WORD)
result_text.pack(pady=10)
result_text.config(state='disabled') 


notes_label = tk.Label(root, text="Notes : (pseudos intéressants, etc.)", bg="lightgreen")
notes_label.pack(pady=10)

notes_text = scrolledtext.ScrolledText(root, width=90, height=10, wrap=tk.WORD)
notes_text.pack(pady=10)


save_button = tk.Button(root, text="Sauvegarder les notes", command=save_notes)
save_button.pack(pady=10)


label.lift()
entry.lift()
check_button.lift()
result_text.lift()
notes_label.lift()
notes_text.lift()
save_button.lift()


root.mainloop()
