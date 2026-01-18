import random
from tkinter import *
import os
import csv

from fonction_principale import action_bot
from placement_tir import gestion_tir
from placement_bateaux_sur_grille import CASE, TAILLE_GRILLE, Jeu

#creation CSV suvegarde ectt
SCORES_FILE = "scores.csv"
score_joueur = 0
score_bot = 0

def charger_score():
    """
    Charge les scores depuis le fichier CSV.
    Lit les scores du joueur et du bot depuis "scores.csv".
    Si le fichier n'existe pas, il le crée avec des scores à 0.
    Met à jour les variables globales score_joueur et score_bot.
    """
    global score_joueur, score_bot
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["joueur", "bot"])
            writer.writerow([0, 0])
        score_joueur, score_bot = 0, 0
        return
    with open(SCORES_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        score_joueur, score_bot = map(int, next(reader))

def sauvegarder_score():
     """
    Sauvegarde les scores actuels dans le fichier CSV.
    Écrit les scores du joueur et du bot dans "scores.csv".
    Permet de conserver les scores entre plusieurs parties.
    """
    global score_joueur, score_bot
    with open(SCORES_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["joueur", "bot"])
        writer.writerow([score_joueur, score_bot])

#main Tkinter 
accueil = Tk()
accueil.title("Bataille Navale")
accueil.geometry("1600x1143")

# mise de l'image en fond
canvas = Canvas(accueil, width=1600, height=1143)
canvas.place(x=0, y=0)
fond = PhotoImage(file="fond.png")
canvas.create_image(650, 0, anchor="n", image=fond)

# Label titre
Label(accueil, text="Bataille Navale", bg="lightblue", font=("Arial", 50)).place(
    x=430, y=200, width=600, height=100
)

# Label score
charger_score()
label_score = Label(accueil, text=f"Score Joueur : {score_joueur} | Bot : {score_bot}",
                    font=("Arial", 18), bg="lightyellow")
label_score.place(x=500, y=320)



historique_tirs_joueur = set()
historique_tirs_bot = set()
partie_terminee = False

def afficher_fin(victoire):
   """
    Affiche la fin de la partie.
    Affiche un message central indiquant "VICTOIRE" ou "LE BOT EST PLUS FORT".
    Change la couleur du message selon le résultat (vert pour victoire, rouge pour défaite).
    Crée des boutons "Recommencer" et "Quitter".
    Permet de gérer visuellement la fin de la partie.
    """
    global score_joueur, score_bot

    frame_fin = Frame(accueil, bg="lightgrey", bd=3, relief="ridge")
    frame_fin.place(anchor="center", x=800, y=570)

    if victoire:
        message = "VICTOIRE !"
        couleur = "green"
        score_joueur += 1
    else:
        message = "LE BOT EST PLUS FORT"
        couleur = "red"
        score_bot += 1

    Label(frame_fin, text=message, bg=couleur, fg="white", font=("Arial", 30),
          padx=20, pady=10).pack(pady=(10,5))

    Button(frame_fin, text="Recommencer", font=("Arial", 15), bg="lightblue",
           command=lambda: [frame_fin.destroy(), recommencer_partie()]).pack(pady=(5,10))
    Button(frame_fin, text="Quitter", font=("Arial", 15), bg="orange",
           command=accueil.quit).pack(pady=(5,15))

    label_score.config(text=f"Score Joueur : {score_joueur} | Bot : {score_bot}")
    sauvegarder_score()

def verifier_victoire():
    """
    Vérifie si la partie est terminée.
    Parcourt toutes les cases des bateaux du joueur et du bot.
    Si tous les bateaux d’un joueur sont touchés, il perd.
    Met à jour les scores (joueur ou bot) et sauvegarde dans le CSV.
    Affiche un message de victoire ou défaite avec boutons Recommencer/Quitter.
    Désactive les boutons du joueur pour empêcher de continuer à tirer.
    """
    global partie_terminee

    if partie_terminee:
        return

    # Joueur perdu
    joueur_perdu = True
    for elem in terrain_joueur.positions:
        for k in range(elem[3]):
            x = elem[0] + k if elem[2] == 'H' else elem[0]
            y = elem[1] if elem[2] == 'H' else elem[1] + k
            if (x, y) not in historique_tirs_bot:
                joueur_perdu = False
                break
        if not joueur_perdu:
            break

    # Bot perdu
    bot_perdu = True
    for y in range(TAILLE_GRILLE):
        for x in range(TAILLE_GRILLE):
            if terrain_adversaire.grille_occupee[y][x] == 1:
                if (x, y) not in historique_tirs_joueur:
                    bot_perdu = False
                    break
        if not bot_perdu:
            break

    if joueur_perdu or bot_perdu:
        partie_terminee = True
        afficher_fin(not joueur_perdu)
        return True
    return False

def recommencer_partie():
    """Réinitialise la partie pour rejouer.
       Detruit tout pour tout recrer via la fonction placement_bateau_bot() 
    """
    global partie_terminee, historique_tirs_joueur, historique_tirs_bot

    partie_terminee = False
    historique_tirs_joueur.clear()
    historique_tirs_bot.clear()

    # Détruire les anciennes grilles
    terrain_joueur.zone.destroy()
    terrain_adversaire.zone.destroy()

    # Recréer les plateaux
    terrain_joueur.plateau(accueil)
    terrain_adversaire.plateau(accueil)

    # Replacer les bateaux du bot
    terrain_adversaire.grille_occupee = placement_bateau_bot()


def tir_effectue(event=None):
    """
    Lorsque le joueur effectue un tir, 
    cette fonction appelle la fonction action_bot pour que le bot riposte automatiquement.
    """
    if partie_terminee:
        return
    # tir du joueur
    x, y = terrain_adversaire.pos_tir
    historique_tirs_joueur.add((x, y))
    action_bot(terrain_joueur, terrain_adversaire)
    verifier_victoire()


def placement_bateau_bot():
    """
    Place les bateaux du bot de manière aléatoire sur la grille de jeu.

    Cette fonction positionne automatiquement les bateaux de l'adversaire (bot)
    sur la grille de combat en respectant les contraintes suivantes 
    les bateaux ne doivent pas se chevaucher
    chaque bateau est placé de manière aléatoire (position et orientation)
    les bateaux ont des tailles de 2, 3, 4 et 5 cases

    Return:
        list: Une grille 2D (TAILLE_GRILLE x TAILLE_GRILLE) où 1 indique une case
              occupée par un bateau et 0 une case libre
    """

    taille_bateau = [2, 3, 4, 5]
    grille_occupee = [[0 for _ in range(TAILLE_GRILLE)] for _ in range(TAILLE_GRILLE)]
    for elem in taille_bateau:
        placer = False
        while not placer:
            longueur = elem
            sens = random.randint(1, 2)
            if sens == 1:
                orientation = "H"
                y = random.randint(0, TAILLE_GRILLE - 1)
                x = random.randint(0, TAILLE_GRILLE - longueur)
            else:
                orientation = "V"
                x = random.randint(0, TAILLE_GRILLE - 1)
                y = random.randint(0, TAILLE_GRILLE - longueur)
            if not terrain_joueur.chevauchement(grille_occupee, x, y, orientation, longueur):
                for k in range(longueur):
                    i = x + k if orientation == "H" else x
                    j = y if orientation == "H" else y + k
                    grille_occupee[j][i] = 1
                    terrain_adversaire.zone.create_rectangle(
                        i * CASE, j * CASE, (i + 1) * CASE, (j + 1) * CASE, state="hidden"
                    )
                placer = True
    return grille_occupee

 # terein bot et joueur 
terrain_adversaire = gestion_tir(accueil, tir_effectue)
terrain_joueur = Jeu(accueil, lambda: terrain_adversaire.bouger_tir())

def commencer():
    """
    Appelle generer_partie() pour afficher les grilles du joueur et de l’adversaire.
    Place aléatoirement les bateaux du bot avec placement_bateau_bot().
    """
    bouton1.destroy()
    terrain_adversaire.plateau(accueil)
    terrain_joueur.plateau(accueil)
    terrain_adversaire.grille_occupee = placement_bateau_bot()

bouton1 = Button(accueil, text="Commencer", command=commencer)
bouton1.place(x=650, y=450)
Button(accueil, text="Quitter", command=accueil.quit).place(x=665, y=100)

accueil.mainloop()
