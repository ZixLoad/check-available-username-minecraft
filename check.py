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
            return False  # Le pseudo est déjà pris
        elif response.status_code == 204:
            return True   # Le pseudo est disponible
        else:
            return None    # Erreur ou autre situation
    except requests.RequestException as e:
        # Gestion des erreurs de requêtes
        return None

def check_usernames_list():
    """Prend la liste de pseudonymes entrés par l'utilisateur et affiche leur statut."""
    user_input = entry.get()  # Récupérer l'entrée de l'utilisateur
    usernames_to_check = user_input.split(',')  # Séparer les pseudos par des virgules

    available = []
    taken = []
    error = []

    for username in usernames_to_check:
        username = username.strip()  # Nettoyage des espaces autour des pseudos
        availability = check_username_availability(username)
        
        if availability is True:
            available.append(username)
        elif availability is False:
            taken.append(username)
        else:
            available.append(username)  # On considère les erreurs comme disponibles
            error.append(username)

    # Affichage des résultats dans le Text widget
    result_message = ""
    if available:
        result_message += f"Pseudos disponibles : {', '.join(available)}\n"
    if taken:
        result_message += f"Pseudos déjà pris : {', '.join(taken)}\n"
    if error:
        result_message += f"Erreurs (considérés comme disponibles) : {', '.join(error)}\n"
    
    # Insère les résultats dans la zone de texte et permet de les sélectionner et copier
    result_text.config(state='normal')  # Débloquer la zone de texte pour y écrire
    result_text.delete(1.0, tk.END)  # Effacer le contenu précédent
    result_text.insert(tk.END, result_message)  # Insérer les nouveaux résultats
    result_text.config(state='disabled')  # Bloquer la zone de texte pour l'édition, mais toujours sélectionnable

def save_notes():
    """Sauvegarde les notes dans un fichier texte."""
    notes = notes_text.get(1.0, tk.END).strip()
    with open("notes.txt", "w") as file:
        file.write(notes)
    print("Notes sauvegardées dans 'notes.txt'.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Vérification de Pseudonymes Minecraft")

# Définir la taille initiale de la fenêtre
root.geometry("800x600")  # Largeur x Hauteur

# Charger et appliquer l'image de fond avec Pillow
try:
    image = Image.open("fond.jpg")
    background_image = ImageTk.PhotoImage(image)
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)  # Redimensionner l'image pour qu'elle couvre toute la fenêtre
except Exception as e:
    print(f"Erreur lors du chargement de l'image de fond : {e}")

# Création des widgets
label = tk.Label(root, text="Entrez une liste de pseudonymes séparés par des virgules :", bg="lightblue")
label.pack(pady=10)

entry = tk.Entry(root, width=60)
entry.pack(pady=10)

check_button = tk.Button(root, text="Vérifier", command=check_usernames_list)
check_button.pack(pady=10)

# Zone de texte défilable pour afficher les résultats
result_text = scrolledtext.ScrolledText(root, width=90, height=15, wrap=tk.WORD)
result_text.pack(pady=10)
result_text.config(state='disabled')  # Rend la zone de texte non modifiable, mais sélectionnable

# Zone de texte pour noter les pseudos
notes_label = tk.Label(root, text="Notes : (pseudos intéressants, etc.)", bg="lightgreen")
notes_label.pack(pady=10)

notes_text = scrolledtext.ScrolledText(root, width=90, height=10, wrap=tk.WORD)
notes_text.pack(pady=10)

# Bouton pour sauvegarder les notes
save_button = tk.Button(root, text="Sauvegarder les notes", command=save_notes)
save_button.pack(pady=10)

# Place les widgets au-dessus de l'image de fond
label.lift()
entry.lift()
check_button.lift()
result_text.lift()
notes_label.lift()
notes_text.lift()
save_button.lift()

# Boucle principale de l'interface
root.mainloop()
