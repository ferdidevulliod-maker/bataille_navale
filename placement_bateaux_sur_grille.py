from tkinter import *

# paramètres
CASE = 50
TAILLE_GRILLE = 8

class Jeu:
    def __init__(self, fen):
        self.fen = fen
        self.fen.title("Bataille navale - placement")
        self.fen.geometry("900x500")

        # creer le rectangle et le place en haut a gauche de la grille 
        self.parts = []          
        self.longueur = 0        
        self.orient = "H"        
        self.pos = [0, 0]       

        # raccourcis clavier pour deplacer le bateau
        fen.bind("<Up>", self.deplacer)
        fen.bind("<Down>", self.deplacer)
        fen.bind("<Left>", self.deplacer)
        fen.bind("<Right>", self.deplacer)
        fen.bind("r", self.tourner)
        fen.bind("R", self.tourner)
    
    def plateau(self,fen):
    #dessin du plateau de jeux 
        self.zone = Canvas(fen, width=CASE*TAILLE_GRILLE, height=CASE*TAILLE_GRILLE, bg="lightblue")
        self.zone.place(x=20, y=400)
    # grille ou l'on met les bateaux 
        for x in range(TAILLE_GRILLE):
            for y in range(TAILLE_GRILLE): 
                self.zone.create_rectangle(x*CASE, y*CASE, (x+1)*CASE, (y+1)*CASE, outline="black")
    # boutons pour choisir la taille du bateau
        Button(fen, text="Bateau 2", command=lambda: self.nouveau_bateau(2)).place(x=450, y=420)
        Button(fen, text="Bateau 3", command=lambda: self.nouveau_bateau(3)).place(x=450, y=460)
        Button(fen, text="Bateau 4", command=lambda: self.nouveau_bateau(4)).place(x=450, y=500)
        Button(fen, text="Bateau 5", command=lambda: self.nouveau_bateau(5)).place(x=450, y=540)
    # petite aide
        Label(fen, text="Flèches = déplacer   R = tourner").place(x=20, y=350)
    #nom plateau
        Label(fen, text="Plateau joueur").place(x=170, y=820)


    def nouveau_bateau(self, n):
        
        self.longueur = n
        self.pos = [0, 0]
        self.orient = "H"
        # supprimer l'ancien
        for p in self.parts:
            self.zone.delete(p)
        self.parts = []
        # dessiner les cases du bateau
        for k in range(n):
            rect = self.zone.create_rectangle(k*CASE, 0, (k+1)*CASE, CASE, fill="gray")
            self.parts.append(rect)

    def dessiner(self):
        
        if not self.parts:
            return
        i, j = self.pos
        for idx, p in enumerate(self.parts):
            if self.orient == "H":
                x1 = (i + idx) * CASE
                y1 = j * CASE
            else:
                x1 = i * CASE
                y1 = (j + idx) * CASE
            x2 = x1 + CASE
            y2 = y1 + CASE
            self.zone.coords(p, x1, y1, x2, y2)

    def deplacer(self, event):
        
        if not self.parts:
            return
        i, j = self.pos

        if event.keysym == "Up":
            if j > 0:
                j -= 1
        elif event.keysym == "Down":
            # si vertical, vérifier le bas du bateau
            if self.orient == "H":
                if j < TAILLE_GRILLE - 1:
                    j += 1
            else:
                if j + self.longueur < TAILLE_GRILLE:
                    j += 1
        elif event.keysym == "Left":
            if i > 0:
                i -= 1
        elif event.keysym == "Right":
            if self.orient == "H":
                if i + self.longueur < TAILLE_GRILLE:
                    i += 1
            else:
                if i < TAILLE_GRILLE - 1:
                    i += 1

        self.pos = [i, j]
        self.dessiner()

    def tourner(self, event):
        
        if not self.parts:
            return
        i, j = self.pos
        if self.orient == "H":
            self.orient = "V"
            if j + self.longueur > TAILLE_GRILLE:
                j = TAILLE_GRILLE - self.longueur
                if j < 0:
                    j = 0
        else:
            self.orient = "H"
            if i + self.longueur > TAILLE_GRILLE:
                i = TAILLE_GRILLE - self.longueur
                if i < 0:
                    i = 0
        self.pos = [i, j]
        self.dessiner()


if __name__ == "__main__":
    root = Tk()
    Jeu(root)
    root.mainloop()
