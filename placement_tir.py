
from tkinter import *
from placement_bateaux_sur_grille import CASE, TAILLE_GRILLE

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
        
        # bouton pour tirer sur une case de l'adversaire
        self.joueur = "humain"
        Button(plateau_adversaire, text="Attaquer", command=lambda:self.creation_tir()).place(x=450, y=20)
         
         # raccourcis clavier pour deplacer le tir
        plateau_adversaire.bind("<Up>", self.deplacer)
        plateau_adversaire.bind("<Down>", self.deplacer)
        plateau_adversaire.bind("<Left>", self.deplacer)
        plateau_adversaire.bind("<Right>", self.deplacer)
        plateau_adversaire.bind("<Return>", self.verifier)

        self.parts = []          
        self.longueur = 0               
        self.pos_tir = [0, 0]

        # petite aide
        Label(plateau_adversaire, text="Flèches = déplacer viseur , enter = tirer ").place(x=450, y=220)
    
    '''def choisir_zone_de_tir(joueur):
        if joueur == "humain":'''

    def creation_tir(self):
        if self.joueur == "humain":
            self.parts = []                
            #dessiner la case du tir
            tir = self.zone.create_rectangle(0, 0, CASE, CASE, fill="yellow")
            self.parts.append(tir) 
            
    def deplacer(self, event):
        
        if not self.parts:
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
        
        if not self.parts:
            return
        i, j = self.pos_tir
        for idx, p in enumerate(self.parts):
                x1 = (i + idx) * CASE
                y1 = j * CASE
                x2 = x1 + CASE
                y2 = y1 + CASE
                self.zone.coords(p, x1, y1, x2, y2)
    
    def verifier(self, event):
        for elem in self.parts:
                 self.zone.delete(elem)
        '''if self.pos_tir == self.pos_bateau:
              tir = self.zone.create_rectangle(self.pos_tir[i], self.pos_tir[j], CASE, CASE, fill="red")
        else:
             tir = self.zone.create_rectangle(self.pos_tir[i], self.pos_tir[j], CASE, CASE, fill="white") '''

if __name__ == "__main__":
    root = Tk()
    gestion_tir(root)
    root.mainloop()
