import random
from tkinter import *

from placement_tir import gestion_tir
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

# garder l'historique des tirs effectués du bot
historique_tirs = set()

# garder l'historique temporaire des tirs reussis du bot
succes_tirs_en_cours = []

# statuts du dernier tir du bot
coord_dernier_tir_bot = None
echec_dernier_tir_bot = True


def tir_effectue(event=None):
    global echec_dernier_tir_bot, coord_dernier_tir_bot
    echec_dernier_tir_bot, coord_dernier_tir_bot = action_bot(
        echec_dernier_tir_bot, coord_dernier_tir_bot
    )


def notif_bateaux_valides():
    terrain_adversaire.bouger_tir()


terrain_adversaire = gestion_tir(accueil, tir_effectue)
terrain_joueur = Jeu(accueil, notif_bateaux_valides)


def action_bot(echec_bot, coord_tir_bot):
    """
    Exécute l'action de tir du bot lors de son tour.

    Cette fonction gère deux scénarios :
    - Si le dernier tir du bot a échoué (echec_bot=True) : sélectionne une case aléatoire non encore ciblée
    - Si le dernier tir a réussi (echec_bot=False) : traite le bateau touché

    Args:
        echec_bot (bool): Indique si le dernier tir du bot a échoué (True) ou a touché un bateau (False).
        coord_tir_bot (tuple): Les coordonnées du dernier tir du bot (x, y).

    Returns:
        tuple: Un tuple contenant :
            - echec_dernier_tir_bot (bool): True si le tir actuel a échoué, False s'il a touché un bateau.
            - coord_dernier_tir_bot (tuple): Les coordonnées du tir actuel (x, y).
    """
    if echec_bot and succes_tirs_en_cours:
        coord_tir_bot = succes_tirs_en_cours[-1]
        echec_bot = False
    if echec_bot:
        while True:
            x_case = random.randint(0, TAILLE_GRILLE - 1)
            y_case = random.randint(0, TAILLE_GRILLE - 1)
            if (x_case, y_case) not in historique_tirs:
                break
        x1 = x_case * CASE
        y1 = y_case * CASE
        x2 = x1 + CASE
        y2 = y1 + CASE
        terrain_joueur.tir = terrain_joueur.zone.create_rectangle(
            x1, y1, x2, y2, fill="yellow"
        )
        terrain_joueur.pos_tir = [x1 / CASE, y1 / CASE]
        historique_tirs.add((x_case, y_case))
        echec_dernier_tir_bot, coord_dernier_tir_bot = verifier()
    else:
        bateau_touche(coord_tir_bot, historique_tirs)
        echec_dernier_tir_bot, coord_dernier_tir_bot = verifier()
    return echec_dernier_tir_bot, coord_dernier_tir_bot


def verifier(event=None):
    echec_tir_bot = True

    for elem in terrain_joueur.positions:
        if elem[2] == "H":
            if elem[1] == terrain_joueur.pos_tir[1]:
                if (terrain_joueur.pos_tir[0] >= elem[0]) and (
                    terrain_joueur.pos_tir[0] < elem[0] + elem[3]
                ):
                    echec_tir_bot = False
        else:
            if elem[0] == terrain_joueur.pos_tir[0]:
                if (terrain_joueur.pos_tir[1] >= elem[1]) and (
                    terrain_joueur.pos_tir[1] < elem[1] + elem[3]
                ):
                    echec_tir_bot = False
    if echec_tir_bot:
        couleur = "white"
        Label(terrain_joueur.fen, text="Plouf", bg="grey").place(x=450, y=350)
    else:
        couleur = "red"
        Label(terrain_joueur.fen, text="Touché", bg="red").place(x=450, y=350)
        succes_tirs_en_cours.append(
            (terrain_joueur.pos_tir[0], terrain_joueur.pos_tir[1])
        )
    terrain_joueur.zone.create_rectangle(
        terrain_joueur.pos_tir[0] * CASE,
        terrain_joueur.pos_tir[1] * CASE,
        terrain_joueur.pos_tir[0] * CASE + CASE,
        terrain_joueur.pos_tir[1] * CASE + CASE,
        fill=couleur,
    )

    echec_tir_joueur = True
    x, y = int(terrain_adversaire.pos_tir[0]), int(terrain_adversaire.pos_tir[1])
    if terrain_adversaire.grille_occupee[y][x] == 1:
        echec_tir_joueur = False
    else:
        echec_tir_joueur = True
    if echec_tir_joueur:
        couleur = "white"
        Label(terrain_adversaire.plateau_adversaire, text="Plouf", bg="grey").place(
            x=850, y=350
        )
    else:
        couleur = "red"
        Label(terrain_adversaire.plateau_adversaire, text="Touché", bg="red").place(
            x=850, y=350
        )
    terrain_adversaire.zone.create_rectangle(
        terrain_adversaire.pos_tir[0] * CASE,
        terrain_adversaire.pos_tir[1] * CASE,
        terrain_adversaire.pos_tir[0] * CASE + CASE,
        terrain_adversaire.pos_tir[1] * CASE + CASE,
        fill=couleur,
    )
    dernier_tir = terrain_joueur.pos_tir
    terrain_joueur.pos_tir = [0, 0]
    terrain_adversaire.pos_tir = [0, 0]
    return echec_tir_bot, dernier_tir


def bateau_touche(dernier_tir, historique_tirs):
    # Suite à un tir touché, détermine la prochaine case à tirer
    # Essaie la case à droite
    if (
        dernier_tir[0] + 1 < TAILLE_GRILLE
        and (dernier_tir[0] + 1, dernier_tir[1]) not in historique_tirs
    ):
        x1 = (dernier_tir[0] + 1) * CASE
        y1 = dernier_tir[1] * CASE
    # Essaie la case à gauche
    elif (dernier_tir[0] - 1, dernier_tir[1]) not in historique_tirs:
        x1 = (dernier_tir[0] - 1) * CASE
        y1 = dernier_tir[1] * CASE

    else:
        # Essaie la case en haut
        if (
            dernier_tir[1] + 1 < TAILLE_GRILLE
            and (dernier_tir[0], dernier_tir[1] + 1) not in historique_tirs
        ):
            x1 = dernier_tir[0] * CASE
            y1 = (dernier_tir[1] + 1) * CASE
        # Essaie la case en bas
        elif (dernier_tir[0], dernier_tir[1] - 1) not in historique_tirs:
            x1 = dernier_tir[0] * CASE
            y1 = (dernier_tir[1] - 1) * CASE
        else:
            # Si toutes les cases autour ont déjà été tirées, choisir une case aléatoire
            while True:
                x_case = random.randint(0, TAILLE_GRILLE - 1)
                y_case = random.randint(0, TAILLE_GRILLE - 1)
                if (x_case, y_case) not in historique_tirs:
                    break
            x1 = x_case * CASE
            y1 = y_case * CASE
            
    # Définit les coordonnées du rectangle à dessiner
    x2 = x1 + CASE
    y2 = y1 + CASE
    # Ajoute la nouvelle case tirée à l'historique
    historique_tirs.add((x1 / CASE, y1 / CASE))
    # Dessine le rectangle représentant le tir
    terrain_joueur.tir = terrain_joueur.zone.create_rectangle(
        x1, y1, x2, y2, fill="yellow"
    )
    # Met à jour les coordonnées du tir actuel
    terrain_joueur.pos_tir = [x1 / CASE, y1 / CASE]


def commencer():
    bouton1.destroy()
    generer_partie()
    placement_bateau_bot()
    terrain_adversaire.grille_occupee = placement_bateau_bot()


def generer_partie():
    terrain_adversaire.plateau(accueil)
    terrain_joueur.plateau(accueil)


bouton1 = Button(accueil, text="Commencer", command=lambda: commencer())
bouton1.place(x=650, y=450)
Button(accueil, text="Quitter", command=accueil.quit).place(x=665, y=100)


def placement_bateau_bot():
    taille_bateau = [2, 3, 4, 5]
    grille_occupee = [
        [0 for _ in range(TAILLE_GRILLE)] for _ in range(TAILLE_GRILLE)
    ]
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
            if (
                terrain_joueur.chevauchement(
                    grille_occupee, x, y, orientation, longueur
                )
                == False
            ):
                for k in range(longueur):
                    i = x + k if orientation == "H" else x
                    j = y if orientation == "H" else y + k
                    grille_occupee[j][i] = 1
                    terrain_adversaire.zone.create_rectangle(
                        i * CASE,
                        j * CASE,
                        (i + 1) * CASE,
                        (j + 1) * CASE,
                        state="hidden",
                    )
                placer = True
    return grille_occupee


accueil.mainloop()
