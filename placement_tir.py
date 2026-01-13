
from tkinter import *
from placement_bateaux_sur_grille import CASE, TAILLE_GRILLE
import random

class gestion_tir:
    def __init__(self, plateau_adversaire, tir_effectue):
        self.plateau_adversaire = plateau_adversaire
        self.plateau_adversaire.title("Bataille navale - plateau de l'adversaire")
        self.plateau_adversaire.geometry("900x500")
        
        self.longueur = 0               
        self.pos_tir = [0, 0]
        self.tir = None
        self.joueur = "humain" #premier joueur
        self.tir_effectue = tir_effectue
        self.grille_occupee = None
         
    def bouger_tir(self):   # raccourcis clavier pour deplacer le tir
        self.plateau_adversaire.bind("<Up>", self.deplacer)
        self.plateau_adversaire.bind("<Down>", self.deplacer)
        self.plateau_adversaire.bind("<Left>", self.deplacer)
        self.plateau_adversaire.bind("<Right>", self.deplacer)
        self.plateau_adversaire.bind("<Return>", self.tir_effectue)
        # bouton pour tirer sur une case de l'adversaire
        Button(self.plateau_adversaire, text="Attaquer", command=lambda:self.creation_tir()).place(x=1230, y=400)

    def plateau(self,plateau_adversaire):
    #dessin du plateau de jeu 
        self.zone = Canvas(plateau_adversaire, width=CASE*TAILLE_GRILLE, height=CASE*TAILLE_GRILLE, bg="lightblue")
        self.zone.place(x=800, y=400)
    # grille ou l'on met les bateaux 
        for x in range(TAILLE_GRILLE):
            for y in range(TAILLE_GRILLE):
                self.zone.create_rectangle(x*CASE, y*CASE, (x+1)*CASE, (y+1)*CASE, outline="black")
    # petite aide
        Label(plateau_adversaire, text="Flèches = déplacer viseur , enter = tirer ").place(x=800, y=350)
    #nom plateau
        Label(plateau_adversaire, text="Plateau ennemi").place(x=950, y=820)

    def creation_tir(self):                
            #dessiner la case du tir
            self.tir = self.zone.create_rectangle(0, 0, CASE, CASE, fill="yellow")
            #self.pos_tir = [x1/CASE, y1/CASE]
    
       
    def deplacer(self, event):
        print(f"deplacer")#à supprimer
        if not self.tir:
            return
        i, j = self.pos_tir

        if event.keysym == "Up":
            if j > 0:
                j -= 1
        elif event.keysym == "Down":
            if j < TAILLE_GRILLE - 1:
                j += 1
        elif event.keysym == "Left":
            if i > 0:
                i -= 1
        elif event.keysym == "Right":
            if i < TAILLE_GRILLE - 1:
                i += 1

        self.pos_tir = [i, j]
        self.dessiner()
    
    def dessiner(self):
        if not self.tir:
            return
        i, j = self.pos_tir
        x1 = i * CASE
        y1 = j * CASE
        x2 = x1 + CASE
        y2 = y1 + CASE
        self.zone.coords(self.tir, x1, y1, x2, y2)

    #changement de joueur
    def tour_suivant(self,event=None):
        if self.joueur == "humain":                
            return self.tour(1)
        else:
            return self.tour(2)
        

    def tour(self,a):#action du joueur
        if a == 1:
            self.joueur = "bot"
            self.creation_tir()
        elif a == 2:
            self.joueur = "humain"


if __name__ == "__main__":
    root = Tk()
    gestion_tir(root)
    root.mainloop()
