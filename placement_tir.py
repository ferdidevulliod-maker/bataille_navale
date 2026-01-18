
from tkinter import Button, Canvas, Label, Tk

from placement_bateaux_sur_grille import CASE, TAILLE_GRILLE


class GestionTir:
    # gère les tirs sur le plateau du bot

    def __init__(self, plateau_adversaire, tir_effectue):
        """
        Initialise une instance de la classe.

        Paramètres:
        -----------
        plateau_adversaire : Tk
            La fenêtre représentant le plateau de l'adversaire.
        tir_effectue : bool
            Indique si un tir a déjà été effectué.

        Attributs:
        ----------
        longueur : int
            La longueur du bateau.
        pos_tir : list
            La position du tir sous forme de coordonnées [x, y].
        tir : objet
            L'objet représentant le tir effectué.
        grille_occupee : objet
            Représente la grille occupée par les navires.
        """
        self.plateau_adversaire = plateau_adversaire
        self.plateau_adversaire.title("Bataille navale - plateau de l'adversaire")
        self.plateau_adversaire.geometry("900x500")

        self.longueur = 0
        self.pos_tir = [0, 0]
        self.tir = None
        self.tir_effectue = tir_effectue
        self.grille_occupee = None

    def bouger_tir(self):  # raccourcis clavier pour deplacer le tir
        self.plateau_adversaire.bind("<Up>", self.deplacer)
        self.plateau_adversaire.bind("<Down>", self.deplacer)
        self.plateau_adversaire.bind("<Left>", self.deplacer)
        self.plateau_adversaire.bind("<Right>", self.deplacer)
        self.plateau_adversaire.bind("<Return>", self.tir_effectue)
        Button(
            self.plateau_adversaire,
            text="Attaquer",
            command=lambda: self.creation_tir(),
        ).place(x=1230, y=400)

    def plateau(self, plateau_adversaire):
        """
        Crée et affiche le plateau de jeu adverse avec sa grille interactive.

        Cette méthode initialise un canvas graphique représentant le plateau de l'adversaire,
        dessine une grille de cases carrées, et ajoute les labels d'aide et de titre.

        Args:
            plateau_adversaire: Widget (Tk) sur lequel dessiner le plateau.

        Returns:
            None
        """
        # dessin du plateau de jeu
        self.zone = Canvas(
            plateau_adversaire,
            width=CASE * TAILLE_GRILLE,
            height=CASE * TAILLE_GRILLE,
            bg="lightblue",
        )
        self.zone.place(x=800, y=400)
        # grille ou l'on met les bateaux
        for x in range(TAILLE_GRILLE):
            for y in range(TAILLE_GRILLE):
                self.zone.create_rectangle(
                    x * CASE,
                    y * CASE,
                    (x + 1) * CASE,
                    (y + 1) * CASE,
                    outline="black",
                )
        # petite aide
        Label(
            plateau_adversaire, text="Flèches = déplacer viseur , enter = tirer "
        ).place(x=800, y=350)
        # nom plateau
        Label(plateau_adversaire, text="Plateau ennemi").place(x=950, y=820)

    def creation_tir(self):
        # dessiner la case du tir
        self.tir = self.zone.create_rectangle(0, 0, CASE, CASE, fill="yellow")

    def deplacer(self, event):
        """
        Déplace le curseur de tir sur la grille en fonction de la touche pressée.

        Cette méthode permet de naviguer sur la grille de jeu en utilisant les touches
        directionnelles du clavier (Haut, Bas, Gauche, Droite). Le curseur ne peut pas
        sortir des limites de la grille.

        Args:
            event: Objet événement Tkinter contenant les informations de la touche pressée
                   (event.keysym contient le symbole de la touche : "Up", "Down", "Left", "Right")

        Returns:
            None
        """
        if not self.tir:
            # aucun tir n'a été créé
            return
        # récupère les coordonnées actuelles du tir
        i, j = self.pos_tir

        if event.keysym == "Up":
            # déplace vers le haut
            if j > 0:
                j -= 1
        elif event.keysym == "Down":
            # déplace vers le bas
            if j < TAILLE_GRILLE - 1:
                j += 1
        elif event.keysym == "Left":
            # déplace vers la gauche
            if i > 0:
                i -= 1
        elif event.keysym == "Right":
            # déplace vers la droite
            if i < TAILLE_GRILLE - 1:
                i += 1

        self.pos_tir = [i, j]
        self.dessiner()

    def dessiner(self):
        # dessine le tir à sa nouvelle position
        if not self.tir:
            # aucun tir n'a été créé
            return
        # récupère les coordonnées actuelles du tir
        i, j = self.pos_tir
        x1 = i * CASE
        y1 = j * CASE
        x2 = x1 + CASE
        y2 = y1 + CASE
        # met à jour la position du tir sur la grille
        self.zone.coords(self.tir, x1, y1, x2, y2)