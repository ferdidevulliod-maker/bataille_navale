import random
from placement_bateaux_sur_grille import CASE, TAILLE_GRILLE

# Historiques des tirs
historique_tirs_bot = set()       # tirs du bot
historique_tirs_joueur = set()    # tirs du joueur
succes_tirs_en_cours = []        # tirs réussis du bot

# Statut du dernier tir du bot
coord_dernier_tir_bot = None
echec_dernier_tir_bot = True

# Variable globale partie terminée
partie_terminee = False

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
    global coord_dernier_tir_bot, echec_dernier_tir_bot, succes_tirs_en_cours, partie_terminee

    if partie_terminee:
        return

    # si le dernier tir a touché, continuer autour
    if not echec_dernier_tir_bot and succes_tirs_en_cours:
        dernier_tir = succes_tirs_en_cours[-1]
        x_next, y_next = dernier_tir
        # essayer cases adjacentes dans l'ordre droite, gauche, bas, haut
        voisins = [
            (x_next + 1, y_next),
            (x_next - 1, y_next),
            (x_next, y_next + 1),
            (x_next, y_next - 1)
        ]
        for vx, vy in voisins:
            if 0 <= vx < TAILLE_GRILLE and 0 <= vy < TAILLE_GRILLE and (vx, vy) not in historique_tirs_bot:
                x_case, y_case = vx, vy
                break
        else:
            # si toutes déjà tirées, choisir aléatoirement
            while True:
                x_case = random.randint(0, TAILLE_GRILLE - 1)
                y_case = random.randint(0, TAILLE_GRILLE - 1)
                if (x_case, y_case) not in historique_tirs_bot:
                    break
    else:
        # tir aléatoire
        while True:
            x_case = random.randint(0, TAILLE_GRILLE - 1)
            y_case = random.randint(0, TAILLE_GRILLE - 1)
            if (x_case, y_case) not in historique_tirs_bot:
                break

    # mettre à jour les coordonnées du tir
    terrain_joueur.pos_tir = [x_case, y_case]

    # dessiner le tir
    x1 = x_case * CASE
    y1 = y_case * CASE
    x2 = x1 + CASE
    y2 = y1 + CASE
    terrain_joueur.tir = terrain_joueur.zone.create_rectangle(x1, y1, x2, y2, fill="yellow")

    # ajouter au bon historique
    historique_tirs_bot.add((x_case, y_case))

    # vérifier si le tir touche un bateau
    echec_dernier_tir_bot, coord_dernier_tir_bot = verifier(terrain_joueur, terrain_adversaire)

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
    global succes_tirs_en_cours

    # Tir du bot
    echec_tir_bot = True
    for elem in terrain_joueur.positions:
        x, y, orient, longueur = elem
        if orient == "H" and terrain_joueur.pos_tir[1] == y and x <= terrain_joueur.pos_tir[0] < x + longueur:
            echec_tir_bot = False
        elif orient == "V" and terrain_joueur.pos_tir[0] == x and y <= terrain_joueur.pos_tir[1] < y + longueur:
            echec_tir_bot = False

    if echec_tir_bot:
        couleur = "white"
    else:
        couleur = "red"
        succes_tirs_en_cours.append(tuple(terrain_joueur.pos_tir))

    # dessiner le tir sur le plateau joueur
    x, y = terrain_joueur.pos_tir
    terrain_joueur.zone.create_rectangle(x * CASE, y * CASE, x * CASE + CASE, y * CASE + CASE, fill=couleur)

    # Tir du joueur
    xj, yj = terrain_adversaire.pos_tir
    if terrain_adversaire.grille_occupee[yj][xj] == 1:
        couleur_joueur = "red"
    else:
        couleur_joueur = "white"
    terrain_adversaire.zone.create_rectangle(xj * CASE, yj * CASE, xj * CASE + CASE, yj * CASE + CASE, fill=couleur_joueur)

    # Retourner le résultat du tir du bot et ses coordonnées
    return echec_tir_bot, terrain_joueur.pos_tir

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
                
            historique_tirs_bot.add((x_case, y_case))
            
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