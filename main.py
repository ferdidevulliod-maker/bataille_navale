
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

def tir_effectue(event):
    print("tir effectué!!!")
    action_bot()

#definit le comportement du bot adverse
def action_bot():
    # choisit une case aléatoire pour le premier tir du bot
    x_case = random.randint(0, TAILLE_GRILLE - 1)
    y_case = random.randint(0, TAILLE_GRILLE - 1)
    x1 = x_case * CASE  
    y1 = y_case * CASE 
    x2 = x1 + CASE
    y2 = y1 + CASE
    terrain_joueur.tir = terrain_joueur.zone.create_rectangle(x1, y1, x2, y2, fill="yellow")
    terrain_joueur.pos_tir = [x1/CASE, y1/CASE]
    verifier()

#vérifie la présence d'un bateau sur la case du tir
def verifier(event=None):
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
            terrain_joueur.pos_tir[0] * CASE, 
            terrain_joueur.pos_tir[1] * CASE, 
            terrain_joueur.pos_tir[0] * CASE + CASE, 
            terrain_joueur.pos_tir[1] * CASE + CASE, 
            fill=couleur)
    terrain_joueur.pos_tir = [0,0]
    terrain_adversaire.tour_suivant()


terrain_adversaire = gestion_tir(accueil, tir_effectue)
terrain_joueur = Jeu(accueil)


def commencer():
    bouton1.destroy() 
    generer_partie()
    placement_bateau_bot()

def generer_partie():
    terrain_adversaire.plateau(accueil)
    terrain_joueur.plateau(accueil)

bouton1 = Button(accueil, text="Commencer", command=lambda:commencer())
bouton1.place(x=650,y=450)
Button(accueil, text="Quitter", command=accueil.quit).place(x=665,y=100)

def placement_bateau_bot():
    n = 2
    for i in range(4):
        n +=1
        for k in range (n):
            terrain_adversaire.rect = terrain_adversaire.zone.create_rectangle(k*CASE, 0, (k+1)*CASE, CASE, fill="gray")



accueil.mainloop()
