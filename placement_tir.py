
from tkinter import *
from placement_bateaux_sur_grille import CASE, TAILLE_GRILLE
import random

class gestion_tir:
    def __init__(self, plateau_adversaire):
        self.plateau_adversaire = plateau_adversaire
        self.plateau_adversaire.title("Bataille navale - plateau de l'adversaire")
        self.plateau_adversaire.geometry("900x500")

        #dessin du plateau de l'adversaire 
        self.zone = Canvas(plateau_adversaire, width=CASE*TAILLE_GRILLE, height=CASE*TAILLE_GRILLE, bg="lightblue")
        self.zone.place(x=20, y=20)

        # grille ou l'on met les bateaux 
        for x in range(TAILLE_GRILLE):
            for y in range(TAILLE_GRILLE):
                self.zone.create_rectangle(x*CASE, y*CASE, (x+1)*CASE, (y+1)*CASE, outline="black")
        
        self.longueur = 0               
        self.pos_tir = [0, 0]
        self.tir = None
        self.joueur = "humain" #premier joueur
        
        # bouton pour tirer sur une case de l'adversaire
        Button(plateau_adversaire, text="Attaquer", command=lambda:self.creation_tir()).place(x=450, y=20)
         
         # raccourcis clavier pour deplacer le tir
        plateau_adversaire.bind("<Up>", self.deplacer)
        plateau_adversaire.bind("<Down>", self.deplacer)
        plateau_adversaire.bind("<Left>", self.deplacer)
        plateau_adversaire.bind("<Right>", self.deplacer)
        plateau_adversaire.bind("<Return>", self.verifier)

        # petite aide
        Label(plateau_adversaire, text="Flèches = déplacer viseur , enter = tirer ").place(x=450, y=220)

    def creation_tir(self):
        print(f"creation_tir pour joueur {self.joueur}, tir: {self.tir}")#à supprimer
        if self.joueur == "humain":                
            #dessiner la case du tir
            self.tir = self.zone.create_rectangle(0, 0, CASE, CASE, fill="yellow")
        elif self.joueur == "bot":
            self.action_bot()
       
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
        print(f"dessiner")#à supprimer
        if not self.tir:
            return
        i, j = self.pos_tir
        x1 = i * CASE
        y1 = j * CASE
        x2 = x1 + CASE
        y2 = y1 + CASE
        self.zone.coords(self.tir, x1, y1, x2, y2)

    def verifier(self,event=None):
        print(f"verifier {self.pos_tir}")#à supprimer
        self.zone.delete(self.tir)
        if self.joueur == "humain":
            color = "blue"
        else:
            color = "green"
        self.zone.create_rectangle(self.pos_tir[0] * CASE, self.pos_tir[1] * CASE, self.pos_tir[0] * CASE + CASE, self.pos_tir[1] * CASE + CASE, fill=color)
        self.pos_tir = [0,0]
        #else:
        #    self.zone.create_rectangle(self.pos_tir[0], self.pos_tir[1], CASE, CASE, fill="green")
        '''if self.pos_tir == self.pos_bateau:
              tir = self.zone.create_rectangle(self.pos_tir[i], self.pos_tir[j], CASE, CASE, fill="red")
        else:
             tir = self.zone.create_rectangle(self.pos_tir[i], self.pos_tir[j], CASE, CASE, fill="white") '''
        if self.joueur == "humain":                
            return self.tour(1)
        else:
            return self.tour(2)
        

        
    def action_bot(self):
        # choisit une case aléatoire pour le tir du bot
        x_case = random.randint(0, TAILLE_GRILLE - 1)
        y_case = random.randint(0, TAILLE_GRILLE - 1)
        x1 = x_case * CASE  
        y1 = y_case * CASE 
        x2 = x1 + CASE
        y2 = y1 + CASE
        self.tir = self.zone.create_rectangle(x1, y1, x2, y2, fill="yellow")
        self.pos_tir = [x1/CASE, y1/CASE]
        #event = self.master.event_generate("<Return>")
        #self.verifier(event)
        self.verifier()

    def tour(self,a):#pour passer au joueur suivant
        if a == 1:
            self.joueur = "bot"
            self.creation_tir()
        elif a == 2:
            self.joueur = "humain"


if __name__ == "__main__":
    root = Tk()
    gestion_tir(root)
    root.mainloop()
