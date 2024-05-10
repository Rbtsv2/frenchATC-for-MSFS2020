import os
import platform
import sys
from colorama import Fore, Back, Style
from config import DATA_PROVIDER


def config(q):
    print(Fore.GREEN + "✅ Informations météo délivrées par {0}".format(DATA_PROVIDER) + Style.RESET_ALL)
    print(Fore.GREEN + "✅ Liste des chemins de recherche dans sys.path :" + Style.RESET_ALL)
    for path in sys.path:
        print(Fore.YELLOW + "  => " + path + Style.RESET_ALL) 

    print(Fore.GREEN + "✅ La file d'attente a été correctement initialisée." + Style.RESET_ALL)
    for item in list(q.queue):
        print(Fore.YELLOW + "  => " + item + Style.RESET_ALL)

def start():
    while True:
        reponse = input("Le programme est prêt a être lancé ? (Yes/Y ou No/N) : ").strip().lower()
        if reponse in ['yes', 'y']:
            print("Vous avez choisi 'Yes'. Le programme continue...")
            break  # Sort de la boucle si la réponse est 'yes' ou 'y'
        elif reponse in ['no', 'n']:
            sys.exit(1)
            break  # Sort de la boucle si la réponse est 'no' ou 'n'
        else:
            print("Réponse non valide. Veuillez saisir 'Yes' ou 'No'.")

def display(car:str)->bool:
    """
    Affiche la chaine de caractère donnée en paramètre à la manière d'un print
    Pré  : chaine de caractères à afficher
    Post : renvoie un booléen (True) une fois exécuté
    """
    print(car)
    return True

def defTitleOfWindow(car:str)->bool:
    """
    Modifie le titre de la fenêtre de l'invite de commandes
    Pré  : chaine de caractères qui sera le nom de la fenêtre
    Post : renvoie un booléen (True) une fois exécuté
    """
    os.system("title " + car)
    return True

def clear()->bool:
    """
    Efface le texte dans l'invite de commande
    Pré  : /
    Post : renvoie un booléen (True) une fois exécuté
    """
    if  platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

    return True