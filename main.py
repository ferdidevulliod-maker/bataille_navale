
import random
from  tkinter import*
from placement_tir import gestion_tir
from placement_bateaux_sur_grille import CASE, TAILLE_GRILLE, Jeu

accueil=Tk()

#création d'un titre
Label(accueil, text="Bataille navale").place(x=650, y=200)

#création d'une image en fond
canvas = Canvas(accueil,width=1600, height=1143)
canvas.place(x=0,y=0)
fond=PhotoImage(file="fond.png")
canvas.create_image(650, 0 , anchor="n", image=fond)

#création d'un titre
Label(accueil, text="Bataille navale",bg="lightblue",font=("Arial", 50)).place(x=430, y=200, width=600, height=100)

# garder l'historique des tirs effectués
historique_tirs = set()

def tir_effectue(event):
    action_bot()

def notif_bateaux_valides():
    terrain_adversaire.bouger_tir()

terrain_adversaire = gestion_tir(accueil, tir_effectue)
terrain_joueur = Jeu(accueil, notif_bateaux_valides)

#definit le comportement du bot adverse
def action_bot():
    in_water, dernier_tir = verifier(terrain_adversaire.grille_occupee)
    grille = terrain_adversaire.grille_occupee
    if in_water:
        print("a")
        while True:
            # choisit une case aléatoire pour le tir du bot
            x_case = random.randint(0, TAILLE_GRILLE - 1)
            y_case = random.randint(0, TAILLE_GRILLE - 1)
            if (x_case, y_case) not in historique_tirs:
                break
        x1 = x_case * CASE  
        y1 = y_case * CASE 
        x2 = x1 + CASE
        y2 = y1 + CASE
        terrain_joueur.tir = terrain_joueur.zone.create_rectangle(x1, y1, x2, y2, fill="yellow")
        terrain_joueur.pos_tir = [x1/CASE, y1/CASE]
        historique_tirs.add((x_case, y_case))
        verifier(grille)
    else:
        bateau_touche(dernier_tir, historique_tirs)
        verifier(grille)
        print("b")
        return historique_tirs


#vérifie la présence d'un bateau sur la case du tir
def verifier(grille_occupee,event=None):
    in_water = True
    for elem in terrain_joueur.positions:
        if elem[2] == 'H':
            # bateau en postion horizontale
            if elem[1] == terrain_joueur.pos_tir[1]:
                # tir sur la même ligne que le bateau
                if (terrain_joueur.pos_tir[0] >= elem[0]) and (terrain_joueur.pos_tir[0] < elem[0] + elem[3]):
                    in_water = False
        else:
            # bateau en postion verticale
            if elem[0] == terrain_joueur.pos_tir[0]:
                # tir sur la même colonne que le bateau
                if (terrain_joueur.pos_tir[1] >= elem[1]) and (terrain_joueur.pos_tir[1] < elem[1] + elem[3]):
                    in_water = False
    if in_water:
        couleur = "white"
        Label(terrain_joueur.fen, text="Plouf", bg="grey").place(x=450, y=350)
    else:
        couleur = "red"
        Label(terrain_joueur.fen, text="Touché", bg="red").place(x=450, y=350)
    terrain_joueur.zone.create_rectangle(
        terrain_joueur.pos_tir[0] * CASE,\
        terrain_joueur.pos_tir[1] * CASE,\
        terrain_joueur.pos_tir[0] * CASE + CASE,\
        terrain_joueur.pos_tir[1] * CASE + CASE, \
        fill=couleur)
    x, y = int(terrain_adversaire.pos_tir[0]), int(terrain_adversaire.pos_tir[1])
    if terrain_adversaire.grille_occupee[y][x] == 1:
        in_water = False
    else: 
        in_water = True
    if in_water:
        couleur = "white"
        Label(terrain_adversaire.plateau_adversaire, text="Plouf", bg="grey").place(x=850, y=350)
    else:
        couleur = "red"
        Label(terrain_adversaire.plateau_adversaire, text="Touché", bg="red").place(x=850, y=350)
    terrain_adversaire.zone.create_rectangle(
        terrain_adversaire.pos_tir[0] * CASE,\
        terrain_adversaire.pos_tir[1] * CASE,\
        terrain_adversaire.pos_tir[0] * CASE + CASE,\
        terrain_adversaire.pos_tir[1] * CASE + CASE, \
        fill=couleur)
    dernier_tir = terrain_joueur.pos_tir
    terrain_joueur.pos_tir = [0,0]
    terrain_adversaire.pos_tir = [0,0]
    terrain_adversaire.tour_suivant()
    return in_water, dernier_tir

def bateau_touche(dernier_tir, historique_tirs):
    if dernier_tir[0] + 1 < TAILLE_GRILLE and (dernier_tir[0] + 1, dernier_tir[1]) not in historique_tirs:
        x1 = (dernier_tir[0] + 1) * CASE
        y1 = dernier_tir[1] * CASE
        x2 = x1 + CASE
        y2 = y1 + CASE
    elif (dernier_tir[0] - 1, dernier_tir[1]) not in historique_tirs:
        x1 = (dernier_tir[0] - 1) * CASE
        y1 = dernier_tir[1] * CASE
        x2 = x1 + CASE
        y2 = y1 + CASE

    else:
        if dernier_tir[1] + 1 < TAILLE_GRILLE and (dernier_tir[0], dernier_tir[1] + 1) not in historique_tirs:
            x1 = dernier_tir[0] * CASE
            y1 = (dernier_tir[1] + 1) * CASE
            x2 = x1 + CASE
            y2 = y1 + CASE
        elif (dernier_tir[0], dernier_tir[1] - 1) not in historique_tirs: 
            x1 = dernier_tir[0] * CASE
            y1 = (dernier_tir[1] - 1) * CASE
            x2 = x1 + CASE
            y2 = y1 + CASE
    historique_tirs.add((dernier_tir[0], dernier_tir[1]))
    terrain_joueur.tir = terrain_joueur.zone.create_rectangle(x1, y1, x2, y2, fill="yellow")
    verifier(terrain_joueur.grille_occupee)
    return historique_tirs

def commencer():
    bouton1.destroy() 
    generer_partie()
    placement_bateau_bot()
    terrain_adversaire.grille_occupee = placement_bateau_bot()

def generer_partie():
    terrain_adversaire.plateau(accueil)
    terrain_joueur.plateau(accueil)

bouton1 = Button(accueil, text="Commencer", command=lambda:commencer())
bouton1.place(x=650,y=450)
Button(accueil, text="Quitter", command=accueil.quit).place(x=665,y=100)

def placement_bateau_bot():
    taille_bateau = [2,3,4,5]
    # construire grille locale à partir des bateaux déjà validés
    grille_occupee = [[0 for _ in range(TAILLE_GRILLE)] for _ in range(TAILLE_GRILLE)]
    for elem in taille_bateau:
        placer = False
        while not placer:
            longueur = elem
            sens = random.randint(1,2)
            if sens == 1:#orientation horizontale
                orientation = "H"
                y = random.randint(0,TAILLE_GRILLE-1)
                x = random.randint(0,TAILLE_GRILLE-longueur)
            else:#orientation verticale
                orientation = "V"
                x = random.randint(0,TAILLE_GRILLE-1)
                y = random.randint(0,TAILLE_GRILLE-longueur)
            # vérifier chevauchement / bordure
            if terrain_joueur.chevauchement(grille_occupee, x, y, orientation, longueur) == False:
                for k in range(longueur):
                    # marquer la grille comme occupée
                    i = x + k if orientation == "H" else x
                    j = y if orientation == "H" else y + k
                    grille_occupee[j][i] = 1
                    terrain_adversaire.zone.create_rectangle(
                                i * CASE,
                                j * CASE,
                                (i + 1) * CASE,
                                (j + 1) * CASE,
                                state='hidden')  # cacher le bateau
                placer = True
    return grille_occupee
accueil.mainloop()
