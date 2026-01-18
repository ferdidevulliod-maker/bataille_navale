import random
from tkinter import *

from fonction_principale import action_bot
from placement_tir import GestionTir
from placement_bateaux_sur_grille import CASE, TAILLE_GRILLE, Jeu

accueil = Tk()

# création d'un titre
Label(accueil, text="Bataille navale").place(x=650, y=200)

# création d'une image en fond
canvas = Canvas(accueil, width=1600, height=1143)
canvas.place(x=0, y=0)
fond = PhotoImage(file="fond.png")
canvas.create_image(650, 0, anchor="n", image=fond)

# création d'un titre
Label(accueil, text="Bataille navale", bg="lightblue", font=("Arial", 50)).place(
    x=430, y=200, width=600, height=100
)

def tir_effectue(event=None):
    """
    Exécute un tir du bot dans le jeu de bataille navale.

    Paramètres:
        event (tkinter.Event, optionnel): Objet événement passé par la liaison d'événement tkinter.
            Par défaut None.

    Retour:
        None
    """
    action_bot(terrain_joueur, terrain_adversaire)


def notif_bateaux_valides():
    # active le déplacement du tir une fois les bateaux placés
    terrain_adversaire.bouger_tir()


# récupére les classes des autres fichiers
terrain_adversaire = GestionTir(accueil, tir_effectue)
terrain_joueur = Jeu(accueil, notif_bateaux_valides)


def commencer():
    # démarre la partie
    bouton1.destroy()
    generer_partie()
    placement_bateau_bot()
    terrain_adversaire.grille_occupee = placement_bateau_bot()


def generer_partie():
    # dessiner les plateaux de jeu
    terrain_adversaire.plateau(accueil)
    terrain_joueur.plateau(accueil)


# bouton de la page d'accueil
bouton1 = Button(accueil, text="Commencer", command=lambda: commencer())
bouton1.place(x=650, y=450)
Button(accueil, text="Quitter", command=accueil.quit).place(x=665, y=100)


def placement_bateau_bot():
    """
    Place les bateaux du bot de manière aléatoire sur la grille de jeu.

    Cette fonction positionne automatiquement les bateaux de l'adversaire (bot)
    sur la grille de combat en respectant les contraintes suivantes :
    - Les bateaux ne doivent pas se chevaucher
    - Chaque bateau est placé de manière aléatoire (position et orientation)
    - Les bateaux ont des tailles de 2, 3, 4 et 5 cases

    Returns:
        list: Une grille 2D (TAILLE_GRILLE x TAILLE_GRILLE) où 1 indique une case
              occupée par un bateau et 0 une case libre
    """
    # liste des tailles des bateaux à placer
    taille_bateau = [2, 3, 4, 5]
    # grille pour suivre les cases occupées
    grille_occupee = [
        [0 for _ in range(TAILLE_GRILLE)] for _ in range(TAILLE_GRILLE)
    ]
    for elem in taille_bateau:
        # place les bateaux un par un
        placer = False
        while not placer:
            longueur = elem
            # orientation aléatoire
            sens = random.randint(1, 2)
            if sens == 1:
                # horizontal
                orientation = "H"
                y = random.randint(0, TAILLE_GRILLE - 1)
                x = random.randint(0, TAILLE_GRILLE - longueur)
            else:
                # vertical
                orientation = "V"
                # position aléatoire
                x = random.randint(0, TAILLE_GRILLE - 1)
                y = random.randint(0, TAILLE_GRILLE - longueur)
            if (
                terrain_joueur.chevauchement(
                    grille_occupee, x, y, orientation, longueur
                )
                == False
                # pas de chevauchement
            ):
                # Marque les cases occupées par le bateau dans la grille
                for k in range(longueur):
                    # Calcule les coordonnées x et y selon l'orientation
                    i = x + k if orientation == "H" else x
                    j = y if orientation == "H" else y + k
                    # Marque la case comme occupée (1)
                    grille_occupee[j][i] = 1
                    # Dessine un rectangle invisible pour représenter le bateau du bot
                    terrain_adversaire.zone.create_rectangle(
                        i * CASE,
                        j * CASE,
                        (i + 1) * CASE,
                        (j + 1) * CASE,
                        state="hidden",
                    )
                # bateau placé
                placer = True
    return grille_occupee

accueil.mainloop()
