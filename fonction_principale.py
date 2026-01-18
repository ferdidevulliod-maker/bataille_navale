import random
from placement_bateaux_sur_grille import *
from placement_tir import *

# garder l'historique des tirs effectués du bot
historique_tirs = set()

# garder l'historique temporaire des tirs reussis du bot
succes_tirs_en_cours = []

# statuts du dernier tir du bot
coord_dernier_tir_bot = None
echec_dernier_tir_bot = True

def action_bot(terrain_joueur, terrain_adversaire):
    """
    Exécute l'action d'attaque du bot sur le plateau adversaire.

    Cette fonction gère la prise de décision du bot pour tirer des coups pendant le jeu.
    Elle implémente deux stratégies :
    1. Sélection aléatoire de coups quand le dernier tir a échoué
    2. Stratégie de tir ciblé quand un bateau a été touché

    Args:
        terrain_joueur (Terrain): Le plateau du joueur où les tirs du bot sont affichés.
        terrain_adversaire (Terrain): Le plateau adverse pour vérifier les résultats.

    Returns:
        tuple: Un tuple contenant :
            - echec_dernier_tir_bot (bool): True si le dernier tir a échoué, False s'il a touché.
            - coord_dernier_tir_bot (tuple): Les coordonnées (x, y) du dernier tir effectué.
    """
    global echec_dernier_tir_bot, coord_dernier_tir_bot
    
    if echec_dernier_tir_bot and succes_tirs_en_cours:
        # Reprendre le tir sur le bateau en cours
        coord_dernier_tir_bot = succes_tirs_en_cours[-1]
        echec_dernier_tir_bot = False
    
    if echec_dernier_tir_bot:
        while True:
            # Choisir une case au hasard si le dernier tir a échoué
            x_case = random.randint(0, TAILLE_GRILLE - 1)
            y_case = random.randint(0, TAILLE_GRILLE - 1)
            if (x_case, y_case) not in historique_tirs:
                break
        
        x1 = x_case * CASE
        y1 = y_case * CASE
        x2 = x1 + CASE
        y2 = y1 + CASE
        
        # Dessiner le tir
        terrain_joueur.tir = terrain_joueur.zone.create_rectangle(
            x1, y1, x2, y2, fill="yellow"
        )
        # Mettre à jour la position du tir
        terrain_joueur.pos_tir = [x1 / CASE, y1 / CASE]
        # Mettre à jour l'historique des tirs
        historique_tirs.add((x_case, y_case))
    else:
        # Faire une stratégie de tir si le dernier tir a touché un bateau
        bateau_touche(coord_dernier_tir_bot, historique_tirs, terrain_joueur)
    
    # Vérifier le résultat du tir
    echec_dernier_tir_bot, coord_dernier_tir_bot = verifier(terrain_joueur, terrain_adversaire)
    action_bot(terrain_joueur, terrain_adversaire)
    verifier_victoire()

    return echec_dernier_tir_bot, coord_dernier_tir_bot
    
def verifier(terrain_joueur, terrain_adversaire, event=None):
    """
    Vérifie les résultats des tirs du joueur et du bot sur leurs terrains respectifs.

    Compare les positions de tir avec les navires placés et met à jour l'affichage
    des terrains en fonction des résultats (touché ou raté).

    Args:
        event (tk.Event, optional): Événement Tkinter déclenché par le joueur. Par défaut None.

    Returns:
        tuple: Un tuple contenant :
            - echec_tir_bot (bool): True si le tir du bot a raté, False s'il a touché.
            - dernier_tir (list): Les coordonnées [x, y] du dernier tir du joueur.
    """
    # part du principe que le tir a échoué
    echec_tir_bot = True

    for elem in terrain_joueur.positions:
        # vérifier si le tir du bot touche un bateau
        if elem[2] == "H":
            # horizontal
            if elem[1] == terrain_joueur.pos_tir[1]:
                # verifie la superposition entre tir et bateau
                if (terrain_joueur.pos_tir[0] >= elem[0]) and (
                    terrain_joueur.pos_tir[0] < elem[0] + elem[3]
                ):
                    # tir réussi
                    echec_tir_bot = False
        else:
            if elem[0] == terrain_joueur.pos_tir[0]:
                # verifie la superposition entre tir et bateau
                if (terrain_joueur.pos_tir[1] >= elem[1]) and (
                    terrain_joueur.pos_tir[1] < elem[1] + elem[3]
                ):
                    # tir réussi
                    echec_tir_bot = False
    if echec_tir_bot:
        # tir raté
        couleur = "white"
        plouf = Label(terrain_joueur.fen, text="Plouf", bg="grey")
        plouf.place(x=450, y=300)
        terrain_joueur.fen.after(1000, plouf.destroy)

    else:
        # tir réussi
        couleur = "red"
        touche = Label(terrain_joueur.fen, text="Touché", bg="red")
        touche.place(x=450, y=300)
        terrain_joueur.fen.after(1000, touche.destroy)
        # enregistre la position du tir réussi
        succes_tirs_en_cours.append(
            (terrain_joueur.pos_tir[0], terrain_joueur.pos_tir[1])
        )
    # dessine le tir
    terrain_joueur.zone.create_rectangle(
        terrain_joueur.pos_tir[0] * CASE,
        terrain_joueur.pos_tir[1] * CASE,
        terrain_joueur.pos_tir[0] * CASE + CASE,
        terrain_joueur.pos_tir[1] * CASE + CASE,
        fill=couleur,
    )
    # part du principe que le tir a échoué
    echec_tir_joueur = True
    # récupère les coordonnées du tir du joueur
    x, y = int(terrain_adversaire.pos_tir[0]), int(terrain_adversaire.pos_tir[1])
    # vérifier si le tir du joueur touche un bateau
    if terrain_adversaire.grille_occupee[y][x] == 1:
        echec_tir_joueur = False
    else:
        echec_tir_joueur = True
    if echec_tir_joueur:
        # tir raté
        couleur = "white"
        plouff = Label(terrain_adversaire.plateau_adversaire, text="Plouf", bg="grey")
        plouff.place(x=850, y=300)
        terrain_adversaire.plateau_adversaire.after(1000, plouff.destroy)
    else:
        # tir réussi
        couleur = "red"
        touchee = Label(terrain_adversaire.plateau_adversaire, text="Touché", bg="red")
        touchee.place(x=850, y=300)
        terrain_adversaire.plateau_adversaire.after(1000, touchee.destroy)
    # dessine le tir
    terrain_adversaire.zone.create_rectangle(
        terrain_adversaire.pos_tir[0] * CASE,
        terrain_adversaire.pos_tir[1] * CASE,
        terrain_adversaire.pos_tir[0] * CASE + CASE,
        terrain_adversaire.pos_tir[1] * CASE + CASE,
        fill=couleur,
    )
    # sauvegarde les coordonnées du dernier tir
    dernier_tir = terrain_joueur.pos_tir
    # réinitialise les positions des tirs
    terrain_joueur.pos_tir = [0, 0]
    terrain_adversaire.pos_tir = [0, 0]
    return echec_tir_bot, dernier_tir

def bateau_touche(dernier_tir, historique_tirs, terrain_joueur):
    """
    Suite à un tir touché, détermine la prochaine case à tirer de manière intelligente.
    La fonction essaie d'abord les cases adjacentes (droite, gauche, haut, bas) au dernier tir
    pour tracer le bateau. Si toutes les cases adjacentes ont déjà été tirées, elle choisit
    une case aléatoire non encore tirée.
    Args:
        dernier_tir (tuple): Les coordonnées (x, y) du dernier tir touché en cases de grille.
        historique_tirs (set): L'ensemble des coordonnées (x, y) des cases déjà tirées.
    Returns:
        None: La fonction modifie directement l'état du terrain du joueur en dessinant
              le tir et en mettant à jour sa position.
    """
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
