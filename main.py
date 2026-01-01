
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
    terrain_joueur.zone.delete(terrain_joueur.tir)
    '''if self.joueur == "humain":
        color = "blue"
    else:
        color = "green"'''
    terrain_joueur.zone.create_rectangle(
        terrain_joueur.pos_tir[0] * CASE, 
        terrain_joueur.pos_tir[1] * CASE, 
        terrain_joueur.pos_tir[0] * CASE + CASE, 
        terrain_joueur.pos_tir[1] * CASE + CASE, 
        fill="blue")
    terrain_joueur.pos_tir = [0,0]
    #else:
    #    self.zone.create_rectangle(self.pos_tir[0], self.pos_tir[1], CASE, CASE, fill="green")
    '''if self.pos_tir == self.pos_bateau:
            tir = self.zone.create_rectangle(self.pos_tir[i], self.pos_tir[j], CASE, CASE, fill="red")
    else:
            tir = self.zone.create_rectangle(self.pos_tir[i], self.pos_tir[j], CASE, CASE, fill="white") '''
    terrain_adversaire.tour_suivant()

terrain_adversaire = gestion_tir(accueil, tir_effectue)
terrain_joueur = Jeu(accueil)

def commencer():
    bouton1.destroy() 
    generer_partie()

def generer_partie():
    terrain_adversaire.plateau(accueil)
    terrain_joueur.plateau(accueil)



bouton1 = Button(accueil, text="Commencer", command=lambda:commencer())
bouton1.place(x=650,y=450)
Button(accueil, text="Quitter", command=accueil.quit).place(x=665,y=100)



accueil.mainloop()
